## Introducción

### La transformada de Fourier

La transformada de Fourier de una señal continua es

> X(f) = ∫ x(t) e^{−j2πft} dt,  y su inversa,  x(t) = ∫ X(f) e^{j2πft} df.

Describe la señal como una «suma continua» de exponenciales complejas: |X(f)| dice cuánto hay de cada frecuencia y ∠X(f), con qué fase. Con la pulsación ω = 2πf se escribe X(jω). Algunos pares básicos: un pulso rectangular de anchura 1 centrado da sinc(f); el triangular de anchura 2, sinc²(f); la gaussiana e^{−πt²}, ella misma, e^{−πf²}; la exponencial e^{−t}u(t), 1/(1 + j2πf).

### Las propiedades: cada operación tiene su pareja

Calcular transformadas desde la definición es laborioso. Casi siempre se combinan unos pocos pares conocidos con las propiedades:

| Tiempo | Frecuencia | Qué significa |
|---|---|---|
| x(t − t₀) | e^{−j2πft₀} X(f) | desplazar no cambia el módulo; añade una fase lineal de pendiente −2πt₀ |
| x(at) | X(f/a)/∣a∣ | comprimir en el tiempo ensancha el espectro, y al revés |
| x(t) cos(2πf₀t) | ½X(f − f₀) + ½X(f + f₀) | modular traslada el espectro a ±f₀ (es lo que hace una emisora de radio) |
| dx/dt | j2πf X(f) | derivar realza las frecuencias altas y anula la continua |
| (x ∗ h)(t) | X(f) H(f) | convolucionar es multiplicar los espectros |

### Duración y ancho de banda

La propiedad de escalado expresa un principio general: una señal no puede ser a la vez muy corta y muy estrecha en frecuencia. El producto de su duración por su ancho de banda está acotado inferiormente; la gaussiana es la que mejor lo cumple. Por eso un pulso más corto necesita más ancho de banda para transmitirse.

### Parseval

La energía se conserva: ∫|x(t)|² dt = ∫|X(f)|² df. De las operaciones de la tabla, el desplazamiento no cambia la energía, el escalado la divide por |a| y la modulación, la derivada y la convolución la cambian en general.

### Simetrías

Si x es real, X(−f) = X*(f): el módulo es par y la fase impar, y basta dibujar f ≥ 0. Si además x es par, X es real; si es impar, imaginaria pura.

## Guía de uso

- **Señal x(t)** elige entre un pulso rectangular de anchura 1, un triangular de anchura 2, la gaussiana e^{−πt²} y la exponencial e^{−t}u(t), todas en t = 0.
- **Operación** aplica una de las propiedades de la tabla; **t₀**, **a** y **f₀** son sus parámetros.
- Arriba, x(t) en gris y el resultado y(t) en azul. Debajo, el módulo y la fase de X(f) y de Y(f). La fase se omite donde el módulo es casi nulo.
- El recuadro escribe la relación entre Y(f) y X(f) y compara las energías.
- La transformada se calcula con una FFT de la señal muestreada cada 0,02 s, así que es una aproximación muy buena, pero no exacta.

## Ejercicios

**1. Desplazamiento.** Con el pulso rectangular y t₀ = 1, ¿cambia |Y(f)|? ¿Qué pendiente tiene la fase? Comprueba con t₀ = −0,5.

<details><summary>Solución</summary>
|Y| = |X|: el módulo no cambia. La fase añade −2πft₀: con t₀ = 1 baja 2π rad por cada hercio (la gráfica la envuelve en [−π, π]). Con t₀ = −0,5 sube π rad por hercio. La energía es la misma.
</details>

**2. Escalado.** Con el pulso rectangular y a = 2, ¿dónde está el primer cero de |Y(f)|? ¿Y su valor en f = 0?

<details><summary>Solución</summary>
x(2t) es un pulso de anchura 0,5: Y(f) = ½ sinc(f/2). El primer cero pasa de 1 Hz a 2 Hz y el valor en f = 0, que es el área, baja de 1 a 0,5. La energía pasa de 1 a 0,5.
</details>

**3. Modulación.** Con la gaussiana y f₀ = 1,5 Hz, describe |Y(f)|. ¿Qué pasa si f₀ = 0,3 Hz?

<details><summary>Solución</summary>
Dos copias de e^{−πf²} de altura 0,5 centradas en ±1,5 Hz. Con f₀ = 0,3 las copias se solapan y su suma ya no es la de dos gaussianas separadas: la modulación solo «traslada limpiamente» si f₀ es mayor que el ancho de banda de x.
</details>

**4. Derivada.** Con la gaussiana, aplica la derivada. ¿Cuánto vale |Y(0)|? ¿Dónde está el máximo de |Y(f)|?

<details><summary>Solución</summary>
Y(f) = j2πf e^{−πf²}: Y(0) = 0, porque la derivada tiene área nula. |Y| = 2π|f|e^{−πf²} es máximo donde su derivada se anula, 1 − 2πf² = 0, es decir, en |f| = 1/√(2π) ≈ 0,40 Hz.
</details>

**5. Ejercicio 8 c de la hoja.** Con el pulso rectangular, aplica la convolución x ∗ x. ¿Qué señal sale y cuál es su transformada?

<details><summary>Solución</summary>
El triángulo de anchura 2 y altura 1, el mismo que la segunda señal de la lista. Su transformada es sinc²(f): la convolución en el tiempo se convierte en el producto X(f)·X(f). Los ceros siguen en los enteros, pero los lóbulos laterales bajan más deprisa.
</details>

## Para profundizar

- [Apuntes del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Apuntes.pdf), sección 6, «Transformada de Fourier en tiempo continuo» y «Propiedades de la transformada de Fourier».
- [Transparencias T1-02](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%2002%20-%20Operaciones.pdf), transformada de Fourier y sus propiedades.
- [Hoja de ejercicios del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios.pdf), ejercicio 8, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T1/codigo/python/dtft_pulso.py` (la versión discreta del ejercicio 8) y su versión en Matlab.
- A. V. Oppenheim, A. S. Willsky y S. H. Nawab, *Signals and Systems*, 2.ª ed., Prentice Hall, 1997, capítulo 4 (y el 5 para la DTFT).

## Relación con otros conceptos

- **Serie de Fourier.** La transformada es el límite de la serie cuando el periodo tiende a infinito. Herramienta: [Serie de Fourier](T1-serie-fourier.html).
- **Operaciones sobre la variable independiente.** Desplazar y escalar en el tiempo son las operaciones de la herramienta. Herramienta: [Operaciones sobre la variable independiente](T1-variable-independiente.html).
- **Convolución.** El producto de espectros es la base del filtrado. Herramienta: [Convolución continua](T1-convolucion-continua.html).
- **Muestreo (Tema 2).** Muestrear multiplica por un tren de impulsos y repite el espectro, que es la modulación aplicada a todos los múltiplos de fs. Herramienta: [Muestreo ideal](T2-muestreo-ideal.html).
- **Fase lineal (Tema 4).** Un filtro con fase lineal retrasa la señal sin deformarla, por la propiedad de desplazamiento. Herramienta: [Fase lineal y retardo de grupo](T4-fase-lineal.html).
