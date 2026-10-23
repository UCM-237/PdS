## Introducción

### Diseñar solo paso bajos

Las fórmulas de Butterworth, Chebyshev y elíptico dan un **prototipo** paso bajo normalizado, con corte en ω = 1. Los demás filtros se obtienen sustituyendo s por una función de s que lleva el eje de frecuencias del prototipo al del filtro deseado. Así, todo el trabajo de aproximación se hace una sola vez.

### Las cuatro transformaciones

| Filtro | Sustitución en el prototipo | Orden |
|---|---|---|
| Paso bajo con corte ω₁ | s → s/ω₁ | N |
| Paso alto con corte ω₁ | s → ω₁/s | N |
| Paso banda de ω₁ a ω₂ | s → (s² + ω₀²)/(B s) | 2N |
| Banda eliminada de ω₁ a ω₂ | s → B s/(s² + ω₀²) | 2N |

con **ω₀ = √(ω₁ω₂)**, la frecuencia central geométrica, y **B = ω₂ − ω₁**, el ancho de banda.

- El **paso alto** invierte el eje: la frecuencia ω del filtro corresponde a ω₁/ω del prototipo, y los polos p van a ω₁/p.
- El **paso banda** lleva ω = 0 del prototipo a ω₀ y los bordes ±1 a ω₁ y ω₂. Cada polo del prototipo da dos polos, así que el orden se duplica. La respuesta tiene **simetría geométrica**: |H| es igual en ω y en ω₀²/ω, no en ω₀ ± Δ.

### Plantillas para el prototipo

Para elegir el orden se traduce la plantilla del filtro a la del prototipo. En un paso banda, cada borde de la banda eliminada ω_s va a

> ω′ = |ω_s² − ω₀²|/(B ω_s),

y se toma el más exigente (el menor). Si la plantilla no es geométricamente simétrica, uno de los dos bordes se cumple con margen.

### En discreto

Para un filtro digital se combinan dos pasos: se **predistorsionan** las frecuencias de corte con ω = (2/T) tan(Ω/2), se aplica la transformación analógica y se discretiza con la **bilineal**. Las frecuencias de corte quedan exactamente donde se pidieron. También existen transformaciones directas en el plano z (de Constantinides), que dan el mismo resultado.

## Guía de uso

- **Prototipo** elige Butterworth o Chebyshev I, con su **orden** y **rizado**.
- **Transformación** elige el tipo de filtro, y **Frecuencia de corte 1 y 2** sus bordes (la segunda solo en paso banda y banda eliminada).
- **Continuo o Discreto (bilineal)**: en discreto, las frecuencias son Ω en rad/muestra, se predistorsionan y se aplica la bilineal con 2/T = 2.
- Arriba, el prototipo, y los polos y ceros del filtro transformado. Abajo, el filtro transformado, con los bordes marcados. **Lineal o dB** cambia la escala.
- El recuadro da la sustitución, ω₀ y B, las frecuencias predistorsionadas y el orden.

## Ejercicios

**1. Paso alto.** Con un Butterworth de orden 3, elige paso alto con ω₁ = 1. ¿Dónde están los polos? ¿Qué atenuación tiene en ω = 0,5? Compárala con la del prototipo en ω = 2.

<details><summary>Solución</summary>
Los polos del prototipo están en la circunferencia unidad, y 1/p también: el paso alto tiene los mismos polos, más tres ceros en s = 0. La atenuación en ω = 0,5 es la del prototipo en 1/0,5 = 2: 10 log₁₀(1 + 2⁶) ≈ 18 dB.
</details>

**2. El ejercicio 7 de la hoja: paso banda.** Butterworth de orden 3, paso banda con ω₁ = 0,9 y ω₂ = 1,1 (las frecuencias de la hoja en kHz). ¿Qué ω₀ y B da la herramienta? ¿Qué orden tiene el filtro?

