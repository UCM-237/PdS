# Imagen con ruido

Restauración de seis imágenes con degradaciones distintas: ruido gaussiano, sal y pimienta, interferencia periódica, una mezcla de las tres, desenfoque y ruido de poca luz (Poisson). Hay que diagnosticar qué le pasa a cada imagen midiendo la propia imagen y elegir el método con argumentos de señal: espectro, estadística del ruido y respuesta en frecuencia.

| Parte | Herramienta | Tema | Hito |
|---|---|---|---|
| Muestreo, cuantificación, espectro de las filas | DFT 1D, aliasing, ruido de cuantificación | T1–T3 | H1 |
| Filtrado lineal y no lineal | FIR por enventanado, filtros separables, muesca IIR, mediana | T4 | H2 |
| Estadística del ruido y filtros adaptativos | Histograma, autocorrelación, estimación de σ, Monte Carlo, Wiener local | T5 | H3 |
| Interferencias y desenfoque | DFT 2D, muescas 2D, deconvolución de Wiener | T6 | H4 |

**Dificultad:** media. **Datos:** fotos de dominio público o CC0 (scikit-image) degradadas de forma sintética; las tres primeras traen su versión limpia y las tres últimas son de prueba.

## Contenido

- [`00_Enunciado/Enunciado.md`](00_Enunciado/Enunciado.md): contexto, teoría mínima y evaluación.
- `01_Datos/`: imágenes con ruido y versiones limpias de las de desarrollo.
- `02_Codigo/python/` y `02_Codigo/matlab/`: código de partida equivalente (Matlab sin Image Processing Toolbox).
- [`03_Hitos/Hitos.md`](03_Hitos/Hitos.md): tareas y preguntas de cada hito.
- `04_Entrega_Final/`: plantilla de la memoria.
