## Introducción

### El filtro más sencillo

La media móvil de L muestras sustituye cada valor por el promedio de los L últimos:

> y[n] = (1/L) Σ_{k=0}^{L−1} x[n − k],  h[n] = 1/L para 0 ≤ n < L.

Es un filtro FIR (respuesta al impulso finita), causal y siempre estable. Se usa para suavizar medidas con ruido, para calcular tendencias o como primer ejemplo de filtro paso bajo.

### Respuesta en frecuencia

Sumando la serie geométrica,

> H(e^{jΩ}) = (1/L) · sin(ΩL/2)/sin(Ω/2) · e^{−jΩ(L−1)/2}.

- El módulo vale 1 en Ω = 0 y tiene **ceros en Ω = 2πk/L**, k = 1, …, L − 1: elimina por completo las sinusoides que completan un número entero de periodos en L muestras.
- El primer cero, 2π/L, marca aproximadamente el ancho de la banda de paso: cuanto mayor es L, más estrecho es el paso bajo.
- Entre ceros hay lóbulos secundarios; el primero solo está unos 13 dB por debajo. Es un paso bajo pobre, pero barato.
- La fase es **lineal**, −Ω(L − 1)/2, con saltos de π donde el seno cambia de signo: todas las componentes se retrasan (L − 1)/2 muestras.

### Ruido frente a resolución temporal

Si x[n] lleva ruido blanco de varianza σ², la salida tiene varianza σ²/L: el ruido se reduce √L veces en desviación. A cambio, un escalón tarda L muestras en subir (la salida es una rampa) y la señal llega retrasada (L − 1)/2 muestras. Elegir L es un compromiso entre quitar ruido y conservar los detalles.

### Polos y ceros

H(z) = (1/L)(1 − z^{−L})/(1 − z^{−1}). Los ceros son las raíces L-ésimas de la unidad salvo z = 1, que se cancela con el polo. Visto como FIR, todos sus polos están en el origen.

## Guía de uso

- **Señal** elige un seno lento, escalones o un seno lento más un tono rápido en Ω = 0,8π.
- **L** es el número de muestras promediadas y **Desviación del ruido**, la del ruido añadido.
- Arriba, la señal con ruido (gris), la señal sin ruido (verde discontinua) y la salida (azul). Abajo, el módulo (**Lineal o dB**) y la fase de H.
- El recuadro da h[n], el primer cero, el retardo y la reducción de varianza.

## Ejercicios

**1. Retardo.** Con los escalones, sin ruido y L = 20, ¿cuánto tarda la salida en subir? ¿Dónde está el punto medio de la subida respecto al escalón?

<details><summary>Solución</summary>
La salida sube en rampa durante L = 20 muestras y llega a la mitad 9,5 muestras después del escalón: el retardo (L − 1)/2. Es el precio de la causalidad: el filtro solo ve muestras pasadas.
</details>

**2. Ruido.** Con el seno lento y desviación 0,3, compara L = 1, 4 y 16. ¿Cuánto se reduce la desviación del ruido? ¿Qué pasa con L = 60?

<details><summary>Solución</summary>
La varianza se divide por L, la desviación por √L: a la mitad con L = 4 y a la cuarta parte con L = 16. Con L = 60 el ruido casi desaparece, pero el seno, de periodo 150 muestras, sale retrasado unas 30 muestras y con menor amplitud: el primer cero, 2π/60, está ya cerca de su frecuencia, 2π/150.
</details>

**3. Eliminar un tono.** Con el seno lento más el tono rápido en 0,8π, sin ruido, prueba L = 5, 8 y 10. ¿Con qué L desaparece el tono? ¿Por qué?

<details><summary>Solución</summary>
Con L = 5 y L = 10, porque 0,8π = 2π·2/5 = 2π·4/10 es un cero de H. Con L = 8, |H(e^{j0,8π})| ≈ 0,08 (unos −22 dB): queda un resto del tono. Lo mismo hace el ejercicio 18 de la hoja con un peine para la red de 50 Hz.
</details>

**4. Fase lineal.** Con L = 8, mira la fase. ¿Qué pendiente tiene? ¿Por qué tiene saltos?

<details><summary>Solución</summary>
La pendiente es −(L − 1)/2 = −3,5 rad por rad/muestra: un retardo de 3,5 muestras. Hay saltos de π en los ceros, Ω = 2πk/8, porque ahí el factor real sin(4Ω)/sin(Ω/2) cambia de signo; entre saltos, la fase es lineal.
</details>

**5. El ejercicio 2 a de la hoja.** El filtro h = (1, 2, 1)/4 es la media móvil de 2 aplicada dos veces. ¿Qué respuesta en frecuencia tiene? Compárala con la media de 3 muestras (L = 3).

<details><summary>Solución</summary>
H = ((1 + e^{−jΩ})/2)² = e^{−jΩ}(1 + cos Ω)/2: un solo cero doble en Ω = π, sin lóbulos secundarios, y retardo de 1 muestra. La media de 3 tiene ceros en ±2π/3 y un lóbulo secundario de amplitud 1/3 en Ω = π. (1, 2, 1)/4 suaviza un poco menos, pero no deja pasar las frecuencias altas.
</details>

## Para profundizar

- [Apuntes del Tema 4](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Apuntes.pdf), sección 1 (Filtros ideales, especificaciones y fase): «Fase y retardo de grupo» y «Filtros FIR e IIR».
- [Transparencias T4-01](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%2001%20-%20Introducci%C3%B3n.pdf), filtros discretos.
- [Hoja de ejercicios del Tema 4](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Ejercicios.pdf), ejercicio 2, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Ejercicios%20resueltos.pdf).
- J. H. McClellan, R. W. Schafer y M. A. Yoder, *DSP First*, 2.ª ed., Pearson, 2016, capítulos 5 y 6.

## Relación con otros conceptos

- **Convolución discreta (Tema 1).** La media móvil es la convolución con un pulso. Herramienta: [Convolución discreta](T1-convolucion-discreta.html).
- **Polos y ceros.** Carga el ejemplo de media móvil de 5 muestras. Herramienta: [Polos y ceros en el plano z](T4-polos-ceros-z.html).
- **Ventana rectangular (Tema 3).** |H| es el núcleo de Dirichlet, el espectro de la ventana rectangular. Herramienta: [Ventanas y fuga espectral](T3-ventanas.html).
- **Fase lineal.** Herramienta: [Fase lineal y retardo de grupo](T4-fase-lineal.html).
- **Filtros en peine.** 1 − z^{−L} es el numerador de la media móvil. Herramienta: [Filtro en peine](T4-peine.html).
