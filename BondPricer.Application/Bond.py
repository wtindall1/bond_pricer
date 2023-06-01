import datetime as dt
from typing import Optional, Dict

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

    def treasury_yield_closest_maturity(self):
        ...

    def get_coupon_dates(self):
        #last is maturity
        ...

    def accrued_interest(self):
        ...




    