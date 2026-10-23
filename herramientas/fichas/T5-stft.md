## Introducción

### Señales cuyo espectro cambia

La DFT de una señal entera dice qué frecuencias contiene, pero no cuándo. En la voz, la música, un chirp de radar o una avería que aparece en una máquina, el contenido en frecuencia **cambia con el tiempo** y lo que interesa es justo ese cambio.

### Definición

La **transformada de Fourier de tiempo corto** (STFT) corta la señal en tramos con una ventana w[n] de L muestras que avanza R muestras, y calcula la DFT de N puntos de cada tramo:

> X[m, k] = Σ_n x[n] w[n − mR] e^{−j2πkn/N}.

El índice m es el tramo (el instante t_m = (mR + L/2)/f_s) y k la frecuencia (f_k = k f_s/N). El **espectrograma** es |X[m, k]|², normalmente en dB, dibujado como una imagen con el tiempo en horizontal y la frecuencia en vertical.

### Los parámetros

- **L** fija la resolución. Un tramo de L/f_s segundos no distingue sucesos más próximos que esa duración, y su espectro es el de la señal convolucionado con el de la ventana, cuyo lóbulo principal mide 2f_s/L (rectangular), 4f_s/L (Hann, Hamming) o 6f_s/L (Blackman) entre ceros.
- **R** es el salto entre tramos: cuántos espectros por segundo se calculan. No cambia la resolución, solo lo densa que es la rejilla en el tiempo. Lo habitual es un solapamiento L − R del 50 al 75 %.
- **N ≥ L** rellena con ceros: muestrea más finamente el mismo espectro, pero no separa mejor dos tonos.

### Síntesis por solapamiento y suma

Si se calcula la IDFT de cada tramo y se suman todos en su posición, se obtiene x[n] multiplicada por Σ_m w[n − mR]. Cuando esa suma es una **constante C** (condición COLA, *constant overlap-add*), la señal se recupera dividiendo por C. La Hann periódica la cumple con R = L/2 o L/4, la rectangular con R = L. Así se modifica una señal tramo a tramo (por ejemplo, para quitar ruido) y se vuelve al tiempo.

## Guía de uso

- **Señal**: un chirp de 100 a 1500 Hz con un tono de 1200 Hz entre 0,4 y 0,8 s y un clic en 1,1 s; dos tonos sucesivos de 500 y 1200 Hz; o una voz sintética cuyo tono sube de 110 a 150 Hz y cuyos formantes pasan de /a/ a /i/. Se muestrea a f_s = 4000 Hz durante 1,5 s.
- **Ventana**, **L**, **solapamiento** y **N** son los parámetros de la STFT. Las ventanas son periódicas, las que cumplen COLA.
- **Instante del tramo** elige un tramo: se ve sombreado sobre la señal, marcado en el espectrograma y con su espectro a la derecha.
- Abajo, la reconstrucción por solapamiento y suma dividida por C y, a trazos, la suma de las ventanas. El recuadro da R, el número de tramos, las resoluciones, C, el rizado de la suma y el error de la reconstrucción.

## Ejercicios

**1. Los números de partida.** Con Hann, L = 128, 75 % y N = L, ¿cuánto duran los tramos y cada cuánto se calcula uno? ¿Cuántos tramos hay? ¿Qué separación hay entre frecuencias de la DFT y cuánto mide el lóbulo principal?

<details><summary>Solución</summary>
Los tramos duran 128/4000 = 32 ms y avanzan R = 32 muestras, 8 ms. Hay ⌊(6000 − 128)/32⌋ + 1 = 184 tramos. Las frecuencias de la DFT están separadas f_s/N = 31,25 Hz y el lóbulo principal de Hann mide 4f_s/L = 125 Hz entre ceros. Es el mismo cálculo que el ejercicio 1 de la hoja, con otros números.
</details>

**2. El chirp.** Con la primera señal, lleva el tramo a t = 0,5 s. ¿En qué frecuencia está el máximo? ¿Cuánto cambia la frecuencia del chirp dentro de una ventana de 128 muestras, y de una de 512?

<details><summary>Solución</summary>
La frecuencia instantánea es 100 + (1400/1,5)t = 100 + 933t Hz: en t = 0,5 s, unos 567 Hz. Dentro de 32 ms cambia 933 · 0,032 ≈ 30 Hz, menos que el lóbulo de 125 Hz: el chirp se ve como una línea fina. Con L = 512 (128 ms) cambia 119 Hz, mucho más que el lóbulo de 31 Hz de esa ventana, y la línea se ensancha. El tono de 1200 Hz, en cambio, sale más fino con L = 512.
</details>

