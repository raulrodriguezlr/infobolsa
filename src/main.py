# Entry point for infobolsa toolkit
import sys
import logging
import pandas as pd
import matplotlib.pyplot as plt
import warnings
from src.extractors.yahoo_enriched import YahooEnrichedExtractor
from src.extractors.yahoo_extractor import YahooFinanceExtractor
from src.extractors.alpha_vantage_extractor import AlphaVantageExtractor
from src.extractors.stooq_extractor import StooqExtractor
from src.extractors.finnhub_extractor import FinnhubExtractor
from src.simulation.montecarlo import MonteCarloSimulator
from src.utils.output_manager import OutputManager
from src.variables import OUTPUTS_BASE_PATH, START_DATE, END_DATE, SYMBOLS 

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

EXTRACTORS = [
    ("Yahoo Finance (enriquecido)", YahooEnrichedExtractor),
    ("Yahoo Finance (básico)", YahooFinanceExtractor),
    ("Alpha Vantage", AlphaVantageExtractor),
    ("Stooq", StooqExtractor),
    ("Finnhub", FinnhubExtractor)
]

def main() -> None:
    """
    Punto de entrada principal para Infobolsa Toolkit (Enriquecido).
    Descarga, muestra y guarda datos bursátiles enriquecidos y visualizaciones para una lista de símbolos.
    """
    print("\nSeleccione el extractor de datos:")
    for idx, (name, _) in enumerate(EXTRACTORS, 1):
        print(f"  {idx}. {name}")
    while True:
        try:
            opt = int(input("Opción [1-{}]: ".format(len(EXTRACTORS))))
            if 1 <= opt <= len(EXTRACTORS):
                break
        except Exception:
            pass
        print("Opción no válida. Intente de nuevo.")
    extractor_class = EXTRACTORS[opt-1][1]
    extractor = extractor_class()

    output_manager = OutputManager()
    # Suprimir todos los warnings (incluyendo DeprecationWarning y FutureWarning)
    warnings.filterwarnings("ignore")

    for symbol in SYMBOLS:
        logging.info(f"Descargando y mostrando datos de: {symbol}")
        try:
            # Llama al método adecuado y maneja ambos tipos de retorno
            if hasattr(extractor, 'get_all_data'):
                result = extractor.get_all_data(symbol, start=START_DATE, end=END_DATE)
                hist = result['historical'] if isinstance(result, dict) and 'historical' in result else result
            else:
                result = extractor.get_historical_prices(symbol, start=START_DATE, end=END_DATE)
                hist = result['historical'] if isinstance(result, dict) and 'historical' in result else result
            if isinstance(hist, pd.DataFrame) and not hist.empty:
                print(f"\nDatos históricos para {symbol}:")
                print(hist.head(10))
                plt.figure(figsize=(10, 4))
                plt.plot(hist['date'], hist['close'], label=f"{symbol} Close")
                plt.title(f"{symbol} - Precio histórico")
                plt.xlabel("Fecha"); plt.ylabel("Precio")
                plt.legend(); plt.tight_layout()
                output_manager.save_plot(plt, f"{symbol}_historical_plot.png")
                plt.show()
                # --- Monte Carlo usando PriceSeries ---
                from src.models.price_series import PriceSeries, PricePoint
                # Convertir DataFrame a PriceSeries
                price_points = []
                for _, row in hist.iterrows():
                    price_points.append(PricePoint(
                        date=row['date'],
                        open=row['open'],
                        high=row['high'],
                        low=row['low'],
                        close=row['close'],
                        volume=row['volume']
                    ))
                ps = PriceSeries(symbol=symbol, currency="USD", data=price_points)
                sim = MonteCarloSimulator(n_simulations=200, n_days=252)
                simulations = sim.simulate_price_series(ps)
                plt.figure(figsize=(10, 4))
                for i in range(min(100, simulations.shape[0])):
                    plt.plot(simulations[i], color="blue", alpha=0.1)
                plt.title(f"{symbol} - Simulación Monte Carlo (252 días)")
                plt.xlabel("Días"); plt.ylabel("Precio simulado")
                plt.tight_layout()
                output_manager.save_plot(plt, f"{symbol}_montecarlo_plot.png")
                plt.show()
        except Exception as e:
            logging.error(f"Error al obtener datos de {symbol}: {e}")
            continue
    logging.info(f"Todos los datos y gráficos han sido guardados en la carpeta de outputs ({OUTPUTS_BASE_PATH}).")

if __name__ == "__main__":
    main()
