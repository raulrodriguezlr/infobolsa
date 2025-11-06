from typing import Dict, List
import os
from dotenv import load_dotenv

# ======================
# CONFIGURACIÓN GENERAL
# ======================
# Todas las variables aquí deben ser fáciles de entender para cualquier usuario.
# Si tienes dudas, revisa el README o pregunta a tu equipo.



# Fechas para extracción de datos
START_DATE = os.getenv("START_DATE", "2022-01-01")  # Fecha de inicio (YYYY-MM-DD)
END_DATE = os.getenv("END_DATE", "2023-12-31")      # Fecha de fin (YYYY-MM-DD)

load_dotenv()

# Constantes generales
TRADING_DAYS_PER_YEAR = 252
DEFAULT_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_CURRENCY = "USD"
REQUEST_TIMEOUT = 10  # segundos
REQUEST_RETRIES = 3
REQUEST_BACKOFF_FACTOR = 0.3

# ======================
# VARIABLES PRINCIPALES
# ======================
# Lista de símbolos/tickers de la cartera (puedes modificarla en modo interactivo)
SYMBOLS = ["AAPL", "MSFT"]

# Número máximo de gráficos por archivo PNG (por ejemplo, 4 = 4 gráficos juntos)
PLOTS_PER_PNG = 4

# ¿Incluir simulación Monte Carlo para cada ticker individual? (True/False)
INCLUDE_MONTECARLO_TICKERS = True

# ¿Usar precios ajustados (adjusted close)? (True/False)
USE_ADJUSTED_CLOSE = True
# Nombres de variables de entorno para API keys
API_ENV_VARS = {
    "ALPHAVANTAGE": "ALPHAVANTAGE_API_KEY",
    "FINNHUB": "FINNHUB_API_KEY",
    "IEXCLOUD": "IEXCLOUD_API_KEY",
    "TIINGO": "TIINGO_API_KEY",
    "POLYGON": "POLYGON_API_KEY",
    "QUANDL": "QUANDL_API_KEY",
    "TWELVEDATA": "TWELVEDATA_API_KEY",
    "EOD": "EOD_API_KEY",
    "FRED": "FRED_API_KEY",
    "IEX": "IEX_API_KEY",
}

# Listado de fuentes y metadatos útiles para los extractores
# Cada entrada es un diccionario con información orientativa; los extractores pueden usarlo
# para construir URLs, documentar sus límites de peticiones o decidir si requieren key.
DATA_SOURCES: List[Dict] = [
    {
        "id": "yfinance",
        "name": "Yahoo Finance (yfinance)",
        "requires_key": False,
        "note": "Usar la librería `yfinance` para descargar históricos. Sin API key.",
        "historical_endpoint": "yfinance.Ticker.history",
        "rate_limit_per_min": None,
    },
    {
        "id": "alpha_vantage",
        "name": "Alpha Vantage",
        "requires_key": True,
        "env_var": API_ENV_VARS.get("ALPHAVANTAGE"),
        "base_url": "https://www.alphavantage.co/query",
        "historical_endpoint": "TIME_SERIES_DAILY_ADJUSTED",
        "rate_limit_per_min": 5,
    },
    {
        "id": "finnhub",
        "name": "Finnhub",
        "requires_key": True,
        "env_var": API_ENV_VARS.get("FINNHUB"),
        "base_url": "https://finnhub.io/api/v1",
        "historical_endpoint": "/stock/candle",
        "rate_limit_per_min": 60,
    },
    {
        "id": "iex_cloud",
        "name": "IEX Cloud",
        "requires_key": True,
        "env_var": API_ENV_VARS.get("IEXCLOUD"),
        "base_url": "https://cloud.iexapis.com/stable",
        "historical_endpoint": "/stock/{symbol}/chart/",
        "rate_limit_per_min": None,
    },
    {
        "id": "tiingo",
        "name": "Tiingo",
        "requires_key": True,
        "env_var": API_ENV_VARS.get("TIINGO"),
        "base_url": "https://api.tiingo.com",
        "historical_endpoint": "/tiingo/daily/{symbol}/prices",
        "rate_limit_per_min": 500,
    },
    {
        "id": "polygon",
        "name": "Polygon.io",
        "requires_key": True,
        "env_var": API_ENV_VARS.get("POLYGON"),
        "base_url": "https://api.polygon.io",
        "historical_endpoint": "/v2/aggs/ticker/{symbol}/range/1/day/{from}/{to}",
        "rate_limit_per_min": None,
    },
    {
        "id": "quandl",
        "name": "Quandl / Nasdaq Data Link",
        "requires_key": True,
        "env_var": API_ENV_VARS.get("QUANDL"),
        "base_url": "https://data.nasdaq.com/api/v3",
        "historical_endpoint": "/datasets/{database_code}/{dataset_code}/data.json",
        "rate_limit_per_min": None,
    },
    {
        "id": "twelvedata",
        "name": "Twelve Data",
        "requires_key": True,
        "env_var": API_ENV_VARS.get("TWELVEDATA"),
        "base_url": "https://api.twelvedata.com",
        "historical_endpoint": "/time_series",
        "rate_limit_per_min": 8,
    },
    {
        "id": "eod",
        "name": "EOD Historical Data",
        "requires_key": True,
        "env_var": API_ENV_VARS.get("EOD"),
        "base_url": "https://eodhistoricaldata.com/api",
        "historical_endpoint": "/eod/{symbol}",
        "rate_limit_per_min": None,
    },
    {
        "id": "stooq",
        "name": "Stooq",
        "requires_key": False,
        "base_url": "https://stooq.com/q/d/l/",
        "historical_endpoint": "(query params)",
        "note": "Fuente gratuita con CSV histórico; no requiere key.",
        "rate_limit_per_min": None,
    },
    {
        "id": "fred",
        "name": "FRED (macro / series temporales)",
        "requires_key": True,
        "env_var": API_ENV_VARS.get("FRED"),
        "base_url": "https://api.stlouisfed.org/fred",
        "historical_endpoint": "/series/observations",
        "rate_limit_per_min": None,
    }
]



