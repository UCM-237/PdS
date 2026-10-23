## Introducción

### La autocorrelación

La **autocorrelación** de una señal estacionaria,

> φ_xx[l] = E{x[n + l] x[n]},

mide cuánto se parecen dos muestras separadas l posiciones. Es par, φ_xx[−l] = φ_xx[l]; su máximo está en l = 0, donde vale la potencia media E{x²[n]}; y si la señal tiene media μ y olvida su pasado, tiende a μ² para |l| grande. La **autocovarianza** es φ_xx[l] − μ².

Algunos ejemplos: el ruido blanco de media nula y varianza σ² tiene φ_xx[l] = σ²δ[l]; un ruido i.i.d. de media μ, μ² + σ²δ[l]; un AR(1) x[n] = a x[n−1] + w[n], σ_w² a^{|l|}/(1 − a²); una sinusoide de fase aleatoria de amplitud A, (A²/2) cos(Ω₀l).

### Estimarla con una realización

Si la señal es ergódica, la esperanza se sustituye por un promedio temporal sobre la única realización disponible, de N muestras. Para la separación l solo hay N − |l| productos:

- **Insesgado**: φ̂_i[l] = (1/(N − |l|)) Σ_n x[n + |l|] x[n]. Su media es φ_xx[l], pero para |l| cerca de N promedia muy pocos productos y su varianza es enorme.
- **Sesgado**: φ̂_s[l] = (1/N) Σ_n x[n + |l|] x[n] = (1 − |l|/N) φ̂_i[l]. Está sesgado hacia 0 (multiplicado por una ventana triangular), pero tiene menos varianza y su DTFT nunca es negativa: es el periodograma. Es el que devuelven `xcorr(x, 'biased')` en Matlab y `np.correlate(x, x, 'full')/N` en Python.

Con la FFT, la suma de todos los productos cuesta O(N log N): basta rellenar con ceros hasta 2N y calcular la IDFT de |X[k]|².

## Guía de uso

- **Señal**: ruido i.i.d. N(5, 1) o U[2, 6] (con media no nula), un AR(1), una sinusoide de fase aleatoria de frecuencia 0,15 con ruido, o ruido blanco N(0, 1).
- **a** es el coeficiente del AR(1), **N** el número de muestras y **separación máxima** la parte de la gráfica que se dibuja.
- Arriba, la realización. Abajo, las dos estimaciones y la teórica. Los botones muestran una, otra o las dos.
- El recuadro da φ̂[0], los dos estimadores en l = 5 y en una separación cercana a N, y la media y la varianza de la realización.

## Ejercicios

**1. Media no nula.** Con el ruido N(5, 1) y N = 512, ¿cuánto vale la autocorrelación teórica en l = 0 y en l ≠ 0? ¿Qué hace cada estimador cerca de l = N?

<details><summary>Solución</summary>
φ_xx[0] = μ² + σ² = 26 y φ_xx[l] = μ² = 25 para l ≠ 0: un pico de altura σ² sobre un pedestal μ². El sesgado decae linealmente hasta 0 (en l = 460 vale 2,6) porque se multiplica por 1 − |l|/N; el insesgado sigue en 25,3. Aquí el insesgado acierta, porque la señal varía poco alrededor de 5.
</details>

**2. La uniforme de la hoja.** Con U[2, 6], ¿qué valores teóricos hay en l = 0 y l ≠ 0? Compáralos con el ejercicio 2 de la hoja.

<details><summary>Solución</summary>
E{X²} = μ² + σ² = 16 + 4/3 = 17,33 en l = 0 y μ² = 16 en l ≠ 0. Con esta realización salen 16,9 y 15,5: la media de la realización es 3,94 en lugar de 4, y ese error se multiplica en μ². Por eso suele restarse la media y estimar la autocovarianza.
</details>

**3. El AR(1).** Con a = 0,9 y N = 512, compara φ̂[0] y φ̂[5] con los teóricos. ¿Mejora con N = 4096? ¿Por qué el AR(1) necesita más muestras que el ruido blanco?

<details><summary>Solución</summary>
Teóricos: 1/(1 − 0,81) = 5,26 y 5,26 · 0,9⁵ = 3,11. Con N = 512 salen 4,31 y 2,23; con N = 4096, 5,22 y 2,87. Las muestras de un AR(1) con a = 0,9 están muy correladas (tardan unas 1/(1 − a) = 10 muestras en olvidarse), así que N muestras valen como unas N(1 − a)/(1 + a) independientes, unas 27 con N = 512. Con el ruido blanco, N = 512 da φ̂[0] = 1,005.
</details>

**4. Los extremos.** Con el AR(1) y N = 512, mira el insesgado en las separaciones grandes. ¿Por qué oscila tanto? ¿Cuántos productos promedia en l = 460?

<details><summary>Solución</summary>
En l = 460 solo hay 52 productos, y además están correlados entre sí: el insesgado vale −1,13 donde el teórico es 0. Su varianza crece como 1/(N − |l|). El sesgado vale −0,12: tiene sesgo, pero cerca de los extremos lo multiplica por (N − |l|)/N y lo lleva a 0. Por eso se suele usar el sesgado y mirar solo |l| ≪ N.
</details>

**5. AR(1) con a negativo.** Con a = −0,9, ¿cómo es φ_xx[l]? ¿Qué signo tiene en l = 5?

<details><summary>Solución</summary>
φ_xx[l] = 5,26 (−0,9)^{|l|}: alterna de signo. En l = 5 es negativa, −3,11 (estimada, −2,65). La señal cambia de signo casi en cada muestra: es ruido de alta frecuencia. Es el apartado c del ejercicio 13 de la hoja.
</details>

**6. Una sinusoide escondida.** Con la sinusoide de fase aleatoria y ruido, ¿qué se ve en la autocorrelación que no se ve en la señal? ¿Cuánto vale φ_xx[0] y por qué?

<details><summary>Solución</summary>
φ_xx[l] = cos(0,15l) + 0,25δ[l]: el ruido solo aporta un pico en l = 0, y para l ≠ 0 queda una cosinusoide perfecta, de periodo 2π/0,15 = 42 muestras, aunque en la señal se vea ruidosa. φ_xx[0] = 1 + 0,25 = 1,25: la potencia de la sinusoide (A²/2 = 1) más la del ruido (0,5²). Así se detectan periodicidades enterradas en ruido.
</details>

## Para profundizar

- [Apuntes del Tema 6](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%20Apuntes.pdf), sección 3, «Autocorrelación».
- [Transparencias T6-03](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%2003%20-%20Se%C3%B1ales%20aleatorias.pdf), estimar la autocorrelación y AR(1).
- [Hoja de ejercicios del Tema 6](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%20Ejercicios.pdf), ejercicios 11 a 13, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%20Ejercicios%20resueltos.pdf).
- M. H. Hayes, *Statistical Digital Signal Processing and Modeling*, Wiley, 1996, apartados 3.3 y 8.2.

## Relación con otros conceptos

- **Promedios de conjunto y temporales.** Herramienta: [Realizaciones, estacionariedad y ergodicidad](T6-realizaciones.html).
- **La correlación cruzada.** Herramienta: [Estimación de un retardo por correlación](T6-retardo-correlacion.html).
- **La DEP.** La DTFT del estimador sesgado es el periodograma. Herramienta: [Periodograma y método de Welch](T6-periodograma-welch.html).
- **Convolución (Tema 1).** La autocorrelación es la convolución de x con x[−n]. Herramienta: [Convolución discreta](T1-convolucion-discreta.html).
