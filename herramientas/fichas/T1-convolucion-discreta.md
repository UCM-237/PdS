## Introducción

### La suma de convolución

En tiempo discreto, cualquier secuencia es una suma de impulsos desplazados: x[n] = Σ_k x[k] δ[n − k]. Si un sistema es lineal e invariante (LTI) y su respuesta al impulso es h[n], cada término x[k]δ[n − k] produce x[k]h[n − k] y la salida es

> y[n] = (x ∗ h)[n] = Σ_k x[k] h[n − k].

Es la misma idea que en continuo, pero aquí la operación se puede hacer a mano con exactitud y es la que ejecuta un procesador: cada muestra de salida es una suma de productos.

### Cómo se calcula

Para cada n:

1. Se escribe x[k] en función de k.
2. Se invierte h, h[−k], y se desplaza n muestras: h[n − k].
3. Se multiplican las dos secuencias muestra a muestra.
4. Se suman los productos: el resultado es y[n].

Una forma equivalente, cómoda para secuencias cortas, es la «multiplicación de polinomios»: los coeficientes de (Σ x[k] z^{−k})(Σ h[k] z^{−k}) son las muestras de y. Otra es sumar copias de h desplazadas y escaladas por cada muestra de x.

### Longitud y propiedades

- Si x tiene L muestras y h tiene P, y tiene **L + P − 1** muestras, y empieza en la suma de los índices iniciales.
- Es conmutativa, asociativa y distributiva; δ[n] es el elemento neutro y δ[n − n₀] desplaza.
- Convolucionar con u[n] acumula: y[n] = Σ_{k≤n} x[k].
- Un sistema con h de duración finita es un **FIR**; cada salida usa un número finito de entradas.

### Por qué importa

Toda la teoría de filtros digitales parte de aquí: un filtro FIR es exactamente esta suma, y la DFT y la FFT del Tema 3 sirven para calcularla más deprisa cuando las secuencias son largas.

## Guía de uso

- **Señal x[n]** y **Respuesta al impulso h[n]** se eligen entre pulsos de 4 y 6 muestras, una rampa 1, 2, 3, 4, la exponencial 0,8ⁿu[n] (truncada en 25 muestras), δ[n] + δ[n − 3], una media móvil de 3 muestras y la diferencia δ[n] − δ[n − 1].
- **n** elige la muestra de salida que se calcula.
- Arriba, x[k] y h[n − k]; en medio, su producto; abajo, la salida completa con la muestra y[n] marcada. El recuadro escribe la suma de productos que da y[n].

## Ejercicios

**1. Dos pulsos de 4 muestras.** Predice y[n] para dos pulsos de 4 muestras: longitud, forma y valor máximo. Compruébalo.

<details><summary>Solución</summary>
y = {1, 2, 3, 4, 3, 2, 1} para n = 0, …, 6: 4 + 4 − 1 = 7 muestras, triangular, con máximo 4 en n = 3, cuando los pulsos se solapan por completo.
</details>

**2. Ecos.** Con x la rampa 1, 2, 3, 4 y h = δ[n] + δ[n − 3], calcula y[n].

<details><summary>Solución</summary>
y[n] = x[n] + x[n − 3] = {1, 2, 3, 5, 2, 3, 4}. La muestra n = 3 suma x[3] = 4 y x[0] = 1. Cada impulso de h coloca una copia de x.
</details>

**3. Suavizar.** Con x el pulso de 6 muestras y h la media móvil de 3, ¿qué valores toma y[n]? ¿Qué le pasa a los bordes del pulso?

<details><summary>Solución</summary>
y = {1/3, 2/3, 1, 1, 1, 1, 2/3, 1/3} para n = 0, …, 7 (6 + 3 − 1 = 8 muestras). Los saltos del pulso se convierten en rampas de 3 muestras: la media móvil es un paso bajo.
</details>

**4. Detector de bordes.** Con x el pulso de 4 muestras y h = δ[n] − δ[n − 1], ¿qué sale? ¿Qué operación hace este h?

<details><summary>Solución</summary>
y[n] = x[n] − x[n − 1] = δ[n] − δ[n − 4]: un 1 donde el pulso empieza y un −1 donde acaba. Es la primera diferencia, la versión discreta de la derivada; deja pasar los cambios y anula lo constante.
</details>

**5. El ejercicio 6 c de la hoja, truncado.** La hoja calcula u[n] ∗ aⁿu[n] = (1 − a^{n+1})/(1 − a). Con x el pulso de 6 muestras y h = 0,8ⁿu[n], calcula y[5] y compáralo con la fórmula de la hoja para a = 0,8.

<details><summary>Solución</summary>
Para n ≤ 5 el pulso se comporta como un escalón: y[n] = (1 − 0,8^{n+1})/0,2, y y[5] = (1 − 0,8⁶)/0,2 ≈ 3,69. Con un escalón de verdad la salida seguiría subiendo hasta 1/(1 − 0,8) = 5; con el pulso, a partir de n = 6 decae como 0,8ⁿ.
</details>

## Para profundizar

- [Apuntes del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Apuntes.pdf), sección 5 (Convolución) y sección 9, «Sistemas FIR e IIR».
- [Transparencias T1-02](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%2002%20-%20Operaciones.pdf), «Convolución discreta: ejemplo».
- [Hoja de ejercicios del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios.pdf), ejercicio 6, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T1/codigo/python/convolucion.py` y su versión en Matlab (comprueba los resultados con `np.convolve` o `conv`).
- A. V. Oppenheim, A. S. Willsky y S. H. Nawab, *Signals and Systems*, 2.ª ed., Prentice Hall, 1997, apartado 2.1.
- J. H. McClellan, R. W. Schafer y M. A. Yoder, *DSP First*, 2.ª ed., Pearson, 2016, capítulo 5.

## Relación con otros conceptos

- **Convolución continua.** Herramienta: [Convolución continua](T1-convolucion-continua.html).
- **Filtros FIR (Tema 4).** Un FIR calcula exactamente esta suma; la media móvil es el más sencillo. Herramienta: [Filtro de media móvil](T4-media-movil.html).
- **Convolución circular (Tema 3).** El producto de DFT da una convolución circular, que coincide con la lineal si se rellena con ceros. Herramienta: [Convolución circular](T3-convolucion-circular.html).
- **Convolución por bloques (Tema 3).** Para señales largas, se trocea la entrada. Herramienta: [Convolución por bloques](T3-solapamiento-suma.html).
- **Respuesta en frecuencia.** Si x es una sinusoide, la suma de convolución se reduce a multiplicar por H(e^{jΩ}). Herramienta: [Respuesta de un sistema LTI discreto](T1-respuesta-lti-discreta.html).
