## Introducción

### Filtrar una señal que no se acaba

La convolución circular permite filtrar con la FFT, pero exige tener toda la señal y una FFT de longitud mayor que la salida. Con una señal muy larga, o en tiempo real, eso no es posible: se **trocea la entrada en bloques**, se filtra cada uno con FFT de tamaño fijo y se recompone la salida. Como el sistema es lineal e invariante, la salida total es la suma de las salidas de los bloques, bien colocadas. Hay dos formas de hacerlo.

### Solapamiento-suma

Se divide x[n] en bloques de L muestras que no se solapan, x_b[n] = x[n + bL] para 0 ≤ n < L.

1. Cada bloque se rellena con ceros hasta N = L + P − 1 y se convoluciona con h[n] (P muestras) mediante FFT de N puntos. Como N basta, la circular es la lineal: L + P − 1 muestras.
2. La salida de cada bloque se coloca a partir de bL. Las P − 1 últimas muestras de un bloque se solapan con las primeras del siguiente y se **suman**.

### Solapamiento-almacenamiento

Se toman bloques de N = L + P − 1 muestras que se solapan P − 1 con el anterior.

1. Cada bloque se convoluciona circularmente con h[n] en N puntos, sin rellenar.
2. Las P − 1 primeras muestras de cada salida tienen aliasing temporal y se **descartan**. Las L restantes son correctas y se **guardan** una tras otra.

Este método no necesita sumas de solapamiento, pero hay que guardar las P − 1 últimas muestras de entrada de cada bloque.

### Coste

Por bloque se hacen una FFT de x, un producto por H[k] (calculado una vez) y una IFFT: unos N log₂N + N productos complejos. Repartido entre L muestras nuevas, el coste por muestra crece como log₂N, mientras que la convolución directa cuesta P productos por muestra. Compensa cuando P es grande. N se elige como potencia de 2 y L = N − P + 1; si L es mucho mayor que P, se desperdicia poco. El precio es un **retardo** de al menos un bloque.

## Guía de uso

- **Método** elige solapamiento-suma o solapamiento-almacenamiento.
- **Respuesta al impulso** elige h[n]: media móvil, exponencial o diferenciador. **P** es su longitud.
- **L** es el número de muestras nuevas de cada bloque. La entrada tiene 80 muestras.
- Arriba, x[n] con los bloques marcados con barras de colores, y h[n]. En medio, las salidas parciales; en solapamiento-almacenamiento, en trazo discontinuo y claro, las muestras descartadas. Abajo, la salida y[n] por bloques (puntos) y la convolución directa (línea).
- El recuadro da N, el tamaño de FFT, el número de bloques, la diferencia con la convolución directa y el coste.

## Ejercicios

**1. Dónde se suman.** Con solapamiento-suma, la media móvil, L = 16 y P = 6, ¿cuántas muestras tiene cada salida parcial? ¿Cuántas se solapan entre bloques vecinos? ¿Cuántos bloques hay?

<details><summary>Solución</summary>
Cada salida tiene L + P − 1 = 21 muestras, y las P − 1 = 5 últimas de un bloque se suman con las 5 primeras del siguiente. Con 80 muestras hay 80/16 = 5 bloques. La FFT necesaria es de 32 puntos.
</details>

**2. Qué se descarta.** Cambia a solapamiento-almacenamiento con los mismos valores. ¿Cuántas muestras tiene cada bloque de entrada? ¿Cuántas se descartan de cada salida y por qué?

<details><summary>Solución</summary>
Cada bloque tiene N = 21 muestras y repite las 5 últimas del anterior; el primero empieza con 5 ceros. De cada convolución circular se descartan las P − 1 = 5 primeras, que reciben la cola plegada; las 16 restantes son exactamente la convolución lineal. Hacen falta 6 bloques para llegar al final de la salida, que tiene 85 muestras.
</details>

**3. Aprovechar la FFT.** Con P = 6 y L = 16, la FFT es de 32 puntos pero N = 21. ¿Qué L aprovecha toda la FFT? ¿Cuánto baja el coste por muestra?

<details><summary>Solución</summary>
L = 32 − 6 + 1 = 27, y N = 32. En solapamiento-suma, el coste baja de unos 13 a unos 8 productos complejos por muestra, porque cada FFT da 27 muestras nuevas en vez de 16. Es el criterio del ejercicio 16 de la hoja: L = N − M + 1.
</details>

**4. Bloques demasiado cortos.** Con P = 16, compara L = 4 y L = 40. ¿Cuántos bloques y qué coste hay en cada caso? ¿Cuál es el coste de la convolución directa?

<details><summary>Solución</summary>
Con L = 4, N = 19 y FFT de 32: 20 bloques y unos 49 productos complejos por muestra, mucho más que los 16 reales de la directa. Con L = 40, N = 55 y FFT de 64: 2 bloques y unos 14 por muestra. Con bloques cortos, casi todo el trabajo de cada FFT se gasta en las P − 1 muestras de cola.
</details>

**5. El ejercicio 16 de la hoja.** Un sistema de audio a 48 kHz filtra con un FIR de M = 101 coeficientes con FFT de 1024 puntos. ¿Qué L se usa? ¿Cuántos bloques por segundo? ¿Qué retardo hay?

<details><summary>Solución</summary>
L = 1024 − 101 + 1 = 924 muestras, unos 52 bloques por segundo. Cada bloque cuesta unos 2·512·10 + 1024 = 11 264 productos complejos, unos 12 por muestra, frente a 101 productos reales de la directa. El retardo es de al menos un bloque, 924/48 000 ≈ 19 ms, más el tiempo de cálculo.
</details>

## Para profundizar

- [Apuntes del Tema 3](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%20Apuntes.pdf), sección 5 (FFT y convolución rápida), «Convolución rápida» y «Señales largas: procesado por bloques».
- [Transparencias T3-04](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%2004%20-%20FFT.pdf), convolución rápida.
- [Hoja de ejercicios del Tema 3](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%20Ejercicios.pdf), ejercicios 8 y 16, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T3/codigo/python/solapamiento_suma.py` y su versión en Matlab.
- A. V. Oppenheim y R. W. Schafer, *Discrete-Time Signal Processing*, 3.ª ed., Pearson, 2010, apartado 8.7.3.

## Relación con otros conceptos

- **Convolución circular.** Por qué se rellena con ceros o se descartan P − 1 muestras. Herramienta: [Convolución circular](T3-convolucion-circular.html).
- **FFT.** El coste de cada bloque. Herramienta: [FFT: el grafo de mariposas](T3-fft-mariposa.html).
- **Linealidad e invarianza (Tema 1).** Lo que permite filtrar por trozos y sumar. Herramienta: [Propiedades de los sistemas](T1-propiedades-sistemas.html).
- **Filtros FIR (Tema 4).** Un FIR de muchos coeficientes se aplica así. Herramienta: [Diseño FIR por ventanas](T4-fir-ventana.html).
