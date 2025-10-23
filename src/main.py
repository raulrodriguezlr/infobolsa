# Entry point for infobolsa toolkit
import sys
from extractor.extractor import GeneralExtractor
from models.portfolio import Portfolio
from visualization.plots import plots_report


def main():
    print("Bienvenido a Infobolsa Toolkit")
    symbols = ["AAPL", "MSFT"]
    extractor = GeneralExtractor()
    print(f"Descargando históricos de: {symbols}")
    series_list = extractor.get_price_series("yfinance", symbols, period="2y")
    portfolio = Portfolio(name="Demo", assets=series_list)
    print("Simulando cartera...")
    sim_result = portfolio.monte_carlo_simulation(n_simulations=200, n_days=252)
    portfolio.report(show=True)
    plots_report(portfolio, sim_result, n_simulations=100)


if __name__ == "__main__":
    main()
