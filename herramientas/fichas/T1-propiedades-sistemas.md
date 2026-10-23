## Introducción

### Qué es un sistema

Un sistema transforma una señal de entrada x en una de salida y = T{x}. Antes de estudiar un sistema concreto conviene saber qué propiedades tiene, porque de ellas depende qué herramientas se le pueden aplicar. Las definiciones son las mismas en continuo y en discreto; aquí se usan secuencias.

### Las propiedades

- **Memoria.** Un sistema es sin memoria si y[n] solo depende de x[n] en el mismo instante, como y = 2x + 1 o y = x².
- **Causalidad.** Es causal si y[n] solo depende de x[k] con k ≤ n: no puede adelantarse a la entrada. Todo sistema que funcione en tiempo real lo es; uno que procesa una grabación completa no necesita serlo.
- **Estabilidad (BIBO).** Es estable si toda entrada acotada produce una salida acotada. El acumulador y[n] = Σ_{k≤n} x[k] no lo es: un escalón produce una rampa.
- **Linealidad.** Es lineal si T{αx₁ + βx₂} = αT{x₁} + βT{x₂} para todas las entradas y constantes. Una consecuencia: la entrada nula da salida nula, así que y = 2x + 1 no es lineal.
- **Invarianza en el tiempo.** Es invariante si retrasar la entrada solo retrasa la salida: si y[n] = T{x[n]}, entonces T{x[n − n₀]} = y[n − n₀]. Un coeficiente que depende de n, como en y = n·x[n] o y = x[n] cos(πn/4), rompe la invarianza; también la rompen x[−n] y x[2n].
- **Invertibilidad.** Es invertible si entradas distintas dan salidas distintas, de modo que la entrada se puede recuperar.

### Cómo se comprueban

Para **negar** una propiedad basta un contraejemplo: dos entradas para las que la definición falle. Para **afirmarla** hay que demostrarla para todas las entradas, normalmente con álgebra. Esta herramienta busca contraejemplos con las señales que elijas: si las salidas no coinciden, el sistema no tiene la propiedad; si coinciden, puede tenerla o puede que esas señales no lo revelen.

### Sistemas LTI

Los sistemas lineales e invariantes (LTI) son los más importantes, porque quedan descritos por su respuesta al impulso h[n] y su salida es una convolución. Para ellos, causalidad y estabilidad se leen en h: es causal si h[n] = 0 para n < 0 y estable si Σ|h[n]| < ∞.

## Guía de uso

- **Sistema** elige uno de nueve sistemas.
- **Propiedad que se comprueba** elige la prueba:
  - Linealidad: compara T{αx₁ + βx₂} con αT{x₁} + βT{x₂}.
  - Invarianza: compara T{x₁[n − n₀]} con y₁[n − n₀].
  - Causalidad: aplica x₁ y una versión de x₁ cambiada solo después de n₀ (se le suma x₂ a partir de n₀ + 1); si las salidas difieren antes de n₀, el sistema mira al futuro.
  - Estabilidad: aplica un escalón y mide la salida.
- **x₁, x₂, α, β y n₀** son los datos de la prueba.
- Arriba, las entradas; abajo, las dos salidas que se comparan. El recuadro da la diferencia máxima y las propiedades teóricas del sistema.

## Ejercicios

**1. Afín no es lineal.** Con y[n] = 2x[n] + 1, comprueba la linealidad con α = 1,5 y β = −1. ¿Cuánto vale la diferencia? Explica de dónde sale.

<details><summary>Solución</summary>
T{αx₁ + βx₂} = 2(αx₁ + βx₂) + 1, mientras que αT{x₁} + βT{x₂} = 2(αx₁ + βx₂) + α + β. La diferencia es 1 − (α + β) = 1 − 0,5 = 0,5 en todas las muestras. Solo con α + β = 1 la prueba pasaría, y por eso hay que probar varios valores.
</details>

**2. Lineal pero variante.** Con y[n] = n·x[n], comprueba la linealidad y después la invarianza con n₀ = 3. ¿Qué se ve?

<details><summary>Solución</summary>
La linealidad pasa con cualquier α, β y señal: diferencia nula. La invarianza falla: T{x[n − 3]} = n·x[n − 3], mientras que y[n − 3] = (n − 3)·x[n − 3]. Además no es estable: con un escalón, la salida crece como n.
</details>

**3. Mirar al futuro.** Con y[n] = x[n + 1] − x[n], haz la prueba de causalidad con n₀ = 3. ¿En qué muestra difieren por primera vez las salidas?

<details><summary>Solución</summary>
En n = 3: y[3] = x[4] − x[3] usa x[4], que ya está cambiada. El sistema es LTI con h[n] = δ[n + 1] − δ[n], no nula en n = −1: no es causal. Retrasándolo una muestra, x[n] − x[n − 1], se vuelve causal.
</details>

**4. El acumulador.** Con el acumulador, haz la prueba de estabilidad. ¿Es LTI? ¿Qué h[n] tiene y por qué no es estable?

<details><summary>Solución</summary>
Es LTI, con h[n] = u[n]. El escalón produce una rampa que crece sin límite: Σ|h[n]| = ∞, así que no es BIBO estable, aunque su respuesta a entradas de duración finita sea acotada.
</details>

**5. Ejercicio 10 de la hoja.** La hoja incluye y[n] = x[2n] y y(t) = x(t) cos(ω₀t). Con las versiones de la herramienta (x[2n] y x[n] cos(πn/4)), comprueba qué propiedades fallan y compáralo con la tabla de la solución.

<details><summary>Solución</summary>
x[2n]: lineal sí; invariante no (con n₀ = 3, T{x[n − 3]} = x[2n − 3] y y[n − 3] = x[2n − 6]); causal no (y[n] = x[2n] usa entradas futuras para n > 0); estable sí. El modulador: lineal sí, invariante no, causal sí, estable sí. Coincide con la tabla de la hoja.
</details>

## Para profundizar

- [Apuntes del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Apuntes.pdf), sección 7 (Propiedades de los sistemas) y sección 8, «Propiedades del sistema a partir de h».
- [Transparencias T1-03](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%2003%20-%20Sistemas.pdf), propiedades de los sistemas.
- [Hoja de ejercicios del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios.pdf), ejercicio 10, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T1/codigo/python/comprobar_linealidad.py` y su versión en Matlab.
- A. V. Oppenheim, A. S. Willsky y S. H. Nawab, *Signals and Systems*, 2.ª ed., Prentice Hall, 1997, apartado 1.6.

## Relación con otros conceptos

- **Convolución.** Un sistema LTI es una convolución con h. Herramienta: [Convolución discreta](T1-convolucion-discreta.html).
- **Operaciones sobre la variable independiente.** x[−n] y x[2n] son lineales pero variantes. Herramienta: [Operaciones sobre la variable independiente](T1-variable-independiente.html).
- **Región de convergencia.** Causalidad y estabilidad se leen en la ROC de H. Herramienta: [Región de convergencia](T1-region-convergencia.html).
- **Diezmado (Tema 2).** El compresor x[Mn] no es invariante: por eso el espectro de su salida no es un simple producto. Herramienta: [Diezmado e interpolación](T2-diezmado-interpolacion.html).
- **Cuantificación (Tema 2).** El cuantificador es un sistema sin memoria y no lineal. Herramienta: [Cuantificación y SQNR](T2-cuantificacion.html).
