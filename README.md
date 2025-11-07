# Infobolsa Toolkit

Infobolsa Toolkit es un conjunto de utilidades para descargar, enriquecer y analizar series bursátiles desde múltiples APIs públicas. El proyecto automatiza la recopilación de precios históricos, genera simulaciones de Monte Carlo y produce reportes y visualizaciones listos para presentar.

## Índice rápido

- Visión general
- Arquitectura y módulos
- Requisitos y configuración
- Ejecución (Windows y Linux/macOS)
- Flujo de trabajo y outputs
- Personalización y extensibilidad
- Buenas prácticas y estándares

## Visión general

- **Objetivo**: ofrecer un pipeline reproducible para análisis de tickers (descarga → limpieza → simulación → reportes).
- **Entradas**: lista de símbolos, fechas de análisis y credenciales de APIs (`AlphaVantage`, `Finnhub`, Yahoo Finance).
- **Salidas**: gráficos PNG agrupados, reportes Markdown y visualizaciones interactivas en pantalla.
- **Público**: analistas financieros, estudiantes o cualquier persona que necesite informes rápidos de mercados.

## Arquitectura y módulos

```
src/
├── main.py                 # Punto de entrada (modo interactivo/no interactivo)
├── variables.py            # Configuración centralizada y lectura de .env
├── extractors/             # Conectores a APIs externas
│   ├── base.py             # Lógica compartida (reintentos, normalización)
│   ├── yahoo_enriched.py   # Yahoo Finance con datos adicionales
│   ├── yahoo_extractor.py  # Yahoo Finance básico
│   ├── alpha_vantage_extractor.py
│   └── finnhub_extractor.py
├── models/                 # Representaciones de dominio (datos normalizados)
│   ├── price_series.py     # `PriceSeries` y `PricePoint`
│   └── portfolio.py        # `Portfolio` y reportes agregados
├── simulation/
│   └── montecarlo.py       # `MonteCarloSimulator`
├── utils/
│   ├── data_cleaning.py    # Normalización y utilidades varias
│   ├── output_manager.py   # Gestión de carpetas y guardado de artefactos
│   └── 10k10q.py           # Descarga opcional de filings SEC EDGAR
└── visualizations/
    └── plots.py            # Funciones auxiliares para plotting
```

Consulta también `docs/architecture.md` para un diagrama mermaid con las dependencias entre módulos.

## Requisitos y configuración

1. **Python**: 3.10 o superior.
2. **Entorno virtual** (recomendado):
   ```sh
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # Linux/macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Dependencias**:
   ```sh
   pip install -r requirements.txt
   ```
4. **Variables de entorno**:
   - Copia `.env.example` a `.env` (si existe) o crea uno nuevo.
   - Declara las API keys que vayas a utilizar:
     - `ALPHAVANTAGE_API_KEY`
     - `FINNHUB_API_KEY`
     - `YAHOO_API_KEY` (opcional para endpoints enriquecidos)
     - `CIK` (para activar la descarga de 10-K/10-Q cuando se habilite)
   - Ajusta fechas (`START_DATE`, `END_DATE`), ruta de outputs (`OUTPUTS_BASE_PATH`) y demás parámetros descritos en `src/variables.py`.

## Ejecución

### Windows

Sitúate en la raíz del proyecto y ejecuta cualquiera de los siguientes comandos:

```powershell
# Ejecución directa (puede fallar si no estás en la raíz o si faltan imports)
python src\main.py

