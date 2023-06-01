import requests
import os
import json

def get_treasury_yield(
        maturity: str, #Strings 3month, 2year, 5year, 7year, 10year, and 30year are accepted.

) -> float:
    
    #get api key from config
    with open("C:\\Users\Will.Tindall\Projects\Bond_Pricer_Project\config.json") as f:
        config = json.load(f)
    api_key = config["API_KEY"]

    url = f"https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=monthly&maturity={maturity}&apikey={api_key}"

    #call alpha vantage
    response = requests.get(url)
    all_data = response.json()

    most_recent = all_data["data"][0]

    return float(most_recent["value"])/100





