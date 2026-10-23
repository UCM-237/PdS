## Introducción

### Una función racional

La función de transferencia de un filtro analógico de parámetros concentrados es un cociente de polinomios en s, que se escribe con sus raíces:

> H(s) = k · Π_i (s − c_i) / Π_j (s − p_j).

Los **ceros** c_i anulan H y los **polos** p_j la hacen infinita. Si los coeficientes son reales, los polos y ceros complejos van en pares conjugados. Conocidos los polos, los ceros y la ganancia k, el filtro está determinado.

### Leer el módulo con distancias

La respuesta en frecuencia es H(s) evaluada sobre el eje imaginario, s = jω. Cada factor (jω − p) es un vector que va del polo al punto jω, así que

> |H(jω)| = k · Π |jω − c_i| / Π |jω − p_j|,  ∠H(jω) = Σ ∠(jω − c_i) − Σ ∠(jω − p_j).

Esta lectura geométrica permite diseñar a mano:

- Un **polo cerca del eje** jω da un **pico** en la frecuencia correspondiente: la distancia se hace pequeña. Cuanto más cerca, más alto y estrecho, y su anchura a −3 dB es aproximadamente 2|Re p|.
- Un **cero sobre el eje** anula la respuesta en esa frecuencia: un **nulo**.
- Polos y ceros lejanos afectan poco y de forma suave.

### Estabilidad y respuesta temporal

Cada polo p aporta a la respuesta al impulso un término e^{pt}. Si **Re p < 0** decae, y el sistema es **estable** cuando todos los polos están en el semiplano izquierdo. Un par −σ ± jω_d oscila a ω_d y decae con constante de tiempo 1/σ: los polos cercanos al eje dan oscilaciones largas, la otra cara de un pico estrecho. Los ceros no afectan a la estabilidad, pero un cero en el semiplano derecho da el mismo módulo que su reflejado con más fase: **fase no mínima**.

## Guía de uso

- En el plano s, los polos son × y los ceros, ○. Con **Mover**, arrástralos (los complejos se mueven con su conjugado). Con **Añadir polo**, **Añadir cero** o **Borrar**, haz clic en el plano.
- **ω₀** mueve el punto de prueba jω₀ por el eje imaginario; las líneas de puntos son los vectores hasta él.
- A la derecha, el módulo en dB, la fase y la respuesta al escalón. La ganancia se ajusta para que H(0) = 1 (o el máximo, si hay polos o ceros en el origen).
- El recuadro dice si es estable y da |H(jω₀)| y las distancias.

## Ejercicios

**1. Distancias.** Con el filtro de partida (polos en −0,3 ± j y −1) y ω₀ = 1, comprueba |H(j1)| con las distancias del recuadro. ¿Dónde está el máximo del módulo?

<details><summary>Solución</summary>
Las distancias a los polos son 0,30, 2,02 y 1,41, y k = 1,09 para que H(0) = 1: |H(j1)| = 1,09/(0,30·2,02·1,41) = 1,27. El máximo está en ω ≈ 0,9, con unos +2,5 dB, junto al polo más próximo al eje.
</details>

**2. Resonancia.** Arrastra el par de polos a −0,1 ± j. ¿Qué pasa con el pico y con la respuesta al escalón?

<details><summary>Solución</summary>
El pico sube a unos +11 dB en ω ≈ 0,99 y se estrecha (anchura ≈ 2·0,1 = 0,2 rad/s). La respuesta al escalón oscila a 1 rad/s durante mucho más tiempo, con envolvente e^{−0,1t}: constante de tiempo de 10 s.
</details>

**3. Cruzar el eje.** Sigue moviendo el par hacia la derecha hasta pasar el eje. ¿Qué indica la herramienta? ¿Qué significa en el tiempo?

<details><summary>Solución</summary>
Con Re p ≥ 0 el sistema es inestable y la respuesta al escalón no está acotada: el término e^{pt} crece. El módulo que se dibuja ya no describe la respuesta en régimen permanente, que no existe.
</details>

**4. Un nulo.** Añade un cero en j1,5 (se añade también −j1,5). ¿Qué pasa en ω = 1,5? ¿Y lejos, en altas frecuencias?

<details><summary>Solución</summary>
|H(j1,5)| = 0: el módulo cae a −∞ dB en un nulo estrecho, como en los filtros de Chebyshev II y elípticos. En altas frecuencias el filtro cae más despacio, porque ahora tiene 3 polos y 2 ceros: −20 dB por década en vez de −60.
</details>

**5. El ejercicio 4 b de la hoja: un Butterworth de orden 4.** Borra los polos y coloca cuatro en ωc·e^{jπ(2k + 3)/8} con ωc = 1: −0,38 ± 0,92j y −0,92 ± 0,38j. ¿Cómo es el módulo? ¿Cuánto vale en ω = 1?

<details><summary>Solución</summary>
Plano hasta cerca de ω = 1 y −3 dB en ω = 1, el corte; después cae 80 dB por década. Los polos en una semicircunferencia equiespaciados dan la respuesta máximamente plana. La respuesta al escalón tiene una pequeña sobreoscilación, de un 11 %.
</details>

## Para profundizar

- [Apuntes del Tema 4](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Apuntes.pdf), sección 1, «Polos, ceros y diseño a mano», y sección 2 (Filtros continuos), «Butterworth».
- [Transparencias T4-02](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%2002%20-%20Filtros%20continuos.pdf), polos, ceros y respuesta en frecuencia.
- [Hoja de ejercicios del Tema 4](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Ejercicios.pdf), ejercicio 4, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T4/codigo/python/butter_continuo.py` y su versión en Matlab.
- A. V. Oppenheim, A. S. Willsky y S. H. Nawab, *Signals and Systems*, 2.ª ed., Prentice Hall, 1997, apartado 9.4.

## Relación con otros conceptos

- **Transformada de Laplace (Tema 1).** Polos, ceros y región de convergencia. Herramienta: [Región de convergencia](T1-region-convergencia.html).
- **Respuesta de un sistema continuo.** Herramienta: [Respuesta de un sistema LTI continuo](T1-respuesta-lti-continua.html).
- **Plano z.** La misma lectura sobre la circunferencia unidad. Herramienta: [Polos y ceros en el plano z](T4-polos-ceros-z.html).
- **Aproximaciones.** Dónde colocan los polos y ceros Butterworth, Chebyshev y elíptico. Herramienta: [Aproximaciones de filtros analógicos](T4-filtros-continuos.html).
