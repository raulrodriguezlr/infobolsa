import pytest
from src.main import main

def test_main_runs():
    """Testea que el main se ejecuta sin lanzar excepciones."""
    try:
        main()
    except Exception as e:
        pytest.fail(f"main() lanzó una excepción: {e}")
