import datetime as dt
from typing import Optional, Dict
from dateutil.relativedelta import relativedelta

def bond_present_value(
        face_value: float,
        interest_rate: float,
        coupon_frequency: int, #per year
        maturity_date: dt.date,
        discount_rate: float = 0.05

) -> Dict[str, float]:
    
    today = dt.date.today()
    
    #risk free rate - use US treasury rate if none specified
    #find closest us treasury maturity- 3month, 2year, 5year, 7year, 10year, and 30year
    maturities = {
        0.25: "3month",
        2: "2year",
        5: "5year",
        7: "7year",
        10: "10year",
        30: "30year"
    }
    years_to_maturity = (maturity_date - today).days / 365
    closest_maturity = min(maturities.keys(), key=lambda x: abs(years_to_maturity - x))
    

    #coupon payment dates
    coupon_dates = []
    current_date = maturity_date
    while current_date > today:
        coupon_dates.append(current_date)
        current_date -= relativedelta(months=12 // coupon_frequency)
    #get previous coupon date for accrued interest calc
    prev_coupon_date = current_date - relativedelta(months=12 // coupon_frequency)
    
    coupon_dates.reverse()
    num_payments = len(coupon_dates)
    coupon = (face_value * interest_rate) / coupon_frequency

    #calculate PV
    coupons_pv = coupon * ((1 - pow((1+discount_rate), - num_payments)) / discount_rate)
    maturity_pv = face_value * pow((1+discount_rate), - num_payments)
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


print(bond_present_value(100, 0.05, 4, dt.date(2030, 6, 30), 0.05))



