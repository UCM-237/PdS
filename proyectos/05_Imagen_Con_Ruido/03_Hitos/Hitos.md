# Hitos: Imagen con ruido

Cada informe responde a las preguntas numeradas. Las figuras que se piden son el mínimo. En las imágenes de desarrollo da siempre la PSNR y la SSIM frente a la limpia.

## Hito 1 · La imagen como señal (T1–T3, semana 6)

**Tareas**

1. Carga las seis imágenes y represéntalas con la misma escala de grises (0 negro, 1 blanco).
2. Cuantifica la imagen 1 limpia con b = 1 … 7 bits y representa la PSNR frente a b. Compárala con el modelo de ruido de cuantificación uniforme (error de varianza Δ²/12).
3. Diezma por 4 la placa zonal (`placa_zonal` en el código de partida) y la imagen 2 limpia, sin filtrar y con un paso bajo previo.
4. Calcula el periodograma medio de las filas (ventana de Hann, promedio sobre todas las filas) de las imágenes 1, 2 y 3 y de sus limpias. Haz lo mismo con las columnas de la imagen 3.

**Preguntas**

1. ¿Cuántos dB gana la PSNR por cada bit? ¿Por qué el modelo falla con 1 o 2 bits?
2. ¿Qué frecuencia de corte necesita el paso bajo antes de diezmar por 4? ¿Qué aparece en la placa zonal sin él y por qué tiene esa forma?
3. ¿A qué nivel queda el espectro del ruido de la imagen 1 y cómo se relaciona con σ²? ¿Por qué el ruido de la imagen 2 también da un espectro casi plano?
4. ¿Qué picos ves en las filas y en las columnas de la imagen 3? ¿Puedes saber con estos espectros 1D cuántas interferencias hay y en qué dirección van?

**Figuras mínimas:** las seis imágenes; PSNR frente a bits; aliasing; periodogramas.

## Hito 2 · Filtrado 1D aplicado a imágenes (T4, semana 9)

**Tareas**

1. En la imagen 1, compara filtros de media (3×3, 5×5, 7×7), gaussianos (σ = 0,8; 1; 1,5 px) y un FIR por enventanado de 15 coeficientes aplicados por filas y columnas. Para el FIR, barre la frecuencia de corte.
2. Representa la respuesta en frecuencia 2D de los tres núcleos separables.
3. En la imagen 2, compara la media y la mediana de 3×3 y 5×5.
4. En la imagen 3, diseña una muesca IIR de 2.º orden en la frecuencia del pico más fuerte de las filas y aplícala fila a fila con fase cero.

**Preguntas**

1. ¿Qué frecuencia de corte da la mejor PSNR en la imagen 1? Relaciónala con el espectro de la imagen limpia y el nivel del ruido del H1.
2. ¿Por qué la PSNR y la SSIM no eligen el mismo filtro?
3. ¿Por qué la mediana funciona mucho mejor que la media con sal y pimienta? ¿Tiene respuesta en frecuencia?
4. ¿Qué parte de la interferencia de la imagen 3 quita la muesca por filas y qué parte no? ¿Por qué hace falta fase cero?

**Figuras mínimas:** PSNR frente a fc; respuestas 2D; recortes de la imagen 2 filtrada; espectro de las filas de la imagen 3 antes y después de la muesca.

## Hito 3 · Estadística del ruido (T5, semana 13)

**Tareas**

1. En las imágenes 1 y 2, calcula el residuo y − x. Representa su histograma y compáralo con una gaussiana de la misma σ. Calcula la autocorrelación 2D del residuo de la imagen 1.
2. Programa un estimador de σ sin la imagen limpia (por ejemplo, el de la teoría mínima). Mide su sesgo y su dispersión por Monte Carlo: añade ruido de varias σ a la imagen 1 limpia, 20 realizaciones por σ.
3. Diagnostica las seis imágenes con medidas: fracción de píxeles impulsivos, picos aislados en el espectro, σ estimada y pendiente de la varianza local frente a la media local en zonas planas.
4. Programa el filtro de Wiener local y una mediana que solo sustituya los píxeles impulsivos. Aplícalos a las imágenes 1 y 2 y compáralos con lo mejor del H2.
5. Usa la pendiente de la tarea 3 para estimar P en la imagen que tenga ruido de Poisson, y filtra con la transformada de Anscombe.

**Preguntas**

1. ¿Es blanco el ruido de la imagen 1? ¿Qué deberías ver en la autocorrelación y en el espectro si no lo fuera?
2. ¿Cuándo sobrestima σ tu estimador y cuándo la subestima? ¿Por qué?
3. ¿Qué medida separa cada tipo de ruido de los demás? ¿En qué orden hay que hacerlas para que una degradación no confunda la medida de otra?
4. ¿Por qué el Wiener local conserva mejor los bordes que un gaussiano con la misma reducción de ruido en zonas planas?

**Figuras mínimas:** histogramas y autocorrelación; σ estimada frente a σ real; varianza frente a media en dos imágenes; recortes comparando filtros.

## Hito 4 · DFT 2D, desenfoque y memoria final (T6, semana 16)

**Tareas**

1. Calcula la DFT 2D de la imagen 3 con y sin ventana. Detecta los picos de la interferencia de forma automática y elimínalos con muescas 2D. Compara con la muesca por filas del H2.
2. Mira el error de la restauración de la tarea 1 cerca de los bordes de la imagen. Explica de dónde sale y propón una mejora (por ejemplo, estimar la amplitud y la fase de cada interferencia y restarla).
3. En la imagen desenfocada, estima el radio del disco a partir de los anillos del espectro (perfil radial de log|Y|²). Aplica la deconvolución de Wiener con varios K y con un modelo de S_x(f).
4. Monta la cadena completa y aplícala a las seis imágenes. Entrega `restaurada_1.png` … `restaurada_6.png`.

**Preguntas**

1. ¿Por qué hace falta la ventana para encontrar los picos? ¿Qué es la cruz que aparece sin ella?
2. ¿Qué pasa en la deconvolución si K es demasiado pequeño? ¿Y demasiado grande? ¿Por qué un K que dependa de la frecuencia es mejor?
3. ¿En qué orden aplicas las etapas en una imagen con varias degradaciones y por qué?
4. ¿Qué imagen es la más difícil de restaurar y qué limita el resultado?

**Entrega:** memoria final, código completo y las seis imágenes restauradas.

## Criterios específicos por hito

| Hito | Imprescindible para aprobar | Para Excelente |
|---|---|---|
| H1 | Curva PSNR–bits y periodogramas de filas | Explica el aliasing de la placa zonal y la relación entre el nivel del espectro del ruido y σ² |
| H2 | Comparación de filtros con PSNR y SSIM | Elige fc a partir del espectro y explica qué deja la muesca por filas |
| H3 | Histograma, σ estimada y Wiener local | Monte Carlo del estimador, diagnóstico de las seis imágenes con medidas y Anscombe |
| H4 | Muescas 2D, deconvolución y seis imágenes restauradas | Detección automática de picos, radio estimado del espectro y cadena guiada por el diagnóstico |
