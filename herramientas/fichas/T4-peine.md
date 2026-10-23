## Introducción

### Una interferencia con muchos armónicos

El zumbido de la red eléctrica no es una sinusoide pura: tiene 50 Hz y sus armónicos, 100, 150, 200 Hz… Es una señal **periódica** de periodo 1/50 s, con espectro de líneas en múltiplos de f₀. Para eliminarla con un filtro de muesca haría falta un par de ceros por armónico. Un **filtro en peine** los pone todos a la vez.

### El peine FIR

Si fs = L f₀, con L entero, restar la señal retrasada un periodo,

> y[n] = x[n] − x[n − L],  H(z) = 1 − z^{−L},

anula cualquier componente de periodo L muestras. Los ceros son las raíces L-ésimas de la unidad, z = e^{j2πk/L}, es decir, las frecuencias f = k fs/L = k f₀, incluida la continua. Pero su módulo, |H| = 2|sin(ΩL/2)|, oscila entre 0 y 2 entre muescas: deforma mucho la señal útil.

### Ranuras en peine

Se añaden polos justo dentro de los ceros, a radio a^{1/L}:

> H(z) = (1 + a)/2 · (1 − z^{−L})/(1 − a z^{−L}).

Lejos de cada muesca, polo y cero se compensan y |H| ≈ 1; cerca de ella, el cero manda. La anchura de cada ranura a −3 dB es de unos

> (1 − a) fs/(πL) Hz,

más estrecha cuanto más se acerca a a 1. El precio es un **transitorio** largo, de unas L/(1 − a) muestras: el filtro tarda en "aprender" la interferencia.

### Resonador en peine

Con el mismo denominador y sin ceros, H(z) = (1 − a)/(1 − a z^{−L}) tiene picos estrechos en los múltiplos de f₀: **extrae** la componente periódica en vez de quitarla. Sirve para estimar la interferencia, para realzar señales periódicas en ruido o como modelo de una cuerda vibrante (algoritmo de Karplus–Strong).

### El periodo tiene que ser exacto

Las muescas están en múltiplos de fs/L. Si fs/f₀ no es entero, o la red se desvía de 50 Hz, las muescas no caen en los armónicos y, si son estrechas, apenas atenúan. En la práctica se elige fs múltiplo de 50 Hz o se usan peines adaptativos.

## Guía de uso

- **Filtro** elige las ranuras en peine (IIR), el peine FIR o el resonador.
- **f₀** es la frecuencia de diseño: L = round(fs/f₀), con fs = 1000 Hz. **a** fija el radio de los polos.
- La señal útil tiene tonos de 7 y 23 Hz. La interferencia tiene 50 Hz y **Armónicos** de amplitud decreciente, con **Amplitud** ajustable.
- Arriba, el módulo en dB y los polos y ceros. Abajo, la señal con interferencia y la salida, con la referencia en verde (la señal útil o, con el resonador, la interferencia), y los espectros en régimen permanente.
- El recuadro da L, la ganancia a 50 Hz, la anchura de las ranuras y la duración del transitorio.

## Ejercicios

**1. Ranuras.** Con los valores de partida (f₀ = 50, a = 0,95), ¿cuánto vale L? ¿Dónde están las ranuras y cuánto miden? ¿Cuánto dura el transitorio?

<details><summary>Solución</summary>
L = 1000/50 = 20. Las ranuras están en 0, 50, 100, …, 500 Hz y miden unos 0,05·1000/(20π) ≈ 0,8 Hz. El transitorio dura unas 20/0,05 = 400 muestras, 0,4 s: en la gráfica, la interferencia tarda eso en desaparecer de la salida.
</details>

**2. El compromiso de a.** Baja a a 0,8. ¿Qué pasa con la anchura de las ranuras, el transitorio y la ganancia a 49 Hz?

<details><summary>Solución</summary>
Las ranuras se ensanchan a unos 3,2 Hz y el transitorio se acorta a unas 100 muestras (0,1 s). A cambio, la señal cercana a la interferencia se atenúa más: a 49 Hz, unos −6 dB, frente a −0,7 dB (|H| ≈ 0,93) con a = 0,95.
</details>

**3. El peine FIR.** Cambia al peine FIR 1 − z^{−L}. ¿Qué ganancia tiene a 25 Hz? ¿Y a 7 y 23 Hz? ¿Qué le pasa a la señal útil?

<details><summary>Solución</summary>
2 a 25 Hz, a mitad de camino entre muescas; 0,85 a 7 Hz y 1,98 a 23 Hz. La interferencia desaparece sin transitorio largo (basta L muestras), pero la señal útil sale muy deformada: un tono se amplifica casi al doble y el otro no. Es el problema del ejercicio 18 a de la hoja con el ECG.
</details>

**4. Desajuste.** Vuelve a las ranuras con a = 0,95 y cambia f₀ a 48 Hz. ¿Qué L sale? ¿Cuánto se atenúa la interferencia? ¿Y con a = 0,8?

<details><summary>Solución</summary>
L = round(1000/48) = 21, y las ranuras están en múltiplos de 47,6 Hz: a 50 Hz, la ganancia es solo de −0,1 dB y el zumbido pasa casi entero. Con a = 0,8 las ranuras son más anchas y atenúa algo más (−1,7 dB), pero sigue siendo inútil. Con f₀ = 49 Hz, L sigue siendo 20 y no cambia nada.
</details>

**5. El ejercicio 18 de la hoja: el ECG a 8 kHz.** ¿Qué L haría falta? Con a = 0,95, ¿cuánto vale |H| a 25 y a 49 Hz? Compáralo con el resonador de la herramienta: ¿qué extrae?

<details><summary>Solución</summary>
L = 8000/50 = 160. A 25 Hz, z^{−L} = −1 y |H| = 1; a 49 Hz, |H| ≈ 0,93: las muescas son estrechas y el resto pasa casi sin cambios. El resonador de la herramienta deja pasar solo los múltiplos de 50 Hz (a 7 Hz la ganancia es 0,06): su salida es una estimación de la interferencia, que se podría restar de la señal.
</details>

## Para profundizar

- [Apuntes del Tema 4](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Apuntes.pdf), sección 5 (Filtros especiales), «Filtros en peine».
- [Transparencias T4-05](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%2005%20-%20Filtros%20especiales.pdf), filtros en peine.
- [Hoja de ejercicios del Tema 4](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Ejercicios.pdf), ejercicios 3 y 18, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T4/codigo/python/peine_50hz.py` y su versión en Matlab.
- K. Karplus y A. Strong, «Digital synthesis of plucked-string and drum timbres», *Computer Music Journal*, 7(2), 1983.

## Relación con otros conceptos

- **Muesca de un solo tono.** Carga la muesca. Herramienta: [Polos y ceros en el plano z](T4-polos-ceros-z.html).
- **Media móvil.** (1 − z^{−L})/(1 − z^{−1}) es la media de L muestras. Herramienta: [Filtro de media móvil](T4-media-movil.html).
- **Serie de Fourier (Tema 1).** Una señal periódica tiene espectro de líneas en múltiplos de f₀. Herramienta: [Serie de Fourier](T1-serie-fourier.html).
- **Fase cero.** En un registro grabado se puede aplicar el peine sin retardo. Herramienta: [Filtrado de fase cero](T4-fase-cero.html).
