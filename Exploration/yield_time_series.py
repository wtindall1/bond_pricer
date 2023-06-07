from enum import Enum
import json
import requests
from datetime import date, timedelta
import pandas as pd
import numpy as np

#s&p / fitch ratings
class CreditRating(str, Enum):
    AAAplus = "AAA+"
    AAA = "AAA"
    AAplus = "AA+"
    AA = "AA"
    AAminus = "AA-"
    Aplus = "A+"
    A = "A"
    Aminus = "A-"
    BBBplus = "BBB+"
    BBB = "BBB"
    BBBminus = "BBB-"
    BBplus = "BB+"
    BB = "BB"
    BBminus = "BB-"
    Bplus = "B+"
    B = "B"
    Bminus = "B-"
    CCCplus = "CCC+"
    CCC = "CCC"
    CCCminus = "CCC-"
    CC = "CC"
    C = "C"
    D = "D"
    

def get_yield_time_series(credit_rating: CreditRating, years:int):

    #using yield from bond indices with same or similar credit rating
    #assuming input bond maturity is same as index average, due to data limitations
    try:
        rating = CreditRating(credit_rating)
        print(f"Valid credit rating: {rating.name}")
    except ValueError:
        print("Invalid credit rating")
        return

    #match creditrating to FRED series_id
    if "AAA" in rating.value:
        series_id = "BAMLC0A1CAAAEY"
    elif "AA" in rating.value:
        series_id = "BAMLC0A2CAAEY"
    elif "A" in rating.value:
        series_id = "BAMLC0A3CAEY"
    elif "BBB" in rating.value:
        series_id = "BAMLC0A4CBBBEY"
    elif "BB" in rating.value:
        series_id = "BAMLEM3BRRBBCRPIEY"
    else:
        series_id = "BAMLEMHBHYCRPIEY"



    #get api key from config
    with open("C:\\Users\Will.Tindall\Projects\Bond_Pricer_Project\config.json") as f:
        config = json.load(f)
    api_key = config["FRED_API_KEY"]

    #get yesterday's date so api only returns one value
    observation_start = date.today() - timedelta(weeks=years*52)


    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json&observation_start={observation_start}"

    response = requests.get(url)
    data = response.json()
    dates = [item["date"] for item in data["observations"]]
    yields = [float(item["value"]) if item["value"] != '.' else np.nan for item in data["observations"]]


    series = pd.Series(np.array(yields), index=dates)
    
    return series


#get_yield_time_series('AA+', 1)


