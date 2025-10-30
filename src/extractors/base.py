from abc import ABC, abstractmethod
import pandas as pd

class BaseExtractor(ABC):
    """
    Clase base para extractores de datos bursátiles.
    Todos los extractores deben implementar el método get_historical_prices,
    que devuelve un DataFrame estandarizado.
    """
    @abstractmethod
    def get_historical_prices(self, ticker: str, start: str, end: str) -> pd.DataFrame:
        pass

    def get_multiple_historical_prices(self, tickers: list, start: str, end: str) -> dict:
        """
        Descarga precios históricos para varios tickers.
        Devuelve un diccionario {ticker: DataFrame}
        """
        return {ticker: self.get_historical_prices(ticker, start, end) for ticker in tickers}
