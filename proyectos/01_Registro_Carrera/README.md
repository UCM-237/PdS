# Registro de carrera

Análisis de cinco sesiones reales de carrera descargadas de Strava (velocidad GPS, frecuencia cardiaca y altitud, con muestreo irregular) y de sesiones sintéticas con eventos conocidos. Hay que limpiar y remuestrear las señales, filtrarlas, modelar su ruido, detectar cambios de ritmo y clasificar el tipo de entrenamiento.

| Parte | Herramienta | Tema | Hito |
|---|---|---|---|
| Muestreo irregular, anomalías, espectro | Remuestreo, interpolación, Welch | T1–T3 | H1 |
| Suavizado y desnivel | EMA (IIR de 1.er orden), Butterworth de fase cero, mediana | T4 | H2 |
| Ruido, atípicos y cambios de ritmo | Autocorrelación, MAD, Hampel, segmentación con penalización | T5 | H3 |
| Series y clasificación | STFT, autocorrelación, reglas | T6 | H4 |

**Dificultad:** media-baja. **Datos:** cinco actividades reales y trece sintéticas (diez de desarrollo con sus eventos y tres de prueba).

## Contenido

- [`00_Enunciado/Enunciado.md`](00_Enunciado/Enunciado.md): contexto, teoría mínima y evaluación.
- `01_Datos/`: actividades reales y `sinteticas/`.
- `02_Codigo/python/` y `02_Codigo/matlab/`: código de partida equivalente.
- [`03_Hitos/Hitos.md`](03_Hitos/Hitos.md): tareas y preguntas de cada hito.
- `04_Entrega_Final/`: plantilla de la memoria.
- `entrenamiento/`: scripts para descargar actividades de Strava y una pequeña aplicación Bokeh de visualización. Las claves se leen de variables de entorno (`STRAVA_CLIENT_ID`, `STRAVA_ACCESS_TOKEN`).
