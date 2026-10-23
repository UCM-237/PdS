## Introducción

### Tres operaciones sobre el eje del tiempo

Muchas manipulaciones de señales no cambian sus valores, sino el instante en que aparecen. Las tres básicas son:

- **Desplazamiento:** x(t − t₀) retrasa la señal t₀ segundos si t₀ > 0 (la mueve a la derecha) y la adelanta si t₀ < 0.
- **Inversión:** x(−t) refleja la señal respecto a t = 0, como si se reprodujera al revés.
- **Escalado:** x(at), con a > 0, comprime la señal si a > 1 (va más deprisa) y la expande si a < 1.

En tiempo discreto, n, n₀ y a son enteros: x[n − n₀] desplaza n₀ muestras y x[−n] invierte, igual que en continuo, pero el escalado es distinto (ver más abajo).

### La operación combinada x(αt + β)

Cualquier combinación de las tres se escribe y(t) = x(αt + β). La forma segura de dibujarla es hacer las operaciones en este orden:

1. **Desplazar:** v(t) = x(t + β), que mueve x β unidades a la izquierda.
2. **Escalar e invertir:** y(t) = v(αt) = x(αt + β).

También se puede escalar primero, pero entonces el desplazamiento cambia: x(αt + β) = x(α(t + β/α)), es decir, primero x(αt) y después un desplazamiento de β/α. El error típico es escalar y desplazar β en lugar de β/α. Un punto útil para comprobar el resultado: el valor que x tenía en t = 0 aparece en y en t = −β/α.

### Escalado en tiempo discreto: diezmado y expansión

En discreto, x[Mn] con M entero mayor que 1 se queda con una de cada M muestras: es el **diezmado**, y las muestras intermedias se pierden. El «escalado» contrario no existe como tal, porque x[n/L] solo está definido cuando n es múltiplo de L; la **expansión** rellena con ceros las posiciones intermedias. Las dos operaciones aparecen en el Tema 2 al cambiar la frecuencia de muestreo.

### Para qué sirve

El desplazamiento modela retardos (un eco, la propagación de una onda), la inversión aparece en la convolución (h(t − τ) es h invertida y desplazada) y el escalado, en cualquier cambio de velocidad de reproducción. En frecuencia, desplazar solo cambia la fase y escalar por a comprime o expande el espectro por 1/a.

## Guía de uso

- **Señal x** elige la señal original: un triángulo asimétrico (no nulo entre −1 y 3, con el pico en 0), un pulso con un escalón (1 en [−1, 1) y 0,5 en [1, 2)) o una exponencial truncada (e^{−0,8t} en [0, 4]).
- **Continuo o Discreto** cambia el tipo de señal. En discreto, α y β se redondean a enteros.
- **α** escala el eje (si es negativo, también invierte) y **β** desplaza.
- La primera gráfica es la señal original, la segunda el paso 1 (v = x(t + β)) y la de abajo el resultado y = x(αt + β), con x en gris como referencia.
- El recuadro dice dónde acaba el punto t = 0 de x y si la señal se comprime, se expande o se invierte.

## Ejercicios

**1. Predecir y comprobar.** Con el triángulo asimétrico, dibuja a mano y(t) = x(2t − 4): ¿dónde está el pico y entre qué instantes es no nula? Compruébalo con α = 2 y β = −4.

<details><summary>Solución</summary>
x es no nula para −1 ≤ u ≤ 3 con u = 2t − 4, es decir, para 1,5 ≤ t ≤ 3,5. El pico (u = 0) está en t = 2 = −β/α. La señal dura la mitad: 2 en lugar de 4.
</details>

**2. Invertir y desplazar.** ¿Qué α y β dan x(3 − t)? ¿Dónde está el pico del triángulo y hacia qué lado cae la pendiente suave?

<details><summary>Solución</summary>
α = −1 y β = 3. La señal es no nula para 0 ≤ t ≤ 4 y el pico está en t = 3. La pendiente suave, que en x iba de 0 a 3 hacia la derecha, ahora va de t = 3 hacia la izquierda, hasta t = 0.
</details>

**3. El orden importa.** Una compañera escribe x(2(t + 1)) y otra x(2t + 1). ¿Qué α y β corresponde a cada una? ¿Dónde está el punto t = 0 de x en cada caso?

<details><summary>Solución</summary>
x(2(t + 1)) = x(2t + 2): α = 2, β = 2, con el punto en t = −1. x(2t + 1): α = 2, β = 1, con el punto en t = −0,5. Si se escala primero, el desplazamiento que hay que aplicar después es β/α, no β.
</details>

**4. Diezmado.** En discreto, con el pulso con escalón, calcula a mano x[2n] y compruébalo con α = 2 y β = 0. ¿Qué muestras se pierden? ¿Se puede recuperar x a partir de x[2n]?

<details><summary>Solución</summary>
x[−1] = x[0] = 1 y x[1] = 0,5. x[2n] toma x[0], x[±2], …: solo queda x[0] = 1, así que x[2n] = δ[n]. Se pierden x[−1] y x[1], y no hay forma de recuperarlas: el diezmado no es invertible.
</details>

**5. Ejercicio 5 e de la hoja, con otra señal.** La hoja pide x₃[n − 2] y x₃[−n]. Con la exponencial truncada en discreto, obtén x[2 − n] (α = −1, β = 2) y di qué muestra de y vale 1.

<details><summary>Solución</summary>
x es no nula para 0 ≤ u ≤ 4 con u = 2 − n, es decir, para −2 ≤ n ≤ 2. y[2] = x[0] = 1 y la exponencial decrece hacia la izquierda: y[1] = x[1], y[0] = x[2], etc. Es x invertida y retrasada 2 muestras.
</details>

## Para profundizar

- [Apuntes del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Apuntes.pdf), sección 4, «Transformaciones de la variable independiente».
- [Transparencias T1-02](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%2002%20-%20Operaciones.pdf), transformaciones de la variable independiente.
- [Hoja de ejercicios del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios.pdf), ejercicio 5, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T1/codigo/python/senales_basicas.py` y su versión en Matlab.
- A. V. Oppenheim, A. S. Willsky y S. H. Nawab, *Signals and Systems*, 2.ª ed., Prentice Hall, 1997, apartado 1.2.

## Relación con otros conceptos

- **Par e impar.** La parte par e impar se definen con x(−t). Herramienta: [Par, impar, energía y potencia](T1-par-impar-energia.html).
- **Convolución.** h(t − τ) es h invertida y desplazada t: la convolución repite esta operación para cada t. Herramientas: [Convolución continua](T1-convolucion-continua.html) y [Convolución discreta](T1-convolucion-discreta.html).
- **Propiedades de la transformada de Fourier.** Desplazar multiplica el espectro por e^{−jωt₀} y escalar por a lo escala por 1/a. Herramienta: [Propiedades de la transformada de Fourier](T1-propiedades-fourier.html).
- **Diezmado e interpolación (Tema 2).** El diezmado y la expansión discretos cambian la frecuencia de muestreo. Herramienta: [Diezmado e interpolación](T2-diezmado-interpolacion.html).
- **Invarianza en el tiempo.** Un sistema es invariante si desplazar la entrada solo desplaza la salida. Herramienta: [Propiedades de los sistemas](T1-propiedades-sistemas.html).
