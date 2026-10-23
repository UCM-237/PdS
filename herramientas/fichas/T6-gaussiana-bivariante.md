## Introducción

### Dos variables a la vez

Dos variables aleatorias X₁ y X₂ quedan descritas por su densidad conjunta f(x₁, x₂). De ella salen las **marginales**, integrando la otra variable, f₁(x₁) = ∫ f(x₁, x₂) dx₂, y las **condicionadas**, f(x₂ | x₁) = f(x₁, x₂)/f₁(x₁): la distribución de X₂ cuando se sabe que X₁ = x₁. Son **independientes** si f(x₁, x₂) = f₁(x₁) f₂(x₂), es decir, si conocer una no cambia la distribución de la otra.

### Covarianza y correlación

La **covarianza** C₁₂ = E{(X₁ − μ₁)(X₂ − μ₂)} y el **coeficiente de correlación** ρ = C₁₂/(σ₁σ₂), entre −1 y 1, miden la dependencia **lineal**: ρ = ±1 si X₂ es función lineal de X₁. Si son independientes, ρ = 0. Lo contrario no es cierto en general: dos variables pueden ser incorreladas y dependientes.

### La gaussiana bivariante

La gaussiana de media nula y matriz de covarianza

> Σ = [σ₁², ρσ₁σ₂; ρσ₁σ₂, σ₂²]

tiene densidad f(x) = e^{−xᵀΣ^{−1}x/2}/(2π√det Σ). Sus curvas de nivel son **elipses** con los ejes en los autovectores de Σ y semiejes proporcionales a la raíz de los autovalores. Tiene propiedades que la hacen única:

- Las marginales son gaussianas, N(0, σ₁²) y N(0, σ₂²).
- La condicionada también: X₂ | X₁ = c es N(ρσ₂c/σ₁, σ₂²(1 − ρ²)). La media es la recta de regresión y la varianza no depende de c.
- **Incorreladas implica independientes**: si ρ = 0, Σ es diagonal y la densidad se factoriza.

### Generar muestras

Con la factorización de **Cholesky** Σ = LLᵀ, L triangular inferior, y z con dos N(0, 1) independientes, x = Lz tiene covarianza LLᵀ = Σ. En dos dimensiones, L = [σ₁, 0; ρσ₂, σ₂√(1 − ρ²)].

## Guía de uso

- **Ejemplo**: la gaussiana bivariante o dos ejemplos de variables incorreladas y dependientes (una parábola y un anillo).
- **σ₁, σ₂ y ρ** fijan Σ en la gaussiana. **Condición x₁ = c** coloca una banda estrecha alrededor de x₁ = c; las muestras de la banda (en verde) dan la condicionada.
- A la izquierda, las muestras, las elipses de 1σ y 2σ y los ejes principales. A la derecha, las dos marginales y la condicionada, con las densidades teóricas.
- El recuadro da Σ, sus autovalores y la orientación del eje mayor, el factor de Cholesky, la media y la desviación de la condicionada, y ρ̂ estimado.

## Ejercicios

**1. La matriz de la hoja.** Con los valores de partida (σ₁ = 1,4, σ₂ = 1, ρ = 0,85), Σ es casi la del ejercicio 10 de la hoja. ¿Cuánto valen sus autovalores y el factor de Cholesky? ¿Qué forma tienen las elipses?

<details><summary>Solución</summary>
Σ = [1,96, 1,19; 1,19, 1]. Autovalores 2,76 y 0,20 (en la hoja, con 2 y 1,2, salen 2,8 y 0,2): las elipses son muy alargadas, con semiejes en proporción √(2,76/0,20) ≈ 3,7 y el eje mayor a 34° del eje x₁. L = [1,40, 0; 0,85, 0,53]: x₁ = 1,4z₁ y x₂ = 0,85z₁ + 0,53z₂.
</details>

**2. La condicionada.** Con los mismos valores y c = 1, ¿qué media y desviación tiene X₂ | X₁ = 1? Compáralas con la marginal de X₂ y con las muestras de la banda.

