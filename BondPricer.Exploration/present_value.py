import datetime as dt
from typing import Optional, Dict
import numpy as np
import math
from dateutil.relativedelta import relativedelta

def bond_present_value(
        face_value: float,
        interest_rate: float,
        coupon_frequency: int, #per year
        maturity_date: dt.date,
        risk_free_rate: Optional[float] = None

) -> Dict[str, float]:
    
    #risk free rate - use US treasury rate if none specified
    if not risk_free_rate:
        risk_free_rate = 0.08

    #coupon payment dates
    coupon_dates = []
    current_date = maturity_date
    today = dt.date.today()
    while current_date > today:
        coupon_dates.append(current_date)
        current_date -= relativedelta(months=12 // coupon_frequency)
    #get previous coupon date for accrued interest calc
    prev_coupon_date = current_date - relativedelta(months=12 // coupon_frequency)
    
    coupon_dates.reverse()
    num_payments = len(coupon_dates)
    coupon = face_value * interest_rate

    #calculate PV
    coupons_pv = coupon * ((1 - pow((1+risk_free_rate), - num_payments)) / risk_free_rate)
    maturity_pv = face_value * pow((1+risk_free_rate), - num_payments)
    dirty_price = coupons_pv + maturity_pv

    #subtract accrued interest to get clean price
    num_days_accrued = (today - prev_coupon_date).days
    days_in_coupon_period = (coupon_dates[0] - prev_coupon_date).days
    accrued_interest = coupon * (num_days_accrued / days_in_coupon_period)

    clean_price = dirty_price - accrued_interest


    return {
        "CleanPrice": clean_price,
        "DirtyPrice": dirty_price
    }


    


    #should we be using YTM or risk free rate?? rfr to reflect market dynamics more, ytm for long term investment value


print(bond_present_value(100, 0.1, 4, dt.date(2023, 6, 30)))



