import pytest
import datetime as dt
from ..Bond import Bond

class TestBondClass:

    def test_get_coupon_dates(self, mocker):

        #patch datetime.date.today to a certain date so test will not fail in future
        mock_date = mocker.patch("datetime.date")
        mock_date.today.return_value = dt.date(2023, 5, 3)

        #bond = Bond()

        assert 1==1

