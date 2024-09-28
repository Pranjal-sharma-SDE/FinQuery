import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query"
DATA_DIR = "./data"

def fetch_stock_data(symbol: str, interval: str = "5min"):
    url = f"{BASE_URL}?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    time_series_key = f"Time Series ({interval})"
    if time_series_key in data:
        stock_data = pd.DataFrame.from_dict(data[time_series_key], orient='index')
        save_stock_data(stock_data, symbol, interval)
        return stock_data
    else:
        raise ValueError("Failed to fetch data. Check API Key or symbol.")

def save_stock_data(stock_data, symbol, interval):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    file_name = os.path.join(DATA_DIR, f"stock_data_{symbol}_{interval}.csv")
    stock_data.to_csv(file_name)
    print(f"Stock data saved to {file_name}")

def fetch_top_gainers_losers():
    url = f"{BASE_URL}?function=TOP_GAINERS_LOSERS&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "top_gainers" in data and "top_losers" in data:
        gainers = pd.DataFrame(data["top_gainers"])
        losers = pd.DataFrame(data["top_losers"])
        save_gainers_losers(gainers, losers)
        return gainers, losers
    else:
        raise ValueError("Failed to fetch gainers and losers.")

def save_gainers_losers(gainers, losers):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    gainers_file = os.path.join(DATA_DIR, "top_gainers.csv")
    losers_file = os.path.join(DATA_DIR, "top_losers.csv")
    
    gainers.to_csv(gainers_file, index=False)
    losers.to_csv(losers_file, index=False)
    
    print(f"Gainers data saved to {gainers_file}")
    print(f"Losers data saved to {losers_file}")
