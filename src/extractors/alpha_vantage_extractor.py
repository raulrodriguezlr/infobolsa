
import pandas as pd
import requests
from .base import BaseExtractor
from src.utils.data_cleaning import clean_dataframe
from src.variables import ALPHA_VANTAGE_API_KEY

class AlphaVantageExtractor(BaseExtractor):
    """
    Extractor de datos históricos desde Alpha Vantage.
    """
    BASE_URL = "https://www.alphavantage.co/query"

    def get_historical_prices(self, ticker: str, start: str, end: str) -> pd.DataFrame:
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": ticker,
            "outputsize": "full",
            "apikey": ALPHA_VANTAGE_API_KEY
        }
        response = requests.get(self.BASE_URL, params=params)
        data = response.json().get("Time Series (Daily)", {})
        rows = []
        for date, values in data.items():
            rows.append({
                "date": date,
                "open": float(values["1. open"]),
                "high": float(values["2. high"]),
                "low": float(values["3. low"]),
                "close": float(values["4. close"]),
                "volume": float(values["5. volume"]),
                "ticker": ticker
            })
        df = pd.DataFrame(rows)
        df = df[(df["date"] >= start) & (df["date"] <= end)]
        df = clean_dataframe(df)
        return df
