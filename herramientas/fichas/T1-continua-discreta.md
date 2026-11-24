## Introducción

### De la sinusoide continua a la secuencia

Una sinusoide continua $x(t) = \cos(2\pi f t + \theta)$ tiene una frecuencia $f$ en hercios (ciclos por segundo), o una pulsación $\omega = 2\pi f$ en rad/s. Si se toma una muestra cada $T_s$ segundos, la secuencia que resulta es

> $$x[n] = x(nT_s) = \cos(2\pi f n T_s + \theta) = \cos(\Omega n + \theta), \qquad \Omega = \frac{2\pi f}{f_s} = \omega T_s.$$

$\Omega$ es la **frecuencia discreta**, en radianes por muestra, y $F = \Omega/2\pi = f/f_s$ es la frecuencia discreta en ciclos por muestra. Una secuencia no sabe nada de segundos: solo «sabe» cuánto avanza la fase de una muestra a la siguiente.

### Las frecuencias discretas se repiten cada 2π

En tiempo continuo, dos frecuencias distintas dan siempre señales distintas. En tiempo discreto no: como $n$ es entero,

> $$\cos\big((\Omega + 2\pi k)\, n + \theta\big) = \cos(\Omega n + 2\pi k n + \theta) = \cos(\Omega n + \theta).$$

Por tanto basta con estudiar $\Omega$ en un intervalo de longitud $2\pi$, normalmente $[-\pi, \pi)$. Al valor de ese intervalo se le llama **valor principal**. Para $\theta = 0$, además, $\cos(-\Omega n) = \cos(\Omega n)$: $\Omega$ y $2\pi - \Omega$ dan la misma secuencia.

### Qué significa en hercios

Deshaciendo el cambio $\Omega = 2\pi f/f_s$, sumar $2\pi$ a $\Omega$ equivale a sumar $f_s$ a $f$. Todas las sinusoides de frecuencias $f + k f_s$ dan las mismas muestras. El valor principal de $\Omega$ corresponde a una frecuencia entre $-f_s/2$ y $f_s/2$: si la sinusoide original estaba por encima de $f_s/2$, sus muestras son las de otra más lenta. Es el **aliasing**, que se estudia en el Tema 2.

### Lo más rápido que oscila una secuencia

La secuencia que más rápido cambia es $\cos(\pi n) = (-1)^n$, que alterna entre 1 y $-1$: $\Omega = \pi$, o $f = f_s/2$. Por encima de $\Omega = \pi$ la secuencia vuelve a oscilar más despacio, como si la frecuencia bajara.

### Periodicidad

$x[n] = \cos(\Omega n + \theta)$ es periódica solo si $\Omega/2\pi = F$ es un número racional, $F = k/N$ con la fracción irreducible. Entonces el periodo es $N$ muestras, que contienen $k$ ciclos de la sinusoide continua.

## Guía de uso

- **f** es la frecuencia de la sinusoide continua, en hercios, y **fs**, la frecuencia de muestreo; $T_s = 1/f_s$.
- **θ** es la fase inicial.
- La gráfica muestra la sinusoide continua y sus muestras $x[n] = x(nT_s)$; en rojo discontinuo, la sinusoide de la frecuencia principal, que pasa por las mismas muestras. Los deslizadores están arriba, a la izquierda.
- El recuadro indica $\Omega = 2\pi f/f_s$, su valor principal en $[-\pi, \pi)$ y la frecuencia en hercios que le corresponde. Si $f$ supera $f_s/2$, avisa de que las muestras son las de una sinusoide más lenta.

## Ejercicios

**1. Calcular Ω.** Con $f = 3$ Hz y $f_s = 10$ muestras/s, calcula $\Omega$ y $F$. ¿Cuántas muestras tiene un periodo de $x[n]$? Comprueba en la gráfica.

<details><summary>Solución</summary>
$\Omega = 2\pi \cdot 3/10 = 0{,}6\pi \approx 1{,}885$ rad/muestra y $F = 3/10$. La fracción es irreducible, así que el periodo es $N = 10$ muestras, que abarcan 3 ciclos de la sinusoide continua.
</details>

**2. Frecuencias que no se distinguen.** Con $f_s = 10$ muestras/s y $\theta = 0$, compara las muestras de $f = 3$, 7 y 13 Hz. ¿Qué valor principal da cada una?

