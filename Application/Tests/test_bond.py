import pytest
import datetime as dt
import sys
sys.path.append("..")
from Bond import Bond
import time_machine

class TestBondClass:

    #set date so coupon dates don't change over time
    @time_machine.travel(dt.date(2023, 5, 3))
    def test_get_coupon_dates(self):

        bond = Bond(100, 0.1, 2, dt.date(2024, 12, 31), 'AA+')
        coupon_dates = bond.get_coupon_dates()

        expected_num_coupon_dates = 4

        assert len(coupon_dates) == expected_num_coupon_dates

