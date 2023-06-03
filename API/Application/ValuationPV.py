from .Bond import Bond
from typing import Dict, Optional
import datetime as dt

class ValuationPV:

    def __init__(self, bond: Bond):
        self.bond = bond

    #discounts cash flows to return clean and dirty bond price
    #disount rate can be specified, proxy used if not
    def price(self, discount_rate_specified: Optional[float] = None) -> Optional[Dict[str, float]]:

        #inputs
        coupon_dates = self.bond.get_coupon_dates()
        #for zero coupon bond, set num_periods to number of years
        if self.bond.coupon_frequency == 0:
            number_periods = (coupon_dates[-1] - dt.date.today()).days / 365
        else:
            number_periods = len(coupon_dates)
        
        discount_rate = self.bond.get_proxy_yield() if not discount_rate_specified else discount_rate_specified
        
        #exit if discount rate not specified and no proxy found
        if discount_rate is None:
            print("No discount rate was specified and no proxy could be found.")
            return None
        
        #adjust discount rate for coupon frequency
        if self.bond.coupon_frequency > 1:
            discount_rate = (1+discount_rate)**(1/self.bond.coupon_frequency) - 1
        

        #calculate pv (dirty)
        coupons_pv = self.bond.coupon * ((1 - (1+discount_rate)**(-number_periods)) / discount_rate)
        maturity_pv = self.bond.face_value * ((1+discount_rate)**(-number_periods))
        dirty_price = coupons_pv + maturity_pv

        if self.bond.coupon_frequency == 0: #zero coupon no accrued interest
            clean_price = dirty_price
        else:
            #substract accrued interest to get clean price
            clean_price = dirty_price - self.bond.accrued_interest(
                next_coupon_date=coupon_dates[0]
            )

        return {
            "CleanPrice": clean_price,
            "DirtyPrice": dirty_price
        }
    

