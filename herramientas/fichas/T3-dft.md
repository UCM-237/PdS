## Introducción

### La transformada discreta de Fourier

La DFT de N puntos de una secuencia x[n], 0 ≤ n < N, es

> X[k] = Σ_{n=0}^{N−1} x[n] W_N^{kn},  W_N = e^{−j2π/N},  k = 0, …, N − 1,

y la IDFT la invierte: x[n] = (1/N) Σ_k X[k] W_N^{−kn}. Es la única transformada de Fourier que se puede calcular con un número finito de operaciones, y por eso es la que se usa en la práctica para analizar espectros. Si x[n] tiene L ≤ N muestras (el resto, ceros), X[k] son las muestras de su DTFT en Ω_k = 2πk/N.

### El eje de frecuencias

El índice k corresponde a la frecuencia discreta Ω_k = 2πk/N y, si la señal se muestreó con fs, a

> f_k = k fs/N hercios,  separados Δf = fs/N.

Las muestras k > N/2 son frecuencias negativas: k = N − 1 es −fs/N. Para una señal real, X[N − k] = X*[k] y basta mirar 0 ≤ k ≤ N/2.

### Amplitud de una sinusoide

Si A cos(Ω₀n + φ) completa un número entero de periodos en las L muestras, cae exactamente en una muestra k₀ de la DFT con |X[k₀]| = AL/2 y fase φ, y el resto de muestras son nulas. La amplitud se lee como A = 2|X[k₀]|/L (sin el factor 2 en k = 0 y k = N/2).

### Fuga espectral

Si la frecuencia del tono cae entre dos muestras, la DTFT de las L muestras es un núcleo de Dirichlet centrado en Ω₀, y las muestras de la DFT lo pillan fuera del máximo: la energía se reparte entre muchas k (**fuga**) y el pico más alto subestima la amplitud. En el peor caso, a media muestra, la pérdida es de unos 3,9 dB con la ventana rectangular (**festoneado**).

### Relleno con ceros y resolución

Añadir ceros hasta N > L no cambia la DTFT, que sigue siendo la de las L muestras: solo la muestrea más densamente. Eso interpola el espectro, ayuda a localizar los picos y reduce el festoneado, pero **no mejora la resolución**. Dos tonos se distinguen si su separación es mayor que la semianchura del lóbulo principal,

> |Ω₂ − Ω₁| ≳ 2π/L,  es decir, |f₂ − f₁| ≳ fs/L = 1/T_obs,

que depende de la duración del registro, no de N ni de fs.

## Guía de uso

- **L** es el número de muestras de señal. El deslizador **N** da el logaritmo en base 2 del tamaño de la DFT (6 son 64 puntos); si es menor que L, se usa la potencia de 2 siguiente. Las muestras de relleno salen en gris.
- La señal es cos(2πF₁n) + A₂ cos(2πF₂n), con **F₁**, **F₂** en ciclos por muestra y la **amplitud de la segunda** A₂.
- **Ω, k o f (Hz)** cambia el eje de la gráfica de abajo; con **fs** se elige la frecuencia de muestreo para el eje en hercios.
- **|X[k]| o 2|X[k]|/L** cambia la escala; la segunda estima la amplitud de cada tono.
- Abajo, la DTFT de las L muestras en gris y la DFT en rojo. El recuadro da la separación entre muestras, la resolución y la frecuencia y amplitud medidas de cada tono.

## Ejercicios

**1. El ejercicio 10 de la hoja.** Con fs = 8000, eje en hercios, L = 128 y N = 9 (512 puntos), ¿cuánto vale Δf? Pon F₁ = 0,125: ¿en qué k aparece el tono y a qué frecuencia corresponde?

<details><summary>Solución</summary>
Δf = 8000/512 = 15,625 Hz. F₁ = 0,125 son 1000 Hz, en k = 64. Con la escala 2|X|/L, la amplitud es 1. La duración del registro es L/fs = 16 ms, pero el relleno hasta 512 puntos da la separación de 15,625 Hz; sin rellenar, con N = L = 128, sería 62,5 Hz.
</details>

**2. Sin fuga.** Con L = 64, N = 6 (64 puntos), F₁ = 0,125, F₂ = 0,3125 y A₂ = 0,5 (el ejercicio 11 de la hoja con otras amplitudes), ¿en qué k caen los tonos? ¿Cuánto valen |X[k]| y 2|X[k]|/L en ellos? ¿Y en el resto de las k?

