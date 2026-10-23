## Introducción

### Aproximar el filtro ideal

El paso bajo ideal no se puede construir con un número finito de componentes. Lo que se hace es fijar una **plantilla**: la atenuación debe ser como mucho R_p dB hasta la frecuencia ω_p (banda de paso) y al menos R_s dB desde ω_s (banda eliminada), con una banda de transición entre ellas. Después se busca la función racional H(s) de menor orden N que cumple la plantilla. Hay cuatro soluciones clásicas, que reparten de forma distinta el error:

| Aproximación | Banda de paso | Banda eliminada | Ceros |
|---|---|---|---|
| Butterworth | máximamente plana | monótona | ninguno finito |
| Chebyshev I | rizado constante | monótona | ninguno finito |
| Chebyshev II | monótona | rizado constante | en el eje jω |
| Elíptico (Cauer) | rizado constante | rizado constante | en el eje jω |

### Butterworth

> |H(jω)|² = 1/(1 + (ω/ω_c)^{2N}).

Las 2N − 1 primeras derivadas de |H|² son nulas en ω = 0: es la respuesta más plana posible. Los polos están equiespaciados en una semicircunferencia de radio ω_c. En ω_c atenúa 3 dB y, lejos, cae 20N dB por década.

### Chebyshev

> |H(jω)|² = 1/(1 + ε² T_N²(ω/ω_p)),

donde T_N es el polinomio de Chebyshev (T₀ = 1, T₁ = x, T_{N+1} = 2xT_N − T_{N−1}), que oscila entre −1 y 1 en |x| ≤ 1 y crece muy deprisa fuera. El tipo I tiene N oscilaciones de amplitud fija en la banda de paso y polos en una elipse. Con el mismo orden, corta mucho más abrupto que Butterworth. El tipo II (inverso) lleva el rizado a la banda eliminada, con ceros en el eje imaginario, y es plano en la banda de paso.

### Elíptico

Tiene rizado constante en las dos bandas y ceros en el eje jω, que hacen la transición lo más estrecha posible: para una plantilla dada, es el de **menor orden**. A cambio, su fase es la más alejada de la lineal y su retardo de grupo tiene picos grandes junto al borde.

### Elegir

Las fórmulas de orden mínimo (`buttord`, `cheb1ord`, `cheb2ord`, `ellipord`) dan N para cada familia. El orden mínimo crece en este sentido: elíptico < Chebyshev < Butterworth, mientras la regularidad de la fase va al revés. Butterworth se prefiere si importa la forma de onda o la planitud; elíptico, si importa el coste.

## Guía de uso

- **Orden N**, **Rp**, **Rs** y **ωs** fijan el orden y la plantilla (con ωp = 1). La plantilla se dibuja sombreada.
- Arriba, el módulo en dB de las cuatro aproximaciones con el mismo N.
- **Aproximación seleccionada** elige la que se muestra abajo: polos y ceros, módulo lineal y retardo de grupo.
- **Normalizados**: Butterworth con −3 dB en ω = 1; Chebyshev I y elíptico con −Rp en ω = 1; Chebyshev II con −Rs en ω = 1. **Ajustados a la plantilla**: todos escalados para que cumplan la plantilla en ωp = 1 o en ωs.
- El recuadro da el orden mínimo de cada familia y la atenuación en ωs con el N elegido; con «Ajustados», ✓ o ✗ si cumple.

## Ejercicios

**1. El ejercicio 5 de la hoja: comparar familias.** Pon Rp = 0,5, Rs = 50 y ωs = 2. ¿Qué orden mínimo necesita cada familia? Con N = 5 y «Ajustados», ¿cuáles cumplen?

<details><summary>Solución</summary>
Butterworth 10, Chebyshev I y II 6, elíptico 5. Con N = 5 solo cumple el elíptico: los demás se quedan cortos de atenuación en ωs.
</details>

