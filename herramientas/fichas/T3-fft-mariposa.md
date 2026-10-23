## Introducción

### El coste de la DFT directa

Calcular X[k] = Σ x[n] W_N^{kn} para las N frecuencias exige N productos complejos por cada una: N² en total. Con N = 1024 son más de un millón. La **FFT** (transformada rápida de Fourier) es un conjunto de algoritmos que calculan exactamente la misma DFT con del orden de N log₂ N operaciones, aprovechando que W_N^{kn} solo toma N valores distintos y es periódica y simétrica.

### Diezmado en el tiempo

Si N es par, se separan las muestras pares, f[m] = x[2m], y las impares, g[m] = x[2m + 1]. Como W_N² = W_{N/2},

> X[k] = F[k] + W_N^{k} G[k],  X[k + N/2] = F[k] − W_N^{k} G[k],  k = 0, …, N/2 − 1,

donde F y G son DFT de N/2 puntos. La DFT de N puntos se reduce a dos de N/2 más N/2 productos por los **factores de giro** W_N^{k}. Cada par de ecuaciones es una **mariposa**: dos entradas a y b, dos salidas a + Wb y a − Wb, y un solo producto complejo.

### Repetir hasta el final

Si N = 2^{ν}, cada DFT de N/2 se vuelve a partir, hasta llegar a DFT de 2 puntos, que son solo una suma y una resta. Quedan **ν = log₂N etapas** de N/2 mariposas:

> (N/2) log₂N productos complejos,

frente a N². Con N = 1024, 5120 frente a 1 048 576. Muchos de esos productos son triviales (por ±1 o ±j).

### El orden de bits invertido

Al separar pares e impares una y otra vez, la entrada acaba en un orden extraño: la posición i contiene x[n] con n igual a i escrito en binario al revés. Con N = 8, el orden es 0, 4, 2, 6, 1, 5, 3, 7. La salida sale en orden natural. Ordenar la entrada así permite hacer todo el cálculo **en el sitio**, sobre el mismo vector.

### Otras variantes

El **diezmado en frecuencia** separa la salida en k pares e impares y deja el orden invertido en la salida. Hay algoritmos en base 4, de base mixta para N que no son potencia de 2 y otros, pero todos tienen un coste del orden de N log N. Los programas de cálculo (`fft` de NumPy o de Matlab) eligen el mejor según N.

## Guía de uso

- **Entrada x[n]** elige una secuencia de 8 muestras.
- **Etapa resaltada** marca en rojo una etapa del grafo: las mariposas que la forman y los valores de entrada y de salida.
- En el grafo, cada columna es un vector de 8 valores: la entrada en orden de bits invertido, después de la etapa 1 (DFT de 2 puntos), de la etapa 2 (DFT de 4) y de la etapa 3 (la DFT de 8). En rojo, los factores de giro W₈^{e} de cada mariposa.
- A la derecha, el número de productos de la DFT directa y de la FFT frente a N, en escala logarítmica.

## Ejercicios

**1. Bits invertidos.** Con la rampa n, lee la primera columna. ¿En qué orden están las muestras? Explica por qué x[3] ocupa la posición 6.

<details><summary>Solución</summary>
0, 4, 2, 6, 1, 5, 3, 7. 3 en binario con 3 bits es 011 y, al revés, 110, que es 6. Las posiciones 0 a 3 tienen las muestras pares y las 4 a 7, las impares, y dentro de cada mitad se repite la separación.
</details>

**2. Una constante.** Con la entrada constante, anota los valores de cada etapa. ¿Qué hacen las mariposas?

<details><summary>Solución</summary>
Etapa 1: (2, 0, 2, 0, 2, 0, 2, 0); etapa 2: (4, 0, 0, 0, 4, 0, 0, 0); etapa 3: X = (8, 0, 0, 0, 0, 0, 0, 0). Cada mariposa suma y resta: las sumas acumulan la componente continua y las restas se anulan.
</details>

**3. Un impulso desplazado.** Con δ[n − 1], sigue el valor 1 por el grafo. ¿Por qué la salida es X[k] = W₈^{k}?

<details><summary>Solución</summary>
x[1] está en la posición 4. En las etapas 1 y 2 solo se suma o se resta sin factores de giro no triviales y llega a las posiciones 4 a 7 con valor 1. En la etapa 3, cada mariposa multiplica por W₈^{j} y da W₈^{j} y −W₈^{j} = W₈^{j + 4}. Es la propiedad del desplazamiento: módulo 1 y fase lineal.
</details>

**4. El ejercicio 15 de la hoja, en grande.** Con el coseno cos(2πn/8), ¿qué vale X[k]? Mira la etapa 2: ¿qué DFT de 4 puntos son las dos mitades?

<details><summary>Solución</summary>
X[1] = X[7] = 4 y el resto, cero. La mitad de arriba es la DFT de 4 puntos de las muestras pares, cos(πm/2) = (1, 0, −1, 0): (0, 2, 0, 2). La de abajo es la de las impares, (0,71; −0,71; −0,71; 0,71): (0; 1,41 + 1,41j; 0; 1,41 − 1,41j). La etapa 3 las combina con W₈^{k}. En la hoja, con N = 4, el mismo procedimiento da (8, −3 − 3j, 2, −3 + 3j) para x = (1, 3, 4, 0).
</details>

**5. El ejercicio 14 de la hoja: cuánto se gana.** ¿Cuántos productos no triviales hay en la FFT de 8 puntos? A un nanosegundo por producto, ¿cuánto tarda una DFT de 4096 puntos directamente y con la FFT?

<details><summary>Solución</summary>
De los 12 productos, solo los de W₈¹ y W₈³ de la etapa 3 no son triviales: 2 productos, frente a 64 de la DFT directa. Con N = 4096: N² = 1,68·10⁷ productos, 16,8 ms, frente a (N/2)·12 = 24 576, 24,6 µs, unas 680 veces menos.
</details>

## Para profundizar

- [Apuntes del Tema 3](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%20Apuntes.pdf), sección 5 (FFT y convolución rápida): «Coste de la DFT directa», «Diezmado en el tiempo en base 2» y «Otras variantes».
- [Transparencias T3-04](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%2004%20-%20FFT.pdf), la FFT.
- [Hoja de ejercicios del Tema 3](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%20Ejercicios.pdf), ejercicios 14 y 15, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T3/codigo/python/fft_radix2.py` y su versión en Matlab, una FFT en base 2 con inversión de bits, etapa a etapa.
- A. V. Oppenheim y R. W. Schafer, *Discrete-Time Signal Processing*, 3.ª ed., Pearson, 2010, apartados 9.1 a 9.3.
- J. W. Cooley y J. W. Tukey, «An algorithm for the machine calculation of complex Fourier series», *Mathematics of Computation*, 19(90), 1965.

## Relación con otros conceptos

- **DFT.** La FFT calcula exactamente la misma transformada. Herramientas: [Editor de la DFT](T3-editor-dft.html) y [DFT, fuga y relleno con ceros](T3-dft.html).
- **Propiedades de la DFT.** El desplazamiento y la periodicidad de W_N son las que usa el algoritmo. Herramienta: [Propiedades de la DFT](T3-propiedades-dft.html).
- **Convolución rápida.** Herramienta: [Convolución por bloques](T3-solapamiento-suma.html).
- **Diezmado (Tema 2).** Separar pares e impares es diezmar por 2. Herramienta: [Diezmado e interpolación](T2-diezmado-interpolacion.html).