<details><summary>Solución</summary>
ω₀ = √0,99 = 0,995 y B = 0,2; el filtro es de orden 6, con seis polos agrupados en dos ternas cerca de ±jω₀. En la hoja, con 1 dB en la banda de paso y 30 dB en los bordes, el prototipo necesita N = 3.
</details>

**3. Simetría geométrica.** En el filtro anterior, en dB, compara la atenuación en 0,6 y en 1,5. ¿Por qué son distintas, si 0,6 está más lejos de ω₀?

<details><summary>Solución</summary>
0,6 va a |0,36 − 0,99|/(0,2·0,6) = 5,25 del prototipo y 1,5 a (2,25 − 0,99)/(0,2·1,5) = 4,2: unos 43 y 37 dB con el Butterworth de corte en 1. La respuesta es simétrica en escala logarítmica, alrededor de ω₀ (|H(ω)| = |H(ω₀²/ω)|), no en escala lineal: 0,6 y 1,5 no son simétricos, porque 0,6·1,5 = 0,9 ≠ 0,99.
</details>

**4. Chebyshev en banda eliminada.** Con un Chebyshev I de orden 2 y rizado 1 dB, elige banda eliminada de 0,8 a 1,6. ¿Cuántos polos y ceros tiene? ¿Dónde están los ceros?

<details><summary>Solución</summary>
Cuatro polos y cuatro ceros. Los ceros están sobre el eje imaginario en ±jω₀ = ±j1,13, dobles: la sustitución lleva el infinito del prototipo a ω₀, y ahí la respuesta se anula. El rizado de 1 dB aparece en las dos bandas de paso.
</details>

**5. El ejercicio 11 de la hoja: paso alto discreto.** Chebyshev I de orden 4, rizado 1 dB, paso alto, modo discreto, corte Ω₁ = 1,55 (casi π/2). ¿Qué ω predistorsionada da la herramienta? ¿Dónde quedan los ceros en el plano z?

<details><summary>Solución</summary>
ω₁ = 2 tan(1,55/2) = 1,96 (con Ω₁ = π/2 exacto saldría 2). Los cuatro ceros del paso alto en s = 0 van, con la bilineal, a z = 1: el filtro anula la continua. La respuesta tiene el rizado de 1 dB por encima de Ω₁, y los polos, dentro de la circunferencia unidad.
</details>

## Para profundizar

- [Apuntes del Tema 4](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Apuntes.pdf), sección 2, «Transformaciones de frecuencia», y sección 3, «Procedimiento de diseño» y «Transformaciones de frecuencia en discreto».
- [Transparencias T4-02](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%2002%20-%20Filtros%20continuos.pdf) y [T4-03](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%2003%20-%20Filtros%20IIR.pdf), transformaciones en frecuencia.
- [Hoja de ejercicios del Tema 4](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Ejercicios.pdf), ejercicios 7 y 11, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T4/codigo/python/paso_alto_continuo.py` e `iir_paso_banda.py`, y sus versiones en Matlab.
- A. V. Oppenheim y R. W. Schafer, *Discrete-Time Signal Processing*, 3.ª ed., Pearson, 2010, apartado 7.4.
- A. G. Constantinides, «Spectral transformations for digital filters», *Proceedings of the IEE*, 117(8), 1970.

## Relación con otros conceptos

- **Prototipos.** Herramienta: [Aproximaciones de filtros analógicos](T4-filtros-continuos.html).
- **Bilineal y predistorsión.** Herramienta: [Discretización de filtros IIR](T4-discretizacion-iir.html).
- **Polos y ceros.** Herramientas: [Polos y ceros en el plano s](T4-polos-ceros-s.html) y [Polos y ceros en el plano z](T4-polos-ceros-z.html).
- **Modulación (Tema 1).** En discreto, multiplicar h[n] por (−1)ⁿ convierte un paso bajo en paso alto: otra transformación de frecuencia. Herramienta: [Propiedades de la DFT](T3-propiedades-dft.html).
