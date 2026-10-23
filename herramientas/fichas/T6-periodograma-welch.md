## Introducción

### El periodograma

La DEP es la DTFT de la autocorrelación, Φ_xx(e^{jΩ}) = Σ_l φ_xx[l] e^{−jΩl}. Con una realización de N muestras, la estimación más directa es el **periodograma**

> P_N(e^{jΩ}) = |X_N(e^{jΩ})|²/N,

donde X_N es la DTFT de las N muestras. Es la DTFT del estimador sesgado de la autocorrelación, y se calcula con una FFT.

### Un estimador que no mejora con N

El periodograma es **asintóticamente insesgado** (su media tiende a Φ_xx), pero **no es consistente**: su varianza no baja al aumentar N. Para ruido gaussiano, en cada frecuencia P_N/Φ_xx se comporta como una exponencial de media 1, con desviación típica igual a la media: la estimación fluctúa tanto como el valor que se quiere medir. Con más muestras hay más frecuencias, igual de ruidosas, no frecuencias mejor estimadas.

### Promediar: Bartlett y Welch

- **Bartlett**: se divide la señal en K tramos de L muestras sin solapar y se promedian sus periodogramas. Si los tramos son casi independientes, la varianza baja en un factor K. A cambio, cada periodograma tiene la resolución de L muestras, no de N: el lóbulo principal de la ventana rectangular mide 4π/L entre ceros.
- **Welch**: además, cada tramo se multiplica por una ventana (Hann, Hamming…) que reduce las fugas, y los tramos se **solapan**, normalmente un 50 %. El solapamiento aprovecha las muestras que la ventana atenúa en los extremos y casi duplica K sin que los tramos dejen de ser casi independientes. Es `pwelch` en Matlab y `scipy.signal.welch` en Python.

El compromiso es entre **varianza** (más tramos, más cortos) y **resolución** (menos tramos, más largos).

## Guía de uso

- La señal es un AR(2) con polos en 0,9e^{±jπ/3} (un pico ancho en Ω = π/3) más un tono de amplitud **A** y frecuencia **Ω₁** (línea naranja), de fase aleatoria.
- **Método**, **N**, **L**, **solapamiento** y **ventana** (estas dos, solo en Welch). **Realización** cambia la semilla.
- La gráfica muestra, en dB, la estimación de una realización, la franja entre el mínimo y el máximo de 10 realizaciones y la DEP teórica del AR(2).
- El recuadro da los tramos, la anchura del lóbulo principal (la resolución), la varianza relativa media de la estimación (calculada con las 10 realizaciones, lejos del tono) comparada con 1/K, y las potencias del tono y del AR(2).

## Ejercicios

**1. El periodograma no mejora.** Con el periodograma, prueba N = 256, 4096 y 16 384. ¿Cómo cambian la franja y la varianza relativa? ¿Y la resolución?

<details><summary>Solución</summary>
La varianza relativa se queda cerca de 1 (0,95, 0,89 y 0,91, con la incertidumbre de estimarla con 10 realizaciones) y la franja mantiene unos 15 dB de anchura. La resolución sí mejora: el lóbulo de la rectangular mide 4π/N, de 0,049 a 0,0008 rad/muestra. Más muestras dan más detalle en frecuencia, pero no menos ruido.
</details>

**2. Bartlett.** Con N = 4096 y L = 256, ¿cuántos tramos hay y en cuánto baja la varianza? ¿Qué se pierde?

<details><summary>Solución</summary>
K = 16 tramos y la varianza relativa baja a 0,064, muy cerca de 1/K = 0,063. La estimación se ve suave y la franja se estrecha a unos pocos dB. Se pierde resolución: el lóbulo mide 4π/256 = 0,049 rad/muestra en lugar de 0,003.
</details>

**3. El solapamiento.** Con Welch (Hann, L = 256, N = 4096), compara el 0, el 50 y el 75 % de solapamiento. ¿Cuántos tramos hay? ¿Sigue bajando la varianza como 1/K?

