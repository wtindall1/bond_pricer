#retrieve time series data for bond with similar yield - note only has week days
# convert to daily change (percentage points)
#calculate mean and standard deviation of the data
#run simulations using np.random.normal - assumes data is normally distributed
#this will pick yield change (% points) each step from probability distribution
#average yield at each step (day)
#visualise simulations and average yields
import matplotlib.pyplot as plt

from yield_time_series import get_yield_time_series
import pandas as pd
import numpy as np

historical_yields = get_yield_time_series('AA', 10) / 100
daily_yield_change = historical_yields.diff()[1:]

#historical_yields.info()

mean, st_dev = np.mean(daily_yield_change), np.std(daily_yield_change)

num_simulations = 1000
num_periods = 365*30

yield_changes = np.random.normal(mean, st_dev, (num_simulations, num_periods))

starting_yield = historical_yields[-1]

yield_simulations = np.zeros((num_simulations, num_periods))

yield_simulations[:,0] = starting_yield # set starting value for each simulation

for i, sim in enumerate(yield_simulations):
    for j in range(1, len(sim)):
        sim[j] = sim[j-1] + yield_changes[i,j]




print(yield_simulations)



# # Plot individual simulations
# plt.figure(figsize=(10, 6))
# for i in range(num_simulations):
#     plt.plot(yield_simulations[i], linewidth=0.8, alpha=0.4)

# # Plot average yields
# average_yield = np.mean(yield_simulations, axis=0)
# plt.plot(average_yield, color='red', linewidth=2)

# plt.xlabel('Day')
# plt.ylabel('Yield')
# plt.title('Monte Carlo Simulation of Yields')
# plt.legend(['Simulations', 'Average Yield'])
# plt.grid(True)
# plt.show()









