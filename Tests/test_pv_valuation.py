import pytest
import sys
import time_machine
sys.path.append("..")
from API.Application.ValuationPV import ValuationPV
from API.Application.Bond import Bond
import datetime as dt

class TestValuationPVClass:

    #test case expected results calculated in Excel

    #set date so coupon dates don't change over time
    @time_machine.travel(dt.date(2023, 6, 5))
    def test_annual_coupon_bond_pricing(self):
        bond = Bond(100, 0.05, 1, dt.date(2025, 12, 31), 'AA')
        valuation = ValuationPV(bond)

        expected = {"CleanPrice": 93.20, "DirtyPrice": 95.34}

        actual = valuation.price(discount_rate_specified=0.08)

        assert actual == expected, f"Prices did not match. Actual: {actual}, Expected: {expected}"

    
        
    @time_machine.travel(dt.date(2023, 6, 5))   
    def test_zero_coupon_bond_pricing(self):
        bond = Bond(200, 0, 0, dt.date(2026, 12, 31), 'AA')
        valuation = ValuationPV(bond)

        expected = {"CleanPrice": 104.21, "DirtyPrice": 104.21}

        actual = valuation.price(discount_rate_specified=0.2)

        assert actual == expected, f"Prices did not match. Actual: {actual}, Expected: {expected}"

    @time_machine.travel(dt.date(2023, 6, 5))
    def test_quarterly_coupon_bond_pricing(self):
        bond = Bond(150, 0.1, 4, dt.date(2024, 12, 31), 'AA')
        valuation = ValuationPV(bond)

        expected = {"CleanPrice": 152.71, "DirtyPrice": 155.44}

        actual = valuation.price(discount_rate_specified=0.09)

        assert actual == expected, f"Prices did not match. Actual: {actual}, Expected: {expected}"
