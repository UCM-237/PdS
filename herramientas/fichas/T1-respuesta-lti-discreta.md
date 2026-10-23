## Introducción

### La respuesta en frecuencia discreta

Si la entrada de un sistema LTI discreto es e^{jΩ₀n}, la salida es H(e^{jΩ₀}) e^{jΩ₀n}, con

> H(e^{jΩ}) = Σ_n h[n] e^{−jΩn},

la DTFT de la respuesta al impulso o, si el sistema tiene función de transferencia, H(z) evaluada en z = e^{jΩ}. Para un sistema real, la entrada cos(Ω₀n) sale como |H(e^{jΩ₀})| cos(Ω₀n + ∠H(e^{jΩ₀})), una vez pasado el **transitorio** que aparece al conectar la entrada en n = 0.

### Diferencias con el caso continuo

- H(e^{jΩ}) es **periódica de periodo 2π**, porque las frecuencias discretas lo son. Para un sistema real, |H| es par y la fase impar, así que basta dibujarla en [0, π].
- Ω = 0 es la frecuencia más baja (la continua) y Ω = π la más alta, la de (−1)ⁿ. Un paso bajo discreto deja pasar cerca de Ω = 0 y atenúa cerca de Ω = π.

### Tres sistemas de ejemplo

- **Media móvil de L muestras**, y[n] = (1/L) Σ_{k=0}^{L−1} x[n − k]. Es un FIR paso bajo:
  > |H(e^{jΩ})| = |sin(ΩL/2)/(L sin(Ω/2))|,
  con ceros en los múltiplos de 2π/L y un retardo de (L − 1)/2 muestras. El transitorio dura L − 1 muestras.
- **Primer orden**, y[n] = a y[n − 1] + (1 − a) x[n], con H(z) = (1 − a)/(1 − a z^{−1}). Es un IIR con un polo en z = a. Con 0 < a < 1 es un paso bajo: |H(1)| = 1 y |H(−1)| = (1 − a)/(1 + a). Cuanto más cerca de 1 está a, más estrecho es y más largo el transitorio (unas 1/(1 − a) muestras).
- **Diferencia**, y[n] = x[n] − x[n − 1], con |H| = 2|sin(Ω/2)|. Es un paso alto que anula la continua: la versión discreta de la derivada.

## Guía de uso

- **Sistema** elige la media móvil, el de primer orden o la diferencia.
- **Ω₀** es la frecuencia de la entrada cos(Ω₀n), entre 0 y π.
- **L** y **a** son los parámetros de la media móvil y del primer orden.
- Arriba, el módulo y la fase de H(e^{jΩ}) en [0, π], con Ω₀ marcada. Abajo, la entrada y la salida calculada con la ecuación en diferencias desde n = 0, así que se ve el transitorio.
- El recuadro da |H| y ∠H en Ω₀.

## Ejercicios

**1. Un cero de la media móvil.** Con la media móvil de L = 4 muestras, ¿para qué Ω₀ entre 0 y π la salida es nula? Compruébalo y fíjate en las primeras muestras.

<details><summary>Solución</summary>
Los ceros están en Ω = 2πk/4: π/2 y π. Con Ω₀ = π/2 ≈ 1,57, cuatro muestras consecutivas de cos(πn/2) suman cero, así que la salida es nula a partir de n = 3. Las tres primeras no lo son: es el transitorio, mientras el promedio aún incluye ceros anteriores a n = 0.
</details>

**2. La diferencia.** Con el sistema de diferencia, ¿cuánto vale |H| en Ω₀ = π/3 y en Ω₀ = π? ¿Y en Ω₀ = 0?

<details><summary>Solución</summary>
|H| = 2|sin(Ω/2)|: 1 en π/3, 2 en π y 0 en Ω = 0. Es un paso alto: la componente continua desaparece y (−1)ⁿ sale duplicada.
</details>

**3. Primer orden paso bajo.** Con a = 0,8, calcula |H| en Ω = 0 y Ω = π. ¿Cuánto tarda la salida en llegar al régimen permanente con Ω₀ = 0,5?

<details><summary>Solución</summary>
|H(1)| = 1 y |H(−1)| = 0,2/1,8 ≈ 0,11. El transitorio decae como 0,8ⁿ: a las 10 muestras queda un 11 % y a las 20, un 1 %. Con a = 0,95 tardaría cuatro veces más.
</details>

**4. Un polo en el semieje negativo.** Pon a = −0,8 en el sistema de primer orden. ¿Qué tipo de filtro es? ¿Cuánto vale |H(e^{jπ})|?

<details><summary>Solución</summary>
Con el polo en z = −0,8, cerca de Ω = π, |H| crece con la frecuencia: |H(1)| = 1,8/1,8 = 1 y |H(−1)| = 1,8/0,2 = 9. Realza las frecuencias altas. La ganancia (1 − a) normaliza la continua, no la de alta frecuencia.
</details>

**5. Comparar dos paso bajos.** Busca un a para el primer orden que tenga, como la media móvil de L = 4, ganancia 1/√2 en la misma frecuencia. ¿Qué diferencias ves en la fase y en el transitorio?

<details><summary>Solución</summary>
La media móvil de 4 tiene |H| = 0,707 en Ω ≈ 0,72. El primer orden da 0,707 en esa frecuencia con a ≈ 0,50. La media móvil tiene fase lineal (retardo constante de 1,5 muestras) y un transitorio de 3 muestras; el primer orden tiene fase no lineal y un transitorio que no termina nunca del todo, aunque aquí es muy corto. Además, el primer orden no tiene ceros: nunca anula ninguna frecuencia.
</details>

## Para profundizar

- [Apuntes del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Apuntes.pdf), sección 8, «Autofunciones y respuesta en frecuencia», y sección 9, «Sistemas discretos» y «Sistemas FIR e IIR».
- [Transparencias T1-03](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%2003%20-%20Sistemas.pdf), sistemas discretos y respuesta en frecuencia.
- [Hoja de ejercicios del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios.pdf), ejercicios de sistemas (10 a 16), y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T1/codigo/python/lti_discreto.py` y su versión en Matlab.
- A. V. Oppenheim y R. W. Schafer, *Discrete-Time Signal Processing*, 3.ª ed., Pearson, 2010, apartados 2.6 y 2.7.
- J. H. McClellan, R. W. Schafer y M. A. Yoder, *DSP First*, 2.ª ed., Pearson, 2016, capítulo 6.

## Relación con otros conceptos

- **Sistema continuo.** Herramienta: [Respuesta de un sistema LTI continuo](T1-respuesta-lti-continua.html).
- **Frecuencia discreta.** La periodicidad de H viene de la de Ω. Herramienta: [Exponencial compleja discreta](T1-exponencial-discreta.html).
- **Media móvil (Tema 4).** El mismo filtro, aplicado a una señal con ruido. Herramienta: [Filtro de media móvil](T4-media-movil.html).
- **Polos y ceros en z (Tema 4).** El polo en z = a y los ceros de la media móvil explican la forma de |H|. Herramienta: [Polos y ceros en el plano z](T4-polos-ceros-z.html).
- **Fase lineal (Tema 4).** La media móvil retrasa todas las frecuencias lo mismo; el primer orden, no. Herramienta: [Fase lineal y retardo de grupo](T4-fase-lineal.html).
