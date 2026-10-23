## Introducción

### Por qué la convolución

Un sistema lineal e invariante en el tiempo (LTI) queda descrito por completo por su **respuesta al impulso** h(t), la salida cuando la entrada es δ(t). La razón es que cualquier entrada se puede escribir como una suma (una integral) de impulsos desplazados y escalados, x(t) = ∫ x(τ) δ(t − τ) dτ. Por linealidad e invarianza, cada impulso x(τ)δ(t − τ) produce x(τ)h(t − τ), y la salida es la suma de todas esas respuestas:

> y(t) = (x ∗ h)(t) = ∫ x(τ) h(t − τ) dτ.

### Cómo se calcula, paso a paso

Para un instante t fijo:

1. Se dibuja x(τ) en función de τ.
2. Se invierte h: h(−τ).
3. Se desplaza hasta t: h(t − τ). Para t > 0 se mueve a la derecha.
4. Se multiplican punto a punto: x(τ) h(t − τ).
5. Se integra el producto: el área es y(t).

Repitiendo para cada t se obtiene y(t). Las zonas de t se separan según cómo se solapan las dos señales: sin solape, solape parcial por la izquierda, solape completo, solape parcial por la derecha.

### Propiedades útiles

- **Conmutativa:** x ∗ h = h ∗ x. Se puede invertir la que resulte más cómoda.
- **Duración:** si x es no nula en un intervalo de longitud T_x y h en uno de longitud T_h, y es no nula en un intervalo de longitud T_x + T_h, que empieza en la suma de los instantes iniciales.
- **Elemento neutro y desplazamiento:** x ∗ δ = x y x ∗ δ(t − t₀) = x(t − t₀).
- **Escalón:** x ∗ u es la integral acumulada de x. Por eso la respuesta al escalón de un sistema es la integral de su respuesta al impulso.
- **En frecuencia,** la convolución es un producto: Y(f) = X(f) H(f).

## Guía de uso

- **Señal x(t)** y **Respuesta al impulso h(t)** se eligen entre pulsos de anchura 1 y 2, un triángulo de anchura 2, la exponencial e^{−t}u(t), el escalón y una rampa en [0, 1]. Todas empiezan en t = 0.
- **t** es el desplazamiento: el instante en que se calcula la salida.
- Arriba, x(τ) y h(t − τ); en medio, su producto, cuya área sombreada es y(t); abajo, la salida completa y, marcado, el valor y(t) actual.

## Ejercicios

**1. Dos pulsos iguales.** Con dos pulsos de anchura 1, predice la forma, la duración y el máximo de y(t). Mueve t para comprobarlo.

<details><summary>Solución</summary>
Es un triángulo entre t = 0 y t = 2 con el pico y(1) = 1. La salida sube linealmente mientras crece el solape y baja cuando disminuye; la duración es 1 + 1 = 2.
</details>

**2. Ejercicio 6 d de la hoja.** Con x un pulso de anchura 2 y h un pulso de anchura 1, obtén y(t) por tramos.

<details><summary>Solución</summary>
Un trapecio: 0 para t < 0, t en [0, 1], 1 en [1, 2], 3 − t en [2, 3] y 0 para t > 3. La duración es 2 + 1 = 3 y el tramo plano aparece cuando el pulso estrecho cabe entero dentro del ancho.
</details>

**3. Respuesta al escalón.** Con x el escalón y h = e^{−t}u(t), calcula y(t). ¿Cuánto vale en t = 1? ¿A qué valor tiende?

<details><summary>Solución</summary>
y(t) = ∫₀^t e^{−(t−τ)} dτ = 1 − e^{−t} para t ≥ 0. y(1) = 1 − e^{−1} ≈ 0,632 y tiende a 1: es la respuesta al escalón de un sistema de primer orden con constante de tiempo 1 s.
</details>

**4. Un pulso que entra y sale.** Con x un pulso de anchura 1 y h = e^{−t}u(t), escribe y(t) en los tramos 0 ≤ t < 1 y t ≥ 1. ¿Dónde está el máximo?

<details><summary>Solución</summary>
Para 0 ≤ t < 1, y = 1 − e^{−t}; para t ≥ 1, y = (e − 1)e^{−t}. El máximo está en t = 1, cuando el pulso termina, con y(1) ≈ 0,632. Después la salida decae con la misma constante de tiempo que h.
</details>

**5. Duraciones.** Sin calcular, ¿cuánto dura el resultado de convolucionar un pulso de anchura 2 con el triángulo? ¿Cuánto vale y(2)? Compruébalo.

<details><summary>Solución</summary>
Dura 2 + 2 = 4 (de t = 0 a t = 4). En t = 2, h(2 − τ) es el triángulo entero dentro del pulso, así que y(2) es el área del triángulo: 1.
</details>

## Para profundizar

- [Apuntes del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Apuntes.pdf), sección 5 (Convolución) y sección 8, «Respuesta al impulso y convolución».
- [Transparencias T1-02](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%2002%20-%20Operaciones.pdf), «Convolución continua: ejemplo».
- [Hoja de ejercicios del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios.pdf), ejercicio 6, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T1/codigo/python/convolucion.py` y su versión en Matlab.
- A. V. Oppenheim, A. S. Willsky y S. H. Nawab, *Signals and Systems*, 2.ª ed., Prentice Hall, 1997, apartado 2.2.

## Relación con otros conceptos

- **Convolución discreta.** La misma operación con sumas en lugar de integrales. Herramienta: [Convolución discreta](T1-convolucion-discreta.html).
- **Inversión y desplazamiento.** h(t − τ) es h invertida y desplazada t. Herramienta: [Operaciones sobre la variable independiente](T1-variable-independiente.html).
- **Producto en frecuencia.** Convolucionar en el tiempo es multiplicar los espectros. Herramienta: [Propiedades de la transformada de Fourier](T1-propiedades-fourier.html), con la operación «Convolución x ∗ x».
- **Sistemas LTI continuos.** La salida de un sistema LTI es la convolución con h; con una sinusoide, se reduce a multiplicar por H(jω). Herramienta: [Respuesta de un sistema LTI continuo](T1-respuesta-lti-continua.html).
- **Reconstrucción (Tema 2).** El reconstructor ideal y los retenedores convolucionan el tren de muestras con una respuesta al impulso. Herramienta: [Reconstrucción](T2-reconstruccion.html).
