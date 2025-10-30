import pandas as pd
from src.utils.data_cleaning import clean_dataframe, check_temporal_consistency

def test_clean_dataframe():
    df = pd.DataFrame({
        'date': ['2023-01-01', '2023-01-01', '2023-01-02'],
        'open': [1, 1, 2],
        'high': [2, 2, 3],
        'low': [0, 0, 1],
        'close': [1.5, 1.5, 2.5],
        'volume': [100, 100, 200],
        'ticker': ['AAPL', 'AAPL', 'AAPL']
    })
    cleaned = clean_dataframe(df)
    assert cleaned.shape[0] == 2
    assert cleaned.isnull().sum().sum() == 0

def test_check_temporal_consistency():
    df = pd.DataFrame({
        'date': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'open': [1, 2, 3],
        'high': [2, 3, 4],
        'low': [0, 1, 2],
        'close': [1.5, 2.5, 3.5],
        'volume': [100, 200, 300],
        'ticker': ['AAPL', 'AAPL', 'AAPL']
    })
    assert check_temporal_consistency(df)
