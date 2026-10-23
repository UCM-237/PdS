## Introducción

### Las transformadas de Laplace y Z

La transformada de Fourier no existe para señales que crecen, como e^{t}u(t). Las transformadas de Laplace y Z la generalizan multiplicando la señal por una exponencial real que la «amortigua»:

> X(s) = ∫ x(t) e^{−st} dt, con s = σ + jω;  X(z) = Σ_n x[n] z^{−n}, con z = r e^{jΩ}.

Con σ = 0 (s = jω) la de Laplace se reduce a la de Fourier; con r = 1 (z = e^{jΩ}), la Z se reduce a la DTFT.

### La región de convergencia

La integral o la suma solo convergen para algunos valores de s o z. Ese conjunto es la **región de convergencia** (ROC) y forma parte de la transformada: la misma expresión algebraica puede corresponder a señales distintas según la ROC. El ejemplo básico:

> aⁿu[n] → 1/(1 − a z^{−1}), con ROC |z| > |a|;  −aⁿu[−n − 1] → 1/(1 − a z^{−1}), con ROC |z| < |a|.

En Laplace, e^{at}u(t) y −e^{at}u(−t) tienen la misma transformada 1/(s − a), con ROC Re s > a y Re s < a.

### La forma de la ROC dice cómo es la señal

- La ROC nunca contiene polos.
- En **Laplace**, la ROC es una franja vertical; en **Z**, un anillo centrado en el origen. Sus bordes pasan por polos.
- Una señal **causal** (a la derecha) tiene una ROC a la derecha del polo de mayor parte real, o fuera del polo de mayor módulo.
- Una señal **anticausal** (a la izquierda) tiene una ROC a la izquierda del polo de menor parte real, o dentro del de menor módulo.
- Una señal **bilateral** tiene una ROC limitada por los dos lados: una franja o un anillo entre polos.

### Estabilidad

Un sistema LTI es BIBO estable si y solo si su respuesta al impulso es absolutamente integrable (o sumable), y eso equivale a que la ROC de H contenga el **eje jω** (Laplace) o la **circunferencia unidad** (Z). Por eso un sistema causal y estable tiene todos los polos en el semiplano izquierdo, o dentro de la circunferencia unidad. Un sistema estable con un polo fuera de ellos existe, pero no es causal.

## Guía de uso

- **Transformada Z o Laplace** elige el tipo de transformada.
- **p₁ y p₂** son dos polos reales. La transformada es X = 1/(1 − p₁z^{−1}) + 1/(1 − p₂z^{−1}) en Z o 1/(s − p₁) + 1/(s − p₂) en Laplace.
- **Región de convergencia** elige una de las tres regiones posibles con dos polos.
- A la izquierda, los polos y la ROC sombreada, con la circunferencia unidad o el eje jω. A la derecha, la señal que corresponde a esa ROC.
- El recuadro escribe X, la ROC, la señal y si el sistema es estable.

## Ejercicios

**1. Una expresión, tres señales.** En Z, con p₁ = 0,5 y p₂ = −1,4, recorre las tres ROC. Escribe la señal de cada una y di cuál es estable.

<details><summary>Solución</summary>
|z| > 1,4: x = 0,5ⁿu[n] + (−1,4)ⁿu[n], causal e inestable. 0,5 < |z| < 1,4: x = 0,5ⁿu[n] − (−1,4)ⁿu[−n−1], bilateral y estable (la ROC contiene |z| = 1). |z| < 0,5: x = −0,5ⁿu[−n−1] − (−1,4)ⁿu[−n−1], anticausal e inestable.
</details>

**2. Causal y estable.** En Z, ¿qué condición deben cumplir p₁ y p₂ para que la señal causal sea estable? Compruébalo moviendo los polos.

<details><summary>Solución</summary>
La ROC causal es |z| > max(|p₁|, |p₂|). Contiene la circunferencia unidad si los dos polos tienen módulo menor que 1. Basta un polo fuera para que la secuencia crezca.
</details>

**3. Laplace.** Con p₁ = −1 y p₂ = 0,5, ¿qué ROC da un sistema estable? ¿Es causal?

<details><summary>Solución</summary>
La franja −1 < Re s < 0,5 contiene el eje jω: es estable, y la señal es e^{−t}u(t) − e^{0,5t}u(−t), bilateral, no causal. La ROC causal, Re s > 0,5, no contiene el eje jω y es inestable.
</details>

**4. Polos con el mismo módulo.** En Z, pon p₁ = 0,8 y p₂ = −0,8 y elige «Entre los dos polos». ¿Qué ocurre?

<details><summary>Solución</summary>
Los dos polos están en la misma circunferencia |z| = 0,8, así que no hay anillo entre ellos: esa ROC no existe. Solo son posibles |z| > 0,8 (causal, estable) y |z| < 0,8 (anticausal, inestable).
</details>

**5. Ejercicios 11 y 12 de la hoja.** La hoja estudia la estabilidad de sistemas causales. Con H(z) = z/(z − 1,5) = 1/(1 − 1,5z^{−1}), pon p₁ = 1,5 y p₂ = 0 (el segundo término vale 1 y solo añade δ[n]). ¿Es estable el sistema causal? ¿Hay alguna ROC que dé un sistema estable?

<details><summary>Solución</summary>
El causal tiene ROC |z| > 1,5, que no contiene |z| = 1: inestable, con h[n] = 1,5ⁿu[n] (más el δ[n] del segundo término). La ROC 0 < |z| < 1,5 sí contiene la circunferencia unidad y da un sistema estable, con −1,5ⁿu[−n−1] en lugar de 1,5ⁿu[n], pero no causal.
</details>

## Para profundizar

- [Apuntes del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Apuntes.pdf), sección 6, apartados «Transformada de Laplace», «Transformada Z» y «Relación entre las transformadas», y sección 8, «Propiedades del sistema a partir de h».
- [Transparencias T1-02](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%2002%20-%20Operaciones.pdf), transformadas de Laplace y Z.
- [Hoja de ejercicios del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios.pdf), ejercicios 11 y 12, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios%20resueltos.pdf).
- A. V. Oppenheim, A. S. Willsky y S. H. Nawab, *Signals and Systems*, 2.ª ed., Prentice Hall, 1997, capítulos 9 y 10.
- A. V. Oppenheim y R. W. Schafer, *Discrete-Time Signal Processing*, 3.ª ed., Pearson, 2010, capítulo 3.

## Relación con otros conceptos

- **Exponenciales.** Cada polo p aporta una exponencial e^{pt} o pⁿ. Herramientas: [Exponencial compleja continua](T1-exponencial-continua.html) y [Exponencial compleja discreta](T1-exponencial-discreta.html).
- **Estabilidad y causalidad.** Herramienta: [Propiedades de los sistemas](T1-propiedades-sistemas.html).
- **Polos y ceros (Tema 4).** La respuesta en frecuencia se lee sobre el eje jω o la circunferencia unidad, que deben estar en la ROC. Herramientas: [Polos y ceros en el plano s](T4-polos-ceros-s.html) y [Polos y ceros en el plano z](T4-polos-ceros-z.html).
- **Fase cero (Tema 4).** Los filtros de fase cero son no causales: su ROC es un anillo con polos dentro y fuera. Herramienta: [Filtrado de fase cero](T4-fase-cero.html).
