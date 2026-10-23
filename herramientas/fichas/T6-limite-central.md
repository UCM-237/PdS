## Introducción

### La densidad de una suma

Si X e Y son independientes, la densidad de S = X + Y es la **convolución** de sus densidades:

> f_S(s) = ∫ f_X(x) f_Y(s − x) dx.

La suma de dos uniformes U[0, 1] es un triángulo; la de tres, tres trozos de parábola; y cada nueva suma suaviza más el resultado. Las medias y las varianzas se suman: S_n = X₁ + … + X_n, con X_i independientes de media μ y varianza σ², tiene media nμ y varianza nσ².

### El teorema

El **teorema del límite central** dice que la suma normalizada

> Z_n = (S_n − nμ)/(√n σ)

tiende a una gaussiana N(0, 1) cuando n → ∞, **sea cual sea la distribución de las X_i**, con tal de que tengan varianza finita. Por eso el ruido térmico, que suma la contribución de muchísimos electrones, es gaussiano; y por eso la media de N muestras de Monte Carlo es casi gaussiana.

### Qué tan deprisa

La convergencia es más rápida si la distribución de partida es simétrica. La **asimetría** E{(X − μ)³}/σ³ de Z_n es la de X dividida por √n: la exponencial (asimetría 2) necesita muchos más términos que la uniforme (asimetría 0). Las colas son lo último en converger: una suma de n uniformes está acotada y nunca llega a valores muy grandes, aunque su centro sea casi gaussiano.

### Cuando no se cumple

La distribución de **Cauchy**, f(x) = 1/(π(1 + x²)), no tiene media ni varianza: sus colas caen tan despacio que la integral de x² diverge. La media de n variables de Cauchy es otra Cauchy idéntica: promediar no sirve de nada.

## Guía de uso

- **Distribución de cada X_i**: uniforme, exponencial, Bernoulli de p = 0,2, un dado o Cauchy. A la izquierda se ve su densidad o sus probabilidades.
- **n** es el número de variables que se suman y **número de sumas** las realizaciones simuladas.
- A la derecha, el histograma de Z_n, la densidad exacta (por convolución numérica para la uniforme, la gamma para la exponencial y las probabilidades exactas, en la red de valores posibles, para las discretas) y la N(0, 1). Para Cauchy se representa la media S_n/n.
- El recuadro da μ, σ, la media, la varianza y la asimetría de las muestras, y las probabilidades P(|Z| ≤ 1) y P(|Z| > 3), comparadas con las de la gaussiana.

## Ejercicios

**1. Dos uniformes.** Con la uniforme y n = 2, ¿qué forma tiene la densidad de Z₂? ¿Por qué P(|Z| > 3) es exactamente cero?

<details><summary>Solución</summary>
Es un triángulo: la convolución de dos pulsos, como en el ejercicio 9 de la hoja. S₂ está en [0, 2], así que |Z₂| ≤ 1/(√2 · 0,289) = 2,45, y nunca pasa de 3. La gaussiana daría 0,0027.
</details>

**2. Doce uniformes.** Con n = 12 y 50 000 sumas, compara con la gaussiana. ¿Por qué Z₁₂ = S₁₂ − 6?

<details><summary>Solución</summary>
Con σ² = 1/12, √12 σ = 1: Z₁₂ = S₁₂ − 6. El histograma es casi indistinguible de N(0, 1): P(|Z| ≤ 1) = 0,680 y P(|Z| > 3) = 0,0022, frente a 0,683 y 0,0027. Es el viejo generador gaussiano de la hoja (ejercicio 9), acotado en ±6.
</details>

**3. La exponencial.** Con la exponencial, ¿cuánto vale la asimetría de las muestras con n = 1, 10 y 50? Compárala con 2/√n. ¿Qué se ve en las colas?

<details><summary>Solución</summary>
Sale 1,93, 0,60 y 0,26, frente a 2, 0,63 y 0,28. Con n = 10 el centro ya se parece a la gaussiana (P(|Z| ≤ 1) = 0,687), pero la cola derecha sigue pesando más: P(|Z| > 3) = 0,0064, más del doble que 0,0027. Con n = 50, 0,0028. La densidad exacta es una gamma.
</details>

**4. Una variable discreta.** Con la Bernoulli de p = 0,2 y n = 5 y 50, ¿qué valores puede tomar Z_n? ¿Por qué P(|Z| ≤ 1) sale tan lejos de 0,683 con n = 5?

<details><summary>Solución</summary>
S_n es binomial y solo toma n + 1 valores, separados 1/(√n σ) = 1/(0,4√n) en Z_n: 1,12 con n = 5. Con tan pocos valores, P(|Z| ≤ 1) depende de cuáles caen dentro y sale 0,41. Con n = 50 la red es más fina (0,35) y sale 0,63. El teorema habla de la distribución, no de la densidad: una variable discreta nunca tiene densidad gaussiana, pero su F se acerca a la de la gaussiana.
</details>

**5. Cauchy.** Con Cauchy, compara n = 1 y n = 50. ¿Se concentra la media? ¿Cuánto vale P(|S_n/n| ≤ 1)?

<details><summary>Solución</summary>
No se concentra: el histograma de S_n/n es el mismo para cualquier n, y P(|S_n/n| ≤ 1) = (2/π) arctan 1 = 0,5 en los dos casos (sale 0,504 y 0,500). P(|S_n/n| > 3) = 1 − (2/π) arctan 3 = 0,205. La varianza muestral sale enorme y cambia mucho de una simulación a otra, porque la verdadera es infinita.
</details>

## Para profundizar

- [Apuntes del Tema 6](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%20Apuntes.pdf), sección 2, «Suma de variables y teorema del límite central».
- [Transparencias T6-02](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%2002%20-%20Varias%20variables.pdf), suma de variables independientes.
- [Hoja de ejercicios del Tema 6](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%20Ejercicios.pdf), ejercicio 9, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%20Ejercicios%20resueltos.pdf).
- A. Papoulis y S. U. Pillai, *Probability, Random Variables and Stochastic Processes*, 4.ª ed., McGraw-Hill, 2002, apartado 7.4.

## Relación con otros conceptos

- **Convolución (Tema 1).** La densidad de la suma es la convolución de las densidades. Herramienta: [Convolución continua](T1-convolucion-continua.html).
- **Monte Carlo.** La media de N muestras es casi gaussiana, con desviación σ/√N. Herramienta: [Método de Monte Carlo](T6-monte-carlo.html).
- **Las distribuciones de partida.** Herramienta: [Distribuciones de probabilidad](T6-distribuciones.html).
- **Ruido filtrado.** La salida de un filtro es una suma ponderada de muchas muestras de ruido y tiende a ser gaussiana. Herramienta: [Ruido a través de un sistema LTI](T6-ruido-lti.html).
