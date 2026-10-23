## Introducción

### Calcular una esperanza con muestras

Muchas cantidades se pueden escribir como una esperanza: una integral, una probabilidad (la esperanza de una indicatriz 1{X ∈ A}), la tasa de error de un receptor o la potencia de una señal. El **método de Monte Carlo** genera N muestras independientes X_i de la distribución y aproxima

> E{h(X)} ≈ μ̂_N = (1/N) Σ_i h(X_i).

La estimación es **insesgada**, E{μ̂_N} = E{h(X)}, y su varianza es σ²/N, con σ² = Var{h(X)}: el **error típico** es σ/√N. Por el teorema del límite central, μ̂_N es casi gaussiana, y el valor verdadero cae en μ̂_N ± 2σ/√N el 95 % de las veces. σ también se estima con las muestras.

### Lento pero robusto

El error baja como 1/√N, sea cual sea la dimensión del problema: para ganar una cifra decimal hay que multiplicar N por 100. En una dimensión, una regla de cuadratura es mucho mejor; en muchas dimensiones (integrales sobre el estado de un sistema, la trayectoria de un fotón, el ruido de un canal), Monte Carlo suele ser lo único viable.

### Sucesos raros y muestreo de importancia

Para estimar una probabilidad pequeña p, el error relativo es √(p(1 − p)/N)/p ≈ 1/√(Np): hacen falta muchas muestras por cada suceso observado. El **muestreo de importancia** genera las muestras de otra densidad g que ponga más probabilidad en la zona que interesa, y corrige con el peso f/g:

> E_f{h(X)} = E_g{h(Y) f(Y)/g(Y)}.

Si g se parece a h f, la varianza puede bajar en órdenes de magnitud.

## Guía de uso

- **Qué se estima**:
  - π, con la fracción de puntos uniformes del cuadrado unidad que caen en el cuarto de círculo (multiplicada por 4).
  - E{cos X} con X ~ N(0, 1), que vale e^{−1/2} = 0,6065.
  - ∫₀¹ e^{−x²} dx = 0,746824, como la media de e^{−X²} con X ~ U[0, 1].
  - P(X > 3) = 0,00135 con X ~ N(0, 1), contando las muestras de la cola.
  - La misma probabilidad con muestreo de importancia: Y ~ N(3, 1) y el peso φ(y)/φ(y − 3) = e^{4,5 − 3y}.
- **N** y la **realización**.
- A la izquierda, las primeras 2000 muestras (en rojo las que cuentan, en los casos de indicatriz). En el centro, la estimación con las n primeras muestras, la franja ±2σ̂/√n y el valor exacto. Abajo, el error de cinco realizaciones en escala doble logarítmica frente a σ/√n.
- El recuadro da el valor exacto, la estimación, el error y el error típico.

## Ejercicios

**1. Estimar π.** Con N = 10 000, ¿qué estimación sale y cuál es el error típico? ¿Cuántas muestras harían falta para acertar la tercera cifra decimal con un 95 % de probabilidad?

<details><summary>Solución</summary>
Sale 3,1296, con error típico 0,0164: h vale 4 con probabilidad π/4 y 0 si no, así que σ = 4√(π/4 (1 − π/4)) = 1,64. Para que 1,96σ/√N ≤ 0,001 hacen falta N ≥ 1,04 · 10^{7} muestras. Con N = 100 000 sale 3,1380, a 0,7 errores típicos. Es el ejercicio 5 de la hoja con otra σ.
</details>

**2. La pendiente del error.** Mira la gráfica de abajo para cualquiera de los problemas. ¿Qué pendiente tiene la recta σ/√n en escala doble logarítmica? ¿Siguen esa recta las cinco realizaciones?

<details><summary>Solución</summary>
Pendiente −1/2: una década en n baja el error media década, un factor √10 ≈ 3,2. Las realizaciones oscilan alrededor de la recta, a veces por encima y a veces muy por debajo (cuando la estimación cruza el valor exacto), pero siguen la misma tendencia. El error de una realización concreta es aleatorio; lo que baja como 1/√n es su tamaño típico.
</details>

**3. Una integral.** Para ∫₀¹ e^{−x²} dx, ¿cuál es σ? Compara el error relativo típico con N = 10 000 con el de la regla del trapecio con 10 000 puntos.

<details><summary>Solución</summary>
σ² = E{e^{−2X²}} − I² = 0,5981 − 0,5577 = 0,0404, σ = 0,201, y el error típico con N = 10 000 es 0,002 (el 0,27 %). El trapecio con 10 000 puntos tiene un error del orden de h²/12 · |f″| ≈ 10^{−9}. En una dimensión Monte Carlo no compite; su ventaja aparece en integrales de muchas variables, donde una rejilla necesitaría un número de puntos exponencial en la dimensión.
</details>

**4. Un suceso raro.** Estima P(X > 3) con N = 10 000 y N = 100 000. ¿Qué error relativo típico tiene cada estimación? ¿Cuántas muestras harían falta para un 1 %?

<details><summary>Solución</summary>
Solo una muestra de cada 741 cae en la cola: con 10 000 se cuentan unas 13 y el error relativo típico es del 27 %; con 100 000, del 8,6 %. Para un 1 % hace falta (1/0,01)²/p ≈ 7,4 · 10^{6} muestras. Así se estiman las tasas de error de bit de un sistema de comunicaciones (10^{−6} o menos) y por eso se necesitan otros métodos.
</details>

**5. Muestreo de importancia.** Repite con el muestreo de importancia y N = 10 000. ¿Qué error relativo se obtiene? ¿Por cuánto se divide la varianza? ¿Por qué se elige N(3, 1)?

<details><summary>Solución</summary>
El 1,8 %, mejor que el 8,6 % con 100 000 muestras normales. La varianza baja unas 218 veces: para el 1 % bastan unas 34 000 muestras en lugar de 7,4 millones. N(3, 1) pone la mitad de las muestras en la cola, y el peso e^{4,5 − 3y}, pequeño allí, compensa que se hayan generado con demasiada frecuencia. Una g mal elegida (por ejemplo, centrada en 6) daría pesos muy desiguales y una varianza mayor.
</details>

## Para profundizar

- [Apuntes del Tema 6](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%20Apuntes.pdf), sección 1, «Muestreo de variables aleatorias» y «Análisis de muestras».
- [Transparencias T6-01](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%2001%20-%20Variables%20aleatorias.pdf), generación de muestras y Monte Carlo.
- [Hoja de ejercicios del Tema 6](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%20Ejercicios.pdf), ejercicio 5, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%20Ejercicios%20resueltos.pdf).
- C. P. Robert y G. Casella, *Monte Carlo Statistical Methods*, 2.ª ed., Springer, 2004, capítulo 3.
- M. C. Jeruchim, P. Balaban y K. S. Shanmugan, *Simulation of Communication Systems*, 2.ª ed., Kluwer, 2000, capítulo 11 (sucesos raros y muestreo de importancia).

## Relación con otros conceptos

- **Generar las muestras.** Herramienta: [Generación de muestras aleatorias](T6-generacion-muestras.html).
- **Por qué la estimación es casi gaussiana.** Herramienta: [Teorema del límite central](T6-limite-central.html).
- **Estimadores y su varianza.** El mismo 1/√N aparece al estimar la DEP. Herramienta: [Periodograma y método de Welch](T6-periodograma-welch.html).
- **Ergodicidad.** Promediar en el tiempo en lugar de sobre realizaciones. Herramienta: [Realizaciones, estacionariedad y ergodicidad](T6-realizaciones.html).
