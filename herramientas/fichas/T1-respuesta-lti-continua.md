## Introducción

### Las exponenciales son autofunciones

Si la entrada de un sistema LTI continuo con respuesta al impulso h(t) es una exponencial compleja e^{jω₀t}, la salida es

> y(t) = ∫ h(τ) e^{jω₀(t−τ)} dτ = H(jω₀) e^{jω₀t},  con  H(jω) = ∫ h(t) e^{−jωt} dt.

La exponencial sale igual, multiplicada por un número complejo: es una **autofunción** del sistema, y H(jω₀) es su autovalor. La función H(jω) es la **respuesta en frecuencia**: la transformada de Fourier de h(t), o la función de transferencia H(s) evaluada en s = jω.

### Qué le pasa a una sinusoide

Como cos(ω₀t) = ½e^{jω₀t} + ½e^{−jω₀t} y, para un sistema real, H(−jω) = H*(jω), la salida en régimen permanente es

> y(t) = |H(jω₀)| cos(ω₀t + ∠H(jω₀)).

El **módulo** dice cuánto se amplifica o atenúa esa frecuencia, y la **fase**, cuánto se desplaza: un desfase φ equivale a un retardo de −φ/ω₀ segundos. Con una señal cualquiera, cada componente de frecuencia sale escalada y desfasada a su manera; por eso un sistema LTI es un **filtro**.

### Tres sistemas de ejemplo

- **Paso bajo de primer orden**, H(s) = 1/(1 + s/ω_c): deja pasar las frecuencias bajas. En ω = ω_c, |H| = 1/√2 (−3 dB) y la fase es −π/4. Por encima de ω_c, |H| cae 20 dB por década.
- **Paso alto de primer orden**, H(s) = (s/ω_c)/(1 + s/ω_c): lo contrario; atenúa las bajas y adelanta la fase.
- **Segundo orden**, H(s) = ω_n²/(s² + 2ζω_n s + ω_n²): ω_n es la frecuencia natural y ζ el amortiguamiento. Con ζ pequeño hay un pico de resonancia cerca de ω_n, de altura aproximada 1/(2ζ); con ζ ≥ 1/√2 no hay pico.

### Decibelios y escala logarítmica

Es habitual dibujar el módulo en decibelios, 20 log₁₀|H|, frente a log ω (el diagrama de Bode). Así los productos de factores se convierten en sumas y las pendientes se cuentan en dB por década.

## Guía de uso

- **Sistema** elige el paso bajo, el paso alto o el de segundo orden.
- **log₁₀ ω₀** fija la frecuencia de la sinusoide de entrada, entre 0,1 y 100 rad/s.
- **ω_c o ω_n** es la frecuencia de corte de los de primer orden o la natural del de segundo orden, y **ζ** el amortiguamiento de este último.
- Arriba, el módulo y la fase de H(jω) con la frecuencia ω₀ marcada. Abajo, la entrada y la salida en régimen permanente.
- El recuadro da |H(jω₀)|, ∠H(jω₀) y el retardo que corresponde a ese desfase.

## Ejercicios

**1. La frecuencia de corte.** Con el paso bajo, ω_c = 2 rad/s y ω₀ = 2 rad/s (log₁₀ ω₀ ≈ 0,30), ¿cuánto valen |H| y ∠H? ¿Cuánto se retrasa la salida?

<details><summary>Solución</summary>
H(j2) = 1/(1 + j): |H| = 1/√2 ≈ 0,707 (−3 dB) y ∠H = −π/4. El retardo es (π/4)/2 ≈ 0,39 s.
</details>

**2. Una década por encima.** Con el mismo paso bajo, lleva ω₀ a 20 rad/s. ¿Cuánto vale |H| en dB? ¿Y a 200 rad/s, si pudieras?

<details><summary>Solución</summary>
|H(j20)| = 1/√(1 + 100) ≈ 0,0995, unos −20 dB, y la fase se acerca a −π/2. A 200 rad/s serían unos −40 dB: el paso bajo de primer orden cae 20 dB por década.
</details>

**3. Paso alto.** Con el paso alto y ω_c = 2 rad/s, ¿qué fase tiene la salida en ω₀ = 2 rad/s? ¿Está adelantada o retrasada?

<details><summary>Solución</summary>
H(j2) = j/(1 + j): |H| = 0,707 y ∠H = π/2 − π/4 = +π/4. La salida va adelantada respecto a la entrada (el recuadro da un «retardo» negativo).
</details>

**4. Resonancia.** Con el sistema de segundo orden, ω_n = 2 y ζ = 0,1, ¿cuánto vale |H| en ω₀ = ω_n? ¿Qué pasa con ζ = 0,707?

<details><summary>Solución</summary>
En ω = ω_n, H = ω_n²/(j2ζω_n²) = 1/(j2ζ): |H| = 5 y fase −π/2. La entrada sale multiplicada por 5. Con ζ = 1/√2, |H(jω_n)| = 0,707 y no hay pico: es el Butterworth de orden 2 del Tema 4.
</details>

**5. Filtrar una señal con dos tonos.** Una señal tiene componentes de 0,5 y 20 rad/s. Elige un paso bajo de primer orden para que la de 20 rad/s se atenúe al menos 20 dB sin que la de 0,5 baje más de 1 dB.

<details><summary>Solución</summary>
Para la atenuación, 1 + (20/ω_c)² ≥ 100, es decir, ω_c ≤ 2,01. Para la banda de paso, 1 + (0,5/ω_c)² ≤ 10^{0,1} ≈ 1,259, que da ω_c ≥ 0,98. Cualquier ω_c entre 1 y 2 rad/s sirve; con ω_c = 1,5, la de 0,5 rad/s baja 0,46 dB y la de 20 rad/s, 22,5 dB.
</details>

## Para profundizar

- [Apuntes del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Apuntes.pdf), sección 8, «Autofunciones y respuesta en frecuencia», y sección 9, «Sistemas continuos: ecuación diferencial y función de transferencia».
- [Transparencias T1-03](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%2003%20-%20Sistemas.pdf), sistemas LTI y respuesta en frecuencia.
- [Hoja de ejercicios del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios.pdf), ejercicios de sistemas (10 a 16), y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T1/codigo/python/lti_continuo.py` y su versión en Matlab.
- A. V. Oppenheim, A. S. Willsky y S. H. Nawab, *Signals and Systems*, 2.ª ed., Prentice Hall, 1997, apartados 3.2 y 6.5.

## Relación con otros conceptos

- **Exponencial compleja.** La autofunción e^{st}. Herramienta: [Exponencial compleja continua](T1-exponencial-continua.html).
- **Convolución.** La salida de un LTI es x ∗ h; en frecuencia, X·H. Herramienta: [Convolución continua](T1-convolucion-continua.html).
- **Sistema discreto.** La misma idea con e^{jΩn}. Herramienta: [Respuesta de un sistema LTI discreto](T1-respuesta-lti-discreta.html).
- **Polos y ceros (Tema 4).** |H(jω)| se lee como cociente de distancias a los ceros y a los polos. Herramienta: [Polos y ceros en el plano s](T4-polos-ceros-s.html).
- **Filtros analógicos (Tema 4).** Butterworth, Chebyshev y elíptico son paso bajos de orden mayor. Herramienta: [Aproximaciones de filtros analógicos](T4-filtros-continuos.html).
