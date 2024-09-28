import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
NEWS_SENTIMENT_URL = "https://www.alphavantage.co/query"
DATA_DIR = "./data"

def fetch_news_sentiment(tickers: str, limit=50, topics=None, sort="LATEST"):
    url = f"{NEWS_SENTIMENT_URL}?function=NEWS_SENTIMENT&tickers={tickers}&apikey={ALPHA_VANTAGE_API_KEY}&limit={limit}&sort={sort}"
    if topics:
        url += f"&topics={topics}"

    response = requests.get(url)
    data = response.json()

    if "feed" in data:
        save_data(data["feed"], tickers)
        return data["feed"]
    else:
        raise ValueError("Failed to fetch news sentiment data. Check API Key or parameters.")

def save_data(data, tickers):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    file_name = os.path.join(DATA_DIR, f"news_sentiment_{tickers.replace(',', '_')}.json")
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {file_name}")
