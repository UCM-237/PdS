## Introducción

### La señal que lo resume todo

La exponencial compleja continua es x(t) = C e^{st}, con C = |C| e^{jθ} y s = σ + jω números complejos. Con la fórmula de Euler,

> C e^{st} = |C| e^{σt} e^{j(ωt + θ)} = |C| e^{σt} [cos(ωt + θ) + j sin(ωt + θ)].

Según los valores de s salen casi todas las señales básicas: una constante (s = 0), una exponencial real (ω = 0), una sinusoide (σ = 0) o una sinusoide amortiguada o creciente (σ y ω no nulos).

### Qué controla cada parte de s

- La **parte real σ** fija la envolvente |C| e^{σt}. Si σ < 0 la señal se amortigua, si σ > 0 crece y si σ = 0 tiene amplitud constante. La **constante de tiempo** τ = 1/|σ| es lo que tarda la envolvente en multiplicarse o dividirse por e ≈ 2,72.
- La **parte imaginaria ω** es la pulsación de la oscilación, en rad/s; f = ω/2π es la frecuencia en hercios y T = 1/f el periodo.
- La **fase θ** desplaza la oscilación en el tiempo: cos(ωt + θ) = cos(ω(t + θ/ω)). Con θ = −π/2, el coseno se convierte en un seno.

### Por qué importa

Las exponenciales complejas son las **autofunciones** de los sistemas LTI: si la entrada es e^{st}, la salida es H(s) e^{st}, la misma exponencial multiplicada por un número complejo. Por eso las transformadas de Fourier y de Laplace descomponen las señales en exponenciales complejas. Además, la respuesta libre de un sistema continuo es una suma de exponenciales e^{p t}, una por cada polo p: un polo con parte real negativa da una respuesta que se extingue.

### Señal real a partir de exponenciales complejas

Una sinusoide real es la suma de dos exponenciales complejas conjugadas: cos(ωt + θ) = ½ e^{j(ωt+θ)} + ½ e^{−j(ωt+θ)}. Por eso su espectro tiene dos rayas, en ±ω.

## Guía de uso

- **σ** es la parte real de s, en 1/s: negativa para amortiguar y positiva para crecer.
- **f** es la frecuencia de la oscilación, en hercios (ω = 2πf).
- **θ** es la fase inicial, en radianes.
- La gráfica muestra la parte real, e^{σt} cos(2πft + θ), con su envolvente ±e^{σt}.

## Ejercicios

**1. Leer la envolvente.** Con σ = −0,5 1/s y f = 1 Hz, ¿cuánto vale la constante de tiempo? ¿Cuánto tarda la envolvente en reducirse a la mitad? Mídelo en la gráfica.

<details><summary>Solución</summary>
τ = 1/0,5 = 2 s. La envolvente se reduce a la mitad cuando e^{−0,5t} = 1/2, es decir, en t = 2 ln 2 ≈ 1,39 s. En ese tiempo caben unas 1,4 oscilaciones de periodo 1 s.
</details>

**2. Oscilaciones en una constante de tiempo.** Con f = 1 Hz, busca σ para que la señal haga unas 5 oscilaciones antes de que su amplitud caiga a 1/e.

<details><summary>Solución</summary>
5 oscilaciones de 1 s duran 5 s, así que τ = 5 s y σ = −0,2 1/s. Cuanto más cerca de 0 está σ frente a ω, más oscilaciones se ven antes de que la señal se extinga: es lo que pasa con un polo cerca del eje imaginario.
</details>

**3. Del coseno al seno.** Con σ = 0 y f = 1 Hz, ¿qué θ convierte la señal en sin(2πt)? ¿Y en −cos(2πt)?

<details><summary>Solución</summary>
sin(2πt) = cos(2πt − π/2): θ = −π/2. −cos(2πt) = cos(2πt + π): θ = ±π. Un cambio de fase θ equivale a un adelanto de θ/ω segundos.
</details>

**4. Crecer o decrecer.** Fija f = 0,5 Hz. ¿Qué signo de σ corresponde a un sistema estable cuya respuesta libre fuera esta señal? Pon σ = 0 y explica por qué ese caso es el límite.

<details><summary>Solución</summary>
Hace falta σ < 0: la respuesta se extingue. Con σ > 0 crece sin límite y el sistema es inestable. Con σ = 0 la oscilación se mantiene indefinidamente: corresponde a polos sobre el eje imaginario, que no son BIBO estables.
</details>

**5. Ejercicio 11 e de la hoja.** H(s) = (s − 1)/(s² + 2s + 5) tiene polos en s = −1 ± 2j. Reproduce con la herramienta la forma de su respuesta libre e indica si el sistema es estable.

<details><summary>Solución</summary>
σ = −1 1/s y ω = 2 rad/s, es decir, f = 2/(2π) ≈ 0,32 Hz. La señal es una oscilación amortiguada con τ = 1 s: el sistema es estable. El cero en s = 1 cambia la amplitud y la fase de la respuesta, pero no su estabilidad.
</details>

## Para profundizar

- [Apuntes del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Apuntes.pdf), sección 3, apartado «Exponenciales complejas continuas», y sección 8, «Autofunciones y respuesta en frecuencia».
- [Transparencias T1-01](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%2001%20-%20Se%C3%B1ales.pdf), «Exponencial compleja continua».
- [Hoja de ejercicios del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios.pdf), ejercicios 4 y 11, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T1/codigo/python/senales_basicas.py` y su versión en Matlab.
- A. V. Oppenheim, A. S. Willsky y S. H. Nawab, *Signals and Systems*, 2.ª ed., Prentice Hall, 1997, apartado 1.3.
- J. H. McClellan, R. W. Schafer y M. A. Yoder, *DSP First*, 2.ª ed., Pearson, 2016, capítulo 2.

## Relación con otros conceptos

- **Exponencial discreta.** Al muestrear e^{st} se obtiene zⁿ con z = e^{sTs}. Herramientas: [Exponencial compleja discreta](T1-exponencial-discreta.html) y [Continua frente a discreta](T1-continua-discreta.html).
- **Respuesta en frecuencia.** Con s = jω, la salida de un sistema LTI es H(jω) e^{jωt}. Herramienta: [Respuesta de un sistema LTI continuo](T1-respuesta-lti-continua.html).
- **Polos de un sistema continuo (Tema 4).** Cada polo p aporta un término e^{pt} a la respuesta libre; su posición en el plano s decide si se amortigua. Herramienta: [Polos y ceros en el plano s](T4-polos-ceros-s.html).
- **Serie y transformada de Fourier.** Descomponen una señal en exponenciales complejas con σ = 0. Herramienta: [Serie de Fourier](T1-serie-fourier.html).
