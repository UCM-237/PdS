# Códigos de barras

## Contexto

Un lector de códigos de barras de una caja de supermercado usa una cámara barata. Las fotos llegan giradas, con iluminación irregular, con ruido y a veces movidas o desenfocadas. Tu trabajo es leer el código EAN-13 de cada foto tratando la imagen como una señal: una fila que cruza el código es una señal 1D muestreada, y la imagen completa es una señal 2D.

Tienes seis fotos. Las tres primeras traen el código correcto para que ajustes tu método; las otras tres son las de prueba, y el profesor comprobará lo que lees en ellas.

## Objetivos de aprendizaje

1. Entender una fila de la imagen como una señal muestreada: periodo de muestreo, ancho de banda del código y aliasing (T2, T3).
2. Diseñar filtros 2D separables y elegir la dirección del filtrado según la estructura de la señal (T4).
3. Usar la estadística del ruido para decidir cuánto promediar y cómo fijar el umbral de binarización (T5).
4. Usar la DFT 2D para medir la orientación y la deconvolución de Wiener para deshacer un desenfoque (T5, T6).

## Teoría mínima

**EAN-13.** Un código tiene 95 módulos de igual anchura: guarda inicial `101`, seis dígitos de 7 módulos, guarda central `01010`, otros seis dígitos y guarda final `101`. Cada dígito son 2 barras y 2 espacios cuyas anchuras suman 7 módulos. Los seis dígitos de la izquierda usan los juegos L o G, y la combinación de L y G codifica el primer dígito; los de la derecha usan el juego R. El último dígito es de control: la suma de los 12 primeros, pesados alternativamente por 1 y 3, más el control, es múltiplo de 10. Las tablas están en el código de partida.

**La fila como señal.** Si un módulo ocupa m píxeles, la secuencia de barras es una señal binaria de "periodo de símbolo" m. Su espectro tiene una envolvente sinc²(f·m), con el primer cero en f = 1/m ciclos/píxel. Cada píxel integra la luz de su área, que es un paso bajo adicional (otro sinc). Si m es pequeño, los armónicos superan 0,5 ciclos/píxel y se pliegan (aliasing).

**Filtros 2D separables.** Un filtro h[n₁, n₂] = h₁[n₁]·h₂[n₂] se aplica como dos filtros 1D y su respuesta en frecuencia es H₁(ω₁)·H₂(ω₂). Las barras son constantes en vertical: se puede filtrar mucho en esa dirección sin dañar los bordes.

**Orientación con la DFT 2D.** Un patrón de rayas paralelas tiene su energía espectral concentrada en una recta que pasa por el origen, perpendicular a las rayas. El ángulo de esa recta es el del eje del código.

**Deconvolución de Wiener.** Si la imagen se ha desenfocado con un núcleo h (por ejemplo, una caja de L píxeles por movimiento), el filtro X = H*·Y / (|H|² + 1/SNR) deshace el desenfoque sin amplificar el ruido donde |H| es casi cero. Los ceros de H aparecen en el espectro de la imagen desenfocada, en f = k/L.

## Datos

En `01_Datos/`:

| Fichero | Contenido |
|---|---|
| `codigo_1.png` … `codigo_6.png` | Fotos de 640×480 en escala de grises con un código EAN-13 cada una |
| `codigos_desarrollo.csv` | Código correcto de las imágenes 1, 2 y 3 |

## Desarrollo

| Hito | Qué haces | Temas | Entrega |
|---|---|---|---|
| H1 · La fila como señal | Perfil de una fila, módulo, espectro y muestreo | T1–T3 | Semana 6 |
| H2 · Iluminación y filtrado 2D | Corregir la iluminación, filtros separables y su respuesta 2D | T4 | Semana 9 |
| H3 · Ruido, umbral y lectura | Estadística del ruido, promediado de filas, umbral, decodificación | T5 | Semana 13 |
| H4 · Orientación, desenfoque y memoria | DFT 2D, deconvolución, lectura de las seis imágenes | T6 | Semana 16 |

Tareas y preguntas en [`03_Hitos/Hitos.md`](../03_Hitos/Hitos.md).

## Código de partida

`02_Codigo/python/` y `02_Codigo/matlab/` contienen lo mismo: lectura de imágenes, tablas EAN-13 con el dígito de control, giro de imágenes y un esqueleto por hito con `TODO`. El código de Matlab no necesita la Image Processing Toolbox.

## Entregables

- Un informe por hito y su código.
- La memoria final, el código completo y `lecturas.csv` con una fila por imagen: `imagen,codigo` (vacío si no se lee).

## Evaluación

Rúbrica común en `00_Comun/Rubrica/Rubrica.md`. Lo específico de este proyecto:

- **C1 Comprensión:** mides el módulo en píxeles de cada imagen y relacionas el espectro de la fila con él.
- **C2 Fundamento:** la dirección y el tamaño de los filtros, el número de filas promediadas y el umbral salen de medidas.
- **C3 Implementación:** la cadena es la misma para las seis imágenes, sin parámetros ajustados a mano para cada una.
- **C4 Validación:** tasa de lectura frente al nivel de ruido; lecturas de las imágenes de prueba.
- **C5 Comunicación:** figuras de cada etapa sobre la misma imagen.

Como referencia, la solución del profesor lee las seis imágenes.

## Referencias

- GS1, *GS1 General Specifications*, sección 5.2 (EAN/UPC).
- R. C. Gonzalez, R. E. Woods, *Digital Image Processing*, 4.ª ed., Pearson, 2018 (caps. 4 y 5: filtrado en frecuencia y restauración).
