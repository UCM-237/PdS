## Introducción

### Los coeficientes también se redondean

En un procesador de coma fija, o en un circuito, los coeficientes de la ecuación en diferencias se guardan con B bits. Redondearlos cambia el filtro: los polos y ceros que se implementan no son los diseñados. En un FIR solo se deforma un poco la respuesta; en un IIR, un polo que se mueve hacia fuera de la circunferencia puede volver **inestable** el filtro.

### Por qué la forma directa es frágil

En **forma directa** se implementa H(z) = B(z)/A(z) con los coeficientes a_k del polinomio completo A(z) = Π(1 − p_k z^{−1}). La sensibilidad de un polo a los coeficientes es

> ∂p_i/∂a_k = p_i^{N−k} / Π_{j≠i} (p_i − p_j).

Si los polos están **muy juntos**, el denominador es pequeño y un error mínimo en a_k mueve mucho p_i. Es justo lo que ocurre en un paso bajo estrecho de orden alto: todos los polos se agrupan cerca de z = 1. Además, los a_k crecen mucho (son coeficientes binomiales grandes) y, para representarlos, el paso de cuantificación tiene que ser mayor.

### Secciones de orden 2

La solución es factorizar H(z) en **secciones de segundo orden** (SOS, biquads) en cascada, cada una con un par de polos conjugados:

> H(z) = Π_k (b_{0k} + b_{1k}z^{−1} + b_{2k}z^{−2})/(1 + a_{1k}z^{−1} + a_{2k}z^{−2}).

Cada par depende solo de dos coeficientes, a_1 = −2 Re p y a_2 = |p|², acotados por 2 y 1, y la sensibilidad no depende de los demás polos. Con pocos bits, la cascada sigue siendo estable. Es la estructura que usan `sosfilt` (SciPy) y `sosfilt`/`dfilt` (Matlab), y la recomendada para cualquier IIR de orden mayor que 2.

### Otros efectos de la longitud finita

Además de los coeficientes, se redondean los resultados de cada producto (**ruido de redondeo**, que el filtro amplifica más cuanto más cerca están sus polos de la circunferencia), las sumas pueden **desbordar** y pueden aparecer **ciclos límite**, oscilaciones pequeñas que no se extinguen. Se estudian con el mismo modelo de ruido de cuantificación del Tema 2.

## Guía de uso

- El filtro es un Butterworth digital de **orden N** y corte **Ωc/π**. **B** es el número de bits de cada coeficiente.
- En la forma directa, el paso de cuantificación se ajusta a la potencia de 2 que cubre el mayor |a_k|. En las secciones, el paso es fijo, 2/2^{B−1}.
- A la izquierda, los polos ideales, los de la forma directa cuantizada y los de las secciones. A la derecha, |H| del filtro ideal y de las dos implementaciones. El numerador no se cuantifica, para ver solo el efecto sobre los polos.
- El recuadro da el mayor |a_k|, el paso, la estabilidad de cada forma, el radio máximo de los polos y su desplazamiento.

## Ejercicios

**1. Forma directa inestable.** Con los valores de partida (N = 8, Ωc/π = 0,1, B = 12), ¿qué pasa con la forma directa? ¿Cuánto vale el mayor |a_k|? ¿Y las secciones?

<details><summary>Solución</summary>
La forma directa es inestable: algún polo sale a un radio de 1,3 o más. Los a_k llegan a unos 30, así que el paso es 32/2^{11} ≈ 0,016, demasiado grueso para polos tan juntos. Con secciones, los polos apenas se mueven (unas milésimas) y el filtro es estable, con un radio máximo de 0,94.
</details>

**2. Cuántos bits.** Con N = 8 y Ωc/π = 0,1, sube B. ¿A partir de cuántos bits es estable la forma directa? ¿Y la cascada, bajando B?

<details><summary>Solución</summary>
La forma directa necesita unos 21 bits; la cascada es estable desde unos 6 bits. Es una diferencia de 15 bits por coeficiente, y con menos de 21 bits el filtro en forma directa simplemente no funciona.
</details>

**3. El orden.** Con Ωc/π = 0,1 y B = 12, compara N = 4, 6, 8 y 12. ¿Cómo cambia el mayor |a_k|? ¿Con cuáles es estable la forma directa?

<details><summary>Solución</summary>
El mayor |a_k| crece muy deprisa: unos 4, 10, 30 y 270. Con N = 4 la forma directa es estable con 12 bits (le bastan unos 10); con 6, 8 y 12 no. Con N = 12 no lo es ni con 24 bits. La cascada es estable en todos los casos.
</details>

**4. La anchura de banda.** Con N = 8 y B = 12, compara Ωc/π = 0,05, 0,1 y 0,2. ¿Por qué es más difícil el filtro más estrecho?

<details><summary>Solución</summary>
Cuanto más estrecho, más cerca de z = 1 y más juntos están los polos, y más sensibles son. Con 0,2 la forma directa es casi estable con 12 bits (radio próximo a 1, necesita unos 13); con 0,05 se desestabiliza mucho más. Los filtros estrechos a fs alta (por ejemplo, 50 Hz a 48 kHz) son los más delicados.
</details>

**5. El ruido de cuantificación (Tema 2).** Con 16 bits, el paso relativo es 2^{−15} ≈ 3·10^{−5}. Si el error de cada coeficiente es uniforme en ±Δ/2, ¿qué desviación típica tiene? ¿Por qué, aun así, puede mover un polo mucho más?

<details><summary>Solución</summary>
Δ/√12 ≈ 9·10^{−6} relativo al fondo de escala. Pero el desplazamiento del polo es ese error multiplicado por la sensibilidad, 1/Π|p_i − p_j|, que para este filtro (8 polos separados menos de 0,1) es del orden de 10^{3} a 10^{4}: un error de 10^{−5} en un coeficiente mueve un polo del orden de 0,1, lo bastante para sacarlo de la circunferencia. En una sección de orden 2 solo hay un factor, p − p*, que no es pequeño.
</details>

## Para profundizar

- [Apuntes del Tema 4](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Apuntes.pdf), sección 3 (Filtros IIR), «Implementación».
- [Transparencias T4-03](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%2003%20-%20Filtros%20IIR.pdf), estructuras de realización.
- A. V. Oppenheim y R. W. Schafer, *Discrete-Time Signal Processing*, 3.ª ed., Pearson, 2010, apartados 6.3, 6.8 y 6.9.
- L. B. Jackson, *Digital Filters and Signal Processing*, 3.ª ed., Kluwer, 1996, capítulo 11.

## Relación con otros conceptos

- **Cuantificación (Tema 2).** El mismo redondeo, ahora en los coeficientes. Herramienta: [Cuantificación y SQNR](T2-cuantificacion.html).
- **Polos y estabilidad.** Herramienta: [Polos y ceros en el plano z](T4-polos-ceros-z.html).
- **Diseño IIR.** El Butterworth digital por la bilineal. Herramienta: [Discretización de filtros IIR](T4-discretizacion-iir.html).
- **Estabilidad (Tema 1).** Herramienta: [Región de convergencia](T1-region-convergencia.html).
