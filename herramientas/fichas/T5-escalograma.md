## Introducción

### Ventanas que se adaptan a la frecuencia

La STFT usa la misma ventana para todas las frecuencias: si es larga, resuelve bien los tonos graves y emborrona los sucesos rápidos; si es corta, al revés. Muchas señales naturales tienen componentes de baja frecuencia que duran mucho y componentes de alta frecuencia que duran poco. Para ellas conviene analizar las frecuencias bajas con ventanas largas y las altas con ventanas cortas, de forma que cada análisis contenga el mismo número de oscilaciones.

### La transformada wavelet continua

Una **wavelet** ψ(t) es una función oscilante de media nula y energía finita, concentrada en el tiempo. Se desplaza a b y se escala por a > 0:

> ψ_{a,b}(t) = (1/√a) ψ((t − b)/a),  W(a, b) = ∫ x(t) ψ*_{a,b}(t) dt.

W(a, b) mide cuánto se parece x, cerca del instante b, a la wavelet a escala a. El **escalograma** es |W(a, b)|². Una escala grande estira la wavelet y baja su frecuencia; una escala pequeña la comprime y la sube.

### La Morlet y su frecuencia

La wavelet de **Morlet** es una exponencial compleja con envolvente gaussiana, ψ(t) = π^{−1/4} e^{jω₀t} e^{−t²/2}, con ω₀ = 6. A escala a oscila a ω₀/a, es decir, a la frecuencia f = ω₀/(2πa). Su envolvente tiene σ_t = a y su espectro σ_ω = 1/a: el producto es el mínimo, 1/2, en todas las escalas, pero el reparto cambia. La resolución relativa σ_f/f = 1/ω₀ es constante: el análisis es de **Q constante**, como el oído o las octavas de un piano.

El **sombrero mexicano** es la segunda derivada de una gaussiana, real y con solo dos oscilaciones: localiza mejor en el tiempo y peor en frecuencia. Su frecuencia equivalente es f = √2/(2πa).

## Guía de uso

- **Señal**, muestreada a f_s = 1000 Hz durante 1 s: un tono de 20 Hz y después uno de 120 Hz con un clic en 0,3 s; un chirp de 5 a 300 Hz; un tono de 50 Hz con un transitorio breve de 200 Hz; o dos clics separados 10 ms.
- **Wavelet**: Morlet o sombrero mexicano. **L** es la ventana de Hann de la STFT con la que se compara.
- El espectrograma y el escalograma tienen el mismo eje de frecuencias, logarítmico de 4 a 400 Hz; para el escalograma, cada escala se dibuja en su frecuencia equivalente. Los dos se normalizan a su máximo, en dB.
- A la derecha, la parte real de la wavelet a 10, 40 y 160 Hz: siempre el mismo número de oscilaciones, cada vez más cortas.

## Ejercicios

**1. Escalas y duraciones.** Con Morlet, ¿qué escala a corresponde a 10 Hz y a 160 Hz? ¿Cuántas muestras dura (σ_t) la wavelet en cada caso? Compáralo con el recuadro.

<details><summary>Solución</summary>
a = ω₀/(2πf): 95,5 ms a 10 Hz y 5,97 ms a 160 Hz, unas 95 y 6 muestras. A 200 Hz serían 4,77 ms, como en el ejercicio 8 de la hoja. El sombrero mexicano, con f = √2/(2πa), usa escalas más pequeñas: 22,5 ms y 1,41 ms.
</details>

**2. El clic.** Con la primera señal, Morlet y L = 128, compara la anchura del clic de 0,3 s en las dos gráficas a 10 Hz y a 200 Hz.

<details><summary>Solución</summary>
En el espectrograma ocupa lo mismo en todas las frecuencias, unos 128 ms. En el escalograma es un cono: a 10 Hz dura del orden de σ_t = 95 ms y a 200 Hz unos 5 ms. Es el «cono de influencia» del clic, que se estrecha al subir la frecuencia.
</details>

**3. Los tonos.** Con la misma señal, compara la anchura en frecuencia del tono de 20 Hz y del de 120 Hz en las dos gráficas. ¿Cuál resuelve mejor cada uno?

<details><summary>Solución</summary>
La STFT con L = 128 tiene la misma resolución en todas las frecuencias, unos 2f_s/L = 16 Hz: el tono de 20 Hz ocupa casi una octava y el de 120 Hz es una línea fina. La Morlet tiene σ_f = f/ω₀: 3,3 Hz a 20 Hz y 20 Hz a 120 Hz. En la escala logarítmica los dos tonos se ven igual de anchos (Q constante). El escalograma resuelve mejor el grave y el espectrograma, el agudo.
</details>

**4. El chirp.** Con el chirp, prueba L = 32, 128 y 512 en el espectrograma. ¿Hay una L con la que el chirp se vea fino en todo el rango? ¿Y en el escalograma?

<details><summary>Solución</summary>
No. Con L = 512 se ve fino al principio, cuando la frecuencia cambia despacio, y se emborrona al final. Con L = 32 es al revés: el principio, a pocos hercios, ocupa casi todo el eje de frecuencias bajas. El escalograma se adapta: en cada frecuencia la wavelet dura unas pocas oscilaciones, y el chirp sale con una anchura parecida en todo el rango en la escala logarítmica. Con el sombrero mexicano es más ancho en frecuencia.
</details>

**5. Dos clics a 10 ms.** Con la última señal, ¿por qué hay huecos en 50 Hz (y en 150 y 250 Hz) en las dos gráficas? ¿A partir de qué frecuencia se separan los dos clics en el escalograma? Amplía para verlo.

<details><summary>Solución</summary>
La suma de dos impulsos separados Δt = 10 ms tiene espectro |1 + e^{−j2πfΔt}|, que se anula cuando fΔt es medio entero: 50, 150, 250 Hz. La wavelet compleja de cada clic tiene la fase de esa frecuencia, y en esas frecuencias se cancelan. Los dos clics se separan cuando la wavelet dura menos que su separación, 2σ_t = 2a < 10 ms: a > 190 Hz, y en la práctica por encima de unos 300 Hz, donde aparece un valle entre ellos. El espectrograma con L = 128 no los separa nunca; haría falta L < 10.
</details>

## Para profundizar

- [Apuntes del Tema 5](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%20Apuntes.pdf), sección 2, «Wavelets» y «Transformada wavelet continua».
- [Transparencias T5-02](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%2002%20-%20Wavelets.pdf), escala y desplazamiento, escalograma frente a espectrograma.
- [Hoja de ejercicios del Tema 5](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%20Ejercicios.pdf), ejercicio 8, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%20Ejercicios%20resueltos.pdf).
- C. Torrence y G. P. Compo, «A practical guide to wavelet analysis», *Bulletin of the American Meteorological Society* 79(1), 1998, 61-78.
- S. Mallat, *A Wavelet Tour of Signal Processing*, 3.ª ed., Academic Press, 2009, capítulo 4.

## Relación con otros conceptos

- **El espectrograma.** Herramienta: [STFT y espectrograma](T5-stft.html).
- **El principio de incertidumbre.** Herramienta: [Resolución en tiempo y en frecuencia](T5-resolucion-tiempo-frecuencia.html).
- **La versión discreta.** Escalas diádicas y una base ortonormal. Herramienta: [DWT y análisis multirresolución](T5-dwt-multirresolucion.html).
- **Correlación (Tema 6).** W(a, b) es la correlación de x con la wavelet escalada. Herramienta: [Estimación de un retardo por correlación](T6-retardo-correlacion.html).
