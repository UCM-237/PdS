## Introducción

### La transformada Z de un filtro discreto

Un filtro discreto descrito por una ecuación en diferencias tiene una función de transferencia racional en z, que se factoriza con sus raíces:

> H(z) = Σ b_k z^{−k} / Σ a_k z^{−k} = k · Π (1 − c_i z^{−1}) / Π (1 − p_j z^{−1}).

Si todos los polos están en el origen (a_k = 0 salvo a₀), el filtro es **FIR**; si hay polos fuera del origen, es **IIR**.

### La respuesta en frecuencia vive en la circunferencia unidad

La DTFT es H(z) evaluada en z = e^{jΩ}, que recorre la circunferencia unidad: Ω = 0 es z = 1, Ω = π es z = −1. Igual que en el plano s,

> |H(e^{jΩ})| = |k| · Π |e^{jΩ} − c_i| / Π |e^{jΩ} − p_j|.

- Un **polo** de radio r cerca de la circunferencia, en ángulo Ω₀, da un **pico** en Ω₀, de anchura aproximada 2(1 − r) rad a −3 dB.
- Un **cero sobre la circunferencia** anula la respuesta: un **nulo** o muesca.
- Polos o ceros en el origen solo añaden un retraso (fase lineal), sin cambiar el módulo.
- Un paso bajo tiene polos cerca de z = 1 o ceros cerca de z = −1; un paso alto, al revés.

### Estabilidad y respuesta al impulso

Cada polo p aporta un término pⁿ a h[n]. El filtro causal es **estable si todos los polos tienen |p| < 1**. Un polo de radio r cerca de 1 da un pico estrecho y una h[n] que se extingue despacio, como rⁿ: cuantas más muestras dura, más selectivo es. Un polo negativo alterna el signo de h[n].

### Diseño a mano

Con esta lectura se diseñan filtros sencillos colocando polos y ceros: un **resonador** (polos cerca de la circunferencia), un **filtro de muesca** (ceros sobre ella y polos justo dentro, en el mismo ángulo, para que la muesca sea estrecha), un **paso todo** (cada polo p con un cero en 1/p*, de modo que el módulo es constante).

## Guía de uso

- **Cargar un ejemplo** pone polos y ceros de un filtro típico.
- En el plano z, con **Mover**, arrastra polos (×) y ceros (○); los complejos se mueven con su conjugado y los reales se pegan al eje. Con **Añadir polo**, **Añadir cero** o **Borrar**, haz clic.
- **Ω₀** mueve el punto de prueba e^{jΩ₀} por la circunferencia; las líneas de puntos son los vectores hasta él.
- A la derecha, el módulo en dB (normalizado a un máximo de 0 dB), la fase y h[n]. Si hay más ceros que polos, se añaden polos en el origen para que sea causal.

## Ejercicios

**1. Polo real.** Carga el paso bajo de un polo (p = 0,8) y después el paso alto (p = −0,8). ¿Cómo son h[n] y el módulo? Mueve el polo de 0,8 a 0,5, como en el ejercicio 2 b de la hoja.

<details><summary>Solución</summary>
Con p = 0,8, h[n] = 0,8ⁿ y el módulo cae desde Ω = 0, donde el polo está más cerca. Con p = −0,8, h[n] = (−0,8)ⁿ alterna y el máximo está en Ω = π. Con p = 0,5, h[n] decae más rápido y el paso bajo es más ancho: el módulo baja solo unos 9,5 dB hasta Ω = π.
</details>

**2. Resonador.** Carga el resonador (polos en 0,95e^{±j}). ¿Dónde está el pico y qué anchura tiene? ¿Cómo es h[n]?

<details><summary>Solución</summary>
En Ω ≈ 1 rad/muestra, con una anchura de unos 2(1 − 0,95) = 0,1 rad a −3 dB. h[n] es una sinusoide de frecuencia 1 rad/muestra que decae como 0,95ⁿ: tarda unas 20 muestras en bajar a e^{−1}.
</details>

**3. El ejercicio 3 de la hoja: muesca.** Carga la muesca (ceros en e^{±j}, polos en 0,9e^{±j}). ¿Qué pasa en Ω = 1? ¿Qué hacen los polos? Para eliminar 50 Hz a fs = 1 kHz, ¿dónde irían ceros y polos?

<details><summary>Solución</summary>
|H| = 0 en Ω = 1, y el resto del espectro pasa casi plano: cerca del cero, el polo está casi a la misma distancia y su efecto se compensa, salvo muy cerca de la muesca. Si se acerca el polo a la circunferencia, la muesca se estrecha. Para 50 Hz, Ω₀ = 2π·50/1000 = 0,1π: ceros en e^{±j0,1π} y polos en 0,95e^{±j0,1π}, con una muesca de unos 2(1 − 0,95)·1000/2π ≈ 16 Hz.
</details>

**4. Paso todo y FIR.** Carga el paso todo de primer orden (polo en 0,7 y cero en 1/0,7). ¿Cómo es el módulo? Carga después la media móvil de 5 muestras: ¿dónde están los ceros y cómo es h[n]?

<details><summary>Solución</summary>
El paso todo tiene módulo constante, 0 dB, porque la distancia al cero es siempre 1/0,7 veces la distancia al polo; solo cambia la fase. La media móvil tiene ceros en e^{±j2π/5} y e^{±j4π/5}, y la herramienta añade 4 polos en el origen: h[n] tiene 5 muestras iguales y luego es nula.
</details>

**5. Inestable.** Carga el ejemplo inestable (polos en 1,1e^{±j0,6}). ¿Qué hace h[n]? Arrastra los polos hacia dentro: ¿con qué radio deja de crecer?

<details><summary>Solución</summary>
h[n] oscila con amplitud creciente, como 1,1ⁿ. Deja de crecer al llegar a |p| = 1: con radio 1 oscila sin decaer (marginalmente estable) y por debajo de 1 decae. El módulo dibujado no tiene sentido físico mientras el sistema es inestable.
</details>

## Para profundizar

- [Apuntes del Tema 4](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Apuntes.pdf), sección 1, «Polos, ceros y diseño a mano» y «Filtros FIR e IIR».
- [Transparencias T4-01](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%2001%20-%20Introducci%C3%B3n.pdf), polos, ceros y respuesta en frecuencia.
- [Hoja de ejercicios del Tema 4](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Ejercicios.pdf), ejercicios 2 y 3, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Ejercicios%20resueltos.pdf).
- A. V. Oppenheim y R. W. Schafer, *Discrete-Time Signal Processing*, 3.ª ed., Pearson, 2010, apartados 5.3 y 5.4.
- J. H. McClellan, R. W. Schafer y M. A. Yoder, *DSP First*, 2.ª ed., Pearson, 2016, capítulos 9 y 10.

## Relación con otros conceptos

- **Transformada Z (Tema 1).** Herramienta: [Región de convergencia](T1-region-convergencia.html).
- **Plano s.** La misma lectura sobre el eje imaginario. Herramienta: [Polos y ceros en el plano s](T4-polos-ceros-s.html).
- **Exponenciales discretas.** Cada polo aporta pⁿ a h[n]. Herramienta: [Exponencial compleja discreta](T1-exponencial-discreta.html).
- **Peine y muescas.** Herramienta: [Filtro en peine](T4-peine.html).
- **Paso todo y fase mínima.** Herramienta: [Fase mínima y paso todo](T4-fase-minima-paso-todo.html).
- **Cuantificación de coeficientes.** Lo sensibles que son los polos a los coeficientes. Herramienta: [Cuantificación de coeficientes](T4-cuantificacion-coeficientes.html).
