## Introducción

### La señal que lo resume todo

La exponencial compleja continua es $x(t) = C e^{st}$, con $C = |C| e^{j\theta}$ y $s = \sigma + j\omega$ números complejos. Con la fórmula de Euler,

> $$C e^{st} = |C| e^{\sigma t} e^{j(\omega t + \theta)} = |C| e^{\sigma t} \big[\cos(\omega t + \theta) + j \sin(\omega t + \theta)\big].$$

Según los valores de $s$ salen casi todas las señales básicas: una constante ($s = 0$), una exponencial real ($\omega = 0$), una sinusoide ($\sigma = 0$) o una sinusoide amortiguada o creciente ($\sigma$ y $\omega$ no nulos).

### Qué controla cada parte de s

- La **parte real $\sigma$** fija la envolvente $|C| e^{\sigma t}$. Si $\sigma < 0$ la señal se amortigua, si $\sigma > 0$ crece y si $\sigma = 0$ tiene amplitud constante. La **constante de tiempo** $\tau = 1/|\sigma|$ es lo que tarda la envolvente en multiplicarse o dividirse por $e \approx 2{,}72$.
- La **parte imaginaria $\omega$** es la pulsación de la oscilación, en rad/s; $f = \omega/2\pi$ es la frecuencia en hercios y $T = 1/f$ el periodo.
- La **fase $\theta$** desplaza la oscilación en el tiempo: $\cos(\omega t + \theta) = \cos\big(\omega(t + \theta/\omega)\big)$. Con $\theta = -\pi/2$, el coseno se convierte en un seno.

### Por qué importa

Las exponenciales complejas son las **autofunciones** de los sistemas LTI: si la entrada es $e^{st}$, la salida es $H(s)\, e^{st}$, la misma exponencial multiplicada por un número complejo. Por eso las transformadas de Fourier y de Laplace descomponen las señales en exponenciales complejas. Además, la respuesta libre de un sistema continuo es una suma de exponenciales $e^{pt}$, una por cada polo $p$: un polo con parte real negativa da una respuesta que se extingue.

### Señal real a partir de exponenciales complejas

Una sinusoide real es la suma de dos exponenciales complejas conjugadas:

$$\cos(\omega t + \theta) = \tfrac12 e^{j(\omega t + \theta)} + \tfrac12 e^{-j(\omega t + \theta)}.$$

Por eso su espectro tiene dos rayas, en $\pm\omega$.

## Guía de uso

- **σ** es la parte real de $s$, en 1/s: negativa para amortiguar y positiva para crecer.
- **f** es la frecuencia de la oscilación, en hercios ($\omega = 2\pi f$).
- **θ** es la fase inicial, en radianes.
- La gráfica muestra la parte real, $e^{\sigma t}\cos(2\pi f t + \theta)$, con su envolvente $\pm e^{\sigma t}$. Los tres deslizadores están arriba, a la izquierda.

## Ejercicios

**1. Leer la envolvente.** Con $\sigma = -0{,}5$ 1/s y $f = 1$ Hz, ¿cuánto vale la constante de tiempo? ¿Cuánto tarda la envolvente en reducirse a la mitad? Mídelo en la gráfica.

<details><summary>Solución</summary>
$\tau = 1/0{,}5 = 2$ s. La envolvente se reduce a la mitad cuando $e^{-0{,}5t} = 1/2$, es decir, en $t = 2 \ln 2 \approx 1{,}39$ s. En ese tiempo caben unas 1,4 oscilaciones de periodo 1 s.
</details>

**2. Oscilaciones en una constante de tiempo.** Con $f = 1$ Hz, busca $\sigma$ para que la señal haga unas 5 oscilaciones antes de que su amplitud caiga a $1/e$.

<details><summary>Solución</summary>
5 oscilaciones de 1 s duran 5 s, así que $\tau = 5$ s y $\sigma = -0{,}2$ 1/s. Cuanto más cerca de 0 está $\sigma$ frente a $\omega$, más oscilaciones se ven antes de que la señal se extinga: es lo que pasa con un polo cerca del eje imaginario.
</details>

**3. Del coseno al seno.** Con $\sigma = 0$ y $f = 1$ Hz, ¿qué $\theta$ convierte la señal en $\sin(2\pi t)$? ¿Y en $-\cos(2\pi t)$?

<details><summary>Solución</summary>
$\sin(2\pi t) = \cos(2\pi t - \pi/2)$: $\theta = -\pi/2$. $-\cos(2\pi t) = \cos(2\pi t + \pi)$: $\theta = \pm\pi$. Un cambio de fase $\theta$ equivale a un adelanto de $\theta/\omega$ segundos.
</details>

**4. Crecer o decrecer.** Fija $f = 0{,}5$ Hz. ¿Qué signo de $\sigma$ corresponde a un sistema estable cuya respuesta libre fuera esta señal? Pon $\sigma = 0$ y explica por qué ese caso es el límite.

<details><summary>Solución</summary>
Hace falta $\sigma < 0$: la respuesta se extingue. Con $\sigma > 0$ crece sin límite y el sistema es inestable. Con $\sigma = 0$ la oscilación se mantiene indefinidamente: corresponde a polos sobre el eje imaginario, que no son BIBO estables.
</details>

**5. Ejercicio 11 e de la hoja.** $H(s) = \dfrac{s - 1}{s^2 + 2s + 5}$ tiene polos en $s = -1 \pm 2j$. Reproduce con la herramienta la forma de su respuesta libre e indica si el sistema es estable.

<details><summary>Solución</summary>
$\sigma = -1$ 1/s y $\omega = 2$ rad/s, es decir, $f = 2/(2\pi) \approx 0{,}32$ Hz. La señal es una oscilación amortiguada con $\tau = 1$ s: el sistema es estable. El cero en $s = 1$ cambia la amplitud y la fase de la respuesta, pero no su estabilidad.
</details>

## Para profundizar

- [Apuntes del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Apuntes.pdf), sección 3, apartado «Exponenciales complejas continuas», y sección 8, «Autofunciones y respuesta en frecuencia».
- [Transparencias T1-01](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%2001%20-%20Se%C3%B1ales.pdf), «Exponencial compleja continua».
- [Hoja de ejercicios del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios.pdf), ejercicios 4 y 11, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T1/codigo/python/senales_basicas.py` y su versión en Matlab.
- A. V. Oppenheim, A. S. Willsky y S. H. Nawab, *Signals and Systems*, 2.ª ed., Prentice Hall, 1997, apartado 1.3.
- J. H. McClellan, R. W. Schafer y M. A. Yoder, *DSP First*, 2.ª ed., Pearson, 2016, capítulo 2.

## Relación con otros conceptos

- **Exponencial discreta.** Al muestrear $e^{st}$ se obtiene $z^n$ con $z = e^{sT_s}$. Herramientas: [Exponencial compleja discreta](T1-exponencial-discreta.html) y [Exponencial continua frente a discreta](T1-continua-discreta.html).
- **Respuesta en frecuencia.** Con $s = j\omega$, la salida de un sistema LTI es $H(j\omega)\,e^{j\omega t}$. Herramienta: [Respuesta de un sistema LTI continuo](T1-respuesta-lti-continua.html).
- **Polos de un sistema continuo (Tema 4).** Cada polo $p$ aporta un término $e^{pt}$ a la respuesta libre; su posición en el plano $s$ decide si se amortigua. Herramienta: [Polos y ceros en el plano s](T4-polos-ceros-s.html).
- **Serie y transformada de Fourier.** Descomponen una señal en exponenciales complejas con $\sigma = 0$. Herramienta: [Serie de Fourier](T1-serie-fourier.html).
