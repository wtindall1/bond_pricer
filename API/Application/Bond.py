import datetime as dt
from typing import Optional, Dict, List
from dateutil.relativedelta import relativedelta
from .CreditRating import CreditRating
import requests
import json
import numpy as np
import pandas as pd
import os

class Bond:

    def __init__(self,               
        face_value: float,
        interest_rate: float,
        coupon_frequency: int, #per year
        maturity_date: dt.date,
        credit_rating: str
            ):
        
        self.face_value = face_value
        self.interest_rate = interest_rate
        self.coupon_frequency = coupon_frequency
        self.maturity_date = maturity_date

        #handling for zero coupon bonds
        if self.coupon_frequency > 0:
            self.coupon = (self.face_value * self.interest_rate) / self.coupon_frequency
        else:
            self.coupon = 0

        try:
            self.credit_rating = CreditRating(credit_rating)
            print(f"Valid credit rating: {self.credit_rating.name}")
        except ValueError:
            print("Invalid credit rating")



    def get_coupon_dates(self) -> List[dt.date]:
        self.coupon_dates: List[dt.date] = []

        #zero coupon bond
        if self.coupon_frequency == 0:
            return self.coupon_dates

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
    
    
    #gets proxy yield from index with similar credit rating, to use as discount rate
    def get_proxy_yield(self) -> Optional[float]:

        #match creditrating to FRED series_id
        if "AAA" in self.credit_rating.value:
            series_id = "BAMLC0A1CAAAEY"
        elif "AA" in self.credit_rating.value:
            series_id = "BAMLC0A2CAAEY"
        elif "A" in self.credit_rating.value:
            series_id = "BAMLC0A3CAEY"
        elif "BBB" in self.credit_rating.value:
            series_id = "BAMLC0A4CBBBEY"
        elif "BB" in self.credit_rating.value:
            series_id = "BAMLEM3BRRBBCRPIEY"
        else:
            series_id = "BAMLEMHBHYCRPIEY"

        #get api key from env
        api_key = os.environ.get("FRED_API_KEY")

        #request data from 1 week ago, so doesn't return whole timeseries
        observation_start = dt.date.today() - dt.timedelta(days=7)


        url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json&observation_start={observation_start}"

        #call FRED Api
        response = requests.get(url)

        if response.status_code == 200: #successful
            
            data = response.json()
            #get yield value for last observation item
            return float(data["observations"][-1]["value"])/100
        
        else:
            print("Request failed with status code:", response.status_code)
            return None
        

    def get_proxy_yield_time_series(self, credit_rating: CreditRating, years: int) -> pd.Series:

        #match creditrating to FRED series_id
        if "AAA" in self.credit_rating.value:
            series_id = "BAMLC0A1CAAAEY"
        elif "AA" in self.credit_rating.value:
            series_id = "BAMLC0A2CAAEY"
        elif "A" in self.credit_rating.value:
            series_id = "BAMLC0A3CAEY"
        elif "BBB" in self.credit_rating.value:
            series_id = "BAMLC0A4CBBBEY"
        elif "BB" in self.credit_rating.value:
            series_id = "BAMLEM3BRRBBCRPIEY"
        else:
            series_id = "BAMLEMHBHYCRPIEY"



        #get api key from env
        api_key = os.environ.get("FRED_API_KEY")

        #give start observation date (will be using 20 years)
        observation_start = dt.date.today() - dt.timedelta(weeks=years*52)


        url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json&observation_start={observation_start}"

        response = requests.get(url)
        data = response.json()
        dates = [item["date"] for item in data["observations"]]
        yields = [float(item["value"])/100 if item["value"] != '.' else np.nan for item in data["observations"]]


        series = pd.Series(np.array(yields), index=dates)
        
        return series
        
        

    
    



    