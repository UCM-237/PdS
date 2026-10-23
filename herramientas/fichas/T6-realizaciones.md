## Introducción

### Una señal aleatoria es un conjunto de señales

Una **señal aleatoria** (o proceso estocástico) x[n] asigna a cada resultado de un experimento una señal entera, una **realización**. Para cada instante n fijo, x[n] es una variable aleatoria; para cada resultado fijo, es una señal determinista. El ruido de un amplificador, la voz de un hablante cualquiera o la temperatura de cada día son ejemplos: lo que se conoce no es la señal, sino su comportamiento estadístico.

### Estadísticos de conjunto

Se describen con promedios **sobre el conjunto** de realizaciones, en cada instante:

> μ_x[n] = E{x[n]},  φ_xx[n + l, n] = E{x[n + l] x[n]}.

Se estiman con muchas realizaciones: la media de los valores en el instante n, o de los productos x[n + l]x[n].

### Estacionariedad

Una señal es **estacionaria en sentido amplio** (ESA) si su media no depende de n y su autocorrelación solo depende de la separación l: φ_xx[l]. Sus estadísticos no cambian con el tiempo. Ejemplos: el ruido blanco, la sinusoide de fase aleatoria cos(Ω₀n + θ) con θ ~ U[0, 2π), o un AR(1) en régimen. Un paseo aleatorio, cuya varianza crece con n, no lo es.

### Ergodicidad

En la práctica casi nunca se tienen muchas realizaciones, sino una sola, larga. Una señal es **ergódica** (en media) si el promedio temporal de una realización tiende a la media de conjunto:

> lim_{N→∞} (1/N) Σ_{n=0}^{N−1} x[n] = μ_x.

Hace falta que la señal sea estacionaria y que «olvide» su pasado (que φ_xx[l] − μ_x² tienda a 0). Una constante aleatoria x[n] = A es estacionaria pero no ergódica: cada realización da su propio A.

## Guía de uso

- **Señal**: ruido blanco N(0, 1), un paseo aleatorio (suma de ruido blanco), la sinusoide de fase aleatoria √2 cos(0,2n + θ), un AR(1) que empieza en régimen, una constante aleatoria A ~ U[0, 1] y ruido de varianza decreciente.
- **Número de realizaciones** y **semilla**. **a** es el coeficiente del AR(1).
- Arriba a la izquierda, hasta 30 realizaciones (la primera en azul) con 200 muestras cada una. Abajo, la media de conjunto con la franja de ±1 desviación de conjunto, y el promedio temporal acumulado de la primera realización. A la derecha, la autocorrelación de conjunto en n₀ = 50 y n₀ = 150, y la teórica cuando es estacionaria.
- El recuadro dice si es estacionaria y ergódica, y da la media y la desviación de conjunto en n = 50 y 150 y el promedio temporal de la primera realización.

## Ejercicios

**1. Ruido blanco.** Con 400 realizaciones, ¿cambian la media y la desviación de conjunto entre n = 50 y n = 150? ¿Coinciden las dos autocorrelaciones? ¿Cuánto vale el promedio temporal y es razonable?

<details><summary>Solución</summary>
Media 0,02 y 0,01, desviación 0,99 y 1,03: no cambian, salvo el error de estimar con 400 realizaciones (del orden de 1/√400 = 0,05). Las dos autocorrelaciones son δ[l]. El promedio temporal de una realización de 200 muestras es 0,13, a menos de dos veces su error típico 1/√200 = 0,07. Es estacionaria y ergódica.
</details>

**2. Paseo aleatorio.** Con el paseo aleatorio, ¿cuánto vale la desviación de conjunto en n = 50 y n = 150? Compárala con la teórica. ¿Tiene sentido su promedio temporal?

<details><summary>Solución</summary>
6,75 y 12,8, frente a √50 = 7,1 y √150 = 12,2: la varianza crece como n, como en el ejercicio 12 de la hoja. No es estacionaria. El promedio temporal de la primera realización, 17,8, no estima nada: la media de conjunto es 0 en todos los instantes, pero cada realización se aleja cada vez más.
</details>

