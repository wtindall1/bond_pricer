import datetime as dt
from typing import Optional
import numpy as np
import math

def bond_present_value(
        face_value: float,
        interest_rate: float,
        coupon_frequency: int, #per year
        maturity_date: dt.date,
        risk_free_rate: Optional[float] = None

) -> float:
    
    #risk free rate - use US treasury rate if none specified
    if not risk_free_rate:
        risk_free_rate = 0.08

    #calculate number of payments
    date_diff = (maturity_date - dt.date.today()).days #gets days attribute of timedelta object
    year_date_diff = date_diff / 365
    num_payments = math.floor(year_date_diff * coupon_frequency)

    
    coupon = face_value * interest_rate

    #calculate PV
    coupons_pv = coupon * ((1 - pow((1+risk_free_rate), - num_payments)) / risk_free_rate)
    maturity_pv = face_value * pow((1+risk_free_rate), - num_payments)
    present_value = coupons_pv + maturity_pv

    return present_value


    


    #should we be using YTM or risk free rate?? rfr to reflect market dynamics more, ytm for long term investment value
    #ASSUMES PAYMENT JUST BEEN MADE - Add adjustments for dates / dirty vs clean price


print(bond_present_value(100, 0.1, 4, dt.date(2027, 1, 1)))