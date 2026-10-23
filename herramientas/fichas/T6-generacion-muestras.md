## Introducción

### Todo empieza con uniformes

Un ordenador genera números **pseudoaleatorios**: una sucesión determinista (la fija la semilla) que se comporta como muestras independientes de U[0, 1). A partir de ellas se obtienen muestras de cualquier otra distribución. Así se simulan ruido, canales, errores de medida o métodos de Monte Carlo.

### La ruleta (variables discretas)

Para una variable que toma los valores x₁ < x₂ < … con probabilidades p_i, se reparte [0, 1) en tramos consecutivos de longitud p_i y se devuelve x_i si u cae en el tramo i, es decir, si F_X(x_{i−1}) ≤ u < F_X(x_i). Cada valor sale con la probabilidad de su tramo.

### El método de la inversa

Si F_X es continua y creciente, X = F_X^{−1}(U) tiene distribución F_X, porque P(F_X^{−1}(U) ≤ x) = P(U ≤ F_X(x)) = F_X(x). Por ejemplo:

- Exponencial: F_X(x) = 1 − e^{−λx}, así que x = −ln(1 − u)/λ.
- Rayleigh: F_X(x) = 1 − e^{−x²/(2σ²)}, así que x = σ√(−2 ln(1 − u)).

### Box-Muller

La gaussiana no tiene F^{−1} en forma cerrada. Pero un par de gaussianas independientes (Z₁, Z₂) tiene, en polares, un radio Rayleigh y un ángulo uniforme independientes. Con dos uniformes,

> R = √(−2 ln U₁), Θ = 2πU₂, Z₁ = R cos Θ, Z₂ = R sen Θ,

y σZ_i es N(0, σ²).

### Aceptación y rechazo

Si se sabe muestrear una densidad q(x) y f(x) ≤ M q(x) en todo x, se genera un candidato x de q y un u uniforme, y se acepta x si u M q(x) ≤ f(x). Las aceptadas siguen f. La fracción aceptada es 1/M: conviene que M q se ajuste a f lo más posible.

### Mezclas

Una mezcla f(x) = Σ_k π_k f_k(x) se muestrea en dos pasos: se elige la componente k con la ruleta de probabilidades π_k y se genera una muestra de f_k.

## Guía de uso

- **Método y distribución**: ruleta (dado cargado, binomial), inversa (exponencial, Rayleigh), Box-Muller, rechazo con propuesta uniforme (dos densidades beta) y una mezcla de N(3; 0,5²) y N(6, 1).
- **Parámetro**: su significado cambia con el método y aparece en el título del deslizador (p de la binomial, λ, σ, M del rechazo o π₁ de la mezcla). Al cambiar de método toma un valor razonable.
- A la izquierda se ve cómo se genera: los u y su valor por la ruleta o la inversa (flechas), los pares de Box-Muller o los candidatos del rechazo, en verde los aceptados. A la derecha, el histograma normalizado y la densidad o las probabilidades teóricas.
- El recuadro compara la media y la varianza muestrales con las teóricas y da datos propios de cada método.

## Ejercicios

**1. El dado cargado.** Con la ruleta del dado cargado (el seis sale la mitad de las veces), ¿qué valor sale para u = 0,37 y para u = 0,62? ¿Cuánto valen la media y la varianza teóricas?

<details><summary>Solución</summary>
F_X vale 0,1, 0,2, 0,3, 0,4, 0,5 y 1. Para u = 0,37, 0,3 ≤ u < 0,4 y sale un 4; para u = 0,62, 0,5 ≤ u < 1 y sale un 6. La media es 4,5 y la varianza 3,25, como en el ejercicio 1 de la hoja; con 2000 muestras salen 4,48 y 3,31.
</details>

**2. La exponencial.** Con la inversa y λ = 2, ¿qué valores teóricos tienen la media, la varianza y P(X > 1)? Compáralos con los de las muestras. ¿Cómo se comprueba que la fórmula usada es la buena?