<details><summary>Solución</summary>
Media ρσ₂c/σ₁ = 0,85 · 1/1,4 = 0,607 y desviación σ₂√(1 − ρ²) = 0,527, frente a 0 y 1 de la marginal: conocer x₁ reduce la incertidumbre sobre x₂ casi a la mitad. Las 369 muestras de la banda dan una media de 0,648; la banda tiene anchura finita y no es exactamente x₁ = 1.
</details>

**3. Correlación nula.** Pon ρ = 0. ¿Cómo quedan las elipses y la condicionada? ¿Son independientes?

<details><summary>Solución</summary>
Las elipses tienen los ejes en los ejes coordenados (autovalores 1,96 y 1). La condicionada es N(0, 1), igual que la marginal, para cualquier c: son independientes. En la gaussiana, incorreladas implica independientes.
</details>

**4. Correlación negativa.** Con σ₁ = σ₂ = 1 y ρ = −0,6, ¿qué orientación tiene el eje mayor? ¿Qué media tiene la condicionada en c = 2? ¿Por qué la de las muestras de la banda sale algo distinta?

<details><summary>Solución</summary>
Con σ₁ = σ₂, los autovectores son las diagonales: el eje mayor está a 135° (autovalor 1 + 0,6 = 1,6) y el menor a 45° (0,4). La condicionada en c = 2 es N(−1,2; 0,8²). En la banda solo hay 72 muestras, porque x₁ = 2 está en la cola, y caen más del lado de x₁ < 2, donde la media condicionada es menos negativa: sale −1,03.
</details>

**5. Incorreladas pero dependientes.** Elige X₂ = X₁² − 4/3 con X₁ ~ U[−2, 2]. ¿Cuánto vale ρ̂? ¿Qué valores toma X₂ en la banda de c = 0 y de c = 1,5? ¿Son independientes?

<details><summary>Solución</summary>
ρ̂ = 0,02, compatible con 0: C₁₂ = E{X₁³} − (4/3)E{X₁} = 0, porque la densidad de X₁ es par. Pero X₂ queda fijada por X₁: en c = 0 vale −1,33 (desviación 0,007, por la anchura de la banda) y en c = 1,5 vale 1,5² − 4/3 = 0,92. Sin condicionar, su desviación es 1,18. Son dependientes; la correlación solo ve la parte lineal. Es el ejercicio 8 de la hoja.
</details>

**6. El anillo.** Con el anillo, ¿cuánto vale ρ̂? ¿Cómo es la condicionada en c = 0?

<details><summary>Solución</summary>
ρ̂ = 0,01: el anillo es simétrico. Pero en c = 0 la condicionada tiene dos picos, en x₂ ≈ ±2, y en c = 2 uno solo, centrado en 0 y con desviación 0,67: la distribución de X₂ cambia con c. La desviación en la banda de c = 0 es 1,98, mayor que la marginal (1,41).
</details>

## Para profundizar

- [Apuntes del Tema 6](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%20Apuntes.pdf), sección 2 (Varias variables aleatorias).
- [Transparencias T6-02](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%2002%20-%20Varias%20variables.pdf), marginales y condicionadas, incorreladas frente a independientes y gaussiana multivariable.
- [Hoja de ejercicios del Tema 6](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%20Ejercicios.pdf), ejercicios 6 a 8 y 10, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%20Ejercicios%20resueltos.pdf).
- A. Papoulis y S. U. Pillai, *Probability, Random Variables and Stochastic Processes*, 4.ª ed., McGraw-Hill, 2002, capítulos 6 y 7.

## Relación con otros conceptos

- **Una variable.** Herramienta: [Distribuciones de probabilidad](T6-distribuciones.html).
- **Box-Muller.** Dos gaussianas independientes a partir de dos uniformes. Herramienta: [Generación de muestras aleatorias](T6-generacion-muestras.html).
- **Sumas.** La suma de gaussianas es gaussiana; la de otras variables, casi. Herramienta: [Teorema del límite central](T6-limite-central.html).
- **Señales aleatorias.** La autocorrelación es la covarianza entre muestras de la misma señal. Herramienta: [Estimación de la autocorrelación](T6-autocorrelacion.html).