**3. El clic y la duración de la ventana.** Mira el clic de 1,1 s con L = 32, 128 y 512. ¿Cuánto dura en el espectrograma? ¿Y qué le pasa al tono de 1200 Hz?

<details><summary>Solución</summary>
El clic ocupa todas las frecuencias durante el tiempo en que está dentro de alguna ventana, unos L/f_s: 8, 32 y 128 ms. El tono hace lo contrario: con L = 32 es una banda de 500 Hz de anchura (el lóbulo 4f_s/L) y con L = 512 de 31 Hz. No hay una L que dé a la vez el clic fino y el tono fino: es el principio de incertidumbre, que se estudia en [Resolución en tiempo y en frecuencia](T5-resolucion-tiempo-frecuencia.html).
</details>

**4. La condición COLA.** Recorre las ventanas y los solapamientos. ¿Qué combinaciones cumplen COLA y cuánto vale C? ¿Qué pasa con Blackman al 50 %? ¿Y con Hann sin solapamiento?

<details><summary>Solución</summary>
Hann: C = 1 al 50 % y C = 2 al 75 % (se solapan el doble de ventanas). Hamming: 1,08 y 2,16, como en el ejercicio 4 de la hoja. Rectangular: C = 1 sin solapar, 2 al 50 % y 4 al 75 %. Blackman al 50 % no la cumple (la suma tiene un rizado del 38 %) y necesita el 75 %. Con Hann sin solapamiento la suma se anula en los extremos de cada tramo, el rizado es del 200 % y la señal reconstruida desaparece cada 32 ms. Al 25 % no la cumple ninguna. Cuando se cumple, el error de reconstrucción es prácticamente nulo, del orden de 10^{−15}.
</details>

**5. Banda estrecha y banda ancha.** Con la voz sintética, compara L = 512 y L = 32 con Hann al 75 %. ¿Qué se ve en cada caso? ¿Qué longitud mínima separa los armónicos de un tono de 110 Hz?

<details><summary>Solución</summary>
Con L = 512 (128 ms, lóbulo de 31 Hz) se ven los **armónicos** del tono glotal como líneas horizontales separadas 110 a 150 Hz que suben poco a poco: es el espectrograma de banda estrecha. Con L = 32 (8 ms, lóbulo de 500 Hz) los armónicos se funden y se ven las **formantes**, las bandas anchas que se mueven de 700 y 1100 Hz a 300 y 1800 Hz, y rayas verticales en cada pulso glotal: es el de banda ancha. Para separar armónicos a 110 Hz con Hann hace falta 2f_s/L ≤ 110, es decir, L ≥ 73 muestras (18 ms).
</details>

## Para profundizar

- [Apuntes del Tema 5](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%20Apuntes.pdf), sección 1 (Transformada de Fourier de tiempo corto).
- [Transparencias T5-01](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%2001%20-%20STFT.pdf), parámetros, espectrograma y solapamiento y suma.
- [Hoja de ejercicios del Tema 5](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%20Ejercicios.pdf), ejercicios 1, 3 y 4, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%20Ejercicios%20resueltos.pdf).
- A. V. Oppenheim y R. W. Schafer, *Discrete-Time Signal Processing*, 3.ª ed., Pearson, 2010, apartados 10.3 a 10.5.

## Relación con otros conceptos

- **Ventanas (Tema 3).** Cada tramo es una señal enventanada, con el mismo lóbulo y las mismas fugas. Herramienta: [Ventanas y fuga espectral](T3-ventanas.html).
- **Solapamiento y suma (Tema 3).** El mismo método por bloques que se usa para filtrar con la FFT. Herramienta: [Convolución por bloques](T3-solapamiento-suma.html).
- **El compromiso tiempo-frecuencia.** Herramienta: [Resolución en tiempo y en frecuencia](T5-resolucion-tiempo-frecuencia.html).
- **Una aplicación.** Herramienta: [Marcación por tonos (DTMF)](T5-dtmf.html).
- **Wavelets.** Ventanas de duración variable según la frecuencia. Herramienta: [Escalograma frente a espectrograma](T5-escalograma.html).
