"""
Tests unitarios para el módulo PriceSeries.
"""
import pytest
from datetime import date
from src.models.price_series import PriceSeries, PricePoint
import math


class TestPricePoint:
    """Tests para la clase PricePoint."""
    
    def test_price_point_creation(self):
        """Test de creación de un PricePoint."""
        pp = PricePoint(
            date=date(2023, 1, 1),
            open=100.0,
            high=105.0,
            low=99.0,
            close=103.0,
            volume=1000000.0
        )
        assert pp.date == date(2023, 1, 1)
        assert pp.open == 100.0
        assert pp.high == 105.0
        assert pp.low == 99.0
        assert pp.close == 103.0
        assert pp.volume == 1000000.0


class TestPriceSeries:
    """Tests para la clase PriceSeries."""
    
    @pytest.fixture
    def sample_price_series(self):
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
    def empty_price_series(self):
        """Fixture con una serie vacía."""
        return PriceSeries(symbol="TEST", currency="USD", data=[])
    
    def test_price_series_creation(self, sample_price_series):
        """Test de creación de una PriceSeries."""
        assert sample_price_series.symbol == "AAPL"
        assert sample_price_series.currency == "USD"
        assert len(sample_price_series.data) == 5
    
    def test_mean(self, sample_price_series):
        """Test del cálculo de la media."""
        mean = sample_price_series.mean()
        expected = (103.0 + 106.0 + 109.0 + 111.0 + 114.0) / 5
        assert abs(mean - expected) < 0.01
    
    def test_mean_empty(self, empty_price_series):
        """Test de la media con serie vacía."""
        mean = empty_price_series.mean()
        assert math.isnan(mean)
    
    def test_stdev(self, sample_price_series):
        """Test del cálculo de la desviación estándar."""
        stdev = sample_price_series.stdev()
        assert stdev > 0
        assert not math.isnan(stdev)
    
    def test_stdev_empty(self, empty_price_series):
        """Test de la desviación estándar con serie vacía."""
        stdev = empty_price_series.stdev()
        assert math.isnan(stdev)
    
    def test_stdev_single_point(self):
        """Test de la desviación estándar con un solo punto."""
        data = [PricePoint(date(2023, 1, 1), 100.0, 105.0, 99.0, 103.0, 1000000.0)]
        ps = PriceSeries(symbol="TEST", currency="USD", data=data)
        stdev = ps.stdev()
        assert math.isnan(stdev)
    
    def test_total_return(self, sample_price_series):
        """Test del cálculo del rendimiento total."""
        total_ret = sample_price_series.total_return()
        expected = (114.0 / 103.0) - 1
        assert abs(total_ret - expected) < 0.01
    
    def test_total_return_empty(self, empty_price_series):
        """Test del rendimiento total con serie vacía."""
        total_ret = empty_price_series.total_return()
        assert math.isnan(total_ret)
    
    def test_total_return_single_point(self):
        """Test del rendimiento total con un solo punto."""
        data = [PricePoint(date(2023, 1, 1), 100.0, 105.0, 99.0, 103.0, 1000000.0)]
        ps = PriceSeries(symbol="TEST", currency="USD", data=data)
        total_ret = ps.total_return()
        assert math.isnan(total_ret)
    
    def test_annualized_return(self, sample_price_series):
        """Test del cálculo del rendimiento anualizado."""
        ann_ret = sample_price_series.annualized_return()
        assert not math.isnan(ann_ret)
        assert ann_ret > 0  # En este caso debería ser positivo
    
    def test_volatility(self, sample_price_series):
        """Test del cálculo de la volatilidad anualizada."""
        vol = sample_price_series.volatility()
        assert not math.isnan(vol)
        assert vol > 0
    
    def test_max_drawdown(self, sample_price_series):
        """Test del cálculo del máximo drawdown."""
        dd = sample_price_series.max_drawdown()
        assert dd >= 0
        assert not math.isnan(dd)
    
    def test_max_drawdown_empty(self, empty_price_series):
        """Test del máximo drawdown con serie vacía."""
        dd = empty_price_series.max_drawdown()
        assert math.isnan(dd)
    
    def test_clean_removes_nan(self):
        """Test de que clean() elimina puntos con NaN."""
        data = [
            PricePoint(date(2023, 1, 1), 100.0, 105.0, 99.0, 103.0, 1000000.0),
            PricePoint(date(2023, 1, 2), 103.0, 108.0, 102.0, float('nan'), 1100000.0),
            PricePoint(date(2023, 1, 3), 106.0, 110.0, 105.0, 109.0, 1200000.0),
        ]
        ps = PriceSeries(symbol="TEST", currency="USD", data=data)
        ps.clean()
        assert len(ps.data) == 2
        assert all(not math.isnan(p.close) for p in ps.data)
    
    def test_clean_sorts_by_date(self):
        """Test de que clean() ordena por fecha."""
        data = [
            PricePoint(date(2023, 1, 3), 106.0, 110.0, 105.0, 109.0, 1200000.0),
            PricePoint(date(2023, 1, 1), 100.0, 105.0, 99.0, 103.0, 1000000.0),
            PricePoint(date(2023, 1, 2), 103.0, 108.0, 102.0, 106.0, 1100000.0),
        ]
        ps = PriceSeries(symbol="TEST", currency="USD", data=data)
        ps.clean()
        assert ps.data[0].date == date(2023, 1, 1)
        assert ps.data[1].date == date(2023, 1, 2)
        assert ps.data[2].date == date(2023, 1, 3)

