# Códigos de barras

Lectura de códigos EAN-13 en seis fotos con giro, iluminación irregular, ruido, desenfoque y muestreo insuficiente. Una fila de la imagen es una señal 1D muestreada y la imagen completa una señal 2D, así que el proyecto recorre muestreo, filtrado, estadística y procesado 2D.

| Parte | Herramienta | Tema | Hito |
|---|---|---|---|
| Módulo, espectro, aliasing | Perfil 1D, DFT, envolvente sinc² | T2, T3 | H1 |
| Iluminación y ruido | Filtros 2D separables, máximo local | T4 | H2 |
| Umbral y lectura | Promediado de filas, Otsu, decodificación EAN-13 | T5 | H3 |
| Giro y desenfoque | DFT 2D, deconvolución de Wiener | T5, T6 | H4 |

**Dificultad:** media. **Datos:** imágenes sintéticas; las tres primeras traen su código y las tres últimas son de prueba.

## Contenido

- [`00_Enunciado/Enunciado.md`](00_Enunciado/Enunciado.md): contexto, teoría mínima y evaluación.
- `01_Datos/`: imágenes y códigos de desarrollo.
- `02_Codigo/python/` y `02_Codigo/matlab/`: código de partida equivalente (Matlab sin Image Processing Toolbox).
- [`03_Hitos/Hitos.md`](03_Hitos/Hitos.md): tareas y preguntas de cada hito.
- `04_Entrega_Final/`: plantilla de la memoria.
