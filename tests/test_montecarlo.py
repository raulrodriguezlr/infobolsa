"""
Tests unitarios para el módulo MonteCarloSimulator.
"""
import pytest
import numpy as np
from datetime import date
from src.simulation.montecarlo import MonteCarloSimulator
from src.models.price_series import PriceSeries, PricePoint


@pytest.fixture
def sample_price_series():
    """Fixture con una serie de precios de ejemplo."""
    data = [
        PricePoint(date(2023, 1, 1), 100.0, 105.0, 99.0, 103.0, 1000000.0),
        PricePoint(date(2023, 1, 2), 103.0, 108.0, 102.0, 106.0, 1100000.0),
        PricePoint(date(2023, 1, 3), 106.0, 110.0, 105.0, 109.0, 1200000.0),
        PricePoint(date(2023, 1, 4), 109.0, 112.0, 108.0, 111.0, 1300000.0),
        PricePoint(date(2023, 1, 5), 111.0, 115.0, 110.0, 114.0, 1400000.0),
    ]
    return PriceSeries(symbol="AAPL", currency="USD", data=data)


@pytest.fixture
def empty_price_series():
    """Fixture con una serie vacía."""
    return PriceSeries(symbol="TEST", currency="USD", data=[])


class TestMonteCarloSimulator:
    """Tests para la clase MonteCarloSimulator."""
    
    def test_simulator_creation(self):
        """Test de creación del simulador."""
        sim = MonteCarloSimulator(n_simulations=100, n_days=252)
        assert sim.n_simulations == 100
        assert sim.n_days == 252
    
    def test_simulate_price_series(self, sample_price_series):
        """Test de simulación de una serie de precios."""
        sim = MonteCarloSimulator(n_simulations=10, n_days=5)
        simulations = sim.simulate_price_series(sample_price_series)
        
        assert simulations.shape == (10, 6)  # 10 simulaciones, 5 días + 1 inicial
        # El primer valor debería ser el último precio de cierre de la serie
        assert abs(simulations[0, 0] - 114.0) < 0.01
        # Todos los valores deben ser positivos
        assert np.all(simulations > 0)
    
    def test_simulate_price_series_with_mu_sigma(self, sample_price_series):
        """Test de simulación con mu y sigma personalizados."""
        sim = MonteCarloSimulator(n_simulations=10, n_days=5)
        mu = 0.001
        sigma = 0.02
        simulations = sim.simulate_price_series(sample_price_series, mu=mu, sigma=sigma)
        
        assert simulations.shape == (10, 6)
        assert np.all(simulations > 0)
    
    def test_simulate_price_series_empty(self, empty_price_series):
        """Test de simulación con serie vacía (debe lanzar error)."""
        sim = MonteCarloSimulator(n_simulations=10, n_days=5)
        with pytest.raises(ValueError, match="No hay suficientes datos"):
            sim.simulate_price_series(empty_price_series)
    
    def test_simulate_price_series_single_point(self):
        """Test de simulación con un solo punto (debe lanzar error)."""
        data = [PricePoint(date(2023, 1, 1), 100.0, 105.0, 99.0, 103.0, 1000000.0)]
        ps = PriceSeries(symbol="TEST", currency="USD", data=data)
        sim = MonteCarloSimulator(n_simulations=10, n_days=5)
        with pytest.raises(ValueError, match="No hay suficientes datos"):
            sim.simulate_price_series(ps)
    
    def test_simulate_portfolio(self, sample_price_series):
        """Test de simulación de un portfolio."""
        from src.models.portfolio import Portfolio
        
        asset2_data = [
            PricePoint(date(2023, 1, 1), 200.0, 205.0, 199.0, 203.0, 2000000.0),
            PricePoint(date(2023, 1, 2), 203.0, 208.0, 202.0, 206.0, 2100000.0),
            PricePoint(date(2023, 1, 3), 206.0, 210.0, 205.0, 209.0, 2200000.0),
        ]
        asset2 = PriceSeries(symbol="MSFT", currency="USD", data=asset2_data)
        portfolio = Portfolio(name="Test Portfolio", assets=[sample_price_series, asset2])
        
        sim = MonteCarloSimulator(n_simulations=10, n_days=5)
        simulations = sim.simulate_portfolio(portfolio)
        
        assert simulations.shape == (10, 6)
        # El valor del portfolio debería ser la suma de los activos
        assert np.all(simulations > 0)
        # El valor inicial debería ser aproximadamente la suma de los últimos precios
        expected_initial = 114.0 + 209.0  # Últimos precios de cierre
        assert abs(simulations[0, 0] - expected_initial) < 1.0  # Pequeña tolerancia
    
    def test_simulate_portfolio_with_mu_sigma_dict(self, sample_price_series):
        """Test de simulación de portfolio con mu y sigma personalizados."""
        from src.models.portfolio import Portfolio
        
        asset2_data = [
            PricePoint(date(2023, 1, 1), 200.0, 205.0, 199.0, 203.0, 2000000.0),
            PricePoint(date(2023, 1, 2), 203.0, 208.0, 202.0, 206.0, 2100000.0),
        ]
        asset2 = PriceSeries(symbol="MSFT", currency="USD", data=asset2_data)
        portfolio = Portfolio(name="Test Portfolio", assets=[sample_price_series, asset2])
        
        sim = MonteCarloSimulator(n_simulations=10, n_days=5)
        mu_sigma_dict = {
            "AAPL": (0.001, 0.02),
            "MSFT": (0.0015, 0.025)
        }
        simulations = sim.simulate_portfolio(portfolio, mu_sigma_dict=mu_sigma_dict)
        
        assert simulations.shape == (10, 6)
        assert np.all(simulations > 0)

