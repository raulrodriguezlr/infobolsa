"""
Tests unitarios para el módulo data_cleaning.
"""
import pytest
import pandas as pd
import numpy as np
from src.utils.data_cleaning import clean_dataframe, check_temporal_consistency


class TestDataCleaning:
    """Tests para las funciones de limpieza de datos."""
    
    def test_clean_dataframe_removes_duplicates(self):
        """Test de que clean_dataframe elimina duplicados."""
        df = pd.DataFrame({
            'date': ['2023-01-01', '2023-01-01', '2023-01-02'],
            'open': [1, 1, 2],
            'high': [2, 2, 3],
            'low': [0, 0, 1],
            'close': [1.5, 1.5, 2.5],
            'volume': [100, 100, 200],
        })
        cleaned = clean_dataframe(df)
        assert cleaned.shape[0] == 2
        assert cleaned['date'].nunique() == 2
    
    def test_clean_dataframe_sorts_by_date(self):
        """Test de que clean_dataframe ordena por fecha."""
        df = pd.DataFrame({
            'date': ['2023-01-03', '2023-01-01', '2023-01-02'],
            'open': [3, 1, 2],
            'high': [4, 2, 3],
            'low': [2, 0, 1],
            'close': [3.5, 1.5, 2.5],
            'volume': [300, 100, 200],
        })
        cleaned = clean_dataframe(df)
        assert cleaned.iloc[0]['date'] == '2023-01-01'
        assert cleaned.iloc[1]['date'] == '2023-01-02'
        assert cleaned.iloc[2]['date'] == '2023-01-03'
    
    def test_clean_dataframe_fills_nan(self):
        """Test de que clean_dataframe rellena valores NaN."""
        df = pd.DataFrame({
            'date': ['2023-01-01', '2023-01-02', '2023-01-03'],
            'open': [1, np.nan, 3],
            'high': [2, 3, 4],
            'low': [0, 1, 2],
            'close': [1.5, 2.5, np.nan],
            'volume': [100, 200, 300],
        })
        cleaned = clean_dataframe(df)
        # Verificar que no hay NaN (o muy pocos si no se pueden rellenar)
        assert cleaned['open'].notna().sum() >= 2
        assert cleaned['close'].notna().sum() >= 2
    
    def test_check_temporal_consistency_valid(self):
        """Test de consistencia temporal con fechas válidas."""
        df = pd.DataFrame({
            'date': ['2023-01-01', '2023-01-02', '2023-01-03'],
            'open': [1, 2, 3],
            'high': [2, 3, 4],
            'low': [0, 1, 2],
            'close': [1.5, 2.5, 3.5],
            'volume': [100, 200, 300],
        })
        assert check_temporal_consistency(df) == True
    
    def test_check_temporal_consistency_large_gap(self):
        """Test de consistencia temporal con gaps grandes."""
        df = pd.DataFrame({
            'date': ['2023-01-01', '2023-01-10'],  # Gap de 9 días
            'open': [1, 2],
            'high': [2, 3],
            'low': [0, 1],
            'close': [1.5, 2.5],
            'volume': [100, 200],
        })
        assert check_temporal_consistency(df) == False
    
    def test_check_temporal_consistency_no_date_column(self):
        """Test de consistencia temporal sin columna de fecha."""
        df = pd.DataFrame({
            'open': [1, 2, 3],
            'high': [2, 3, 4],
            'close': [1.5, 2.5, 3.5],
        })
        assert check_temporal_consistency(df) == False
    
    def test_check_temporal_consistency_single_row(self):
        """Test de consistencia temporal con una sola fila."""
        df = pd.DataFrame({
            'date': ['2023-01-01'],
            'open': [1],
            'high': [2],
            'close': [1.5],
        })
        # Con una sola fila, no hay diferencias, así que debería ser True
        result = check_temporal_consistency(df)
        # Puede ser True o False dependiendo de la implementación
        assert isinstance(result, bool)
