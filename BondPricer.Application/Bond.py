import datetime as dt
from typing import Optional, Dict
from dateutil.relativedelta import relativedelta

class Bond:

    def __init__(self,
        face_value: float,
        interest_rate: float,
        coupon_frequency: int, #per year
        maturity_date: dt.date,
    ) -> Dict[str, float]:
        
        self.face_value = face_value
        self.interest_rate = interest_rate
        self.coupon_frequency = coupon_frequency
        self.maturity_date = maturity_date

    def get_coupon_dates(self) -> None:
        self.coupon_dates = []
        date = self.maturity_date
        #work back from maturity date to find all future coupon dates (estimated)
        while date > dt.date.today():
            self.coupon_dates.append(date)
            date -= relativedelta(months=12 // self.coupon_frequency)
        

    def closest_maturity_UST(self):
        #find the yield on the US treasury with closest maturity to the bond
        maturities = {
            0.25: "3month",
            2: "2year",
            5: "5year",
            7: "7year",
            10: "10year",
            30: "30year"
        }
        years_to_maturity = (self.maturity_date - dt.date.today()).days / 365
        closest_maturity = min(maturities.keys(), key=lambda x: abs(years_to_maturity - x))
        return maturities[closest_maturity]


    def closest_maturity_UST_yield(self):
        ...


    

    def accrued_interest(self):
        ...




    