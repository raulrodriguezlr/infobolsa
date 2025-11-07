# Arquitectura Infobolsa Toolkit (Mermaid)

```mermaid
flowchart TD
    main[main.py]
    ext[extractors]
    mod[models]
    sim[simulation]
    util[utils]
    vis[visualizations]
    port[portfolio]
    rep[report]

    main --> ext
    main --> mod
    main --> sim
    main --> util
    main --> vis
    ext --> mod
    ext --> util
    mod --> sim
    mod --> vis
    sim --> vis
    mod --> port
    port --> rep
```

---

Este diagrama refleja la estructura modular y el flujo de dependencias entre los principales componentes del proyecto Infobolsa Toolkit.
- El punto de entrada es `main.py`.
- Los extractores obtienen datos y los normalizan.
- Los modelos representan series de precios y carteras.
- La simulación Monte Carlo se realiza sobre los modelos.
- Las utilidades ayudan en limpieza y preprocesado.
- Las visualizaciones muestran resultados y reportes.
- Portfolio y reportes agregan valor analítico.