**3. Sinusoide de fase aleatoria.** ¿Es estacionaria? Compara la autocorrelación de conjunto con la teórica. ¿Por qué cada realización es una sinusoide perfecta y, sin embargo, la media de conjunto es nula en todos los instantes?

<details><summary>Solución</summary>
Sí: media 0 y φ_xx[l] = cos(0,2l) (con amplitud √2, potencia 1) en n₀ = 50 y en n₀ = 150. En cada instante, las fases están repartidas uniformemente y los valores se compensan: la media de conjunto es 0 aunque ninguna realización lo sea. Es ergódica en media (el promedio temporal es 0,02), como en el apartado b del ejercicio 11 de la hoja. Su autocorrelación no se amortigua, porque cada realización recuerda su fase para siempre.
</details>

**4. El AR(1).** Con a = 0,8, ¿qué desviación de conjunto se espera? ¿Cómo es la autocorrelación? ¿Qué cambia con a = −0,8?

<details><summary>Solución</summary>
σ_x² = 1/(1 − a²) = 2,78, σ_x = 1,67; con las muestras, 1,69 y 1,57. φ_xx[l] = 2,78 · 0,8^{|l|}, una exponencial que decae: las muestras próximas se parecen. Con a = −0,8 la potencia es la misma, pero φ_xx alterna de signo y las realizaciones cambian de signo casi en cada muestra. Es el ejercicio 13 de la hoja.
</details>

**5. Constante aleatoria.** Con x[n] = A, A ~ U[0, 1], ¿cuánto valen la media y la autocorrelación de conjunto? ¿Es estacionaria? ¿Y ergódica?

<details><summary>Solución</summary>
Media 1/2 (sale 0,48) y φ_xx[l] = E{A²} = 1/3 para todo l: es estacionaria. Pero el promedio temporal de cada realización es su propio A (0,63 en la primera) y no tiende a 1/2: no es ergódica. Como φ_xx[l] − μ² = 1/12 no tiende a 0, la señal no olvida nunca. Es el apartado c del ejercicio 11 de la hoja.
</details>

**6. Varianza decreciente.** Con σ[n] = 0,99^{n}, ¿qué desviación de conjunto hay en n = 50 y n = 150? ¿Por qué no es estacionaria aunque sus muestras sean independientes y de media nula?

<details><summary>Solución</summary>
0,99^{50} = 0,61 y 0,99^{150} = 0,22 (salen 0,60 y 0,23). Tener media constante no basta: la autocorrelación en l = 0, que es la varianza, depende de n. Las dos autocorrelaciones de conjunto son deltas de distinta altura.
</details>

## Para profundizar

- [Apuntes del Tema 6](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%20Apuntes.pdf), sección 3, «Definición y descripción», «Estacionariedad» y «Ergodicidad».
- [Transparencias T6-03](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%2003%20-%20Se%C3%B1ales%20aleatorias.pdf), estacionariedad, sinusoide de fase aleatoria y ergodicidad.
- [Hoja de ejercicios del Tema 6](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%20Ejercicios.pdf), ejercicios 11 a 13, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%20Ejercicios%20resueltos.pdf).
- A. Papoulis y S. U. Pillai, *Probability, Random Variables and Stochastic Processes*, 4.ª ed., McGraw-Hill, 2002, capítulos 9 y 12.

## Relación con otros conceptos

- **Estimar la autocorrelación con una sola realización.** Herramienta: [Estimación de la autocorrelación](T6-autocorrelacion.html).
- **Promedios y Monte Carlo.** La ergodicidad permite sustituir realizaciones por tiempo. Herramienta: [Método de Monte Carlo](T6-monte-carlo.html).
- **Ruido filtrado.** El AR(1) es ruido blanco a través de un IIR de primer orden. Herramienta: [Ruido a través de un sistema LTI](T6-ruido-lti.html).
- **Variables aleatorias.** Cada instante es una. Herramienta: [Distribuciones de probabilidad](T6-distribuciones.html).
