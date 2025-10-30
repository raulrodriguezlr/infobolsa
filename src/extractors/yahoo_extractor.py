import pandas as pd
import yfinance as yf
from .base import BaseExtractor
from src.utils.data_cleaning import clean_dataframe
from src.utils.output_manager import OutputManager

class YahooFinanceExtractor(BaseExtractor):
    """
    Extractor de datos históricos y fundamentales desde Yahoo Finance.
    """
    def __init__(self):
        self.output_manager = OutputManager()

    def get_historical_prices(self, ticker: str, start: str, end: str) -> pd.DataFrame:
        ticker_obj = yf.Ticker(ticker)
        df = ticker_obj.history(start=start, end=end)
        df = df.reset_index()
        df['ticker'] = ticker
        # Estandarizar columnas
        df = df.rename(columns={
            'Date': 'date', 'Open': 'open', 'High': 'high',
            'Low': 'low', 'Close': 'close', 'Volume': 'volume'
        })
        df = df[['date', 'open', 'high', 'low', 'close', 'volume', 'ticker']]
        df = clean_dataframe(df)
        self.output_manager.save_dataframe(df, f"{ticker}_historical.csv")
        return df

    def get_fundamentals(self, ticker: str) -> dict:
        ticker_obj = yf.Ticker(ticker)
        info = ticker_obj.info
        # Guardar como JSON
        import json
        path = self.output_manager.get_path(f"{ticker}_fundamentals.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(info, f, ensure_ascii=False, indent=2)
        return info

    def get_dividends(self, ticker: str) -> pd.DataFrame:
        ticker_obj = yf.Ticker(ticker)
        div = ticker_obj.dividends.reset_index()
        div['ticker'] = ticker
        self.output_manager.save_dataframe(div, f"{ticker}_dividends.csv")
        return div

    def get_splits(self, ticker: str) -> pd.DataFrame:
        ticker_obj = yf.Ticker(ticker)
        splits = ticker_obj.splits.reset_index()
        splits['ticker'] = ticker
        self.output_manager.save_dataframe(splits, f"{ticker}_splits.csv")
        return splits
