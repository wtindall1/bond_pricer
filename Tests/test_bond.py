import pytest
import datetime as dt
import sys
sys.path.append("..")
from API.Application.Bond import Bond
import time_machine

class TestBondClass:

    #set date so coupon dates don't change over time
    @time_machine.travel(dt.date(2023, 5, 3))
    def test_get_coupon_dates(self):

        bond = Bond(100, 0.1, 2, dt.date(2024, 12, 31), 'AA+')
        coupon_dates = bond.get_coupon_dates()

        expected_num_coupon_dates = 4

        assert len(coupon_dates) == expected_num_coupon_dates

    def test_valid_credit_rating(self):
        try:
            bond = Bond(150, 0.1, 2, dt.date(2030, 12, 31), 'CCC')
        except ValueError:
            pytest.fail("Valid credit rating but error occured initialising Bond instance")


    def test_invalid_credit_rating(self):
        bond = Bond(150, 0.1, 2, dt.date(2030, 12, 31), 'AAAA+')

        #should not have a credit rating because input was invalid
        with pytest.raises(AttributeError):
            bond.credit_rating
            


    def test_get_proxy_yield_returns_float(self):
        bond = Bond(150, 0.1, 2, dt.date(2030, 12, 31), 'AA')

        proxy = bond.get_proxy_yield()

        assert type(proxy) == float, "Float not returned"

