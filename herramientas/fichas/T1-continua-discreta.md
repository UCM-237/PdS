## Introducción

### De la sinusoide continua a la secuencia

Una sinusoide continua x(t) = cos(2π f t + θ) tiene una frecuencia f en hercios (ciclos por segundo), o una pulsación ω = 2πf en rad/s. Si se toma una muestra cada Ts segundos, la secuencia que resulta es

> x[n] = x(nTs) = cos(2π f n Ts + θ) = cos(Ω n + θ), con Ω = 2π f / fs = ω Ts.

Ω es la **frecuencia discreta**, en radianes por muestra, y F = Ω/2π = f/fs es la frecuencia discreta en ciclos por muestra. Una secuencia no sabe nada de segundos: solo «sabe» cuánto avanza la fase de una muestra a la siguiente.

### Las frecuencias discretas se repiten cada 2π

En tiempo continuo, dos frecuencias distintas dan siempre señales distintas. En tiempo discreto no: como n es entero,

> cos((Ω + 2πk) n + θ) = cos(Ω n + 2πkn + θ) = cos(Ω n + θ).

Por tanto basta con estudiar Ω en un intervalo de longitud 2π, normalmente [−π, π). Al valor de ese intervalo se le llama **valor principal**. Para θ = 0, además, cos(−Ωn) = cos(Ωn): Ω y 2π − Ω dan la misma secuencia.

### Qué significa en hercios

Deshaciendo el cambio Ω = 2πf/fs, sumar 2π a Ω equivale a sumar fs a f. Todas las sinusoides de frecuencias f + k fs dan las mismas muestras. El valor principal de Ω corresponde a una frecuencia entre −fs/2 y fs/2: si la sinusoide original estaba por encima de fs/2, sus muestras son las de otra más lenta. Es el **aliasing**, que se estudia en el Tema 2.

### Lo más rápido que oscila una secuencia

La secuencia que más rápido cambia es cos(πn) = (−1)ⁿ, que alterna entre 1 y −1: Ω = π, o f = fs/2. Por encima de Ω = π la secuencia vuelve a oscilar más despacio, como si la frecuencia bajara.

### Periodicidad

x[n] = cos(Ωn + θ) es periódica solo si Ω/2π = F es un número racional, F = k/N con la fracción irreducible. Entonces el periodo es N muestras, que contienen k ciclos de la sinusoide continua.

## Guía de uso

- **f** es la frecuencia de la sinusoide continua, en hercios, y **fs**, la frecuencia de muestreo. Ts = 1/fs.
- **θ** es la fase inicial.
- La gráfica muestra la sinusoide continua en gris y sus muestras x[n] = x(nTs) en azul.
- El recuadro indica Ω = 2πf/fs, su valor principal en [−π, π) y la frecuencia en hercios que le corresponde. Si f supera fs/2, avisa de que las muestras son las de una sinusoide más lenta.

## Ejercicios

**1. Calcular Ω.** Con f = 3 Hz y fs = 10 muestras/s, calcula Ω y F. ¿Cuántas muestras tiene un periodo de x[n]? Comprueba en la gráfica.

<details><summary>Solución</summary>
Ω = 2π·3/10 = 0,6π ≈ 1,885 rad/muestra y F = 3/10. La fracción es irreducible, así que el periodo es N = 10 muestras, que abarcan 3 ciclos de la sinusoide continua.
</details>

**2. Frecuencias que no se distinguen.** Con fs = 10 muestras/s y θ = 0, compara las muestras de f = 3, 7 y 13 Hz. ¿Qué valor principal da cada una?

<details><summary>Solución</summary>
3 Hz da Ω = 0,6π; 13 Hz da 2,6π, que es 0,6π + 2π; 7 Hz da 1,4π, cuyo valor principal es −0,6π. Con θ = 0, cos(−0,6πn) = cos(0,6πn), así que las tres dan las mismas muestras. Con θ ≠ 0, la de 7 Hz da las mismas muestras que un coseno de 3 Hz con la fase cambiada de signo.
</details>

**3. La oscilación más rápida.** Con fs = 10 muestras/s, sube f desde 0 hasta 10 Hz. ¿Para qué f cambia más rápido la secuencia? ¿Qué pasa con θ = π/2 en ese caso?

<details><summary>Solución</summary>
En f = 5 Hz = fs/2, Ω = π y x[n] = cos(πn + θ) = (−1)ⁿ cos θ. Con θ = π/2 todas las muestras son nulas: muestrear justo a 2f no basta para ver un seno. Por encima de 5 Hz, la secuencia vuelve a oscilar más despacio.
</details>

**4. ¿Periódica o no?** Con fs = 10, ¿es periódica la secuencia para f = 2,5 Hz? ¿Y para f = 10/(2π) ≈ 1,59 Hz? Busca el periodo cuando exista.

<details><summary>Solución</summary>
f = 2,5 da F = 1/4: periódica con N = 4. f = 10/(2π) da Ω = 1 rad/muestra y F = 1/(2π), irracional: no es periódica, aunque la sinusoide continua sí lo sea. En la herramienta, f = 1,6 da F = 0,16 = 4/25, periódica con N = 25.
</details>

**5. Ejercicio 9 f de la hoja.** La secuencia cos(11πn/6) parece de frecuencia alta. Reprodúcela con fs = 12 muestras/s y f = 11 Hz y explica qué se ve.

<details><summary>Solución</summary>
Ω = 2π·11/12 = 11π/6, cuyo valor principal es 11π/6 − 2π = −π/6, que corresponde a 1 Hz. La secuencia es cos(πn/6), periódica con N = 12, y oscila despacio: es la misma que daría una sinusoide de 1 Hz.
</details>

## Para profundizar

- [Apuntes del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Apuntes.pdf), sección 3, apartado «Exponenciales complejas discretas».
- [Transparencias T1-01](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%2001%20-%20Se%C3%B1ales.pdf), «Exponencial compleja discreta» y «frecuencias equivalentes».
- [Hoja de ejercicios del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios.pdf), ejercicio 9, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T1/codigo/python/alias_discreto.py` y su versión en Matlab.
- A. V. Oppenheim, A. S. Willsky y S. H. Nawab, *Signals and Systems*, 2.ª ed., Prentice Hall, 1997, apartado 1.3.
- J. H. McClellan, R. W. Schafer y M. A. Yoder, *DSP First*, 2.ª ed., Pearson, 2016, capítulo 4.

## Relación con otros conceptos

- **Exponenciales complejas.** cos(Ωn) es la parte real de e^{jΩn}. Herramientas: [Exponencial compleja continua](T1-exponencial-continua.html) y [Exponencial compleja discreta](T1-exponencial-discreta.html).
- **Aliasing (Tema 2).** Que Ω y Ω + 2π sean la misma frecuencia es, en hercios, que f y f + fs den las mismas muestras. Herramienta: [Aliasing](T2-aliasing.html).
- **Teorema del muestreo (Tema 2).** Para que cada f tenga su propia Ω hay que muestrear con fs > 2f. Herramienta: [Espectro de una señal muestreada](T2-muestreo-ideal.html).
- **Respuesta en frecuencia discreta.** Como la frecuencia discreta es periódica, H(e^{jΩ}) también lo es. Herramienta: [Respuesta de un sistema LTI discreto](T1-respuesta-lti-discreta.html).
