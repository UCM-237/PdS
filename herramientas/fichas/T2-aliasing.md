## Introducción

Muestrear una sinusoide de frecuencia f₀ cada Ts = 1/fs segundos da la secuencia x[n] = cos(2π f₀ n / fs), de frecuencia discreta Ω₀ = 2π f₀ / fs. Como las frecuencias discretas Ω₀ y Ω₀ + 2πk dan las mismas muestras, también las dan todas las sinusoides de frecuencias f₀ + k fs (y, por ser el coseno par, −f₀ + k fs). Cada una es un **alias** de las demás.

De todas ellas, la única con |f| ≤ fs/2 es el **alias fundamental**. Un reconstructor que solo produce frecuencias por debajo de fs/2, como el filtro ideal, devuelve siempre esa. Si la sinusoide original estaba por encima de fs/2, aparece en la **frecuencia aparente**

> f_a = |f₀ − k fs|, con k el entero más próximo a f₀ / fs,

y el eje de frecuencias se «pliega» en los múltiplos de fs/2, la **frecuencia de Nyquist**. En el espectro, el muestreo repite X(f) cada fs; hay aliasing cuando una réplica cae dentro de la banda [−fs/2, fs/2].

## Guía de uso

- **fs** fija la frecuencia de muestreo. La banda sombreada en verde es [−fs/2, fs/2].
- **f₁, f₂ y f₃** son las frecuencias de tres cosenos de amplitudes 1; 0,6 y 0,4, que se suman.
- La gráfica de arriba muestra x(t) en gris, las muestras x(nTs) en naranja y, en rojo, la señal que daría el reconstructor ideal.
- La de abajo muestra las rayas del espectro de x(t), una por componente y con su color, y en gris las réplicas que crea el muestreo cada fs.
- El recuadro de la izquierda indica la frecuencia alias de cada componente.
- Para ver una sola sinusoide, lleva las otras dos a 0 Hz (se convierten en una constante).

## Ejercicios

**1. Predecir y comprobar.** Con fs = 10 muestras/s y f₁ = 7 Hz, calcula a mano la frecuencia aparente. Comprueba el resultado con la herramienta. Busca después otras dos frecuencias de f₁ que den exactamente las mismas muestras.

<details><summary>Solución</summary>
f_a = |7 − 10| = 3 Hz: la curva roja es un coseno de 3 Hz que pasa por las mismas muestras. Dan las mismas muestras 3, 13, 17 y 23 Hz (3 + 10k y −3 + 10k).
</details>

**2. El mapa de plegado.** Con fs = 10 muestras/s, mueve f₁ de 0 a 25 Hz en pasos de 1 Hz y anota la frecuencia aparente. Dibuja f_a frente a f₁.

<details><summary>Solución</summary>
Sale una onda triangular: f_a sube de 0 a 5 Hz entre 0 y 5 Hz, baja a 0 en 10 Hz, vuelve a subir hasta 5 Hz en 15 Hz, etc. Los picos están en los múltiplos impares de fs/2 y los ceros en los múltiplos de fs.
</details>

**3. La frecuencia de muestreo mínima.** Con f₁ = 1, f₂ = 3 y f₃ = 7 Hz, ¿cuál es la menor fs que evita el aliasing? Baja fs poco a poco desde 30 y observa en qué orden aparecen los alias.

<details><summary>Solución</summary>
Hace falta fs > 2·7 = 14 muestras/s (la tasa de Nyquist). Por debajo de 14, el primero en aparecer es f₃. Por debajo de 6 aparece también el de f₂, y por debajo de 2, el de f₁.
</details>

**4. Dos componentes que se confunden.** Con fs = 10 muestras/s, f₂ = 3 Hz y f₃ = 7 Hz, ¿qué amplitud tiene la componente de 3 Hz de la señal reconstruida? ¿Se puede recuperar la señal original a partir de las muestras?

<details><summary>Solución</summary>
El alias de 7 Hz cae en 3 Hz y se suma a f₂: la amplitud es 0,6 + 0,4 = 1. No se puede recuperar, porque las muestras son las mismas que las de un único coseno de 3 Hz y amplitud 1. Por eso el filtro antialiasing tiene que actuar antes de muestrear.
</details>

**5. El ejercicio 1 de la hoja, a escala.** La hoja del Tema 2 muestrea 25, 150 y 50 Hz con fs = 200 Hz. Divide todas las frecuencias por 10 (2,5; 15 y 5 Hz con fs = 20) y comprueba en la herramienta el resultado del apartado c.

<details><summary>Solución</summary>
La componente de 15 Hz aparece en 5 Hz y se suma con la de 5 Hz, como en la solución de la hoja (allí, 150 Hz aparece en 50 Hz). La herramienta usa cosenos, así que no se ve el cambio de signo que sufre el seno del enunciado.
</details>

## Para profundizar

- [Apuntes del Tema 2](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%20Apuntes.pdf), sección 2 (Muestreo periódico y aliasing) y apartado 3.4 (Filtro antialiasing).
- [Transparencias T2-01](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%2001%20-%20Muestreo.pdf), «Aliasing en sinusoides», «Ejemplos de aliasing» y «Frecuencia aparente».
- [Hoja de ejercicios del Tema 2](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%20Ejercicios.pdf), ejercicios 1 a 6, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T2/codigo/python/alias_fundamental.py` y su versión en Matlab.
- A. V. Oppenheim y R. W. Schafer, *Discrete-Time Signal Processing*, 3.ª ed., Pearson, 2010, capítulo 4.
- J. H. McClellan, R. W. Schafer y M. A. Yoder, *DSP First*, 2.ª ed., Pearson, 2016, capítulo 4.

## Relación con otros conceptos

- **Frecuencias discretas equivalentes (Tema 1).** El aliasing es la versión en hercios de que Ω y Ω + 2πk son la misma frecuencia discreta. Herramienta: [Continua frente a discreta](T1-continua-discreta.html).
- **Espectro de la señal muestreada y teorema del muestreo.** Las réplicas grises son las del espectro de la señal muestreada. Herramienta: [Muestreo ideal](T2-muestreo-ideal.html).
- **Reconstrucción.** La curva roja es la salida del reconstructor ideal; con retenedores aparecen además otras distorsiones. Herramientas: [Reconstrucción](T2-reconstruccion.html) y [Retenedores](T2-retenedores.html).
- **Muestreo no ideal y filtro antialiasing.** Herramienta: [Muestreo natural y de techo plano](T2-muestreo-natural.html).
- **Diezmado (T2-04).** Reducir la frecuencia de muestreo de una secuencia produce el mismo plegado si no se filtra antes.
- **Análisis espectral con la DFT (Tema 3).** El eje de la DFT solo cubre [0, fs): una raya en k puede venir de cualquier alias. Herramienta: [DFT](T3-dft.html).
