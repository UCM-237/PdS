## Introducción

### Dos tonos por tecla

En la marcación por tonos (DTMF, *dual-tone multi-frequency*), cada tecla del teléfono se codifica con la suma de dos sinusoides: una de **fila** (697, 770, 852 o 941 Hz) y una de **columna** (1209, 1336 o 1477 Hz; la cuarta, 1633 Hz, se reserva para las teclas A a D). La tecla 5, por ejemplo, es 770 + 1336 Hz. Las frecuencias se eligieron para que ningún armónico ni suma ni diferencia de dos de ellas coincida con otra, y así la voz rara vez imita una tecla.

### El receptor

El receptor trabaja con tramos cortos de la señal: es un análisis de tiempo corto. En cada tramo mide la amplitud en las siete frecuencias, elige la mayor de las filas y la mayor de las columnas y decide la tecla. Hay dos dificultades:

- **Resolución.** Las dos filas más próximas, 697 y 770 Hz, distan 73 Hz. Para que el lóbulo principal de una no tape a la otra, la ventana debe ser lo bastante larga: con Hann, 2f_s/L ≤ 73 Hz, es decir, L ≥ 220 muestras a 8 kHz (27 ms).
- **Duración y ruido.** La norma exige reconocer tonos de 40 ms. Con más muestras, la sinusoide suma su amplitud de forma coherente (crece como L) y el ruido solo como √L: la relación señal-ruido del detector mejora 3 dB cada vez que se duplica L.

### El algoritmo de Goertzel

Las siete frecuencias no caen en la rejilla de una DFT de tamaño razonable (con N = 256, 852 Hz cae entre k = 27 y k = 28). En lugar de una FFT completa se usa el **algoritmo de Goertzel**, un IIR de segundo orden que evalúa la DTFT del tramo en una frecuencia cualquiera Ω₀ con un producto real por muestra:

> s[n] = x[n] + 2cos(Ω₀) s[n−1] − s[n−2],  |X(e^{jΩ₀})|² = s[L−1]² + s[L−2]² − 2cos(Ω₀) s[L−1] s[L−2].

Para siete frecuencias cuesta menos que una FFT.

## Guía de uso

- Pulsa una **tecla** del teclado: se genera su tono de la **duración** elegida, con ruido gaussiano de la **desviación** elegida, a f_s = 8000 Hz. Los botones **Oír** reproducen la tecla y el número.
- **L** es el número de muestras que se analizan (o el tono entero, si es más corto), con una ventana de Hann.
- Arriba, la señal y las salidas del algoritmo de Goertzel en las siete frecuencias, con las elegidas en rojo. En el centro, el espectro del tramo, con triángulos en las dos frecuencias de la tecla. Abajo, el espectrograma del número escrito, con los tonos separados por 50 ms de silencio.
- El recuadro da la tecla, la detectada (en verde si acierta) y la resolución.

## Ejercicios

**1. Las frecuencias.** Pulsa varias teclas. ¿Qué dos frecuencias tiene el 0? ¿Y el 9? ¿Cuál es la pareja de frecuencias más próximas y qué L necesita Hann para separarlas?

<details><summary>Solución</summary>
El 0 es 941 + 1336 Hz y el 9, 852 + 1477 Hz. La pareja más próxima es 697 y 770 Hz, a 73 Hz: con Hann hace falta 2f_s/L ≤ 73, L ≥ 220 muestras. Con la rectangular, unas 110. Es el apartado a del ejercicio 5 de la hoja.
</details>

**2. Ventana corta sin ruido.** Con σ = 0 y L = 64, pulsa el 1. ¿Se distinguen 697 y 770 Hz en el espectro? ¿Acierta el detector? ¿Por qué?

<details><summary>Solución</summary>
En el espectro no: el lóbulo de Hann mide 4f_s/L = 500 Hz y las cuatro filas forman un solo lóbulo. Pero el detector acierta, porque Goertzel mide exactamente en 697 y 770 Hz, y en la verdadera la ventana da su máximo, W(0), mientras que en la otra da W a 73 Hz, que es algo menor. Sin ruido basta esa pequeña diferencia; con ruido no.
</details>

**3. Ruido.** Con duración de 200 ms y σ = 3, prueba las doce teclas con L = 64, 128 y 256. ¿Cuántas acierta? ¿Qué SNR tiene cada tono?

<details><summary>Solución</summary>
Con esta realización del ruido, unas 2, 8 y 12 de 12. Cada tono tiene potencia 1/2 y el ruido σ² = 9: una SNR de −12,6 dB por tono, y el tono no se ve en la señal. Al duplicar L, la salida del detector para el tono se duplica y la del ruido crece √2: la SNR del detector mejora 3 dB. Con L = 256 basta.
</details>

**4. Tonos cortos.** Con σ = 3 y L = 512, baja la duración a 40 y a 20 ms. ¿Cuántas muestras se analizan? ¿Sigue acertando?

<details><summary>Solución</summary>
Se analiza el tono entero: 320 muestras a 40 ms, y 160 a 20 ms. Con 40 ms acierta las 12; con 20 ms, unas 8, y además 160 muestras no bastan para separar 697 y 770 Hz con Hann. Por eso la norma pide tonos de al menos 40 ms (con 50 ms de silencio entre ellos), que caben en el ejercicio 5 de la hoja.
</details>

**5. La rejilla de la DFT.** Con una DFT de 256 puntos, ¿qué índices k caen más cerca de 852 y de 1336 Hz? ¿Cuánto se pierde en amplitud por no medir en la frecuencia exacta, con Hann y L = 256?

<details><summary>Solución</summary>
f_s/N = 31,25 Hz. 852/31,25 = 27,3, así que k = 27 (843,75 Hz), y 1336/31,25 = 42,75, k = 43 (1343,75 Hz). El error de 8 Hz es una cuarta parte de la separación entre bins, y con Hann la pérdida es de unos 0,4 dB; en el peor caso, a medio bin, 1,4 dB. Goertzel evita el problema evaluando la DTFT en la frecuencia exacta.
</details>

## Para profundizar

- [Apuntes del Tema 5](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%20Apuntes.pdf), sección 1, «Aplicaciones».
- [Transparencias T5-01](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%2001%20-%20STFT.pdf), ejemplo DTMF y reconocer una tecla.
- [Hoja de ejercicios del Tema 5](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%20Ejercicios.pdf), ejercicio 5, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%20Ejercicios%20resueltos.pdf).
- UIT-T, Recomendación Q.23, *Technical features of push-button telephone sets*, 1988.
- A. V. Oppenheim y R. W. Schafer, *Discrete-Time Signal Processing*, 3.ª ed., Pearson, 2010, apartado 9.2 (algoritmo de Goertzel).

## Relación con otros conceptos

- **El espectrograma.** Herramienta: [STFT y espectrograma](T5-stft.html).
- **Resolución y lóbulo principal (Tema 3).** Herramienta: [Ventanas y fuga espectral](T3-ventanas.html).
- **La DTFT en un punto.** Goertzel calcula un solo coeficiente de la DFT. Herramienta: [DFT, fuga y relleno con ceros](T3-dft.html).
- **Detección con ruido (Tema 6).** Herramienta: [Estimación de un retardo por correlación](T6-retardo-correlacion.html).
