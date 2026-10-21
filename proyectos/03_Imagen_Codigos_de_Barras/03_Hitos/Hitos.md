# Hitos: Códigos de barras

Cada informe responde a las preguntas numeradas. Las figuras que se piden son el mínimo.

## Hito 1 · La fila como señal (T1–T3, semana 6)

**Tareas**

1. Carga las seis imágenes y represéntalas.
2. En la imagen 1 (código horizontal), extrae una fila que cruce el código y represéntala. Localiza el primer y el último borde y calcula el módulo m en píxeles.
3. Dibuja con la tabla EAN-13 la señal ideal del código de la imagen 1 y compárala con la fila muestreada.
4. Calcula el espectro de la fila y compáralo con la envolvente sinc²(f·m).
5. Repite la medida del módulo en la imagen 6 y compara las anchuras de las rachas medidas en las dos imágenes.

**Preguntas**

1. ¿Dónde está el primer cero del espectro y por qué? ¿Qué efecto tiene que cada píxel integre la luz de su área?
2. ¿Cuántos píxeles por módulo hacen falta como mínimo para leer el código? Justifícalo con el teorema de muestreo.
3. ¿Qué le pasa a la imagen 6? ¿Qué filtro habría que haber puesto antes de muestrear?

**Figuras mínimas:** las seis imágenes; fila ideal frente a muestreada; espectro con la envolvente.

## Hito 2 · Iluminación y filtrado 2D (T4, semana 9)

**Tareas**

1. Corrige la iluminación de la imagen 4 con un modelo multiplicativo (imagen = reflectancia × iluminación): estima la iluminación con un filtro adecuado y divide. Compara con restar un paso bajo.
2. En la imagen 2, enderezada, compara filtros de media 5×5, vertical (15×1) y horizontal (1×5). ¿Con cuáles se lee una sola fila?
3. Calcula y representa la respuesta en frecuencia 2D de cada núcleo.

**Preguntas**

1. ¿Por qué el filtro para estimar la iluminación no puede ser un paso bajo lineal sin más? ¿Qué hace el máximo local?
2. ¿Por qué el filtro vertical conserva los bordes y el horizontal no? Explícalo con |H(f_x, f_y)| y con el espectro del código.
3. ¿Qué ventaja computacional tiene un filtro separable de N×N coeficientes?

**Figuras mínimas:** iluminación antes y después; comparación de filtros; respuestas 2D.

## Hito 3 · Ruido, umbral y lectura (T5, semana 13)

**Tareas**

1. Mide el ruido en una zona blanca de la etiqueta: histograma, desviación típica y autocorrelación.
2. Comprueba cómo baja la varianza del ruido al promediar N filas.
3. Binariza el perfil promedio con un umbral (Otsu u otro), localiza los bordes con precisión subpíxel y obtén las 59 rachas.
4. Decodifica: normaliza cada grupo de 4 rachas a 7 módulos, busca el patrón más cercano y comprueba el dígito de control.
5. Añade ruido gaussiano a la imagen 1 y mide la tasa de lectura frente a σ para varios N.

**Preguntas**

1. ¿Por qué el promediado de filas mejora la SNR en un factor N? ¿Qué hipótesis hace falta sobre el ruido?
2. ¿Por qué Otsu funciona bien aquí? ¿Cuándo dejaría de hacerlo?
3. ¿Cómo usa el decodificador la redundancia del código (anchuras que suman 7, paridad, dígito de control) para detectar errores?

**Figuras mínimas:** estadística del ruido; varianza frente a N; histograma con el umbral; tasa de lectura frente a σ.

## Hito 4 · Orientación, desenfoque y memoria final (T6, semana 16)

**Tareas**

1. Calcula la DFT 2D de una imagen girada, mide la energía por direcciones y estima el ángulo del código. Endereza la imagen.
2. Localiza el código en la imagen enderezada (por ejemplo, zonas con mucha derivada horizontal y poca vertical).
3. En la imagen 5 (movida), localiza los ceros del desenfoque en el espectro de la fila, estima su longitud y aplica deconvolución de Wiener.
4. Monta la cadena completa y aplícala a las seis imágenes sin ajustar nada a mano para cada una. Genera `lecturas.csv`.

**Preguntas**

1. ¿Por qué la energía del espectro 2D se concentra en una recta? ¿Qué limita la precisión del ángulo?
2. ¿Qué pasa en la deconvolución si 1/SNR es demasiado pequeño? ¿Y demasiado grande?
3. ¿Qué imagen es la más difícil y qué etapa limita su lectura?

**Entrega:** memoria final, código completo y `lecturas.csv`.

## Criterios específicos por hito

| Hito | Imprescindible para aprobar | Para Excelente |
|---|---|---|
| H1 | Módulo medido y espectro de la fila | Relaciona el primer cero con m, explica el área del píxel y el aliasing de la imagen 6 |
| H2 | Iluminación corregida y comparación de filtros | Respuestas 2D y razonamiento con el espectro del código |
| H3 | Lectura de las imágenes de desarrollo | Curva de tasa de lectura y justificación de N y del umbral |
| H4 | Cadena completa aplicada a las seis imágenes | Ángulo por DFT 2D y deconvolución con la longitud estimada del espectro |
