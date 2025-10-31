# Infobolsa Toolkit

Este proyecto es un conjunto de herramientas para la obtención y análisis de información bursátil. Su objetivo es facilitar la descarga, estandarización, análisis y visualización de datos financieros de diferentes fuentes online.

## Estructura del proyecto

```
infobolsa/
├── README.md
├── requirements.txt
├── .gitignore
├── diagrams/
│   └── architecture.fossflow
├── src/
│   ├── extractor/
│   ├── models/
│   ├── utils/
│   ├── simulation/
│   ├── visualization/
│   └── main.py
└── tests/
```

- **src/**: Núcleo del programa, organizado por módulos.
- **extractor/**: Módulos para obtener datos de diferentes APIs.
- **models/**: DataClasses para series de precios y carteras.
- **utils/**: Funciones de limpieza y utilidades.
- **simulation/**: Simulaciones de Monte Carlo y otras.
- **visualization/**: Métodos para visualización y reportes gráficos.
- **diagrams/**: Diagramas de arquitectura y estructura.
- **tests/**: Pruebas unitarias.

## Instalación

1. Crea un entorno virtual (recomendado):
   ```sh
   # En Windows
   python -m venv .venv
   .venv\Scripts\activate
   # En Linux/Mac
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Instala las dependencias:
   ```sh
   pip install -r requirements.txt
   ```

## Uso

Ejecuta el programa principal:
```sh
python src/main.py
```

## Ejemplo de uso

```sh
# Configura tu .env con las API keys necesarias (ver .env.example)
python src/main.py
# Si falla por rutas en los imports, situarse en la raiz del proyecto y 
python -m src.main
```

- Los datos y gráficos se guardarán automáticamente en la carpeta `outputs/`.
- Puedes cambiar los símbolos y parámetros en el archivo `main.py`.

## Diagrama de arquitectura

Consulta el archivo `diagrams/architecture.fossflow` para ver la estructura general del proyecto.

## Buenas prácticas aplicadas
- Imports absolutos y estructura modular
- Logging profesional en vez de print
- Tipado y docstrings en funciones
- Configuración centralizada en variables.py y .env
- Tests unitarios en la carpeta `tests/`
- Visualizaciones y outputs organizados por fecha

## Notas
- El formato de salida de los extractores es estandarizado para facilitar el análisis y la interoperabilidad.
- El proyecto está diseñado para ser plug-n-play y fácilmente extensible.
- Se recomienda seguir la estructura y buenas prácticas para facilitar el crecimiento y mantenimiento del código.

## Autor
Raul R.

---

## **FLUJO**

```mermaid
flowchart TD
    Start([Inicio: main.py])
    Extractor[Descarga de datos\n(GeneralExtractor)]
    PriceSeries[Normalización\n(PriceSeries)]
    Portfolio[Cartera\n(Portfolio)]
    Simulacion[Simulación Monte Carlo\n(MonteCarloSimulator)]
    Reporte[Reporte y Análisis\n(Portfolio.report)]
    Plots[Visualización\n(plots_report, matplotlib)]
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

- **Punto de partida:** `main.py`
- **Flujo:** Descarga datos → Normaliza → Crea cartera → Simula → Reporta y visualiza
- **Salidas:**
    - Reporte en consola (markdown)
    - Gráficos interactivos (matplotlib pop-up)
    - Mensajes informativos
