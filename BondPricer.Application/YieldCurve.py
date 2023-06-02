class YieldCurve:

    def __init__(self):
        self.maturities = ["2year", "5year", "7year", "10year", "30year"]

    def fetch_data(self):

        ...

        #check db

        #call api if cache date isn't today

    def estimate_yield_for_maturity(years: float) -> float:
        ...

    def print_yield_curve():
        ...