<details><summary>Solución</summary>
F·N = 8 y 20: caen en k = 8 y k = 20, con |X[8]| = 64/2 = 32 y |X[20]| = 0,5·32 = 16, es decir, amplitudes 1 y 0,5. El resto de las muestras son nulas: caen justo en los ceros del núcleo de Dirichlet. La DTFT gris, en cambio, no es nula entre ellas.
</details>

**3. Fuga y festoneado.** En el caso anterior, pon A₂ = 0 y cambia F₁ a 0,133. ¿Qué pasa con las muestras de la DFT? ¿Qué amplitud se mide? Sube N a 9.

<details><summary>Solución</summary>
F₁·L = 8,5: el tono cae entre k = 8 y k = 9. Su energía se reparte entre todas las k y la amplitud medida baja a unos 0,67 (−3,5 dB). Con N = 512 la DFT muestrea la DTFT con mucha más densidad, una muestra cae casi en el máximo y se mide 1,00. La fuga, la anchura del pico, no cambia.
</details>

**4. Rellenar no resuelve.** Con fs = 1000, eje en hercios, A₂ = 1, F₁ = 0,2 y F₂ = 0,22 (200 y 220 Hz), compara L = 32 y L = 128, las dos con N = 9. ¿En cuál se ven dos picos? ¿Ayuda rellenar con ceros en el primer caso?

<details><summary>Solución</summary>
Con L = 32 la resolución es fs/L ≈ 31 Hz > 20 Hz: se ve un único pico ancho, aunque la DFT tenga 512 muestras. Con L = 128, fs/L ≈ 7,8 Hz y los dos picos se separan. Rellenar con ceros solo dibuja mejor la DTFT de las 32 muestras, que tiene un solo lóbulo: no añade información. Es la figura de resolución de los apuntes.
</details>

**5. El ejercicio 12 de la hoja.** Para distinguir 1000 y 1030 Hz a fs = 8 kHz, ¿cuántas muestras hacen falta? Con fs = 8000, F₁ = 0,125 y F₂ = 0,129 (1032 Hz), comprueba si L = 128 basta.

<details><summary>Solución</summary>
Hace falta fs/L < 30 Hz, es decir, L > 267. Con L = 128, la máxima de la herramienta, fs/L = 62,5 Hz y se ve un solo pico, centrado entre las dos frecuencias, aunque se rellene con ceros hasta 512. |F₁ − F₂|·L = 0,51, menos que 1.
</details>

## Para profundizar

- [Apuntes del Tema 3](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%20Apuntes.pdf), sección 2 (La transformada discreta de Fourier) y sección 4 (Análisis espectral con la DFT): «Eje de frecuencias», «Amplitud de una sinusoide», «Fuga espectral» y «Resolución y relleno con ceros».
- [Transparencias T3-01](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%2001%20-%20DFT.pdf) y [T3-03](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%2003%20-%20An%C3%A1lisis%20espectral.pdf), la DFT y el análisis espectral.
- [Hoja de ejercicios del Tema 3](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%20Ejercicios.pdf), ejercicios 10 a 12, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T3/codigo/python/dft_directa.py` y `espectro_dft.py`, y sus versiones en Matlab.
- A. V. Oppenheim y R. W. Schafer, *Discrete-Time Signal Processing*, 3.ª ed., Pearson, 2010, apartados 8.5 y 10.2.

## Relación con otros conceptos

- **Extensión periódica.** Por qué las N muestras bastan si N ≥ L. Herramienta: [Extensión periódica](T3-extension-periodica.html).
- **Ventanas.** Reducen la fuga a cambio de resolución. Herramienta: [Ventanas y fuga espectral](T3-ventanas.html).
- **Propiedades de la DFT.** Herramientas: [Editor de la DFT](T3-editor-dft.html) y [Propiedades de la DFT](T3-propiedades-dft.html).
- **FFT.** Cómo se calcula la DFT en la práctica. Herramienta: [FFT: el grafo de mariposas](T3-fft-mariposa.html).
- **Muestreo (Tema 2).** El eje en hercios usa la misma relación Ω = 2πf/fs. Herramienta: [Aliasing](T2-aliasing.html).
