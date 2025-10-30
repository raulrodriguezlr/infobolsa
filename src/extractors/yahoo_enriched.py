import pandas as pd
import yfinance as yf
from .base import BaseExtractor
from src.utils.data_cleaning import clean_dataframe
from src.utils.output_manager import OutputManager

class YahooEnrichedExtractor(BaseExtractor):
    """
    Extractor enriquecido de Yahoo Finance: precios, fundamentales, dividendos, splits, calendario, recomendaciones, estados financieros, ESG, noticias, opciones...
    """
    def __init__(self):
        self.output_manager = OutputManager()

    def get_historical_prices(self, ticker: str, start: str, end: str) -> dict:
        data = yf.Ticker(ticker)
        result = {}
        # Precios históricos
        hist = data.history(start=start, end=end).reset_index()
        hist['ticker'] = ticker
        hist = hist.rename(columns={
            'Date': 'date', 'Open': 'open', 'High': 'high',
            'Low': 'low', 'Close': 'close', 'Volume': 'volume', 'Adj Close': 'adj_close'
        })
        hist = clean_dataframe(hist)
        self.output_manager.save_dataframe(hist, f"{ticker}_historical.csv")
        result['historical'] = hist
        # Info y fast_info
        info = getattr(data, 'info', {})
        fast = dict(getattr(data, 'fast_info', {})) if hasattr(data, 'fast_info') else {}
        result['info'] = info
        result['fast_info'] = fast
        # Dividendos, splits, acciones
        divs = getattr(data, 'dividends', pd.Series()).reset_index()
        splits = getattr(data, 'splits', pd.Series()).reset_index()
        actions = getattr(data, 'actions', pd.DataFrame())
        self.output_manager.save_dataframe(divs, f"{ticker}_dividends.csv")
        self.output_manager.save_dataframe(splits, f"{ticker}_splits.csv")
        self.output_manager.save_dataframe(actions, f"{ticker}_actions.csv")
        result['dividends'] = divs
        result['splits'] = splits
        result['actions'] = actions
        # Calendario
        cal = getattr(data, 'calendar', pd.DataFrame())
        result['calendar'] = cal
        # Estados financieros
        result['financials'] = getattr(data, 'financials', pd.DataFrame())
        result['balancesheet'] = getattr(data, 'balancesheet', pd.DataFrame())
        result['cashflow'] = getattr(data, 'cashflow', pd.DataFrame())
        # Earnings
        result['earnings'] = getattr(data, 'earnings', pd.DataFrame())
        result['quarterly_earnings'] = getattr(data, 'quarterly_earnings', pd.DataFrame())
        # Recomendaciones
        result['recommendations'] = getattr(data, 'recommendations', pd.DataFrame())
        # ESG
        result['sustainability'] = getattr(data, 'sustainability', pd.DataFrame())
        # Noticias
        result['news'] = getattr(data, 'news', [])
        # Opciones
        expirations = list(getattr(data, 'options', []))
        result['options'] = {}
        for exp in expirations[:3]:  # Solo las 3 primeras para no saturar
            try:
                chain = data.option_chain(exp)
                result['options'][exp] = {'calls': chain.calls, 'puts': chain.puts}
            except Exception:
                continue
        # Guardar info y fast_info
        import json
        self.output_manager.get_path(f"{ticker}_info.json")
        with open(self.output_manager.get_path(f"{ticker}_info.json"), "w", encoding="utf-8") as f:
            json.dump(info, f, ensure_ascii=False, indent=2)
        self.output_manager.get_path(f"{ticker}_fast_info.json")
        with open(self.output_manager.get_path(f"{ticker}_fast_info.json"), "w", encoding="utf-8") as f:
            json.dump(fast, f, ensure_ascii=False, indent=2)
        return result
