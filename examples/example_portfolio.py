"""
Ejemplo completo de cómo instanciar y usar las DataClasses:
- PricePoint
- PriceSeries  
- Portfolio

Este archivo demuestra el flujo completo de creación de objetos.

NOTA: Este archivo requiere instalar las dependencias:
    pip install -r requirements.txt
"""
import sys
from pathlib import Path
# Añadir el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from datetime import date, timedelta
from src.models.price_series import PricePoint, PriceSeries

# Portfolio requiere MonteCarloSimulator que necesita numpy
# Si numpy no está instalado, comentamos esta importación
try:
    from src.models.portfolio import Portfolio
    HAS_PORTFOLIO = True
except ImportError:
    print("⚠️  Portfolio no disponible (numpy no instalado)")
    HAS_PORTFOLIO = False


def ejemplo_pricepoint():
    """Ejemplo de cómo crear un PricePoint individual"""
    print("=" * 60)
    print("EJEMPLO 1: Crear un PricePoint")
    print("=" * 60)
    
    # Crear un PricePoint con datos específicos
    point = PricePoint(
        date=date(2024, 1, 15),
        open=150.0,
        high=155.0,
        low=149.0,
        close=152.5,
        volume=1000000.0
    )
    print(f"PricePoint creado: {point}")
    print(f"Fecha: {point.date}, Close: {point.close}, Volumen: {point.volume}")
    print()


def ejemplo_priceseries():
    """Ejemplo de cómo crear una PriceSeries con varios PricePoints"""
    print("=" * 60)
    print("EJEMPLO 2: Crear una PriceSeries")
    print("=" * 60)
    
    # Crear varios PricePoints
    points = []
    base_date = date(2024, 1, 1)
    base_price = 100.0
    
    for i in range(10):
        point = PricePoint(
            date=base_date + timedelta(days=i),
            open=base_price + i,
            high=base_price + i + 2,
            low=base_price + i - 1,
            close=base_price + i + 1,
            volume=(1000000 + i * 50000)
        )
        points.append(point)
    
    # Crear una PriceSeries
    price_series = PriceSeries(
        symbol="AAPL",
        currency="USD",
        data=points
    )
    
    print(f"PriceSeries creada: {price_series.symbol}")
    print(f"Número de puntos: {len(price_series.data)}")
    print(f"Media de precios: {price_series.mean():.2f}")
    print(f"Volatilidad: {price_series.stdev():.2f}")
    print()


def ejemplo_portfolio():
    """Ejemplo completo de cómo crear un Portfolio con múltiples activos"""
    print("=" * 60)
    print("EJEMPLO 3: Crear un Portfolio con múltiples activos")
    print("=" * 60)
    
    if not HAS_PORTFOLIO:
        print("⚠️  Portfolio no disponible. Sigue el ejemplo conceptual:")
        print()
        print("# Crear varios activos (PriceSeries)")
        print("activos = [ps1, ps2, ps3]  # Lista de PriceSeries")
        print()
        print("# Crear el Portfolio")
        print("portfolio = Portfolio(")
        print("    name='Mi Cartera de Tecnología',")
        print("    assets=activos")
        print(")")
        print()
        print("# Generar reporte")
        print("portfolio.report()")
        print()
        return
    
    # Crear varios activos (PriceSeries)
    activos = []
    
    # Activo 1: AAPL
    aapl_points = []
    for i in range(20):
        aapl_points.append(PricePoint(
            date=date(2024, 1, 1) + timedelta(days=i),
            open=180.0 + i * 0.5,
            high=182.0 + i * 0.5,
            low=179.0 + i * 0.5,
            close=181.0 + i * 0.5,
            volume=5000000 + i * 100000
        ))
    aapl = PriceSeries(symbol="AAPL", currency="USD", data=aapl_points)
    activos.append(aapl)
    
    # Activo 2: MSFT
    msft_points = []
    for i in range(20):
        msft_points.append(PricePoint(
            date=date(2024, 1, 1) + timedelta(days=i),
            open=400.0 + i * 1.0,
            high=405.0 + i * 1.0,
            low=398.0 + i * 1.0,
            close=403.0 + i * 1.0,
            volume=3000000 + i * 80000
        ))
    msft = PriceSeries(symbol="MSFT", currency="USD", data=msft_points)
    activos.append(msft)
    
    # Activo 3: GOOGL
    googl_points = []
    for i in range(20):
        googl_points.append(PricePoint(
            date=date(2024, 1, 1) + timedelta(days=i),
            open=150.0 + i * 0.8,
            high=152.0 + i * 0.8,
            low=149.0 + i * 0.8,
            close=151.0 + i * 0.8,
            volume=2000000 + i * 50000
        ))
    googl = PriceSeries(symbol="GOOGL", currency="USD", data=googl_points)
    activos.append(googl)
    
    # Crear el Portfolio
    portfolio = Portfolio(
        name="Mi Cartera de Tecnología",
        assets=activos
    )
    
    print(f"Portfolio creado: {portfolio.name}")
    print(f"Número de activos: {len(portfolio.assets)}")
    print(f"Activos: {[asset.symbol for asset in portfolio.assets]}")
    print()
    
    # Generar reporte
    print(portfolio.report(show=False))
    print()


def ejemplo_desde_main():
    """
    Ejemplo de cómo se crean las instancias en el main.py real
    (simulando la conversión desde DataFrame)
    """
    print("=" * 60)
    print("EJEMPLO 4: Flujo desde DataFrame (como en main.py)")
    print("=" * 60)
    
    try:
        import pandas as pd
    except ImportError:
        print("⚠️  pandas no instalado. Ejemplo conceptual:")
        print()
        print("# DataFrames tienen columnas: date, open, high, low, close, volume")
        print("for _, row in df.iterrows():")
        print("    price_points.append(PricePoint(...))")
        print()
        return
    
    # Simular un DataFrame como los que devuelven los extractores
    data = {
        'date': pd.date_range('2024-01-01', periods=5, freq='D'),
        'open': [100, 101, 102, 103, 104],
        'high': [102, 103, 104, 105, 106],
        'low': [99, 100, 101, 102, 103],
        'close': [101, 102, 103, 104, 105],
        'volume': [1000000, 1100000, 1200000, 1300000, 1400000]
    }
    df = pd.DataFrame(data)
    
    print("DataFrame original:")
    print(df)
    print()
    
    # Convertir a PriceSeries (como en main.py líneas 72-82)
    price_points = []
    for _, row in df.iterrows():
        price_points.append(PricePoint(
            date=row['date'].date() if hasattr(row['date'], 'date') else row['date'],
            open=row['open'],
            high=row['high'],
            low=row['low'],
            close=row['close'],
            volume=row['volume']
        ))
    
    ps = PriceSeries(symbol="TEST", currency="USD", data=price_points)
    
    print(f"Convertido a PriceSeries: {ps.symbol}")
    print(f"Puntos de datos: {len(ps.data)}")
    print(f"Media: {ps.mean():.2f}")
    print()


if __name__ == "__main__":
    ejemplo_pricepoint()
    ejemplo_priceseries()
    ejemplo_portfolio()
    ejemplo_desde_main()
    
    print("=" * 60)
    print("FIN DE EJEMPLOS")
    print("=" * 60)

