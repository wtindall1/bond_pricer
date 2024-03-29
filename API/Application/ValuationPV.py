from .Bond import Bond
from .MonteCarloSimulation import MonteCarloSimulation
from typing import Dict, Optional
import datetime as dt
import numpy as np
import pandas as pd


class ValuationPV:

    def __init__(self, bond: Bond):
        self.bond = bond

    #discounts cash flows to return clean and dirty bond price
    #disount rate can be specified, proxy used if not
    def price(self, discount_rate_specified: Optional[float] = None) -> Dict[str, Optional[float]]:

        #INPUTS
        coupon_dates = np.array(self.bond.get_coupon_dates())

        #calculate number of (annual) periods until each coupon date
        coupon_dates_n_annual = np.array([(date - dt.date.today()).days / 365 for date in coupon_dates])
        #number of years until maturity date
        n_maturity = (self.bond.maturity_date - dt.date.today()).days / 365

        
        discount_rate = self.bond.get_proxy_yield() if not discount_rate_specified else discount_rate_specified
        #exit if discount rate not specified and no proxy found
        if discount_rate is None:
            print("No discount rate was specified and no proxy could be found.")
            return {
                "CleanPrice": None,
                "DirtyPrice": None,
            }
        
        #discount coupon payments
        coupons = np.array([self.bond.coupon for _ in range(len(coupon_dates))])
        discounted_coupons = coupons / (1+discount_rate)**coupon_dates_n_annual

        #calculate pv (dirty)
        coupons_pv = sum(discounted_coupons)
        maturity_pv = self.bond.face_value / (1+discount_rate)**n_maturity
        dirty_price = coupons_pv + maturity_pv
        
        #calculate clean price
        if self.bond.coupon_frequency == 0: #zero coupon no accrued interest
            clean_price = dirty_price
        else:
            #substract accrued interest to get clean price
            clean_price = dirty_price - self.bond.accrued_interest(
                next_coupon_date=coupon_dates[0]
            )

        return {
            "CleanPrice": round(clean_price, 2),
            "DirtyPrice": round(dirty_price, 2)
        }
    

    #discounts cash flows to return clean and dirty bond price
    #discount rates simulated for each day up to maturity
    def price_with_simulated_yields(self) -> Dict[str, Optional[float]]:

        #INPUTS
        coupon_dates = np.array(self.bond.get_coupon_dates())

        #calculate number of (annual) periods until each coupon date
        coupon_dates_n_annual = np.array([(date - dt.date.today()).days / 365 for date in coupon_dates])
        #number of years until maturity date
        n_maturity = (self.bond.maturity_date - dt.date.today()).days / 365

        
        #simulated yields for bond index of similar credit rating
        sim = MonteCarloSimulation(bond=self.bond)
        forecasted_yields: pd.Series  = sim.run()
        #exit if discount rate not specified and no proxy found
        if forecasted_yields is None:
            print("No discount rate was specified and no proxy could be found.")
            return {
                "CleanPrice": None,
                "DirtyPrice": None,
            }
        
        
        #discount coupon payments
        coupons = np.array([self.bond.coupon for _ in range(len(coupon_dates))])
        #element wise - forecasted yield for each coupon date used
        discounted_coupons = coupons / (1+forecasted_yields[coupon_dates])**coupon_dates_n_annual

        #calculate pv (dirty)
        coupons_pv = sum(discounted_coupons)
        maturity_pv = self.bond.face_value / (1+forecasted_yields[-1])**n_maturity #last forecasted yield is maturity date
        dirty_price = coupons_pv + maturity_pv
        
        #calculate clean price
        if self.bond.coupon_frequency == 0: #zero coupon no accrued interest
            clean_price = dirty_price
        else:
            #substract accrued interest to get clean price
            clean_price = dirty_price - self.bond.accrued_interest(
                next_coupon_date=coupon_dates[0]
            )

        return {
            "CleanPrice": round(clean_price, 2),
            "DirtyPrice": round(dirty_price, 2)
        }
    

