import datetime as dt
from typing import Optional, Dict
from dateutil.relativedelta import relativedelta
from CreditRating import CreditRating

class Bond:

    def __init__(self,               
        face_value: float,
        interest_rate: float,
        coupon_frequency: int, #per year
        maturity_date: dt.date,
        credit_rating: str) -> Dict[str, float]:
        
        self.face_value = face_value
        self.interest_rate = interest_rate
        self.coupon_frequency = coupon_frequency
        self.maturity_date = maturity_date
        self.coupon = self.face_value * self.interest_rate

        try:
            self.credit_rating = CreditRating(credit_rating)
            print(f"Valid credit rating: {self.credit_rating.name}")
        except ValueError:
            print("Invalid credit rating")



    def get_coupon_dates(self) -> None:
        self.coupon_dates = []
        date = self.maturity_date
        #work back from maturity date to find all future coupon dates (estimated)
        while date > dt.date.today():
            self.coupon_dates.append(date)
            date -= relativedelta(months=12 // self.coupon_frequency)

        self.coupon_dates.reverse()
        return self.coupon_dates

        

    #calculate interest accrued between last coupon date and current date
    def accrued_interest(self, next_coupon_date: dt.date) -> float:
        #calculate previous coupon date
        self.prev_coupon_date = next_coupon_date - relativedelta(months=12 // self.coupon_frequency)
        
        #proportion of coupon payment
        num_days_accrued = (dt.date.today() - self.prev_coupon_date).days
        days_in_coupon_period = (next_coupon_date - self.prev_coupon_date).days
        accrued_interest = self.coupon * (num_days_accrued / days_in_coupon_period)

        return accrued_interest
    

    def get_proxy_yield(self):
        ...
    
    


bond = Bond(100, 0.1, 4, dt.date(2030, 6, 30), 'AAAA')

    