## Introducción

### Ondas planas

La DFT bidimensional de una imagen f[m, n] de M×N píxeles es

> F[k, l] = Σ_m Σ_n f[m, n] e^{−j2π(km/M + ln/N)},

y la IDFT la escribe como suma de **ondas planas** e^{j2π(km/M + ln/N)}. La onda de índices (k, l) tiene k ciclos a lo largo de cada columna (en vertical) y l a lo largo de cada fila (en horizontal): sus franjas son perpendiculares al vector (k, l) y su periodo es N/√(k² + l²) píxeles en una imagen cuadrada. Un coseno real da dos coeficientes, en ±(k, l). F[0, 0] es la suma de todos los píxeles: MN veces el nivel medio.

### Cómo se dibuja

Como F es periódica, los índices k ≥ N/2 son en realidad frecuencias negativas. Para verla se **centra** (`fftshift`), con la frecuencia cero en el centro, y se dibuja log(1 + |F|), porque F[0, 0] es muchísimo mayor que el resto. En las imágenes naturales la energía se concentra en las frecuencias bajas, y los bordes rectos dan líneas perpendiculares a ellos.

### Filtrar en frecuencia

La convolución circular 2D es el producto de las DFT: G[k, l] = H[k, l] F[k, l]. Con D = √(k² + l²) la distancia al origen:

- **Ideal**: H = 1 si D ≤ D₀. Su respuesta al impulso es un «sinc circular» con lóbulos negativos, que deja **anillos** alrededor de los bordes (fenómeno de Gibbs).
- **Gaussiano**: H = e^{−D²/(2D₀²)}. Su respuesta al impulso es otra gaussiana, de σ = N/(2πD₀) píxeles, positiva y sin anillos.
- **Butterworth** de orden n: H = 1/(1 + (D/D₀)^{2n}), un término medio.
- El **paso alto** es 1 − H. Unas **muescas** (*notch*) anulan un entorno de las frecuencias de un ruido periódico.

### La fase importa más que el módulo

Una imagen reconstruida solo con la fase de su DFT (|F| = 1 en todas las frecuencias) conserva la posición de los bordes y se reconoce; una con el módulo y la fase de otra, no.

## Guía de uso

- **Imagen**: la de prueba (con o sin un ruido periódico de frecuencia (k₀, l₀)), un coseno de índices (k₀, l₀), un cuadrado de 31×31, los anillos, un texto o una foto propia, que se procesa en el navegador.
- **Filtro**, con D₀, el orden del Butterworth y el radio de las muescas, que se colocan en ±(k₀, l₀).
- **Reconstruir solo con la fase** pone |G| = 1 antes de la IDFT.
- Arriba, la imagen y log(1 + |F|) centrada; abajo, el filtro centrado y el resultado. El recuadro da el nivel medio, el periodo de la onda, la energía que conserva el filtro y el rango de g.

## Ejercicios

**1. Un coseno.** Elige el coseno con (k₀, l₀) = (0, 24). ¿Cómo son las franjas y su periodo? ¿Dónde están los picos de la DFT? Cambia a (24, 0) y a (3, 1).

<details><summary>Solución</summary>
Con (0, 24) hay 24 ciclos a lo largo de cada fila: franjas verticales de periodo 256/24 = 10,7 píxeles, y dos picos en l = ±24 sobre el eje horizontal. Con (24, 0), franjas horizontales y picos en el eje vertical. Con (3, 1), franjas oblicuas, perpendiculares a (3, 1), de periodo 256/√10 = 81 píxeles, y picos en ±(3, 1). Además siempre está F[0, 0], porque el coseno va de 0 a 1 y tiene nivel medio 0,5. Es el ejercicio 15 de la hoja en 256×256.
</details>

**2. El cuadrado.** Mira la DFT del cuadrado. ¿Qué forma tiene y por qué? ¿Cuánto vale el nivel medio?

<details><summary>Solución</summary>
Es separable: un pulso de 31 píxeles en cada dirección, así que |F| es el producto de dos sinc discretos, una cruz con lóbulos a lo largo de los ejes con ceros cada 256/31 ≈ 8 índices. Los bordes verticales del cuadrado dan la línea horizontal del espectro, y al revés. El nivel medio es 31²/256² = 0,015.
</details>

