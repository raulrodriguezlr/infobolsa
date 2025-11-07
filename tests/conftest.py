"""
Configuración compartida para pytest (fixtures comunes, marcadores, etc.).
"""
import pytest


def pytest_configure(config):
    """
    Registra marcadores personalizados para pytest.
    """
    config.addinivalue_line(
        "markers", "integration: marca tests que requieren conexión a internet o recursos externos"
    )
    config.addinivalue_line(
        "markers", "slow: marca tests que pueden tardar mucho tiempo"
    )

