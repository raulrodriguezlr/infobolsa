from abc import ABC, abstractmethod
from typing import List
from models.price_series import PriceSeries, PricePoint
from variables import DATA_SOURCES, get_api_key
from datetime import datetime
import yfinance as yf

class Extractor(ABC):
    """
    Clase base para extractores de datos bursátiles.
    Todos los extractores deben implementar el método get_price_series,
    que devuelve una lista de PriceSeries estandarizadas.
    """
    @abstractmethod
    def get_price_series(self, source: str, symbols: List[str], **kwargs):
        """
        Dado el nombre de la fuente y un listado de símbolos, devuelve una lista de PriceSeries.
        """
        pass

class GeneralExtractor(Extractor):
    """
    Extractor general que delega en el método adecuado según la fuente.
    """
    def get_price_series(self, source: str, symbols: List[str], **kwargs):
        if source == "yfinance":
            return self._get_yfinance(symbols, **kwargs)
        # Aquí se pueden añadir más fuentes: alpha_vantage, finnhub, etc.
        raise NotImplementedError(f"Fuente no soportada: {source}")

    def _get_yfinance(self, symbols: List[str], **kwargs):
        result = []
        for symbol in symbols:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(**kwargs)
            data = []
            for idx, row in hist.iterrows():
                data.append(PricePoint(
                    date=idx.date() if hasattr(idx, 'date') else idx,
                    open=row['Open'],
                    high=row['High'],
                    low=row['Low'],
                    close=row['Close'],
                    volume=row['Volume']
                ))
            currency = getattr(ticker.info, 'currency', 'USD') if hasattr(ticker, 'info') else 'USD'
            result.append(PriceSeries(symbol=symbol, currency=currency, data=data))
        return result