<details><summary>Solución</summary>
Media 1/λ = 0,5, varianza 1/λ² = 0,25 y P(X > 1) = e^{−2} = 0,135; con 2000 muestras salen 0,486, 0,238 y 0,124. Se comprueba con F: P(X ≤ x) = P(−ln(1 − U)/λ ≤ x) = P(U ≤ 1 − e^{−λx}) = 1 − e^{−λx}.
</details>

**3. Box-Muller.** Con σ = 1, ¿qué fracción de muestras cae a menos de una desviación típica? ¿Están correlacionadas z₁ y z₂? ¿Qué distribución tiene el radio de los pares?

<details><summary>Solución</summary>
Sale 0,694, cerca de la teórica 0,683, y la correlación muestral de los pares, −0,016, es compatible con cero (su desviación típica con 1000 pares es 1/√1000 ≈ 0,03). El radio es Rayleigh de parámetro σ: es la misma fórmula que el método de la inversa para la Rayleigh, como en el ejercicio 4 de la hoja.
</details>

**4. Aceptación y rechazo.** Con f(x) = 6x(1 − x), ¿cuál es la menor M válida? ¿Qué fracción se acepta con M = 1,5 y con M = 3? ¿Qué pasa con M = 1?

<details><summary>Solución</summary>
El máximo de f está en x = 1/2 y vale 1,5: M = 1,5. Se acepta el 66 % (teórico 2/3) y con M = 3 el 34 % (teórico 1/3): las muestras siguen igual de bien f, pero se gastan el doble de candidatos. Con M = 1 la recta no cubre la parábola entre 0,21 y 0,79, se aceptan todos los candidatos de esa zona y el histograma queda plano por arriba: la varianza sale 0,058 en lugar de 0,05.
</details>

**5. Una densidad con pico.** Con f(x) = 30x(1 − x)⁴, ¿cuál es la menor M? ¿Por qué se acepta menos que con la anterior? ¿Qué propuesta lo mejoraría?

<details><summary>Solución</summary>
El máximo está en x = 1/5: f(0,2) = 30 · 0,2 · 0,8⁴ = 2,46. Con M = 2,5 se acepta el 40 %. La densidad es más puntiaguda, y la caja uniforme desperdicia mucho espacio a la derecha. Una propuesta que se parezca más a f (por ejemplo, una que decrezca hacia x = 1) necesitaría una M menor.
</details>

**6. La mezcla.** Con π₁ = 0,4, calcula la media y la varianza de la mezcla. ¿Por qué la varianza es mayor que la de cada componente?

<details><summary>Solución</summary>
μ = 0,4 · 3 + 0,6 · 6 = 4,8; E{X²} = 0,4 (0,25 + 9) + 0,6 (1 + 36) = 25,9; σ² = 25,9 − 4,8² = 2,86. Sale 4,81 y 2,88. La varianza de una mezcla es la media de las varianzas (0,7) más la varianza de las medias (0,4 · 1,8² + 0,6 · 1,2² = 2,16): la separación entre las dos gaussianas añade dispersión.
</details>

## Para profundizar

- [Apuntes del Tema 6](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%20Apuntes.pdf), sección 1, «Muestreo de variables aleatorias».
- [Transparencias T6-01](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%2001%20-%20Variables%20aleatorias.pdf), generar muestras con el ordenador.
- [Hoja de ejercicios del Tema 6](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%20Ejercicios.pdf), ejercicios 1 y 4, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%20Ejercicios%20resueltos.pdf).
- C. P. Robert y G. Casella, *Monte Carlo Statistical Methods*, 2.ª ed., Springer, 2004, capítulo 2.
- L. Devroye, *Non-Uniform Random Variate Generation*, Springer, 1986.

## Relación con otros conceptos

- **Las distribuciones.** Herramienta: [Distribuciones de probabilidad](T6-distribuciones.html).
- **Monte Carlo.** Para qué sirven las muestras. Herramienta: [Método de Monte Carlo](T6-monte-carlo.html).
- **Ecualización (Tema 5).** Aplicar F en lugar de F^{−1}. Herramienta: [Histograma y operaciones puntuales](T5-histograma.html).
- **La gaussiana en dos dimensiones.** Herramienta: [Gaussiana bivariante](T6-gaussiana-bivariante.html).
