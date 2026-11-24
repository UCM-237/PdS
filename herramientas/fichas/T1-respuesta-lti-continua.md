## Introducción

### Las exponenciales son autofunciones

Si la entrada de un sistema LTI continuo con respuesta al impulso $h(t)$ es una exponencial compleja $e^{j\omega_0 t}$, la salida es

> $$y(t) = \int_{-\infty}^{\infty} h(\tau)\, e^{j\omega_0 (t-\tau)}\, d\tau = H(j\omega_0)\, e^{j\omega_0 t}, \qquad H(j\omega) = \int_{-\infty}^{\infty} h(t)\, e^{-j\omega t}\, dt.$$

La exponencial sale igual, multiplicada por un número complejo: es una **autofunción** del sistema, y $H(j\omega_0)$ es su autovalor. La función $H(j\omega)$ es la **respuesta en frecuencia**: la transformada de Fourier de $h(t)$, o la función de transferencia $H(s)$ evaluada en $s = j\omega$.

### Qué le pasa a una sinusoide

Como $\cos(\omega_0 t) = \tfrac12 e^{j\omega_0 t} + \tfrac12 e^{-j\omega_0 t}$ y, para un sistema real, $H(-j\omega) = H^*(j\omega)$, la salida en régimen permanente es

> $$y(t) = |H(j\omega_0)| \cos\big(\omega_0 t + \angle H(j\omega_0)\big).$$

El **módulo** dice cuánto se amplifica o atenúa esa frecuencia, y la **fase**, cuánto se desplaza: un desfase $\varphi$ equivale a un retardo de $-\varphi/\omega_0$ segundos. Con una señal cualquiera, cada componente de frecuencia sale escalada y desfasada a su manera; por eso un sistema LTI es un **filtro**.

### Tres sistemas de ejemplo

- **Paso bajo de primer orden**, $H(s) = \dfrac{1}{1 + s/\omega_c}$: deja pasar las frecuencias bajas. En $\omega = \omega_c$, $|H| = 1/\sqrt2$ ($-3$ dB) y la fase es $-\pi/4$. Por encima de $\omega_c$, $|H|$ cae 20 dB por década.
- **Paso alto de primer orden**, $H(s) = \dfrac{s/\omega_c}{1 + s/\omega_c}$: lo contrario; atenúa las bajas y adelanta la fase.
- **Segundo orden**, $H(s) = \dfrac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}$: $\omega_n$ es la frecuencia natural y $\zeta$ el amortiguamiento. Con $\zeta$ pequeño hay un pico de resonancia cerca de $\omega_n$, de altura aproximada $1/(2\zeta)$; con $\zeta \ge 1/\sqrt2$ no hay pico.

### Decibelios y escala logarítmica

Es habitual dibujar el módulo en decibelios, $20\log_{10}|H|$, frente a $\log\omega$ (el diagrama de Bode). Así los productos de factores se convierten en sumas y las pendientes se cuentan en dB por década.

## Guía de uso

- **Sistema** elige el paso bajo, el paso alto o el de segundo orden.
- **ωc o ωn** es la frecuencia de corte de los de primer orden o la natural del de segundo orden, y **ζ** el amortiguamiento de este último (solo aparece con el de segundo orden). Están arriba, junto al selector del sistema, porque cambian $H$.
- **log₁₀ ω₀** fija la frecuencia de la sinusoide de entrada, entre 0,1 y 100 rad/s; está arriba, con el resto de controles.
- Arriba, el módulo y la fase de $H(j\omega)$ con la frecuencia $\omega_0$ marcada. Abajo, la entrada y la salida en régimen permanente.
- El recuadro da $|H(j\omega_0)|$, $\angle H(j\omega_0)$ y el retardo que corresponde a ese desfase.

## Ejercicios

**1. La frecuencia de corte.** Con el paso bajo, $\omega_c = 2$ rad/s y $\omega_0 = 2$ rad/s ($\log_{10}\omega_0 \approx 0{,}30$), ¿cuánto valen $|H|$ y $\angle H$? ¿Cuánto se retrasa la salida?

<details><summary>Solución</summary>
$H(j2) = \dfrac{1}{1 + j}$: $|H| = 1/\sqrt2 \approx 0{,}707$ ($-3$ dB) y $\angle H = -\pi/4$. El retardo es $(\pi/4)/2 \approx 0{,}39$ s.
</details>

