"""
Tests unitarios para el módulo main.
"""
import pytest
from src.main import print_separator, print_title, EXTRACTORS


class TestMain:
    """Tests para funciones del módulo main."""
    
    def test_print_separator(self, capsys):
        """Test de la función print_separator."""
        print_separator()
        captured = capsys.readouterr()
        assert "=" in captured.out
        assert len(captured.out) > 0
    
    def test_print_title(self, capsys):
        """Test de la función print_title."""
        print_title("Test Title")
        captured = capsys.readouterr()
        assert "Test Title" in captured.out
        assert "#" in captured.out
    
    def test_extractors_list(self):
        """Test de que la lista de extractores está definida."""
        assert len(EXTRACTORS) > 0
        assert all(len(item) == 2 for item in EXTRACTORS)  # (nombre, clase)
        assert all(hasattr(item[1], 'get_historical_prices') for item in EXTRACTORS)
    
    @pytest.mark.slow
    @pytest.mark.integration
    def test_main_function_exists(self):
        """
        Test de que la función main existe y es callable.
        No ejecutamos main() completo porque puede tardar mucho y requerir inputs.
        """
        from src.main import main
        assert callable(main)
