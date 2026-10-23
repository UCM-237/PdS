## Introducción

### De la DTFT a algo que se pueda calcular

La DTFT de una secuencia de L muestras,

> X(e^{jΩ}) = Σ_{n=0}^{L−1} x[n] e^{−jΩn},

es una función continua de Ω y periódica de periodo 2π. Un ordenador solo puede guardar un número finito de valores, así que se toman N muestras equiespaciadas en una vuelta:

> X[k] = X(e^{jΩ_k}),  Ω_k = 2πk/N,  k = 0, …, N − 1.

La pregunta es si esas N muestras bastan para recuperar x[n] y, con ella, toda la DTFT.

### Muestrear en frecuencia es periodizar en el tiempo

Igual que muestrear una señal en el tiempo repite su espectro, muestrear la DTFT repite la secuencia. La secuencia de periodo N cuyos coeficientes son las X[k] es la **extensión periódica**

> x̃[n] = Σ_r x[n − rN],

la suma de copias de x[n] desplazadas múltiplos de N. Un periodo de x̃[n] es lo que devuelve la IDFT de las N muestras.

### Aliasing temporal

- Si **N ≥ L**, las copias no se tocan y un periodo de x̃[n] es exactamente x[n]: las N muestras de la DTFT contienen toda la información, y la DTFT se puede reconstruir a partir de ellas.
- Si **N < L**, las copias se solapan y se suman: es el **aliasing temporal**. Las muestras de X[k] siguen estando sobre la curva de la DTFT, pero corresponden a una secuencia más corta que no es x[n].

Es el dual exacto del teorema de muestreo: allí la condición es fs > 2B para que no se solapen las réplicas del espectro; aquí, N ≥ L para que no se solapen las copias de la secuencia.

### Secuencias infinitas

Una secuencia de duración infinita, como 0,5ⁿ u[n], siempre tiene aliasing temporal, porque las colas de las copias caen dentro de cada periodo. Su efecto disminuye al aumentar N, pero nunca desaparece del todo. Por eso la DFT de N puntos se define para secuencias de longitud N, y de ahí sale la condición que se usará en todo el tema.

## Guía de uso

- En la gráfica de arriba, haz clic o arrastra para cambiar x[n]. Solo cuentan las **L** primeras muestras; el resto se ignora.
- **N** es el número de muestras de la DTFT.
- En medio, x̃[n], la suma de copias de x[n] desplazadas N, durante cuatro periodos.
- Abajo, |X(e^{jΩ})| en gris y sus N muestras en rojo.
- El recuadro indica si hay aliasing temporal.

## Ejercicios

**1. Sin aliasing.** Con la secuencia triangular de partida, L = 9 y N = 12, ¿cómo es x̃[n]? ¿Qué cambia en la gráfica de abajo al bajar N a 9?

<details><summary>Solución</summary>
Con N = 12 cada periodo es x[n] seguido de 3 ceros. Con N = 9 las copias se tocan sin solaparse: un periodo es exactamente x[n], y la DTFT tiene solo 9 muestras. Sigue sin haber aliasing, porque N = L.
</details>

**2. Las copias se suman.** Con la misma secuencia y L = 9, baja N a 6. Calcula x̃[n] para n = 0, …, 5 y compruébalo.

<details><summary>Solución</summary>
x = (0,2; 0,4; 0,6; 0,8; 1; 0,8; 0,6; 0,4; 0,2) y x̃[n] = x[n] + x[n + 6]: (0,2 + 0,6; 0,4 + 0,4; 0,6 + 0,2; 0,8; 1; 0,8) = (0,8; 0,8; 0,8; 0,8; 1; 0,8). Ya no se reconoce el triángulo.
</details>

**3. Una sola muestra.** Con la misma secuencia, pon N = 1. ¿Qué vale x̃[n]? ¿Qué muestra de la DTFT queda?

<details><summary>Solución</summary>
x̃[n] = Σ x[n] = 5 para todo n: todas las copias se suman en cada instante. Solo queda X(e^{j0}) = Σ x[n] = 5, el valor en Ω = 0.
</details>

**4. El ejercicio 3 de la hoja.** Dibuja x = (0,1; 0,2; 0,3; 0,4; 0,5; 0,6), la secuencia de la hoja dividida por 10, con L = 6 y N = 4. ¿Qué periodo sale? ¿Cuál es el menor N que la recupera?

<details><summary>Solución</summary>
x̃ = (0,1 + 0,5; 0,2 + 0,6; 0,3; 0,4) = (0,6; 0,8; 0,3; 0,4), que es (6, 8, 3, 4)/10, como en la hoja. Hace falta N ≥ 6.
</details>

**5. El ejercicio 4 de la hoja: una secuencia que no se acaba.** Dibuja aproximadamente 0,5ⁿ (1; 0,5; 0,25; 0,125; …) con L = 16. Con N = 4, ¿cuánto vale x̃[0]? ¿Qué N hace falta para que el error sea menor que 10^{−3}?

<details><summary>Solución</summary>
x̃[0] = 1 + 0,5⁴ + 0,5⁸ + … ≈ 1/(1 − 0,5⁴) ≈ 1,067: cada valor sale un 6,7 % mayor que x[n]. El error es del orden de 0,5^{N}, así que hace falta N ≥ 10. En la herramienta, con N = 10, x̃[0] ≈ 1,001.
</details>

## Para profundizar

- [Apuntes del Tema 3](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%20Apuntes.pdf), sección 1 (De la DTFT a la DFT), «Muestrear la DTFT», y sección 2, «Extensión periódica y aliasing temporal».
- [Transparencias T3-01](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%2001%20-%20DFT.pdf), muestreo en frecuencia.
- [Hoja de ejercicios del Tema 3](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%20Ejercicios.pdf), ejercicios 3 y 4, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%20Ejercicios%20resueltos.pdf).
- A. V. Oppenheim y R. W. Schafer, *Discrete-Time Signal Processing*, 3.ª ed., Pearson, 2010, apartado 8.4.

## Relación con otros conceptos

- **Muestreo ideal (Tema 2).** El mismo fenómeno con los papeles de tiempo y frecuencia cambiados. Herramienta: [Muestreo ideal](T2-muestreo-ideal.html).
- **Serie de Fourier discreta.** Los X[k] son, salvo el factor 1/N, los coeficientes de la serie de x̃[n]. Herramienta: [Serie de Fourier](T1-serie-fourier.html).
- **DFT.** La DFT de N puntos son estas muestras. Herramienta: [DFT, fuga y relleno con ceros](T3-dft.html).
- **Convolución circular.** El aliasing temporal es lo que separa la convolución circular de la lineal. Herramienta: [Convolución circular](T3-convolucion-circular.html).
