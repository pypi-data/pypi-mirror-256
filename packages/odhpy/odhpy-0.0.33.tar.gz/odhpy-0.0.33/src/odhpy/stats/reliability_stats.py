import pandas as pd
import numpy as np
from odhpy import utils
from datetime import datetime, timedelta
from typing import Union

def reliability_ts(demand: Union[list,float,int], supply: pd.Series):
    """Returns demand as a timeseries for input to monthly reliability statistic. Matches date range of supply timeseries input.

    Args:
        demand (list | float | int): Demand timeseries with date as index, list of monthly values or constant daily demand
        supply (pd.Series): Supply timeseries with date as index

    Returns:
        pd.Series: Demand timeseries for input to reliability stats
    """
    # Check if provided demand is a constant value. Copy date range of supply TS and overwite
    # value with constant demand.
    if type(demand) in [float,int]:
        constant_demand=demand
        demand_ts=supply.copy(deep=True)
        demand_ts[:]=constant_demand

    # Check if provided demand is a list of monthly values. Copy date range of supply TS and overwite
    # monthly value with relevant demand. Also ensure that 12 values have been provided.
    if type(demand) is list:
        if len(demand)<12:
            raise Exception("Monthly demand list must have a length of 12")
        monthly_demand=demand
        demand_ts=supply.copy(deep=True)
        month_list=list(utils.get_month(demand_ts.index))
        demand_ts[:]=[monthly_demand[x-1] for x in month_list]

    # Check if provided demand is an accepted type
    if type(demand) not in [float,int,list]:
        raise Exception("Demand must be one of timeseries, monthly list or constant demand")        

    return demand_ts

def monthly_reliability(demand: Union[pd.Series,list,float,int], supply: pd.Series,  tol=1, allow_part_months=False):
    """Returns the monthly reliability statistic for a daily timeseries of demand and supply.

    Args:
        demand (pd.Series | list | float | int): Demand timeseries with date string as index, list of monthly values or constant daily demand
        supply (pd.Series): Supply timeseries with date as index
        tol (float, optional): Percentage of demand treated as full demand. Defaults to 1 (100%).
        allow_part_months (bool, optional): Allow part months or only complete months. Defaults to False.

    Returns:
        float: Monthly reliability
    """    
    # If provided demand is not a timeseries, pass input to reliability_ts first and then proceed. 
    # Enforce common date range
    if type(demand) != pd.Series:
        demand=reliability_ts(demand,supply)
        common_dates=supply.index
    else:
        common_dates=np.intersect1d(demand.index,supply.index)
        demand=demand[common_dates]
        supply=supply[common_dates]

    # Collate timeseries data to monthly
    if (allow_part_months):
        dem_month=demand.groupby(utils.get_year_and_month(common_dates)).sum()
        sup_month=supply.groupby(utils.get_year_and_month(common_dates)).sum()
    else:
        if supply.index[0][8:10]=="01": #0123-56-89
            #First date is the start of a month; use this as start date.
            start_date=supply.index[0]
        else:
            #Start on the first date of the next month
            start_date = utils.get_next_month_start(supply.index[0])
        if supply.index[-1] == utils.get_this_month_end(supply.index[-1]):
            end_date=supply.index[-1]
        else:
            end_date=utils.get_prev_month_end(supply.index[-1])
        demand_trim = demand[start_date:end_date]
        supply_trim = supply[start_date:end_date]
        year_month = utils.get_year_and_month(demand_trim.index)
        dem_month=demand_trim.groupby(year_month).sum()
        sup_month=supply_trim.groupby(year_month).sum()

    # Check whether demand is met within given tolerance and express as a percentage
    rel=np.where((sup_month>=dem_month*tol),1,0).sum()/sup_month.count()
    return rel


def annual_reliability(demand: Union[pd.Series,list,float,int], supply: pd.Series,  tol=1, wy_month=7, allow_part_years=False):
    """Returns the annual reliability statistic for a daily timeseries of demand and supply.

    Args:
        demand (pd.Series | list | float | int): Demand timeseries with date as index, list of monthly values or constant daily demand
        supply (pd.Series): Supply timeseries with date as index
        tol (float, optional): Percentage of demand treated as full demand. Defaults to 1 (100%).
        wy_month (int, optional): Water year start month. Defaults to 7.
        allow_part_years (bool, optional): Allow part water years or only complete water years. Defaults to False.

    Returns:
        float: Annual reliability
    """
    
    # If provided demand is not a timeseries, pass input to reliability_ts first and then proceed.
    # Enforce common date range
    if type(demand) != pd.Series:
        demand=reliability_ts(demand,supply)
    else:
        common_dates=np.intersect1d(demand.index,supply.index)
        demand=demand[common_dates]
        supply=supply[common_dates]
    
    # Collate timeseries data to annual
    if not allow_part_years:
        demand = utils.crop_to_wy(demand, wy_month)
        supply = utils.crop_to_wy(supply, wy_month)
    if (len(demand) == 0):
        return np.nan
    dem_annual=demand.groupby(utils.get_wy(demand.index, wy_month)).sum()
    sup_annual=supply.groupby(utils.get_wy(supply.index, wy_month)).sum()
    no_years=sup_annual.count()

    # Check whether demand is met within given tolerance and express as a percentage
    rel=np.where((sup_annual>=dem_annual*tol),1,0).sum()/no_years

    return rel
