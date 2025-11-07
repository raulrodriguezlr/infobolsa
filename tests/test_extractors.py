"""
Tests unitarios para los extractores de datos.
"""
import pytest
from src.extractors.yahoo_extractor import YahooFinanceExtractor
from src.extractors.base import BaseExtractor


class TestExtractors:
    """Tests para los extractores de datos."""
    
    def test_base_extractor_is_abstract(self):
        """Test de que BaseExtractor es una clase abstracta."""
        with pytest.raises(TypeError):
            BaseExtractor()
    
    def test_yahoo_extractor_creation(self):
        """Test de creación del extractor de Yahoo Finance."""
        extractor = YahooFinanceExtractor()
        assert extractor is not None
        assert hasattr(extractor, 'get_historical_prices')
    
    @pytest.mark.integration
    def test_yahoo_extractor_get_historical_prices(self):
        """
        Test de descarga de datos históricos (requiere conexión a internet).
        Este test se marca como 'integration' para poder ejecutarlo por separado.
        """
        extractor = YahooFinanceExtractor()
        # Usar un rango de fechas pequeño para que sea rápido
        df = extractor.get_historical_prices("AAPL", start="2023-01-01", end="2023-01-10")
        
        assert df is not None
        assert not df.empty
        assert 'date' in df.columns
        assert 'open' in df.columns
        assert 'high' in df.columns
        assert 'low' in df.columns
        assert 'close' in df.columns
        assert 'volume' in df.columns
    
    @pytest.mark.integration
    def test_yahoo_extractor_get_multiple_historical_prices(self):
        """
        Test de descarga de múltiples tickers (requiere conexión a internet).
        """
        extractor = YahooFinanceExtractor()
        tickers = ["AAPL", "MSFT"]
        results = extractor.get_multiple_historical_prices(
            tickers, start="2023-01-01", end="2023-01-05"
        )
        
        assert len(results) == 2
        assert "AAPL" in results
        assert "MSFT" in results
        assert not results["AAPL"].empty
        assert not results["MSFT"].empty
