# 📊 Resumen: Dónde se Instancian las DataClasses

Este documento explica **exactamente dónde y cómo** se crean y dan valores a tus dataclasses en tu proyecto Infobolsa.

---

## 🎯 DataClasses Definidas

Tienes **3 dataclasses principales**:

1. **`PricePoint`** - Un punto individual de datos de precios (un día de trading)
2. **`PriceSeries`** - Una serie de puntos de precios para un activo (ej: AAPL)
3. **`Portfolio`** - Una cartera con múltiples activos

---

## 📍 Ubicaciones Donde se Instancian

### 1. **PricePoint** ✅ Instanciado

Se crea en **2 lugares**:

#### 🔸 A) En `src/main.py` (líneas 74-81)
```python
price_points = []
for _, row in hist.iterrows():
    price_points.append(PricePoint(
        date=row['date'],
        open=row['open'],
        high=row['high'],
        low=row['low'],
        close=row['close'],
        volume=row['volume']
    ))
```

**Contexto**: Se usa al convertir un DataFrame de precios históricos en objetos PricePoint.

#### 🔸 B) En `src/extractor/extractor.py` (líneas 38-45)
```python
for idx, row in hist.iterrows():
    data.append(PricePoint(
        date=idx.date() if hasattr(idx, 'date') else idx,
        open=row['Open'],
        high=row['High'],
        low=row['Low'],
        close=row['Close'],
        volume=row['Volume']
    ))
```

**Contexto**: Similar al anterior, pero usando nombres de columnas con mayúsculas (formato de yfinance).

---

### 2. **PriceSeries** ✅ Instanciado

Se crea en **2 lugares**:

#### 🔸 A) En `src/main.py` (línea 82)
```python
ps = PriceSeries(symbol=symbol, currency="USD", data=price_points)
```

**Contexto**: Después de crear la lista de `price_points` con PricePoints.

#### 🔸 B) En `src/extractor/extractor.py` (línea 47)
```python
result.append(PriceSeries(symbol=symbol, currency=currency, data=data))
```

**Contexto**: Dentro del método `_get_yfinance` que retorna una lista de PriceSeries.

---

### 3. **Portfolio** ✅ **Instanciado**

**✨ AHORA ESTÁ IMPLEMENTADO**: Portfolio ahora se instancia en `main.py` (líneas 106-109).

**Donde se usa:**
Según el README, el flujo es:
```
Extractor → PriceSeries → Portfolio → Simulación → Reporte
```

Y ahora está completamente implementado en `main.py`.

---

## 🔍 Resumen Visual

```
┌─────────────────────────────────────────────────────────┐
│  src/main.py (líneas 69-82)                            │
│                                                          │
│  1. Extrae datos → DataFrame (hist)                     │
│  2. Convierte cada fila → PricePoint                    │
│  3. Agrupa PricePoints → PriceSeries (ps)              │
│  4. Usa PriceSeries para simulación Monte Carlo         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  src/extractor/extractor.py (líneas 31-48)             │
│                                                          │
│  1. Usa yfinance para obtener datos                     │
│  2. Convierte cada fila → PricePoint                    │
│  3. Agrupa PricePoints → PriceSeries                    │
│  4. Retorna lista de PriceSeries                        │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  src/main.py (líneas 103-139)                           │
│                                                          │
│  1. Reúne todas las PriceSeries → all_price_series      │
│  2. Crea Portfolio(name="Portfolio de Infobolsa",       │
│                    assets=all_price_series)              │
│  3. Genera reporte → portfolio.report()                 │
│  4. Simulación Monte Carlo de cartera completa          │
│  5. Guarda reporte en portfolio_report.md               │
└─────────────────────────────────────────────────────────┘
```

---

## 💡 Cómo Usar Portfolio

Ya está implementado en `main.py`. Aquí está el código:

```python
# Reúne todas las PriceSeries de cada símbolo
all_price_series = []

for symbol in SYMBOLS:
    # ... descarga datos ...
    ps = PriceSeries(symbol=symbol, currency="USD", data=price_points)
    all_price_series.append(ps)  # Guardar para el Portfolio

# Crea el Portfolio con todos los activos
portfolio = Portfolio(
    name="Portfolio de Infobolsa",
    assets=all_price_series
)

# Genera y muestra reporte
portfolio.report(show=True)

# Guarda reporte en archivo
report_text = portfolio.report(show=False)
with open("portfolio_report.md", "w") as f:
    f.write(report_text)

# Simulación Monte Carlo de la cartera completa
portfolio_sims = portfolio.monte_carlo_simulation(n_simulations=200, n_days=252)
```

---

## 🎓 Archivo de Ejemplos

He creado **`examples/example_portfolio.py`** con ejemplos completos de:
- ✅ Cómo crear un PricePoint individual
- ✅ Cómo crear una PriceSeries con múltiples puntos
- ✅ Cómo crear un Portfolio con múltiples activos
- ✅ Cómo convertir desde DataFrame (como en main.py)

**Para ejecutar los ejemplos:**
```bash
python examples/example_portfolio.py
```

---

## 📝 Conclusión

**Actualmente:**
- ✅ `PricePoint` se instancia en 2 lugares (main.py y extractor.py)
- ✅ `PriceSeries` se instancia en 2 lugares (main.py y extractor.py)  
- ✅ `Portfolio` se instancia en 1 lugar (main.py)

**Tu código ahora implementa el flujo completo:**
1. Descarga datos de cada símbolo
2. Convierte a PricePoint y PriceSeries
3. **Agrupa todas las PriceSeries en un Portfolio**
4. Genera reporte de la cartera completa
5. Ejecuta simulación Monte Carlo de la cartera
6. Guarda visualizaciones y reportes

¡El flujo está completo y funcional! 🎉

