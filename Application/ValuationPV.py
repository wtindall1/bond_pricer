from Bond import Bond
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
        number_periods = len(coupon_dates)
        discount_rate = self.bond.get_proxy_yield() if not discount_rate_specified else discount_rate_specified

        #exit if discount rate not specified and no proxy found
        if not discount_rate:
            print("No discount rate was specified and no proxy could be found.")
            return None

        #calculate pv (dirty)
        coupons_pv = self.bond.coupon * ((1 - (1+discount_rate)**(-number_periods)) / discount_rate)
        maturity_pv = self.bond.face_value * ((1+discount_rate)**(- number_periods))
        dirty_price = coupons_pv + maturity_pv

        #substract accrued interest to get clean price
        clean_price = dirty_price - self.bond.accrued_interest(
            next_coupon_date=coupon_dates[0]
        )

        return {
            "CleanPrice": clean_price,
            "DirtyPrice": dirty_price
        }
    

bond = Bond(100, 0.05, 4, dt.date(2030, 6, 30), 'AAA')
val = ValuationPV(bond)
print(val.price())