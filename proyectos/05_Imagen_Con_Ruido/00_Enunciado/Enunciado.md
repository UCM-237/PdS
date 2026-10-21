# Imagen con ruido

## Contexto

Un laboratorio recibe imágenes de cámaras y escáneres distintos: unas con ruido electrónico, otras con píxeles muertos, otras con una interferencia de la red eléctrica que deja franjas, alguna desenfocada y alguna tomada con muy poca luz. Antes de analizarlas hay que restaurarlas, y el método que funciona para un defecto estropea las imágenes que tienen otro. Tu trabajo es averiguar qué degradación tiene cada imagen midiendo la propia imagen y elegir y ajustar el método adecuado con argumentos de señal.

Tienes seis imágenes. Las tres primeras traen su versión limpia para que midas la calidad de lo que haces; las otras tres son las de prueba, y el profesor medirá tus restauraciones con sus originales.

## Objetivos de aprendizaje

1. Tratar una imagen como una señal 2D muestreada y cuantificada: aliasing, ruido de cuantificación y espectro de sus filas (T1–T3).
2. Diseñar filtros 1D y aplicarlos por filas y columnas; comparar filtros lineales con la mediana (T4).
3. Caracterizar el ruido con su histograma, su autocorrelación y la relación entre varianza y media, y estimar su nivel sin la imagen limpia (T5).
4. Usar la DFT 2D para localizar interferencias y deshacer un desenfoque con el filtro de Wiener (T6).

## Teoría mínima

**Métricas.** Con imágenes entre 0 y 1, PSNR = 10·log10(1 / ECM) dB. La SSIM compara media, contraste y estructura en ventanas locales y vale 1 si las imágenes son iguales; se parece más a lo que ve una persona. Las dos están en el código de partida.

**Tipos de ruido.**

| Ruido | Modelo | Cómo se reconoce |
|---|---|---|
| Gaussiano aditivo | y = x + n, n ~ N(0, σ²) blanco | Histograma del residuo gaussiano, autocorrelación nula fuera del origen, espectro plano |
| Sal y pimienta | una fracción d de píxeles pasa a 0 o a 1 | Píxeles saturados aislados que no se parecen a sus vecinos |
| Interferencia periódica | y = x + A·cos(2π(fₓ·m + f_y·n) + φ) | Pares de picos aislados y simétricos en la DFT 2D |
| Poisson (poca luz) | y = Poisson(P·x)/P, con P fotones para el blanco | La varianza local crece con la media local: var = media/P |
| Desenfoque | y = h * x + n, h un disco de radio R | Anillos oscuros en el espectro, en los ceros de 2·J₁(2πRf)/(2πRf) |

**Estimar σ sin la imagen limpia.** El núcleo N = [1 −2 1; −2 4 −2; 1 −2 1] anula los planos y las rampas de la imagen y deja pasar el ruido. Si el ruido es blanco de varianza σ², la salida tiene desviación típica 6σ. Con la mediana de |y * N| en lugar de la desviación típica, los bordes de la imagen apenas influyen.

**Filtro de Wiener local.** En cada ventana se estiman la media m y la varianza v de la imagen con ruido, y x̂ = m + max(v − σ², 0)/v · (y − m). En zonas planas (v ≈ σ²) promedia; en bordes (v ≫ σ²) deja la imagen como está.

**Transformada de Anscombe.** z = 2·√(P·y + 3/8) convierte ruido de Poisson en ruido de varianza ≈ 1 independiente de la señal. Se filtra z como si el ruido fuera gaussiano y se deshace la transformación.

**Deconvolución de Wiener.** X̂ = H*·Y / (|H|² + K). Con K = 0 es el filtro inverso, que amplifica el ruido donde |H| es pequeño. El valor óptimo de K es el cociente entre la densidad espectral del ruido y la de la imagen, σ²/S_x(f), que depende de la frecuencia.

## Datos

En `01_Datos/`:

| Fichero | Contenido |
|---|---|
| `imagen_1.png` … `imagen_6.png` | Imágenes degradadas en escala de grises (8 bits) |
| `imagen_1_limpia.png` … `imagen_3_limpia.png` | Versiones sin degradar de las tres de desarrollo |

Las imágenes 1, 2 y 3 tienen una sola degradación cada una. Las 4, 5 y 6 pueden tener cualquiera de las de la tabla, o varias.

## Desarrollo

| Hito | Qué haces | Temas | Entrega |
|---|---|---|---|
| H1 · La imagen como señal | Cuantificación, aliasing, espectro de filas y columnas | T1–T3 | Semana 6 |
| H2 · Filtrado 1D aplicado a imágenes | Paso bajo separable, mediana, muesca por filas | T4 | Semana 9 |
| H3 · Estadística del ruido | Caracterización, estimación de σ, diagnóstico, filtros adaptativos | T5 | Semana 13 |
| H4 · DFT 2D, desenfoque y memoria | Muescas 2D, deconvolución, cadena completa | T6 | Semana 16 |

Tareas y preguntas en [`03_Hitos/Hitos.md`](../03_Hitos/Hitos.md).

## Código de partida

`02_Codigo/python/` y `02_Codigo/matlab/` contienen lo mismo: lectura y escritura de imágenes, PSNR y SSIM, filtros separables con bordes reflejados, el espectro 2D centrado y un esqueleto por hito con `TODO`. El código de Matlab no necesita la Image Processing Toolbox.

## Entregables

- Un informe por hito y su código.
- La memoria final, el código completo y las seis imágenes restauradas (`restaurada_1.png` … `restaurada_6.png`, 8 bits, mismo tamaño que la original).

## Evaluación

Rúbrica común en `00_Comun/Rubrica/Rubrica.md`. Lo específico de este proyecto:

- **C1 Comprensión:** identificas la degradación de cada imagen con medidas (histograma, espectro, varianza frente a media) y no solo mirándola.
- **C2 Fundamento:** el tamaño de las ventanas, la σ, las frecuencias de las muescas, el radio y K salen de medidas de la propia imagen.
- **C3 Implementación:** la cadena se aplica igual a todas las imágenes o, si cambia, el cambio lo decide una medida y no una elección a mano.
- **C4 Validación:** PSNR y SSIM de cada método en las imágenes de desarrollo; restauraciones de las de prueba.
- **C5 Comunicación:** recortes ampliados de la misma zona antes y después; espectros con los ejes en ciclos/píxel.

Como referencia, la solución del profesor mejora la PSNR de las seis imágenes entre 2,6 y 23,6 dB.

## Referencias

- R. C. Gonzalez, R. E. Woods, *Digital Image Processing*, 4.ª ed., Pearson, 2018 (caps. 3 a 5).
- J. S. Lee, «Digital image enhancement and noise filtering by use of local statistics», *IEEE Trans. PAMI*, 2(2), 1980.
- Z. Wang, A. C. Bovik, H. R. Sheikh, E. P. Simoncelli, «Image quality assessment: from error visibility to structural similarity», *IEEE Trans. Image Processing*, 13(4), 2004.
- J. Immerkær, «Fast noise variance estimation», *Computer Vision and Image Understanding*, 64(2), 1996.
- Imágenes: scikit-image, `skimage.data` (astronaut, camera, chelsea, rocket, coffee, brick).
