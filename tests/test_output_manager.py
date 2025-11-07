"""
Tests unitarios para el módulo OutputManager.
"""
import pytest
import os
import pandas as pd
import matplotlib.pyplot as plt
from src.utils.output_manager import OutputManager


class TestOutputManager:
    """Tests para la clase OutputManager."""
    
    def test_output_manager_creation(self):
        """Test de creación del OutputManager."""
        om = OutputManager()
        assert om.base_dir is not None
        assert os.path.exists(om.base_dir)
    
    def test_get_path(self):
        """Test del método get_path()."""
        om = OutputManager()
        path = om.get_path("test_file.txt")
        assert "test_file.txt" in path
        assert om.base_dir in path
    
    def test_save_dataframe(self):
        """Test de guardado de DataFrame."""
        om = OutputManager()
        df = pd.DataFrame({
            'date': ['2023-01-01', '2023-01-02'],
            'close': [100.0, 105.0]
        })
        path = om.save_dataframe(df, "test_data.csv")
        
        assert os.path.exists(path)
        # Verificar que se puede leer el archivo
        df_read = pd.read_csv(path)
        assert len(df_read) == 2
        assert 'date' in df_read.columns
        assert 'close' in df_read.columns
    
    def test_save_plot(self):
        """Test de guardado de gráfico."""
        om = OutputManager()
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [1, 2, 3])
        ax.set_title("Test Plot")
        
        path = om.save_plot(plt, "test_plot.png")
        
        assert os.path.exists(path)
        plt.close(fig)  # Limpiar
    
    def test_output_directory_structure(self):
        """Test de que se crea la estructura de directorios correctamente."""
        om = OutputManager()
        # Verificar que el directorio base existe
        assert os.path.isdir(om.base_dir)
        # Verificar que contiene el formato de fecha esperado
        assert "outputs" in om.base_dir.lower()