**2. Una década por encima.** Con el mismo paso bajo, lleva $\omega_0$ a 20 rad/s. ¿Cuánto vale $|H|$ en dB? ¿Y a 200 rad/s, si pudieras?

<details><summary>Solución</summary>
$|H(j20)| = 1/\sqrt{1 + 100} \approx 0{,}0995$, unos $-20$ dB, y la fase se acerca a $-\pi/2$. A 200 rad/s serían unos $-40$ dB: el paso bajo de primer orden cae 20 dB por década.
</details>

**3. Paso alto.** Con el paso alto y $\omega_c = 2$ rad/s, ¿qué fase tiene la salida en $\omega_0 = 2$ rad/s? ¿Está adelantada o retrasada?

<details><summary>Solución</summary>
$H(j2) = \dfrac{j}{1 + j}$: $|H| = 0{,}707$ y $\angle H = \pi/2 - \pi/4 = +\pi/4$. La salida va adelantada respecto a la entrada (el recuadro da un «retardo» negativo).
</details>

**4. Resonancia.** Con el sistema de segundo orden, $\omega_n = 2$ y $\zeta = 0{,}1$, ¿cuánto vale $|H|$ en $\omega_0 = \omega_n$? ¿Qué pasa con $\zeta = 0{,}707$?

<details><summary>Solución</summary>
En $\omega = \omega_n$, $H = \dfrac{\omega_n^2}{j2\zeta\omega_n^2} = \dfrac{1}{j2\zeta}$: $|H| = 5$ y fase $-\pi/2$. La entrada sale multiplicada por 5. Con $\zeta = 1/\sqrt2$, $|H(j\omega_n)| = 0{,}707$ y no hay pico: es el Butterworth de orden 2 del Tema 4.
</details>

**5. Filtrar una señal con dos tonos.** Una señal tiene componentes de 0,5 y 20 rad/s. Elige un paso bajo de primer orden para que la de 20 rad/s se atenúe al menos 20 dB sin que la de 0,5 baje más de 1 dB.

<details><summary>Solución</summary>
Para la atenuación, $1 + (20/\omega_c)^2 \ge 100$, es decir, $\omega_c \le 2{,}01$. Para la banda de paso, $1 + (0{,}5/\omega_c)^2 \le 10^{0{,}1} \approx 1{,}259$, que da $\omega_c \ge 0{,}98$. Cualquier $\omega_c$ entre 1 y 2 rad/s sirve; con $\omega_c = 1{,}5$, la de 0,5 rad/s baja 0,46 dB y la de 20 rad/s, 22,5 dB.
</details>

## Para profundizar

- [Apuntes del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Apuntes.pdf), sección 8, «Autofunciones y respuesta en frecuencia», y sección 9, «Sistemas continuos: ecuación diferencial y función de transferencia».
- [Transparencias T1-03](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%2003%20-%20Sistemas.pdf), sistemas LTI y respuesta en frecuencia.
- [Hoja de ejercicios del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios.pdf), ejercicios de sistemas (10 a 16), y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T1/codigo/python/lti_continuo.py` y su versión en Matlab.
- A. V. Oppenheim, A. S. Willsky y S. H. Nawab, *Signals and Systems*, 2.ª ed., Prentice Hall, 1997, apartados 3.2 y 6.5.

## Relación con otros conceptos

- **Exponencial compleja.** La autofunción $e^{st}$. Herramienta: [Exponencial compleja continua](T1-exponencial-continua.html).
- **Convolución.** La salida de un LTI es $x * h$; en frecuencia, $X\,H$. Herramienta: [Convolución continua](T1-convolucion-continua.html).
- **Sistema discreto.** La misma idea con $e^{j\Omega n}$. Herramienta: [Respuesta de un sistema LTI discreto](T1-respuesta-lti-discreta.html).
- **Polos y ceros (Tema 4).** $|H(j\omega)|$ se lee como cociente de distancias a los ceros y a los polos. Herramienta: [Polos y ceros en el plano s](T4-polos-ceros-s.html).
- **Filtros analógicos (Tema 4).** Butterworth, Chebyshev y elíptico son paso bajos de orden mayor. Herramienta: [Aproximaciones de filtros analógicos](T4-filtros-continuos.html).