**2. El ejercicio 4 de la hoja: Butterworth.** Pon Rp = 3, Rs = 30 y ωs = 3 (la plantilla de 2 y 6 kHz, normalizada). ¿Qué orden sale? Con ese N, mira los polos del Butterworth.

<details><summary>Solución</summary>
N = 4 (3,15 redondeado). Los cuatro polos están en la circunferencia unidad, en ángulos de ±112,5° y ±157,5°: −0,38 ± 0,92j y −0,92 ± 0,38j. Chebyshev y elíptico se conformarían con 3 y 2.
</details>

**3. El ejercicio 6 de la hoja: Chebyshev I de orden 3.** Con N = 3, Rp = 1 y «Normalizados», ¿cuánto vale |H| en ω = 0 y en ω = 1? Mueve ωs a 2: ¿qué atenuación tiene? ¿Qué cambia con N = 4 en ω = 0?

<details><summary>Solución</summary>
|H(0)| = 1 (0 dB) y |H(j1)| = 1/E, −1 dB. En ω = 2, T₃(2) = 26 y la atenuación es 10 log₁₀(1 + 0,2589·676) = 22,5 dB. Con N par, |T_N(0)| = 1 y la respuesta empieza en −1 dB: el rizado arranca en su mínimo.
</details>

**4. La fase.** Con N = 4, Rp = 1 y Rs = 40, compara el retardo de grupo de Butterworth, Chebyshev I y elíptico. ¿Cuál tiene el pico más alto en la banda de paso?

<details><summary>Solución</summary>
Normalizados, el retardo en continua es parecido (unos 2,2 a 2,7 s), pero el pico junto al borde es de unos 3,9 s para Butterworth, 8,1 para Chebyshev I y 10,6 para el elíptico. Cuanto más abrupto es el corte, más varía el retardo y más se deforman los pulsos.
</details>

**5. Transición estrecha.** Con Rp = 1 y Rs = 40, baja ωs de 2 a 1,5. ¿Cuánto crece el orden mínimo de cada familia?

<details><summary>Solución</summary>
Butterworth pasa de 8 a 14; Chebyshev, de 5 a 7; elíptico, de 4 a 5. El Butterworth es el que más sufre al estrechar la transición, porque su caída depende solo de log ωs; el elíptico, el que menos.
</details>

## Para profundizar

- [Apuntes del Tema 4](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Apuntes.pdf), sección 2 (Filtros continuos): «Aproximación del módulo», «Butterworth», «Chebyshev», «Elíptico» y «Comparación».
- [Transparencias T4-02](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%2002%20-%20Filtros%20continuos.pdf), filtros continuos.
- [Hoja de ejercicios del Tema 4](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Ejercicios.pdf), ejercicios 4 a 6, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T4/codigo/python/butter_continuo.py` y `orden_continuos.py`, y sus versiones en Matlab.
- A. V. Oppenheim y R. W. Schafer, *Discrete-Time Signal Processing*, 3.ª ed., Pearson, 2010, apéndice B.
- L. D. Paarmann, *Design and Analysis of Analog Filters: A Signal Processing Perspective*, Kluwer, 2001.

## Relación con otros conceptos

- **Polos y ceros en el plano s.** Herramienta: [Polos y ceros en el plano s](T4-polos-ceros-s.html).
- **Transformaciones en frecuencia.** De un prototipo paso bajo a paso alto o paso banda. Herramienta: [Transformaciones en frecuencia](T4-transformaciones-frecuencia.html).
- **Filtros IIR.** Estos prototipos se discretizan. Herramienta: [Discretización de filtros IIR](T4-discretizacion-iir.html).
- **Retardo de grupo.** Herramienta: [Fase lineal y retardo de grupo](T4-fase-lineal.html).
- **Antialiasing y reconstrucción (Tema 2).** Los filtros analógicos de un sistema de muestreo. Herramienta: [Retenedores](T2-retenedores.html).