# Variables de entorno para API keys
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "")
YAHOO_API_KEY = os.getenv("YAHOO_API_KEY", "")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "")
# Añade aquí más claves si las necesitas

# Carpeta donde se guardan los resultados (gráficos, datos, etc.)
OUTPUTS_BASE_PATH = os.getenv("OUTPUTS_BASE_PATH", "outputs")
# Formato de subcarpeta por fecha/hora
OUTPUTS_DATE_FORMAT = "%Y-%m-%d_%H%M"


def get_api_key(source_id: str):
    """Devuelve la API key para la fuente indicada, leyendo la variable de entorno correspondiente.

    Retorna None si no existe o si la fuente no está configurada para usar key.
    """
    # Buscar en DATA_SOURCES la entrada que coincida con source_id
    for src in DATA_SOURCES:
        if src.get("id") == source_id:
            env_var = src.get("env_var")
            if env_var:
                return os.getenv(env_var)
            return None
    # Si no hay entrada, también buscar en API_ENV_VARS por coincidencia
    # (por si se llama directamente con el nombre de la variable)
    return os.getenv(API_ENV_VARS.get(source_id.upper(), ""))


# Valores por defecto usados por los extractores
DEFAULTS = {
    "timeout": REQUEST_TIMEOUT,
    "retries": REQUEST_RETRIES,
    "backoff_factor": REQUEST_BACKOFF_FACTOR,
    "date_format": DEFAULT_DATE_FORMAT,
    "trading_days_per_year": TRADING_DAYS_PER_YEAR,
}


# Exportar nombres útiles para autocompletado
__all__ = [
    "TRADING_DAYS_PER_YEAR",
    "DEFAULT_DATE_FORMAT",
    "DEFAULT_CURRENCY",
    "REQUEST_TIMEOUT",
    "REQUEST_RETRIES",
    "REQUEST_BACKOFF_FACTOR",
    "API_ENV_VARS",
    "DATA_SOURCES",
    "get_api_key",
    "DEFAULTS",
    "ALPHA_VANTAGE_API_KEY",
    "YAHOO_API_KEY",
    "FINNHUB_API_KEY",
    "OUTPUTS_BASE_PATH",
    "OUTPUTS_DATE_FORMAT",
    "START_DATE",
    "END_DATE",
    "SYMBOLS",
    "PLOTS_PER_PNG",
    "INCLUDE_MONTECARLO_TICKERS",
    "USE_ADJUSTED_CLOSE",
]
