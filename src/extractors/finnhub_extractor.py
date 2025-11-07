
import pandas as pd
import requests
from .base import BaseExtractor
from src.utils.data_cleaning import clean_dataframe
from src.variables import FINNHUB_API_KEY

class FinnhubExtractor(BaseExtractor):
    """
    Extractor de datos históricos desde Finnhub.
    """
    BASE_URL = "https://finnhub.io/api/v1/stock/candle"

    def get_historical_prices(self, ticker: str, start: str, end: str) -> pd.DataFrame:
        params = {
            'symbol': ticker,
            'resolution': 'D',
            'from': int(pd.Timestamp(start).timestamp()),
            'to': int(pd.Timestamp(end).timestamp()),
            'token': FINNHUB_API_KEY
        }
        response = requests.get(self.BASE_URL, params=params)
        data = response.json()
        if data.get('s') != 'ok':
            return pd.DataFrame()
        df = pd.DataFrame({
            'date': pd.to_datetime(data['t'], unit='s'),
            'open': data['o'],
            'high': data['h'],
            'low': data['l'],
            'close': data['c'],
            'volume': data['v']
        })
        df['ticker'] = ticker
        df = clean_dataframe(df)
        return df