<details><summary>Solución</summary>
3 Hz da $\Omega = 0{,}6\pi$; 13 Hz da $2{,}6\pi$, que es $0{,}6\pi + 2\pi$; 7 Hz da $1{,}4\pi$, cuyo valor principal es $-0{,}6\pi$. Con $\theta = 0$, $\cos(-0{,}6\pi n) = \cos(0{,}6\pi n)$, así que las tres dan las mismas muestras. Con $\theta \neq 0$, la de 7 Hz da las mismas muestras que un coseno de 3 Hz con la fase cambiada de signo.
</details>

**3. La oscilación más rápida.** Con $f_s = 10$ muestras/s, sube $f$ desde 0 hasta 10 Hz. ¿Para qué $f$ cambia más rápido la secuencia? ¿Qué pasa con $\theta = \pi/2$ en ese caso?

<details><summary>Solución</summary>
En $f = 5$ Hz $= f_s/2$, $\Omega = \pi$ y $x[n] = \cos(\pi n + \theta) = (-1)^n \cos\theta$. Con $\theta = \pi/2$ todas las muestras son nulas: muestrear justo a $2f$ no basta para ver un seno. Por encima de 5 Hz, la secuencia vuelve a oscilar más despacio.
</details>

**4. ¿Periódica o no?** Con $f_s = 10$, ¿es periódica la secuencia para $f = 2{,}5$ Hz? ¿Y para $f = 10/(2\pi) \approx 1{,}59$ Hz? Busca el periodo cuando exista.

<details><summary>Solución</summary>
$f = 2{,}5$ da $F = 1/4$: periódica con $N = 4$. $f = 10/(2\pi)$ da $\Omega = 1$ rad/muestra y $F = 1/(2\pi)$, irracional: no es periódica, aunque la sinusoide continua sí lo sea. En la herramienta, $f = 1{,}6$ da $F = 0{,}16 = 4/25$, periódica con $N = 25$.
</details>

**5. Ejercicio 9 f de la hoja.** La secuencia $\cos(11\pi n/6)$ parece de frecuencia alta. Reprodúcela con $f_s = 12$ muestras/s y $f = 11$ Hz y explica qué se ve.

<details><summary>Solución</summary>
$\Omega = 2\pi \cdot 11/12 = 11\pi/6$, cuyo valor principal es $11\pi/6 - 2\pi = -\pi/6$, que corresponde a 1 Hz. La secuencia es $\cos(\pi n/6)$, periódica con $N = 12$, y oscila despacio: es la misma que daría una sinusoide de 1 Hz.
</details>

## Para profundizar

- [Apuntes del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Apuntes.pdf), sección 3, apartado «Exponenciales complejas discretas».
- [Transparencias T1-01](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%2001%20-%20Se%C3%B1ales.pdf), «Exponencial compleja discreta» y «frecuencias equivalentes».
- [Hoja de ejercicios del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios.pdf), ejercicio 9, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T1/codigo/python/alias_discreto.py` y su versión en Matlab.
- A. V. Oppenheim, A. S. Willsky y S. H. Nawab, *Signals and Systems*, 2.ª ed., Prentice Hall, 1997, apartado 1.3.
- J. H. McClellan, R. W. Schafer y M. A. Yoder, *DSP First*, 2.ª ed., Pearson, 2016, capítulo 4.

## Relación con otros conceptos

- **Exponenciales complejas.** $\cos(\Omega n)$ es la parte real de $e^{j\Omega n}$. Herramientas: [Exponencial compleja continua](T1-exponencial-continua.html) y [Exponencial compleja discreta](T1-exponencial-discreta.html).
- **Aliasing (Tema 2).** Que $\Omega$ y $\Omega + 2\pi$ sean la misma frecuencia es, en hercios, que $f$ y $f + f_s$ den las mismas muestras. Herramienta: [Aliasing](T2-aliasing.html).
- **Teorema del muestreo (Tema 2).** Para que cada $f$ tenga su propia $\Omega$ hay que muestrear con $f_s > 2f$. Herramienta: [Espectro de una señal muestreada](T2-muestreo-ideal.html).
- **Respuesta en frecuencia discreta.** Como la frecuencia discreta es periódica, $H(e^{j\Omega})$ también lo es. Herramienta: [Respuesta de un sistema LTI discreto](T1-respuesta-lti-discreta.html).
