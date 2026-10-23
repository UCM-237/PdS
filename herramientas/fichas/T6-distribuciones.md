## Introducción

### Variable aleatoria y función de distribución

Una **variable aleatoria** X asigna un número a cada resultado de un experimento. Queda descrita por su **función de distribución**

> F_X(x) = P(X ≤ x),

que crece de 0 a 1. Si X es **discreta** (toma valores aislados x_i), F_X es una escalera con saltos de altura p_X(x_i) = P(X = x_i), su función de probabilidad. Si es **continua**, F_X es continua y su derivada es la **densidad** f_X(x) = F_X′(x): P(a < X ≤ b) = ∫_a^b f_X(x) dx = F_X(b) − F_X(a).

### Media y varianza

La **media** μ_X = E{X} = ∫ x f_X(x) dx (o Σ x_i p_X(x_i)) es el centro de masas de la distribución. La **varianza** σ_X² = E{(X − μ_X)²} = E{X²} − μ_X² mide su dispersión, y σ_X es la desviación típica, en las mismas unidades que X.

### Distribuciones habituales

| Distribución | Densidad o probabilidad | Media | Varianza |
|---|---|---|---|
| Uniforme U[a, b] | 1/(b − a) en [a, b] | (a + b)/2 | (b − a)²/12 |
| Normal N(μ, σ²) | e^{−(x−μ)²/(2σ²)}/(σ√(2π)) | μ | σ² |
| Exponencial | λe^{−λx}, x ≥ 0 | 1/λ | 1/λ² |
| Rayleigh | (x/σ²)e^{−x²/(2σ²)}, x ≥ 0 | σ√(π/2) | (2 − π/2)σ² |
| Laplace | e^{−\|x−μ\|/s}/(2s) | μ | 2s² |
| Binomial B(n, p) | C(n, k) p^{k}(1 − p)^{n−k} | np | np(1 − p) |
| Poisson | e^{−λ}λ^{k}/k! | λ | λ |

### Estimar a partir de muestras

Con N muestras, la proporción de las que caen en cada intervalo de anchura Δ, dividida entre Δ, es el **histograma normalizado**, que estima f_X. La proporción de muestras menores o iguales que x es la **distribución empírica** F_N(x), que estima F_X. La media muestral estima μ_X con un error típico σ/√N, y la máxima diferencia entre F_N y F_X también baja como 1/√N (teorema de Glivenko-Cantelli y prueba de Kolmogórov-Smirnov).

## Guía de uso

- **Distribución** y sus parámetros: los títulos de los deslizadores cambian con la distribución, y los que no se usan se ocultan.
- **N** es el número de muestras, **intervalos** los del histograma (solo para las continuas) y **realización** cambia la semilla.
- A la izquierda, el histograma normalizado y la densidad teórica (o las frecuencias relativas y las probabilidades, para las discretas). A la derecha, la distribución empírica y la teórica.
- El recuadro compara la media y la varianza teóricas con las muestrales, da el error típico de la media y la máxima distancia entre F_N y F.

## Ejercicios

**1. Más muestras.** Con N(0, 1), prueba N = 100, 1000, 10 000 y 100 000. ¿Cómo bajan el error de la media y la distancia entre F_N y F?

<details><summary>Solución</summary>
Con esta realización, la media muestral vale 0,21, −0,005, −0,003 y 0,001, y la distancia entre F_N y F, 0,13, 0,03, 0,007 y 0,002. Los dos errores bajan como 1/√N: 0,1, 0,03, 0,01 y 0,003. Multiplicar N por 100 da una cifra decimal más.
</details>

**2. La uniforme.** Elige U[2, 6] (a = 2, anchura 4) con N = 10 000. ¿Qué media, varianza y P(X > 5) tiene? Compáralas con las muestras y con la gráfica de F.

<details><summary>Solución</summary>
μ = 4, σ² = 16/12 = 4/3 y P(X > 5) = 1 − F(5) = 1/4: en la gráfica de F, F(5) = 0,75. Las muestras dan 3,993 y 1,332. Es el ejercicio 2 de la hoja.
</details>

**3. Los intervalos del histograma.** Con N(0, 1) y N = 1000, prueba 5, 30 y 100 intervalos. ¿Qué pasa en cada caso? ¿Por qué con N = 100 000 se pueden usar más?

<details><summary>Solución</summary>
Con 5 intervalos, de anchura 1,6, el histograma es demasiado grueso y aplasta el pico (sesgo). Con 100, cada uno recoge unas pocas muestras y las barras fluctúan mucho (varianza). Con N mayor cada intervalo recibe más muestras, la fluctuación relativa baja como 1/√(número de muestras del intervalo) y se pueden usar intervalos más estrechos. Una regla habitual es tomar unos √N intervalos.
</details>

**4. La binomial y la Poisson.** Compara B(60; 0,05) con la Poisson de λ = 3 y N = 10 000. ¿Qué medias y varianzas tienen? ¿Por qué se parecen tanto?

<details><summary>Solución</summary>
La binomial tiene media np = 3 y varianza np(1 − p) = 2,85; la Poisson, 3 y 3. Sus probabilidades casi coinciden: cuando n es grande y p pequeño con np = λ fijo, la binomial tiende a la Poisson. Por eso la Poisson modela el número de sucesos raros (fotones, llegadas a una cola) en un intervalo.
</details>

**5. Misma varianza, distinta forma.** Compara N(0, 1) con la Laplace de media 0 y escala s = 0,71. ¿Qué varianza tiene la Laplace? ¿En qué se diferencian sus densidades?

<details><summary>Solución</summary>
2s² = 2 · 0,71² ≈ 1: la misma que la normal. La Laplace tiene un pico más agudo en 0 y colas más pesadas (decaen como e^{−|x|/s}, no como e^{−x²/2}): da más valores muy pequeños y más valores grandes. La media y la varianza no bastan para describir una distribución.
</details>

**6. La Rayleigh.** Con σ = 1, ¿cuánto valen la media y la varianza? ¿Dónde aparece esta distribución?

<details><summary>Solución</summary>
σ√(π/2) = 1,253 y (2 − π/2) = 0,429; las muestras dan 1,251 y 0,427. Es la distribución del módulo √(X² + Y²) de dos gaussianas independientes de media nula y la misma varianza: la amplitud de un ruido de banda estrecha o la envolvente de una señal de radio con desvanecimiento.
</details>

## Para profundizar

- [Apuntes del Tema 6](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%20Apuntes.pdf), sección 1, «Variable aleatoria», «Esperanza, media y varianza», «Distribuciones habituales» y «Análisis de muestras».
- [Transparencias T6-01](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%2001%20-%20Variables%20aleatorias.pdf), variables aleatorias y distribuciones.
- [Hoja de ejercicios del Tema 6](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%20Ejercicios.pdf), ejercicios 1 a 3 y 5, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%20Ejercicios%20resueltos.pdf).
- A. Papoulis y S. U. Pillai, *Probability, Random Variables and Stochastic Processes*, 4.ª ed., McGraw-Hill, 2002, capítulos 4 y 5.

## Relación con otros conceptos

- **Cómo se generan las muestras.** Herramienta: [Generación de muestras aleatorias](T6-generacion-muestras.html).
- **Error de la media muestral.** Herramienta: [Método de Monte Carlo](T6-monte-carlo.html).
- **Sumas de variables.** Herramienta: [Teorema del límite central](T6-limite-central.html).
- **El histograma de una imagen (Tema 5).** Herramienta: [Histograma y operaciones puntuales](T5-histograma.html).
