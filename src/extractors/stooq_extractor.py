import pandas as pd
import requests
from .base import BaseExtractor
from src.utils.data_cleaning import clean_dataframe

class StooqExtractor(BaseExtractor):
    """
    Extractor de datos históricos desde Stooq (fuente gratuita, sin API key).
    """
    BASE_URL = "https://stooq.com/q/d/l/"

    def get_historical_prices(self, ticker: str, start: str, end: str) -> pd.DataFrame:
        params = {
            's': ticker.lower(),
            'd1': start.replace('-', ''),
            'd2': end.replace('-', ''),
            'i': 'd'
        }
        response = requests.get(self.BASE_URL, params=params)
        df = pd.read_csv(pd.compat.StringIO(response.text))
        df['ticker'] = ticker
        df = df.rename(columns={
            'Date': 'date', 'Open': 'open', 'High': 'high',
            'Low': 'low', 'Close': 'close', 'Volume': 'volume'
        })
        df = df[['date', 'open', 'high', 'low', 'close', 'volume', 'ticker']]
        df = clean_dataframe(df)
        return df
