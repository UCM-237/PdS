## Introducción

### Simetría y fase lineal

Un FIR de longitud M, h[0], …, h[M − 1], tiene fase lineal si sus coeficientes son **simétricos**, h[n] = h[M − 1 − n], o **antisimétricos**, h[n] = −h[M − 1 − n]. Agrupando los términos que se corresponden, la respuesta en frecuencia queda

> H(e^{jΩ}) = A(Ω) e^{−jΩD}  (simétrica),  H(e^{jΩ}) = j A(Ω) e^{−jΩD}  (antisimétrica),

con D = (M − 1)/2 y A(Ω) **real**, una suma de cosenos o de senos. El retardo de grupo es constante, D muestras (que no es entero si M es par). En el caso antisimétrico la fase tiene además un término constante π/2.

### Los cuatro tipos

| Tipo | Simetría | M | A(Ω) | Ceros forzados | Sirve para |
|---|---|---|---|---|---|
| I | simétrica | impar | Σ cos(kΩ) | ninguno | cualquier filtro |
| II | simétrica | par | Σ cos((k − ½)Ω) | z = −1 | paso bajo, paso banda |
| III | antisimétrica | impar | Σ sin(kΩ) | z = 1 y z = −1 | paso banda, derivador, Hilbert |
| IV | antisimétrica | par | Σ sin((k − ½)Ω) | z = 1 | paso alto, paso banda, derivador, Hilbert |

Los ceros forzados salen de evaluar A: un coseno de semientero vale 0 en Ω = π, y un seno vale 0 en Ω = 0. Un tipo II no puede ser paso alto (H(−1) = 0) y un tipo IV no puede ser paso bajo (H(1) = 0).

### Dónde están los ceros

Como H(z) = ±z^{−(M−1)} H(1/z), si z₀ es un cero también lo es 1/z₀, y si los coeficientes son reales, también z₀*. Los ceros van en **cuartetos** z₀, z₀*, 1/z₀, 1/z₀*, salvo los que están sobre la circunferencia (parejas z₀, z₀*) o en el eje real (parejas z₀, 1/z₀). Un FIR de fase lineal no es de fase mínima: tiene tantos ceros fuera de la circunferencia como dentro.

## Guía de uso

- Haz clic en la gráfica de la izquierda para cambiar la mitad de los coeficientes, c[0] … c[4]. **Tipo** construye con ella h[n] completa (simétrica o antisimétrica, de longitud 9 o 10).
- A la derecha, h[n] con su centro de simetría marcado. Abajo, los ceros de H(z), con los forzados en rojo, y |H| junto a la amplitud real A(Ω), que puede ser negativa.
- El recuadro da M, el retardo D, los ceros forzados, para qué sirve el tipo y |H| en Ω = 0 y π.

## Ejercicios

**1. Tipo I.** Con la mitad de partida y el tipo I, ¿qué longitud y qué retardo tiene? ¿Qué filtro es? ¿Hay algún cero forzado?

<details><summary>Solución</summary>
M = 9 y D = 4 muestras. Es un paso bajo: |H(1)| = 1,8. Con estos coeficientes también hay un cero doble en z = −1, pero no es forzado (azul): si se cambia c[0], se mueve y |H(−1)| deja de ser nulo.
</details>

**2. Tipo II.** Cambia al tipo II. ¿Qué cambia en la longitud y el retardo? Edita la mitad para intentar que |H(−1)| no sea nulo. ¿Se puede?

<details><summary>Solución</summary>
M = 10 y D = 4,5: el retardo no es entero. El cero en z = −1 (rojo) no se mueve por mucho que se editen los coeficientes: |H(−1)| = 0 siempre. Un tipo II no sirve para paso alto ni banda eliminada.
</details>

**3. Tipos III y IV.** Prueba los tipos III y IV con la misma mitad. ¿Qué ceros forzados aparecen? ¿Qué filtros podrían ser?

<details><summary>Solución</summary>
El III tiene ceros en z = 1 y z = −1 y la muestra central nula: |H| se anula en Ω = 0 y π, así que solo puede ser paso banda (o un derivador o Hilbert, que no necesitan las frecuencias extremas). El IV tiene un cero en z = 1 y |H(−1)| = 0,6: sirve para paso alto, pero nunca para paso bajo.
</details>

**4. Cuartetos.** En el tipo I, busca un cero fuera de la circunferencia, por ejemplo el de z ≈ 2,97 en el eje real. ¿Dónde está su pareja? Arrastra c[2]: ¿se mueven juntos?

<details><summary>Solución</summary>
En 1/2,97 ≈ 0,34. Al editar los coeficientes, los ceros se mueven siempre en grupos: los reales, en parejas z₀ y 1/z₀; los complejos, en cuartetos; los de la circunferencia, en parejas conjugadas que se desplazan por ella.
</details>

**5. El ejercicio 12 de la hoja.** Clasifica h = (1, 3, 3, 1) y h = (1, −2, 2, −1). Da su retardo y sus ceros, y di si podrían ser paso bajo o paso alto.

<details><summary>Solución</summary>
(1, 3, 3, 1) es simétrica con M = 4: tipo II, retardo 1,5. H(z) = (1 + z^{−1})³: triple cero en −1 y A(0) = 8. Paso bajo, nunca paso alto. (1, −2, 2, −1) es antisimétrica con M = 4: tipo IV, retardo 1,5 y desfase π/2. H(z) = (1 − z^{−1})(1 − z^{−1} + z^{−2}): ceros en 1 y e^{±jπ/3}, y |H(−1)| = 6. Paso alto.
</details>

## Para profundizar

- [Apuntes del Tema 4](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Apuntes.pdf), sección 4 (Filtros FIR), «Fase lineal».
- [Transparencias T4-04](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%2004%20-%20Filtros%20FIR.pdf), filtros FIR de fase lineal.
- [Hoja de ejercicios del Tema 4](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Ejercicios.pdf), ejercicio 12, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Ejercicios%20resueltos.pdf).
- A. V. Oppenheim y R. W. Schafer, *Discrete-Time Signal Processing*, 3.ª ed., Pearson, 2010, apartado 5.7.3.

## Relación con otros conceptos

- **Fase lineal y retardo de grupo.** Herramienta: [Fase lineal y retardo de grupo](T4-fase-lineal.html).
- **Diseño por ventanas.** Da filtros de tipo I (paso bajo y paso alto). Herramienta: [Diseño FIR por ventanas](T4-fir-ventana.html).
- **Parks–McClellan.** El algoritmo trabaja con A(Ω). Herramienta: [Parks–McClellan frente a ventanas](T4-parks-mcclellan.html).
- **Fase mínima.** Un FIR de fase lineal tiene ceros a los dos lados de la circunferencia. Herramienta: [Fase mínima y paso todo](T4-fase-minima-paso-todo.html).
- **Par e impar (Tema 1).** Simétrica y antisimétrica son par e impar respecto al centro. Herramienta: [Par, impar, energía y potencia](T1-par-impar-energia.html).
