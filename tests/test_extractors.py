import pytest
from src.extractors.yahoo_enriched import YahooEnrichedExtractor

def test_yahoo_enriched_extractor():
    extractor = YahooEnrichedExtractor()
    data = extractor.get_historical_prices("AAPL", start="2023-01-01", end="2023-01-10")
    assert 'historical' in data
    assert not data['historical'].empty
