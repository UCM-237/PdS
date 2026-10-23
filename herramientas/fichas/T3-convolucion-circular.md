## Introducción

### Multiplicar DFT es convolucionar circularmente

En la DTFT, multiplicar espectros equivale a convolucionar secuencias. En la DFT ocurre lo mismo, pero con la convolución **circular** de N puntos:

> y[n] = (x ⊛ h)[n] = Σ_{m=0}^{N−1} x[m] h[((n − m))_N],  0 ≤ n < N  ⟷  Y[k] = X[k] H[k].

Es la convolución de siempre, pero h se invierte y se desplaza módulo N: al girar, las muestras que salen por la derecha vuelven a entrar por la izquierda, como si las dos secuencias estuvieran dibujadas en una circunferencia.

### Circular frente a lineal

Si x tiene L muestras y h tiene P, la convolución lineal x ∗ h tiene L + P − 1. La circular de N puntos es la lineal **plegada** con periodo N:

> (x ⊛ h)[n] = Σ_r (x ∗ h)[n + rN],  0 ≤ n < N.

Es el aliasing temporal de la extensión periódica: Y[k] son N muestras de la DTFT de x ∗ h, y si N es menor que su longitud, las copias se solapan.

- Si **N ≥ L + P − 1**, no hay solapamiento y la convolución circular coincide con la lineal. Basta rellenar x y h con ceros hasta N.
- Si **N < L + P − 1**, las últimas L + P − 1 − N muestras de la lineal se suman a las primeras.

### Por qué importa

Esta es la base del **filtrado con la FFT**: para calcular x ∗ h se rellenan las dos con ceros hasta N ≥ L + P − 1 (normalmente la siguiente potencia de 2), se multiplican sus FFT y se calcula la IFFT. Con secuencias largas es mucho más rápido que la suma directa. Si N = L, solo están mal las P − 1 primeras muestras, y esa idea da el método de **solapamiento-almacenamiento**.

## Guía de uso

- **x[n]** y **h[n]** se eligen entre varias secuencias cortas.
- **N** es el número de puntos de la convolución circular. Si es menor que una de las secuencias, esta se pliega antes, como haría la DFT de N puntos.
- **n** es el instante que se está calculando.
- Arriba, x[k] y h[((n − k))_N] en 0 ≤ k < N: la suma de sus productos es la muestra n de la salida.
- Abajo, la circular en azul, la lineal en gris y, en naranja, la muestra n.

## Ejercicios

**1. Mirar la circunferencia.** Con la rampa 1…5, el pulso de 4 y N = 8, recorre n de 0 a 7. ¿Cómo se mueve h[((n − k))_N]? ¿Coincide la circular con la lineal?

<details><summary>Solución</summary>
Con n = 0, h invertido ocupa k = 0 y k = 5, 6, 7: las tres muestras que en la convolución lineal quedarían en k negativo aparecen por la derecha. Al aumentar n, el pulso gira hacia la derecha. Como N = 8 = L + P − 1, la circular coincide con la lineal: (1, 3, 6, 10, 14, 12, 9, 5).
</details>

**2. Plegado.** Con las mismas secuencias, baja N a 6 y luego a 5. ¿Qué sale? Calcúlalo sumando muestras de la lineal.

<details><summary>Solución</summary>
Con N = 6, y_c[n] = y[n] + y[n + 6]: (1 + 9, 3 + 5, 6, 10, 14, 12) = (10, 8, 6, 10, 14, 12). Con N = 5, y_c[n] = y[n] + y[n + 5]: (1 + 12, 3 + 9, 6 + 5, 10, 14) = (13, 12, 11, 10, 14).
</details>

**3. El ejercicio 8 c de la hoja: qué muestras se salvan.** En el caso N = 5 = L, ¿qué muestras de la circular coinciden con la lineal? ¿Cuántas están mal, en general, cuando N = L?

<details><summary>Solución</summary>
Las dos últimas, 10 y 14: las tres primeras reciben la cola de la lineal. Con N = L, la cola tiene P − 1 muestras y caen sobre las P − 1 primeras: n = 0, …, P − 2 son incorrectas y el resto, correctas. En la hoja, con L = 100 y M = 30, son correctas de n = 29 a 99.
</details>

**4. El ejercicio 7 de la hoja, con una diferencia.** Con la rampa 1…5 y h = (1, −1), calcula la convolución lineal y la circular con N = 5. ¿Qué N hace falta para que coincidan?

<details><summary>Solución</summary>
La lineal es la diferencia x[n] − x[n − 1] = (1, 1, 1, 1, 1, −5). Con N = 5, la última muestra se suma a la primera: (−4, 1, 1, 1, 1). Hace falta N ≥ 5 + 2 − 1 = 6. En la hoja, con x = (1, 2, 3, 4) y h = (1, 1), la circular de 4 puntos da (5, 3, 5, 7) y hace falta N ≥ 5.
</details>

**5. Una secuencia más larga que N.** Pon x = pulso de 6, h = 1, 2, 1 y N = 4. ¿Qué secuencia de 4 puntos se usa como x? ¿Cuánto vale la suma de la salida circular? ¿Y la de la lineal?

<details><summary>Solución</summary>
El pulso se pliega: (1 + 1, 1 + 1, 1, 1) = (2, 2, 1, 1). La suma de la salida es Σx·Σh = 6·4 = 24 en los dos casos, porque Y[0] = X[0]H[0] y el plegado no cambia la suma: es la DFT en k = 0.
</details>

## Para profundizar

- [Apuntes del Tema 3](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%20Apuntes.pdf), sección 3, «Convolución circular» y «Convolución circular y convolución lineal».
- [Transparencias T3-02](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%2002%20-%20Propiedades.pdf), convolución circular.
- [Hoja de ejercicios del Tema 3](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%20Ejercicios.pdf), ejercicios 7 y 8, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T3/codigo/python/conv_circular.py` y su versión en Matlab.
- A. V. Oppenheim y R. W. Schafer, *Discrete-Time Signal Processing*, 3.ª ed., Pearson, 2010, apartados 8.6.5 y 8.7.

## Relación con otros conceptos

- **Convolución discreta (Tema 1).** La convolución lineal, paso a paso. Herramienta: [Convolución discreta](T1-convolucion-discreta.html).
- **Extensión periódica.** El plegado es el aliasing temporal. Herramienta: [Extensión periódica](T3-extension-periodica.html).
- **Convolución por bloques.** Solapamiento-suma y solapamiento-almacenamiento. Herramienta: [Convolución por bloques](T3-solapamiento-suma.html).
- **FFT.** Lo que hace rentable filtrar en frecuencia. Herramienta: [FFT: el grafo de mariposas](T3-fft-mariposa.html).
- **Filtros FIR (Tema 4).** Un FIR largo se aplica con FFT. Herramienta: [FIR por el método de ventanas](T4-fir-ventana.html).
