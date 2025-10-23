"""
Visualización de resultados y simulaciones para carteras y series de precios.
"""
import matplotlib.pyplot as plt
import numpy as np
from models.price_series import PriceSeries
from models.portfolio import Portfolio


def plot_price_series(price_series: PriceSeries):
    """
    Dibuja la serie histórica de precios de cierre de un activo.
    """
    dates = [p.date for p in price_series.data]
    closes = [p.close for p in price_series.data]
    plt.figure(figsize=(10, 4))
    plt.plot(dates, closes, label=price_series.symbol)
    plt.title(f"Precio histórico: {price_series.symbol}")
    plt.xlabel("Fecha")
    plt.ylabel(f"Precio ({price_series.currency})")
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_portfolio_simulation(simulation_result, n_simulations=100, title="Simulación Monte Carlo de Cartera"):
    """
    Dibuja varias trayectorias simuladas del valor de la cartera.
    simulation_result: array (n_simulations, n_days+1)
    """
    plt.figure(figsize=(10, 4))
    for i in range(min(n_simulations, simulation_result.shape[0])):
        plt.plot(simulation_result[i], color="blue", alpha=0.1)
    plt.title(title)
    plt.xlabel("Días")
    plt.ylabel("Valor simulado")
    plt.tight_layout()
    plt.show()


def plots_report(portfolio, sim_result=None, n_simulations=100):
    """
    Muestra visualizaciones útiles para la cartera y sus activos.
    Si se pasa sim_result, también muestra la simulación de Monte Carlo.
    """
    for asset in portfolio.assets:
        plot_price_series(asset)
    if sim_result is not None:
        plot_portfolio_simulation(sim_result, n_simulations=n_simulations)
