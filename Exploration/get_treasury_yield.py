import requests
import os
import json
import pickle
import os
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
from typing import Dict, List



def get_treasury_yields():
    
    maturities = ["2year", "5year", "7year", "10year", "30year"] #3month excluded due to 5 api request limitation


    #get api key from config
    with open("C:\\Users\Will.Tindall\Projects\Bond_Pricer_Project\config.json") as f:
        config = json.load(f)
    api_key = config["API_KEY"]

    #use yields stored in pickle file
    if os.path.exists("yields.pickle"):
        with open("yields.pickle", "rb") as file:
            yields = pickle.load(file)
        file.close()

    #otherwise call api
    else:

        yields = {}

        for maturity in maturities:

            url = f"https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=monthly&maturity={maturity}&apikey={api_key}"

            #call alpha vantage
            response = requests.get(url)
            all_data = response.json()
            most_recent = all_data["data"][0]

            yields[maturity] = float(most_recent["value"])/100

        with open("yields.pickle", "wb") as file:
            pickle.dump(yields, file)
        file.close()

    return yields

#maturity in years can be plugged into the CubicSpline object to get yield
def yield_curve(input_yields: Dict) -> CubicSpline:

    maturities = [2, 5, 7, 10, 30]
    yields = [i for i in input_yields.values()]

    spline = CubicSpline(maturities, yields)

    return spline





def print_yield_curve(maturities: List, yields: Dict, spline: CubicSpline) -> None:


    # Generate x-values for interpolation
    x_plot = np.linspace(maturities[0], maturities[-1], 100)

    # Evaluate the CubicSpline on the new x array
    y_plot = spline(x_plot)

    # Plot the yield curve
    plt.figure(figsize=(8, 6))
    plt.plot(x_plot, y_plot, label='Yield Curve')
    plt.scatter(maturities, yields, color='red', label='Data Points')
    plt.xlabel('Time (Years)')
    plt.ylabel('Yield')
    plt.title('Yield Curve')
    plt.legend()
    plt.grid(True)
    plt.show()

   




yields = get_treasury_yields()
spline = yield_curve(yields)
print(spline(3))