**3. Ideal frente a gaussiano.** Con el cuadrado y D₀ = 20, compara los tres paso bajo. ¿Qué rango de valores tiene g en cada caso? ¿A qué gaussiano espacial equivale el filtro gaussiano?

<details><summary>Solución</summary>
Ideal: de −0,12 a 1,17, con anillos alrededor del cuadrado (un 17 % de sobreoscilación). Butterworth de orden 2: de −0,03 a 1,06, anillos débiles. Gaussiano: de 0 a 1, sin anillos, pero con los bordes más emborronados; equivale a un gaussiano de σ = 256/(2π · 20) = 2,04 píxeles, como en el ejercicio 16 de la hoja. El ideal conserva más energía (91 % frente a 86 %): mejor nitidez, peor aspecto.
</details>

**4. Paso alto.** Con la imagen de prueba, aplica el paso alto gaussiano con D₀ = 20. ¿Qué queda? ¿Por qué conserva solo el 1,5 % de la energía?

<details><summary>Solución</summary>
Quedan los bordes y las texturas finas (la rejilla, los anillos), sobre un fondo gris: el nivel medio y la rampa del fondo desaparecen. Casi toda la energía de una imagen está en las frecuencias bajas, y sobre todo en F[0, 0]: la imagen tiene nivel medio 0,48, y F[0, 0] se lleva por sí solo el 83 % de la energía.
</details>

**5. Ruido periódico.** Elige la imagen con ruido periódico y mira su DFT. Después aplica las muescas. ¿Dónde estaba el ruido y qué queda tras filtrar? Cambia (k₀, l₀) y comprueba que las muescas lo siguen.

<details><summary>Solución</summary>
El ruido es un coseno de amplitud 0,2 con (0, 24): en la DFT son dos puntos brillantes en ±(0, 24), muy por encima de lo que los rodea. Las muescas los quitan y la imagen queda casi como la original, con el 92,5 % de la energía (el ruido tenía 0,2²/2 = 0,02 por píxel). Un paso bajo no serviría tan bien: para quitar el ruido de periodo 10,7 píxeles emborronaría toda la imagen.
</details>

**6. Solo la fase.** Con la imagen de prueba o con el texto, marca «reconstruir solo con la fase». ¿Qué se reconoce?

<details><summary>Solución</summary>
Se reconocen los bordes y los contornos de todos los objetos, aunque las zonas uniformes se vuelven grises: al igualar |F| a 1 se refuerzan las frecuencias altas (es un «blanqueado» del espectro). La información de *dónde* están las cosas está en la fase.
</details>

## Para profundizar

- [Apuntes del Tema 5](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%20Apuntes.pdf), sección 3, «DFT bidimensional» y «Filtrado en el dominio de la frecuencia».
- [Transparencias T5-03](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%2003%20-%20Im%C3%A1genes.pdf), DFT 2D y filtros en el dominio de la frecuencia.
- [Hoja de ejercicios del Tema 5](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%20Ejercicios.pdf), ejercicios 15 y 16, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%20Ejercicios%20resueltos.pdf).
- R. C. Gonzalez y R. E. Woods, *Digital Image Processing*, 4.ª ed., Pearson, 2018, capítulo 4.
- A. V. Oppenheim y J. S. Lim, «The importance of phase in signals», *Proceedings of the IEEE* 69(5), 1981, 529-541.

## Relación con otros conceptos

- **La DFT (Tema 3).** Herramienta: [DFT, fuga y relleno con ceros](T3-dft.html).
- **Convolución circular (Tema 3).** El producto de DFT es una convolución circular, también en 2D. Herramienta: [Convolución circular](T3-convolucion-circular.html).
- **Filtros en el espacio.** Herramienta: [Convolución bidimensional](T5-convolucion-2d.html).
- **Fenómeno de Gibbs (Tema 1).** Los anillos del paso bajo ideal. Herramienta: [Serie de Fourier](T1-serie-fourier.html).
- **Filtros analógicos (Tema 4).** El Butterworth, ahora con la distancia radial. Herramienta: [Aproximaciones de filtros analógicos](T4-filtros-continuos.html).
