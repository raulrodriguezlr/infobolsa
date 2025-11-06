
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
from src.variables import OUTPUTS_BASE_PATH, START_DATE, END_DATE, SYMBOLS as DEFAULT_SYMBOLS, PLOTS_PER_PNG as DEFAULT_PLOTS_PER_PNG, INCLUDE_MONTECARLO_TICKERS as DEFAULT_INCLUDE_MONTECARLO_TICKERS, USE_ADJUSTED_CLOSE as DEFAULT_USE_ADJUSTED_CLOSE
from src.models.price_series import PriceSeries, PricePoint
from src.models.portfolio import Portfolio

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

EXTRACTORS = [
    ("Yahoo Finance (enriquecido)", YahooEnrichedExtractor),
    ("Yahoo Finance (básico)", YahooFinanceExtractor),
    ("Alpha Vantage", AlphaVantageExtractor),
    ("Stooq", StooqExtractor),
    ("Finnhub", FinnhubExtractor)
]

def main():
    """
    Punto de entrada principal para Infobolsa Toolkit (Enriquecido).
    Descarga, muestra y guarda datos bursátiles enriquecidos y visualizaciones para una lista de símbolos.
    """
    interactive = '-i' in sys.argv or '--interactive' in sys.argv
    symbols = list(DEFAULT_SYMBOLS)
    plots_per_png = DEFAULT_PLOTS_PER_PNG
    include_mc_tickers = DEFAULT_INCLUDE_MONTECARLO_TICKERS
    use_adjusted_close = DEFAULT_USE_ADJUSTED_CLOSE

    print("\n" + "#"*70)
    print("INFOTBOLSA TOOLKIT - ANÁLISIS DE MERCADOS BURSÁTILES")
    print("#"*70 + "\n")

    if interactive:
        print("[MODO INTERACTIVO]")
        print("\nTickers cargados:", ', '.join(symbols))
        while True:
            resp = input("¿Quieres agregar algún ticker más? (s/n): ").strip().lower()
            if resp == 's':
                while True:
                    print("\n1. Agregar ticker\n2. Continuar")
                    op = input("Elige opción: ").strip()
                    if op == '1':
                        new_ticker = input("Introduce el símbolo del nuevo ticker: ").strip().upper()
                        if new_ticker and new_ticker not in symbols:
                            symbols.append(new_ticker)
                            print(f"Ticker {new_ticker} agregado. Tickers actuales: {', '.join(symbols)}")
                        else:
                            print("Ticker vacío o ya existente.")
                    elif op == '2':
                        break
                    else:
                        print("Opción no válida.")
                break
            elif resp == 'n':
                break
            else:
                print("Por favor, responde 's' o 'n'.")
        print("\nConfiguración de visualización:")
        try:
            plots_per_png = int(input(f"¿Cuántos gráficos por PNG? [por defecto {DEFAULT_PLOTS_PER_PNG}]: ") or DEFAULT_PLOTS_PER_PNG)
        except Exception:
            plots_per_png = DEFAULT_PLOTS_PER_PNG
        try:
            include_mc_tickers = input(f"¿Incluir Monte Carlo para cada ticker? (s/n, por defecto {'s' if DEFAULT_INCLUDE_MONTECARLO_TICKERS else 'n'}): ").strip().lower()
            if include_mc_tickers == 'n':
                include_mc_tickers = False
            else:
                include_mc_tickers = True
        except Exception:
            include_mc_tickers = DEFAULT_INCLUDE_MONTECARLO_TICKERS
        try:
            use_adjusted_close = input(f"¿Usar precios ajustados (adjusted close)? (s/n, por defecto {'s' if DEFAULT_USE_ADJUSTED_CLOSE else 'n'}): ").strip().lower()
            if use_adjusted_close == 'n':
                use_adjusted_close = False
            else:
                use_adjusted_close = True
        except Exception:
            use_adjusted_close = DEFAULT_USE_ADJUSTED_CLOSE
        print("\nConfiguración final:")
        print("Tickers:", ', '.join(symbols))
        print(f"Gráficos por PNG: {plots_per_png}")
        print(f"Monte Carlo por ticker: {'Sí' if include_mc_tickers else 'No'}")
        print(f"Usar precios ajustados: {'Sí' if use_adjusted_close else 'No'}")
        print("\n" + "-"*70 + "\n")
    else:
        print("[MODO NO INTERACTIVO]")
        print("Tickers cargados:", ', '.join(symbols))
        print("\n" + "-"*70 + "\n")

    print("Seleccione el extractor de datos:")
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
    warnings.filterwarnings("ignore")
    all_price_series = []

    for symbol in symbols:
        print("\n" + "="*40)
        print(f"Procesando símbolo: {symbol}")
        print("="*40 + "\n")
        logging.info(f"Descargando y mostrando datos de: {symbol}")
        try:
            if hasattr(extractor, 'get_all_data'):
                result = extractor.get_all_data(symbol, start=START_DATE, end=END_DATE)
                hist = result['historical'] if isinstance(result, dict) and 'historical' in result else result
            else:
                result = extractor.get_historical_prices(symbol, start=START_DATE, end=END_DATE)
                hist = result['historical'] if isinstance(result, dict) and 'historical' in result else result
            if isinstance(hist, pd.DataFrame) and not hist.empty:
                print(f"\nDatos históricos para {symbol} (primeras 10 filas):\n")
                print(hist.head(10))
                plt.figure(figsize=(10, 4))
                plt.plot(hist['date'], hist['close'], label=f"{symbol} Close")
                plt.title(f"{symbol} - Precio histórico")
                plt.xlabel("Fecha"); plt.ylabel("Precio")
                plt.legend(); plt.tight_layout()
                output_manager.save_plot(plt, f"{symbol}_historical_plot.png")
                plt.show()
                # --- Monte Carlo usando PriceSeries ---
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
                all_price_series.append(ps)
                if include_mc_tickers:
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
            print("\n" + "!"*60)
            logging.error(f"Error al obtener datos de {symbol}: {e}")
            print("!"*60 + "\n")
            continue


    # --- Análisis de Portfolio completo ---
    if all_price_series:
        print("\n" + "#"*60)
        logging.info("Creando Portfolio con todos los activos descargados...")
        portfolio = Portfolio(
            name="Portfolio de Infobolsa",
            assets=all_price_series
        )
        print("\n" + "="*60)
        print("REPORTE DE CARTERA")
        print("="*60 + "\n")
        portfolio.report(show=True)
        report_text = portfolio.report(show=False)
        with open(output_manager.get_path("portfolio_report.md"), "w") as f:
            f.write(report_text)
        print("\n" + "-"*60)
        print("Simulación Monte Carlo de la cartera completa...")
        print("-"*60 + "\n")
        portfolio_sims = portfolio.monte_carlo_simulation(n_simulations=200, n_days=252)
        plt.figure(figsize=(12, 6))
        for i in range(min(100, portfolio_sims.shape[0])):
            plt.plot(portfolio_sims[i], color="purple", alpha=0.1)
        plt.title("Portfolio - Simulación Monte Carlo (252 días)")
        plt.xlabel("Días")
        plt.ylabel("Valor total de la cartera")
        plt.tight_layout()
        output_manager.save_plot(plt, "portfolio_montecarlo.png")
        plt.show()

        # --- Matriz de correlación de precios de cierre ---
        print("\n" + "-"*60)
        print("Matriz de correlación de precios de cierre")
        print("-"*60 + "\n")
        # Construir DataFrame de precios de cierre
        close_data = {}
        for ps in all_price_series:
            # ps.data es una lista de PricePoint
            close_data[ps.symbol] = [pp.close for pp in ps.data]
        # Alinear longitudes (rellenar con NaN si es necesario)
        max_len = max(len(lst) for lst in close_data.values())
        for k in close_data:
            if len(close_data[k]) < max_len:
                close_data[k] += [float('nan')] * (max_len - len(close_data[k]))
        close_df = pd.DataFrame(close_data)
        corr = close_df.corr()
        print(corr)
        plt.figure(figsize=(8, 6))
        im = plt.imshow(corr, cmap='coolwarm', vmin=-1, vmax=1)
        plt.colorbar(im, fraction=0.046, pad=0.04)
        plt.xticks(range(len(corr.columns)), corr.columns, rotation=45)
        plt.yticks(range(len(corr.index)), corr.index)
        plt.title("Matriz de correlación de precios de cierre")
        plt.tight_layout()
        output_manager.save_plot(plt, "correlation_matrix.png")
        plt.show()

        print("\n" + "#"*60)
        print("Análisis de cartera completado y guardado.")
        print("#"*60 + "\n")

    print(f"\nTodos los datos y gráficos han sido guardados en la carpeta de outputs ({OUTPUTS_BASE_PATH}).\n")

# Entrypoint
if __name__ == "__main__":
    main()
