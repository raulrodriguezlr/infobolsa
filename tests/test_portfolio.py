"""
Tests unitarios para el módulo Portfolio.
"""
import pytest
from datetime import date
from src.models.portfolio import Portfolio
from src.models.price_series import PriceSeries, PricePoint


@pytest.fixture
def sample_portfolio():
    """Fixture con un portfolio de ejemplo."""
    asset1_data = [
        PricePoint(date(2023, 1, 1), 100.0, 105.0, 99.0, 103.0, 1000000.0),
        PricePoint(date(2023, 1, 2), 103.0, 108.0, 102.0, 106.0, 1100000.0),
        PricePoint(date(2023, 1, 3), 106.0, 110.0, 105.0, 109.0, 1200000.0),
    ]
    asset2_data = [
        PricePoint(date(2023, 1, 1), 200.0, 205.0, 199.0, 203.0, 2000000.0),
        PricePoint(date(2023, 1, 2), 203.0, 208.0, 202.0, 206.0, 2100000.0),
        PricePoint(date(2023, 1, 3), 206.0, 210.0, 205.0, 209.0, 2200000.0),
    ]
    asset1 = PriceSeries(symbol="AAPL", currency="USD", data=asset1_data)
    asset2 = PriceSeries(symbol="MSFT", currency="USD", data=asset2_data)
    return Portfolio(name="Test Portfolio", assets=[asset1, asset2])


@pytest.fixture
def empty_portfolio():
    """Fixture con un portfolio vacío."""
    return Portfolio(name="Empty Portfolio", assets=[])


class TestPortfolio:
    """Tests para la clase Portfolio."""
    
    def test_portfolio_creation(self, sample_portfolio):
        """Test de creación de un Portfolio."""
        assert sample_portfolio.name == "Test Portfolio"
        assert len(sample_portfolio.assets) == 2
    
    def test_mean(self, sample_portfolio):
        """Test del cálculo de la media del portfolio."""
        mean = sample_portfolio.mean()
        # Media de todos los cierres: (103+106+109+203+206+209)/6 = 156.0
        expected = (103.0 + 106.0 + 109.0 + 203.0 + 206.0 + 209.0) / 6
        assert abs(mean - expected) < 0.01
    
    def test_mean_empty(self, empty_portfolio):
        """Test de la media con portfolio vacío."""
        mean = empty_portfolio.mean()
        import math
        assert math.isnan(mean)
    
    def test_volatility(self, sample_portfolio):
        """Test del cálculo de la volatilidad del portfolio."""
        vol = sample_portfolio.volatility()
        assert vol > 0
        import math
        assert not math.isnan(vol)
    
    def test_volatility_empty(self, empty_portfolio):
        """Test de la volatilidad con portfolio vacío."""
        vol = empty_portfolio.volatility()
        import math
        assert math.isnan(vol)
    
    def test_total_value_by_date(self, sample_portfolio):
        """Test del cálculo del valor total por fecha."""
        date_values = sample_portfolio.total_value_by_date()
        assert date(2023, 1, 1) in date_values
        assert date(2023, 1, 2) in date_values
        assert date(2023, 1, 3) in date_values
        # Para la fecha 2023-01-01: 103.0 + 203.0 = 306.0
        assert abs(date_values[date(2023, 1, 1)] - 306.0) < 0.01
    
    def test_clean(self, sample_portfolio):
        """Test del método clean()."""
        # Añadir un punto con NaN
        nan_point = PricePoint(date(2023, 1, 4), 100.0, 105.0, 99.0, float('nan'), 1000000.0)
        sample_portfolio.assets[0].data.append(nan_point)
        initial_len = len(sample_portfolio.assets[0].data)
        sample_portfolio.clean()
        # Debería eliminar el punto con NaN
        assert len(sample_portfolio.assets[0].data) < initial_len
    

    
    def test_report_empty(self, empty_portfolio):
        """Test de reporte con portfolio vacío."""
        report = empty_portfolio.report(show=False)
        assert "Empty Portfolio" in report
        assert "ADVERTENCIA" in report
        assert "no contiene activos" in report
    
    def test_monte_carlo_simulation(self, sample_portfolio):
        """Test básico de simulación Monte Carlo."""
        # Ejecutar simulación pequeña para no tardar mucho
        simulations = sample_portfolio.monte_carlo_simulation(n_simulations=10, n_days=5)
        assert simulations.shape == (10, 6)  # 10 simulaciones, 5 días + 1 inicial
        assert simulations.shape[0] == 10
        assert simulations.shape[1] == 6

