## Introducción

### La exponencial compleja discreta

En tiempo discreto, la exponencial compleja es $x[n] = C z^n$, con $z = r e^{j\Omega}$ complejo y $n$ entero. Su parte real es

> $$\mathrm{Re}\{C z^n\} = |C|\, r^n \cos(\Omega n + \theta).$$

El módulo $r$ fija la envolvente: si $r < 1$ la secuencia decrece, si $r > 1$ crece y si $r = 1$ tiene amplitud constante. El ángulo $\Omega$ es la frecuencia discreta, en rad/muestra. Es la versión discreta de $e^{st}$: al muestrear $e^{st}$ cada $T_s$ se obtiene $z^n$ con $z = e^{sT_s}$, es decir, $r = e^{\sigma T_s}$ y $\Omega = \omega T_s$.

### Dos diferencias con el caso continuo

1. **La frecuencia solo importa salvo múltiplos de $2\pi$.** $e^{j(\Omega + 2\pi)n} = e^{j\Omega n}$ para todo entero $n$, así que basta con considerar $\Omega$ en $[-\pi, \pi)$ o en $[0, 2\pi)$. Las frecuencias bajas están cerca de $\Omega = 0$ (y de $2\pi$) y la más alta es $\Omega = \pi$, que da $(-1)^n$.
2. **No toda sinusoide discreta es periódica.** $\cos(\Omega n)$ es periódica si existe un entero $N$ tal que $\Omega N$ sea múltiplo de $2\pi$, es decir, si $\Omega/2\pi = k/N$ es racional. El periodo fundamental es el $N$ de la fracción irreducible. $\cos(0{,}75n)$, por ejemplo, no es periódica.

### Por qué importa

Igual que en continuo, las exponenciales $z^n$ son autofunciones de los sistemas LTI discretos: la salida es $H(z)\, z^n$. La transformada Z descompone las secuencias en exponenciales $z^n$ y la DTFT en exponenciales $e^{j\Omega n}$ ($r = 1$). Cada polo $p$ de un sistema discreto aporta un término $p^n$ a su respuesta libre, y el sistema es estable si todos los polos tienen $|p| < 1$.

## Guía de uso

- **r** es el módulo de $z$: menor que 1 amortigua y mayor que 1 hace crecer la secuencia.
- **Ω** es la frecuencia discreta, entre 0 y $2\pi$ rad/muestra.
- **θ** es la fase inicial.
- La gráfica muestra las muestras $r^n \cos(\Omega n + \theta)$ y, en gris, la curva continua que pasa por ellas, como referencia. Los deslizadores están debajo.
- El recuadro indica $\Omega/2\pi$, si la secuencia es periódica (y con qué periodo) y el valor principal de $\Omega$.

## Ejercicios

**1. Periodo de una sinusoide discreta.** Con $r = 1$ y $\Omega = \pi/4 \approx 0{,}785$, ¿cuál es el periodo? ¿Y con $\Omega = 3\pi/8$? Compruébalo contando muestras.

<details><summary>Solución</summary>
$\Omega/2\pi = 1/8$: $N = 8$. Con $\Omega = 3\pi/8$, $\Omega/2\pi = 3/16$: $N = 16$, y en ese periodo caben 3 ciclos de la curva gris.
</details>

**2. Una sinusoide que no se repite.** Pon $\Omega = 0{,}75$ rad/muestra. ¿Es periódica? ¿Por qué $\cos(0{,}75t)$ sí lo es?

<details><summary>Solución</summary>
$\Omega/2\pi = 0{,}75/2\pi = 3/(8\pi)$, que es irracional: ninguna muestra se repite exactamente. La curva continua $\cos(0{,}75t)$ tiene periodo $8\pi/3$, pero ese periodo no es un número entero de muestras.
</details>

**3. Frecuencias equivalentes.** Con $r = 1$ y $\theta = 0$, compara $\Omega = \pi/4$ con $\Omega = 2\pi - \pi/4 \approx 5{,}50$. ¿Cuál oscila más rápido? ¿Y si $\theta = 0{,}5$? ¿Dónde está la oscilación más rápida?

<details><summary>Solución</summary>
Las dos dan las mismas muestras con $\theta = 0$, porque la frecuencia es periódica de periodo $2\pi$ ($2\pi - \pi/4$ equivale a $-\pi/4$) y el coseno es par: oscilan igual de rápido, aunque la curva gris de 5,50 parezca mucho más rápida. Con $\theta \neq 0$, $2\pi - \pi/4$ equivale a $-\pi/4$ y da $\cos(\pi n/4 - \theta)$: la fase cambia de signo. Lo más rápido está en $\Omega = \pi$.
</details>

**4. Amortiguamiento.** Con $\Omega = \pi/4$ y $r = 0{,}9$, ¿cuánto vale la envolvente en $n = 10$? ¿Qué $r$ hace que la amplitud caiga a la mitad en 8 muestras?

<details><summary>Solución</summary>
$0{,}9^{10} \approx 0{,}35$. Para caer a la mitad en 8 muestras hace falta $r^8 = 0{,}5$, es decir, $r = 0{,}5^{1/8} \approx 0{,}917$. Si $r > 1$ la envolvente crece: un polo fuera del círculo unidad da un sistema inestable.
</details>

**5. Ejercicio 9 de la hoja.** Determina si $x[n] = 5\, e^{j(3/4)n}$ y $x[n] = \cos(11\pi n/6)$ son periódicas y comprueba la segunda en la herramienta.

<details><summary>Solución</summary>
La primera no es periódica: $\Omega/2\pi = 3/(8\pi)$ es irracional. La segunda tiene $\Omega = 11\pi/6 \approx 5{,}76$, cuyo valor principal es $-\pi/6$: periódica con $N = 12$, y oscila despacio aunque $\Omega$ parezca grande.
</details>

## Para profundizar

- [Apuntes del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Apuntes.pdf), sección 3, apartado «Exponenciales complejas discretas».
- [Transparencias T1-01](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%2001%20-%20Se%C3%B1ales.pdf), «Exponencial compleja discreta».
- [Hoja de ejercicios del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios.pdf), ejercicio 9, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T1/codigo/python/senales_basicas.py` y `alias_discreto.py`, y sus versiones en Matlab.
- A. V. Oppenheim, A. S. Willsky y S. H. Nawab, *Signals and Systems*, 2.ª ed., Prentice Hall, 1997, apartado 1.3.
- J. H. McClellan, R. W. Schafer y M. A. Yoder, *DSP First*, 2.ª ed., Pearson, 2016, capítulo 4.

## Relación con otros conceptos

- **Exponencial continua.** $z^n$ es la versión discreta de $e^{st}$, con $z = e^{sT_s}$. Herramienta: [Exponencial compleja continua](T1-exponencial-continua.html).
- **Muestreo.** El valor principal de $\Omega$ explica por qué frecuencias separadas $f_s$ dan las mismas muestras. Herramientas: [Exponencial continua frente a discreta](T1-continua-discreta.html) y [Aliasing](T2-aliasing.html).
- **Polos de un sistema discreto (Tema 4).** Cada polo $p$ aporta $p^n$ a la respuesta libre; con $|p| < 1$ se extingue. Herramienta: [Polos y ceros en el plano z](T4-polos-ceros-z.html).
- **DFT (Tema 3).** La DFT descompone una secuencia en exponenciales de frecuencias $2\pi k/N$, todas periódicas de periodo $N$. Herramienta: [DFT, fuga y relleno con ceros](T3-dft.html).
