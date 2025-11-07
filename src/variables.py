from typing import Dict, List
import os
from dotenv import load_dotenv

# ======================
# CONFIGURACIÓN GENERAL
# ======================
# Todas las variables aquí deben ser fáciles de entender para cualquier usuario.
# Si tienes dudas, revisa el README o pregunta a tu equipo.



# Fechas para extracción de datos
START_DATE = os.getenv("START_DATE", "2025-01-01")  # Fecha de inicio (YYYY-MM-DD)
END_DATE = os.getenv("END_DATE", "2025-11-06")      # Fecha de fin (YYYY-MM-DD)

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
SYMBOLS = ["AAPL", "MSFT","NFLX","DIS"]

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
    "CIK": "CIK",
}



# Variables de entorno para API keys
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "")
YAHOO_API_KEY = os.getenv("YAHOO_API_KEY", "")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "")
CIK = os.getenv("CIK", "")
# Añade aquí más claves si las necesitas

# Carpeta donde se guardan los resultados (gráficos, datos, etc.)
OUTPUTS_BASE_PATH = os.getenv("OUTPUTS_BASE_PATH", "outputs")
# Formato de subcarpeta por fecha/hora
OUTPUTS_DATE_FORMAT = "%Y-%m-%d_%H%M"





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