<details><summary>Solución</summary>
Hay 16, 31 y 61 tramos. Sin solapar, la varianza relativa es 0,067 (1/K = 0,063). Al 50 % baja a 0,034, casi 1/31: con Hann, tramos solapados a la mitad son casi independientes. Al 75 % se queda en 0,032, no en 1/61 = 0,016, porque los tramos comparten demasiadas muestras. Por eso el 50 % es lo habitual. Con N = 16 384 y el 50 % habría 127 tramos, como en el ejercicio 18 de la hoja.
</details>

**4. La ventana.** Con Welch al 50 % y L = 256, compara Hann y rectangular. ¿Cuál tiene más resolución? ¿Cuál reduce más la varianza? ¿Qué pasa en las frecuencias altas, donde la DEP es baja?

<details><summary>Solución</summary>
La rectangular tiene el lóbulo más estrecho (0,049 frente a 0,098 rad/muestra) pero, al solapar, sus tramos están más correlados y la varianza solo baja a 0,049 (con Hann, 0,034). Además, sus lóbulos laterales llevan potencia del pico de π/3 a las frecuencias en que el AR(2) está 20 dB por debajo, y la estimación se separa de la teórica: es la fuga espectral.
</details>

**5. Resolución contra varianza.** Con Welch, Hann, 50 % y N = 4096, compara L = 64 y L = 1024. ¿Qué se ve mejor en cada caso? Prueba a poner el tono cerca del pico del AR(2), por ejemplo en Ω₁ = 1,2.

<details><summary>Solución</summary>
Con L = 64 hay 127 tramos y la varianza es mínima (0,008), pero el lóbulo mide 0,39 rad/muestra: el tono queda ensanchado y casi se confunde con el pico del AR(2). Con L = 1024, 7 tramos, varianza 0,15 y un lóbulo de 0,025: el tono es una línea estrecha bien separada. Las DEP con picos estrechos piden L grandes; las suaves, L pequeñas.
</details>

**6. Un tono débil.** El tono de amplitud 0,3 tiene potencia 0,045, el 1 % de la del AR(2). ¿Se ve en el periodograma con N = 4096? ¿Y con Welch? ¿Por qué un tono sobresale más cuanto más larga es la ventana?

<details><summary>Solución</summary>
En Ω₁ = 2,2 la DEP del AR(2) vale −5,9 dB. El tono aporta una raya cuya altura en la estimación crece con la longitud del tramo (su energía se concentra en un lóbulo de anchura ∝ 1/L), mientras que la DEP del ruido no depende de L. En el periodograma sobresale mucho, pero entre fluctuaciones de más de 10 dB es difícil distinguirlo de un pico de ruido; con Welch y L = 256 sobresale unos 10 dB sobre una estimación suave y se identifica sin dudas.
</details>

## Para profundizar

- [Apuntes del Tema 6](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%20Apuntes.pdf), sección 4, «Estimación de la densidad espectral».
- [Transparencias T6-04](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%2004%20-%20An%C3%A1lisis%20espectral.pdf), periodograma y método de Welch.
- [Hoja de ejercicios del Tema 6](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%20Ejercicios.pdf), ejercicios 15 y 18, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%20Ejercicios%20resueltos.pdf).
- P. D. Welch, «The use of fast Fourier transform for the estimation of power spectra», *IEEE Transactions on Audio and Electroacoustics* 15(2), 1967, 70-73.
- P. Stoica y R. Moses, *Spectral Analysis of Signals*, Prentice Hall, 2005, capítulo 2.

## Relación con otros conceptos

- **Ventanas y fugas (Tema 3).** Herramienta: [Ventanas y fuga espectral](T3-ventanas.html).
- **La autocorrelación estimada.** Herramienta: [Estimación de la autocorrelación](T6-autocorrelacion.html).
- **El espectrograma (Tema 5).** Usa los mismos tramos enventanados, pero en lugar de promediarlos los muestra uno a uno. Herramienta: [STFT y espectrograma](T5-stft.html).
- **DEP de ruido filtrado.** Herramienta: [Ruido a través de un sistema LTI](T6-ruido-lti.html).
