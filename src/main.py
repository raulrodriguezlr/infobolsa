
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
    start_date = START_DATE
    end_date = END_DATE

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
            plots_per_png = int(input(f"¿Cuántos gráficos por PNG/pop-up? [por defecto {DEFAULT_PLOTS_PER_PNG}]: ") or DEFAULT_PLOTS_PER_PNG)
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
        # Elegir periodo
        print("\nPeriodo de análisis:")
        try:
            start_date_in = input(f"Fecha de inicio (YYYYMMDD, por defecto {START_DATE.replace('-','')}): ").strip()
            if start_date_in:
                start_date = f"{start_date_in[:4]}-{start_date_in[4:6]}-{start_date_in[6:]}"
        except Exception:
            pass
        try:
            end_date_in = input(f"Fecha de fin (YYYYMMDD, por defecto {END_DATE.replace('-','')}): ").strip()
            if end_date_in:
                end_date = f"{end_date_in[:4]}-{end_date_in[4:6]}-{end_date_in[6:]}"
        except Exception:
            pass
        print("\nConfiguración final:")
        print("Tickers:", ', '.join(symbols))
        print(f"Gráficos por PNG/pop-up: {plots_per_png}")
        print(f"Monte Carlo por ticker: {'Sí' if include_mc_tickers else 'No'}")
        print(f"Usar precios ajustados: {'Sí' if use_adjusted_close else 'No'}")
        print(f"Periodo: {start_date} a {end_date}")
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

    # --- Procesamiento y visualización agrupada ---
    import numpy as np
    from math import ceil
    def print_separator():
        print("\n" + "="*80 + "\n")

    def print_title(title):
        print("\n" + "#"*40)
        print(f"{title}")
        print("#"*40 + "\n")

    # Agrupar tickers para gráficos
    n_groups = ceil(len(symbols) / plots_per_png)
    symbol_groups = [symbols[i*plots_per_png:(i+1)*plots_per_png] for i in range(n_groups)]
    all_price_series = []
    all_hists = {}
    for group in symbol_groups:
        print_separator()
        print_title(f"Gráficos para: {', '.join(group)}")
        # --- Descargar y procesar datos de cada ticker del grupo ---
        group_price_series = []
        group_hists = {}
        for symbol in group:
            print_separator()
            print_title(f"Procesando símbolo: {symbol}")
            logging.info(f"Descargando y mostrando datos de: {symbol}")
            try:
                if hasattr(extractor, 'get_all_data'):
                    result = extractor.get_all_data(symbol, start=start_date, end=end_date)
                    hist = result['historical'] if isinstance(result, dict) and 'historical' in result else result
                else:
                    result = extractor.get_historical_prices(symbol, start=start_date, end=end_date)
                    hist = result['historical'] if isinstance(result, dict) and 'historical' in result else result
                if isinstance(hist, pd.DataFrame) and not hist.empty:
                    # EDA: resumen estadístico
                    print("\nResumen estadístico (describe):")
                    print(hist.describe().T)
                    print("\nDistribución de precios de cierre:")
                    print(hist['close'].describe())
                    # --- 10-K/10-Q (placeholder) ---
                    print("\n[INFO] Descargando informes 10-K/10-Q (no implementado, placeholder)")
                    # Aquí se podría integrar la descarga real de informes
                    # --- Gráficos de precios y Monte Carlo agrupados ---
                    group_hists[symbol] = hist
                    price_points = [PricePoint(
                        date=row['date'],
                        open=row['open'],
                        high=row['high'],
                        low=row['low'],
                        close=row['close'],
                        volume=row['volume']
                    ) for _, row in hist.iterrows()]
                    ps = PriceSeries(symbol=symbol, currency="USD", data=price_points)
                    group_price_series.append(ps)
                    all_price_series.append(ps)
                else:
                    print(f"No hay datos históricos para {symbol}.")
            except Exception as e:
                print("\n" + "!"*60)
                logging.error(f"Error al obtener datos de {symbol}: {e}")
                print("!"*60 + "\n")
                continue
        # --- Gráficos agrupados de precios históricos ---
        if group_hists:
            plt.figure(figsize=(6*len(group_hists), 4))
            for idx, (symbol, hist) in enumerate(group_hists.items()):
                plt.subplot(1, len(group_hists), idx+1)
                plt.plot(hist['date'], hist['close'], label=f"{symbol} Close")
                plt.title(f"{symbol} - Precio histórico")
                plt.xlabel("Fecha"); plt.ylabel("Precio")
                plt.legend(); plt.tight_layout()
            output_manager.save_plot(plt, f"{'_'.join(group)}_historical_grouped.png")
            plt.show()
        # --- Gráficos agrupados de Monte Carlo ---
        if include_mc_tickers and group_price_series:
            plt.figure(figsize=(6*len(group_price_series), 4))
            for idx, ps in enumerate(group_price_series):
                sim = MonteCarloSimulator(n_simulations=200, n_days=252)
                simulations = sim.simulate_price_series(ps)
                plt.subplot(1, len(group_price_series), idx+1)
                for i in range(min(100, simulations.shape[0])):
                    plt.plot(simulations[i], color="blue", alpha=0.1)
                plt.title(f"{ps.symbol} - Monte Carlo")
                plt.xlabel("Días"); plt.ylabel("Precio simulado")
                plt.tight_layout()
            output_manager.save_plot(plt, f"{'_'.join([ps.symbol for ps in group_price_series])}_montecarlo_grouped.png")
            plt.show()
        all_hists.update(group_hists)


    # --- Análisis de Portfolio completo ---
    if all_price_series:
        print_separator()
        print_title("REPORTE DE CARTERA")
        logging.info("Creando Portfolio con todos los activos descargados...")
        portfolio = Portfolio(
            name="Portfolio de Infobolsa",
            assets=all_price_series
        )
        portfolio.report(show=True)
        report_text = portfolio.report(show=False)
        with open(output_manager.get_path("portfolio_report.md"), "w") as f:
            f.write(report_text)
        print_separator()
        print_title("Simulación Monte Carlo de la cartera completa")
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
        print_separator()
        print_title("Matriz de correlación de precios de cierre")
        # Construir DataFrame de precios de cierre
        close_data = {}
        for ps in all_price_series:
            close_data[ps.symbol] = [pp.close for pp in ps.data]
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
        print_separator()
        print_title("Análisis de cartera completado y guardado.")

    print_separator()
    print(f"Todos los datos y gráficos han sido guardados en la carpeta de outputs ({OUTPUTS_BASE_PATH}).\n")

# Entrypoint
if __name__ == "__main__":
    main()
