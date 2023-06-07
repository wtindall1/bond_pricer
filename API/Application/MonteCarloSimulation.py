import pandas as pd
import numpy as np
import datetime as dt
from .Bond import Bond


class MonteCarloSimulation:

    def __init__(self, bond: Bond) -> None:
        self.bond = bond

    def run(self) -> pd.Series:

        #2o year time series for bond index with similar credit rating
        yield_time_series = self.bond.get_proxy_yield_time_series(credit_rating=self.bond.credit_rating, years=20)
        #get daily change over 20 years, excluding first day as nan
        daily_yield_change = yield_time_series.diff()[1:]
        #current yield to use as simulation starting point
        starting_yield = yield_time_series[-1]

        mean = np.mean(daily_yield_change)
        st_dev = np.std(daily_yield_change)
        num_simulations = 100
        #number of periods until maturity date
        dates = np.arange(dt.date.today(), self.bond.maturity_date + dt.timedelta(days=1), dt.timedelta(days=1))
        num_periods = dates.size

        #simulate daily yield changes up to maturity date
        #assumes the changes are normally distributed
        simulated_yield_changes = np.random.normal(mean, st_dev, (num_simulations, num_periods))
        #create zeros array to hold the simulated yields
        simulated_yields = np.zeros_like(simulated_yield_changes)

        #set starting value for each simulation
        simulated_yields[:,0] = starting_yield

        for i, sim in enumerate(simulated_yields):
            for j in range(1, len(sim)):
                sim[j] = sim[j-1] + simulated_yield_changes[i,j]

        #average yield across simulations
        average_yield = np.mean(simulated_yields, axis=0)
        date_range = pd.date_range(start=dt.date.today(), end=self.bond.maturity_date, freq="D")
        #create series matching yield to date
        forecasted_yield = pd.Series(average_yield, index=date_range)

    
        return forecasted_yield
    
# bond = Bond(100, 0.1, 2, dt.date(2025, 1, 1), 'AA')
# sim = MonteCarloSimulation(bond)
# print(sim.run())