# Ejecución como módulo: evita problemas de rutas y es la forma recomendada
python -m src.main
```

Para arrancar en modo interactivo añade `-i` o `--interactive`:

```powershell
python -m src.main --interactive
```

### Linux / macOS

```sh
python3 -m src.main            # modo no interactivo
python3 -m src.main -i         # modo interactivo
```

### Parámetros disponibles

- `-i` / `--interactive`: permite añadir tickers y modificar configuración desde la consola.
- Variables como símbolos por defecto, fechas y Monte Carlo se controlan desde `src/variables.py` o vía entorno.

## Flujo de trabajo

1. **Selección de extractor**: al iniciar, se muestran los extractores disponibles (`YahooEnriched`, `Yahoo`, `AlphaVantage`, `Finnhub`).
2. **Descarga y normalización**: cada extractor devuelve `DataFrame` con columnas estándar (`date`, `open`, `high`, `low`, `close`, `volume`).
3. **EDA básica**: se imprimen estadísticas `describe()` y distribución de `close` para cada ticker.
4. **Visualización**: se generan gráficos agrupados por lote (`PLOTS_PER_PNG`) con `matplotlib`.
5. **Simulación Monte Carlo**: opcional por ticker y para la cartera completa (`MonteCarloSimulator`).
6. **Portfolio report**: `Portfolio.report()` devuelve un resumen textual y lo guarda en Markdown.
7. **Correlaciones**: se genera la matriz de correlación y se guarda como imagen.

Los archivos generados se guardan en `outputs/<timestamp>/`, gestionado por `OutputManager`.

## Personalización y extensibilidad

- **Nuevos extractores**: hereda de `extractors.base.BaseExtractor` y registra el nuevo con `EXTRACTORS` en `main.py`.
- **Indicadores adicionales**: añade columnas calculadas en `utils.data_cleaning` o extiende `PriceSeries`.
- **Reportes**: modifica `Portfolio.report()` o agrega nuevas funciones en `visualizations/plots.py`.
- **Descarga de filings**: descomenta las llamadas de `utils.10k10q.fetch_sec_filings()` para incluir 10-K/10-Q.

## Tests unitarios

El proyecto incluye una suite de tests unitarios en la carpeta `tests/`. Los tests cubren los módulos principales:

- **test_price_series.py**: Tests para `PriceSeries` y `PricePoint` (cálculos estadísticos, rendimientos, volatilidad, etc.)
- **test_portfolio.py**: Tests para `Portfolio` (agregación, reportes, simulaciones)
- **test_montecarlo.py**: Tests para `MonteCarloSimulator` (simulaciones de precios y carteras)
- **test_data_cleaning.py**: Tests para funciones de limpieza de datos
- **test_output_manager.py**: Tests para gestión de archivos y directorios
- **test_extractors.py**: Tests para extractores de datos (algunos requieren conexión a internet)
- **test_main.py**: Tests para funciones auxiliares del módulo principal

### Ejecución de tests

#### Instalación de dependencias para tests

Asegúrate de tener `pytest` instalado:

```powershell
# Windows
pip install pytest

# Linux/macOS
pip3 install pytest
```

O instala todas las dependencias (incluyendo pytest si está en requirements.txt):

```powershell
pip install -r requirements.txt
```

#### Ejecutar todos los tests

Desde la raíz del proyecto:

```powershell
# Windows
python -m pytest tests/

# Linux/macOS
python3 -m pytest tests/
```

#### Ejecutar tests específicos

```powershell
# Ejecutar un archivo de test específico
python -m pytest tests/test_price_series.py

# Ejecutar una clase de test específica
python -m pytest tests/test_price_series.py::TestPriceSeries

# Ejecutar un test específico
python -m pytest tests/test_price_series.py::TestPriceSeries::test_mean

# Ejecutar tests con salida detallada
python -m pytest tests/ -v

# Ejecutar tests con cobertura (si está instalado pytest-cov)
python -m pytest tests/ --cov=src --cov-report=html
```

#### Ejecutar tests sin integración

Los tests que requieren conexión a internet están marcados con `@pytest.mark.integration`. Para ejecutar solo los tests unitarios (sin integración):

```powershell
python -m pytest tests/ -m "not integration"
```

#### Ejecutar tests con salida detallada y captura desactivada

Para ver los prints durante la ejecución:

```powershell
python -m pytest tests/ -v -s
```

## Buenas prácticas y estándares

- Estructura modular con imports absolutos para evitar dependencias circulares.
- Logging configurado a nivel global (`logging.basicConfig`) para trazabilidad.
- Parámetros centralizados en `variables.py` y/o `.env`.
- Simulaciones reproducibles utilizando `numpy` y parámetros compartidos (`TRADING_DAYS_PER_YEAR`).
- Gestión de outputs organizada por fecha/hora, lo que facilita auditorías y versionado.
- Suite completa de tests unitarios en `tests/` ejecutables con `pytest`.

## Créditos

Desarrollado por Raul R.

---

```mermaid
flowchart TD
    Start([Inicio: main.py])
    Extractor[Descarga de datos\n(Extractors)]
    PriceSeries[Normalización\n(PriceSeries)]
    Portfolio[Cartera\n(Portfolio)]
    Simulacion[Simulación Monte Carlo\n(MonteCarloSimulator)]
    Reporte[Reporte y Análisis\n(Portfolio.report)]
    Plots[Visualización\n(Matplotlib)]
    Salida[Salidas: Markdown, Gráficos, Consola]

    Start --> Extractor
    Extractor --> PriceSeries
    PriceSeries --> Portfolio
    Portfolio --> Simulacion
    Simulacion --> Plots
    Portfolio --> Reporte
    Reporte --> Salida
    Plots --> Salida
```
