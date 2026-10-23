## Introducción

### Diseñar minimizando el error máximo

El método de las ventanas es sencillo, pero no es óptimo: el error es mayor junto a la transición que lejos de ella, y la atenuación la fija el tipo de ventana, no la especificación. El diseño **equirrizado** plantea el problema al revés: entre todos los FIR de fase lineal de longitud M, buscar el que minimiza el **error máximo ponderado**

> E = max_{Ω ∈ bandas} W(Ω) · |A(Ω) − D(Ω)|,

donde D es la respuesta deseada (1 en la banda de paso, 0 en la eliminada), A la amplitud real del FIR y W un peso. La banda de transición no cuenta. Es un problema de aproximación de Chebyshev (minimax).

### El teorema de alternancia

A(Ω) es un polinomio en cos Ω. El **teorema de alternancia** dice que la solución óptima es la que tiene el error máximo con signos alternados en al menos L + 2 frecuencias de las bandas, siendo L el grado del polinomio. Por eso el resultado tiene **rizado constante** en cada banda: todas las oscilaciones llegan al mismo nivel. El algoritmo de **Remez**, que Parks y McClellan adaptaron a filtros en 1972, busca esas frecuencias de forma iterativa.

### Pesos

Con peso W en la banda eliminada frente a 1 en la de paso, el óptimo cumple

> δ_p/δ_s = W.

Así se reparte el error como pida la especificación: con 0,01 en la banda de paso y 10^{−4} en la eliminada, peso 100. Con una ventana, en cambio, δ_p ≈ δ_s siempre.

### Longitud necesaria

Una estimación de Kaiser para la longitud es

> M − 1 ≈ (−20 log₁₀ √(δ_p δ_s) − 13)/(14,6 Δf),

con Δf = (Ω_s − Ω_p)/2π. Para una misma especificación, Parks–McClellan necesita menos coeficientes que cualquier ventana, y la diferencia crece cuando δ_p puede ser mayor que δ_s. Es el método de diseño FIR estándar: `remez` en SciPy, `firpm` en Matlab.

## Guía de uso

- **Longitud M**, **Ωp/π** (borde de la banda de paso) y **(Ωs − Ωp)/π** (transición) fijan el filtro. **Peso** es el de la banda eliminada frente a la de paso.
- **Ventana para comparar** elige la ventana del diseño alternativo, con la misma longitud y el corte en el centro de la transición.
- Arriba, |H| en dB de los dos diseños, con las bandas sombreadas, y el detalle lineal de la banda de paso. Abajo, las dos respuestas al impulso.
- El recuadro da δ_p y δ_s medidos para los dos, el cociente δ_p/δ_s del óptimo y la transición que necesitaría la ventana.
- Los diseños equirrizados están precalculados con SciPy para las longitudes y bordes de los controles.

## Ejercicios

**1. Equirrizado.** Con los valores de partida (M = 31, Ωp = 0,3π, transición 0,1π, peso 1), mira el detalle de la banda de paso y el rizado de la eliminada. ¿Cuánto valen δ_p y δ_s?

<details><summary>Solución</summary>
δ_p ≈ δ_s ≈ 0,025 (−32 dB). Todas las oscilaciones de cada banda llegan al mismo nivel, a diferencia del diseño con Hamming, cuyas oscilaciones decrecen lejos de la transición.
</details>

**2. Frente a la ventana.** Con la misma configuración, ¿cuánto atenúa el diseño con Hamming? ¿Por qué tan poco? ¿Y con M = 51?

<details><summary>Solución</summary>
Solo unos 17 dB: la ventana de Hamming necesita una transición de unos 6,6π/M = 0,21π con M = 31, el doble de la pedida, así que su banda de transición invade la eliminada. Con M = 51, Hamming llega a unos 29 dB y Parks–McClellan a 48 dB.
</details>

**3. Pesos.** Con M = 31, cambia el peso a 5 y a 10. ¿Cómo cambian δ_p y δ_s? Compruébalo con el cociente del recuadro.

<details><summary>Solución</summary>
Con peso 5: δ_p ≈ 0,055 y δ_s ≈ 0,011 (−39 dB). Con peso 10: δ_p ≈ 0,067 y δ_s ≈ 0,0067 (−43 dB). El cociente δ_p/δ_s es exactamente el peso: se gana atenuación a cambio de rizado en la banda de paso, con la misma longitud.
</details>

**4. Transición.** Con M = 31 y peso 1, compara las transiciones 0,05π, 0,1π y 0,2π. ¿Cómo cambia la atenuación?

<details><summary>Solución</summary>
Unos −20 dB, −32 dB y −54 dB. Para una longitud dada, la atenuación crece casi linealmente con la anchura de la transición en dB, como dice la fórmula de Kaiser: −20 log₁₀ δ ≈ 13 + 14,6 Δf (M − 1).
</details>

**5. El ejercicio 14 b de la hoja: estimar la longitud.** Con la fórmula, ¿qué M hace falta para δ_p = δ_s = 0,025 y transición 0,1π? ¿Qué da la herramienta? Para el filtro de audio de la hoja (δ_p = 0,01, δ_s = 10^{−4}, Δf = 2/48), ¿cuántos coeficientes salen?

<details><summary>Solución</summary>
M − 1 ≈ (32 − 13)/(14,6·0,05) = 26: unos 27 coeficientes; la herramienta muestra que hacen falta 31. La fórmula es optimista con filtros cortos. Para el filtro de audio, M − 1 ≈ (60 − 13)/(14,6·2/48) = 77: unos 79 coeficientes, frente a 123 con la ventana de Kaiser.
</details>

## Para profundizar

- [Apuntes del Tema 4](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Apuntes.pdf), sección 4 (Filtros FIR), «Parks–McClellan y muestreo en frecuencia» y «Coste y retardo».
- [Transparencias T4-04](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%2004%20-%20Filtros%20FIR.pdf), diseño FIR.
- [Hoja de ejercicios del Tema 4](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Ejercicios.pdf), ejercicio 14, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Ejercicios%20resueltos.pdf).
- A. V. Oppenheim y R. W. Schafer, *Discrete-Time Signal Processing*, 3.ª ed., Pearson, 2010, apartado 7.7.
- T. W. Parks y J. H. McClellan, «Chebyshev approximation for nonrecursive digital filters with linear phase», *IEEE Transactions on Circuit Theory*, 19(2), 1972.

## Relación con otros conceptos

- **Diseño por ventanas.** Herramienta: [Diseño FIR por ventanas](T4-fir-ventana.html).
- **Tipos de FIR.** El diseño se hace sobre la amplitud real A(Ω) de un tipo I. Herramienta: [Tipos de FIR de fase lineal](T4-tipos-fir.html).
- **Chebyshev y elíptico.** El mismo criterio minimax, aplicado a filtros analógicos. Herramienta: [Aproximaciones de filtros analógicos](T4-filtros-continuos.html).
- **Ventanas (Tema 3).** Herramienta: [Ventanas y fuga espectral](T3-ventanas.html).
