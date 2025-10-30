"""
Simulación de Monte Carlo para series de precios y carteras.
"""
import numpy as np
from src.models.price_series import PriceSeries

class MonteCarloSimulator:
    """
    Simulador de Monte Carlo para la evolución de un activo o cartera.
    """
    def __init__(self, n_simulations=1000, n_days=252):
        self.n_simulations = n_simulations
        self.n_days = n_days

    def simulate_price_series(self, price_series: PriceSeries, mu=None, sigma=None):
        """
        Simula trayectorias de precios para un activo usando Monte Carlo.
        Si mu y sigma no se pasan, se calculan de la serie histórica.
        Devuelve un array (n_simulations, n_days+1) con las simulaciones.
        """
        closes = [p.close for p in price_series.data]
        if len(closes) < 2:
            raise ValueError("No hay suficientes datos para simular.")
        log_returns = np.diff(np.log(closes))
        if mu is None:
            mu = np.mean(log_returns)
        if sigma is None:
            sigma = np.std(log_returns)
        S0 = closes[-1]
        dt = 1
        simulations = np.zeros((self.n_simulations, self.n_days+1))
        simulations[:, 0] = S0
        for t in range(1, self.n_days+1):
            Z = np.random.standard_normal(self.n_simulations)
            simulations[:, t] = simulations[:, t-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)
        return simulations

    def simulate_portfolio(self, portfolio, mu_sigma_dict=None):
        """
        Simula la evolución de una cartera sumando las simulaciones de cada activo.
        mu_sigma_dict puede ser un dict {symbol: (mu, sigma)} para personalizar parámetros.
        Devuelve un array (n_simulations, n_days+1) con el valor total de la cartera.
        """
        asset_sims = []
        for asset in portfolio.assets:
            mu, sigma = None, None
            if mu_sigma_dict and asset.symbol in mu_sigma_dict:
                mu, sigma = mu_sigma_dict[asset.symbol]
            sim = self.simulate_price_series(asset, mu, sigma)
            asset_sims.append(sim)
        # Suma las simulaciones de todos los activos
        return np.sum(asset_sims, axis=0)
