import pytest
import sys
import time_machine
sys.path.append("..")
from API.Application.ValuationPV import ValuationPV
from API.Application.Bond import Bond
import datetime as dt

"""
Tests for pricing with discount rate input
"""


#test case expected results calculated in Excel
#set date so coupon dates don't change over time
@time_machine.travel(dt.date(2023, 6, 5))
def test_annual_coupon_bond_pricing():
    bond = Bond(100, 0.05, 1, dt.date(2025, 12, 31), 'AA')
    valuation = ValuationPV(bond)

    expected = {"CleanPrice": 93.20, "DirtyPrice": 95.34}

    actual = valuation.price(discount_rate_specified=0.08)

    assert actual == expected, f"Prices did not match. Actual: {actual}, Expected: {expected}"


    
@time_machine.travel(dt.date(2023, 6, 5))   
def test_zero_coupon_bond_pricing():
    bond = Bond(200, 0, 0, dt.date(2026, 12, 31), 'AA')
    valuation = ValuationPV(bond)

    expected = {"CleanPrice": 104.21, "DirtyPrice": 104.21}

    actual = valuation.price(discount_rate_specified=0.2)

    assert actual == expected, f"Prices did not match. Actual: {actual}, Expected: {expected}"

@time_machine.travel(dt.date(2023, 6, 5))
def test_quarterly_coupon_bond_pricing():
    bond = Bond(150, 0.1, 4, dt.date(2024, 12, 31), 'AA')
    valuation = ValuationPV(bond)

    expected = {"CleanPrice": 152.71, "DirtyPrice": 155.44}

    actual = valuation.price(discount_rate_specified=0.09)

    assert actual == expected, f"Prices did not match. Actual: {actual}, Expected: {expected}"


"""
Tests for pricing with monte carlo discount rate simulation
 - can't test exact results so checking behaviour is correct when changing inputs 
"""

def test_higher_credit_rating_gets_higher_price():
    bond1 = Bond(150, 0.1, 4, dt.date(2024, 12, 31), 'AA')
    valuation1 = ValuationPV(bond1)
    actual1 = valuation1.price_with_simulated_yields()
    
    bond2 = Bond(150, 0.1, 4, dt.date(2024, 12, 31), 'C')
    valuation2 = ValuationPV(bond2)
    actual2 = valuation2.price_with_simulated_yields()

    assert actual1["CleanPrice"] > actual2["CleanPrice"], "Higher credit rating bond did not get a higher price."


def test_higher_coupon_frequency_gets_higher_price():
    bond1 = Bond(150, 0.1, 4, dt.date(2030, 12, 31), 'AA')
    valuation1 = ValuationPV(bond1)
    actual1 = valuation1.price_with_simulated_yields()
    
    bond2 = Bond(150, 0.1, 1, dt.date(2030, 12, 31), 'AA')
    valuation2 = ValuationPV(bond2)
    actual2 = valuation2.price_with_simulated_yields()

    assert actual1["CleanPrice"] > actual2["CleanPrice"], "Higher coupon frequency bond did not get a higher price."


