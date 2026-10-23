## Introducción

### Partir del filtro ideal

El paso bajo ideal de corte Ω_c tiene respuesta al impulso

> h_d[n] = sin(Ω_c n)/(πn) = (Ω_c/π) sinc(Ω_c n/π),

que es infinita y no causal. El **método de las ventanas** la hace realizable en dos pasos: se trunca a |n| ≤ L multiplicándola por una ventana w[n] de 2L + 1 muestras, y se retrasa L muestras:

> h[n] = h_d[n − L] · w[n − L],  0 ≤ n ≤ 2L.

El resultado es un FIR de N = 2L + 1 coeficientes, simétrico, con fase lineal y retardo L. Un paso alto se obtiene igual a partir de h_d[n] = δ[n] − sin(Ω_c n)/(πn).

### Qué hace la ventana

Multiplicar por w[n] es convolucionar el espectro ideal con W(e^{jΩ}). El escalón del filtro ideal se convierte en una transición suave, y los lóbulos secundarios de la ventana producen rizado a los dos lados:

- La **anchura de la transición** ΔΩ es proporcional a la del lóbulo principal: se estrecha al aumentar L.
- El **rizado** y la atenuación de la banda eliminada dependen solo de la **forma** de la ventana, no de L.

### Fenómeno de Gibbs

Con la ventana rectangular (simple truncamiento), el rizado junto al borde es de un 9 % y la atenuación, de unos 21 dB, **por largo que sea el filtro**: al aumentar L, las oscilaciones se estrechan y se acercan al borde, pero no bajan. Es el fenómeno de Gibbs de la serie de Fourier. Para atenuar más hay que cambiar de ventana.

### Ventanas fijas

| Ventana | Atenuación (dB) | ΔΩ |
|---|---|---|
| Rectangular | 21 | 0,92π/L |
| Hann | 44 | 3,11π/L |
| Hamming | 53 | 3,32π/L |
| Blackman | 74 | 5,56π/L |

Se elige la ventana más sencilla que da la atenuación pedida y después L para la transición. El rizado de la banda de paso es del mismo orden que el de la eliminada, δ_p ≈ δ_s.

### Ventana de Kaiser

La ventana de Kaiser tiene un parámetro β que regula el compromiso entre lóbulo principal y lóbulos secundarios. Kaiser obtuvo fórmulas empíricas que dan β y L directamente a partir de la atenuación α_s y de la transición ΔΩ:

> β = 0,1102(α_s − 8,7) si α_s > 50;  β = 0,5842(α_s − 21)^{0,4} + 0,07886(α_s − 21) si 21 ≤ α_s ≤ 50;  β = 0 si α_s < 21,
> 2L ≥ (α_s − 8)/(2,285 ΔΩ).

## Guía de uso

- **Tipo** elige paso bajo o paso alto y **Ωc/π**, el centro de la transición.
- Con **Diseño = Ventana fija**, se elige la **ventana** y **L**; con Kaiser fija, el deslizador **β**.
- Con **Diseño = Kaiser a partir de α_s y ΔΩ**, β y L salen de las fórmulas con los deslizadores **α_s** y **ΔΩ/π**; L y β se ignoran.
- A la izquierda, h_d[n] (gris discontinua), la ventana (naranja) y h[n]. A la derecha, el módulo, con la banda de paso en verde y la eliminada en rojo, según la transición de la tabla o la pedida.
- El recuadro da N, el retardo, la transición, la atenuación conseguida y el rizado de la banda de paso.

## Ejercicios

**1. El ejercicio 15 de la hoja: Gibbs.** Paso bajo, ventana rectangular, Ωc/π = 0,5 y L = 10. En escala lineal, ¿cuánto vale el máximo de |H|? Sube L a 40: ¿qué cambia y qué no?

<details><summary>Solución</summary>
El máximo, cerca del borde, es 1,09: un 9 % de sobreoscilación, y |H(1)| = Σh[n] = 1,03. Con L = 40 la transición es cuatro veces más estrecha y las oscilaciones se acercan al borde, pero el máximo sigue en 1,09 y la atenuación en unos 21 dB.
</details>

**2. La tabla de las ventanas.** Paso bajo, Ωc/π = 0,4 y L = 16. Anota la atenuación con las cuatro ventanas fijas. ¿Depende de L? Compruébalo con L = 40.

<details><summary>Solución</summary>
Unos 20 dB con la rectangular, 44 con Hann, 54 con Hamming y 75 con Blackman. Con L = 40 las cifras apenas cambian: la atenuación la fija la forma de la ventana; L solo estrecha la transición.
</details>

**3. El ejercicio 13 a de la hoja.** Paso alto con Ωs = 0,4π, Ωp = 0,6π y 50 dB. ¿Qué ventana fija sirve? ¿Qué L hace falta? Configúralo y comprueba la atenuación.

<details><summary>Solución</summary>
Ωc = 0,5π y ΔΩ = 0,2π. Hann no llega (44 dB); Hamming sí. L ≥ 3,32π/0,2π = 16,6, así que L = 17 y 35 coeficientes. La herramienta da unos 54 dB en la banda eliminada y h[17] = 0,5.
</details>

**4. El ejercicio 13 b de la hoja: con Kaiser.** Mismo filtro con la ventana de Kaiser: α_s = 50 y ΔΩ/π = 0,2. ¿Qué β y qué L salen? ¿Se ahorran coeficientes?

<details><summary>Solución</summary>
β = 0,5842·29^{0,4} + 0,07886·29 = 4,53 y L = 15: 31 coeficientes en vez de 35, con unos 51 dB. Kaiser ajusta β para dar justo la atenuación pedida, mientras que Hamming da más de lo necesario.
</details>

**5. El ejercicio 14 de la hoja: un filtro de audio.** A 48 kHz, paso hasta 20 kHz y 80 dB desde 22 kHz. Paso bajo con Kaiser, Ωc/π = 0,88 (21 kHz), α_s = 80 y ΔΩ/π = 0,08. ¿Cuántos coeficientes salen? ¿Qué retardo hay en milisegundos?

<details><summary>Solución</summary>
β = 7,86 y L = 63: 127 coeficientes (la hoja, con ΔΩ = 0,0833π exacto, obtiene L = 61 y 123), con unos 80 dB. El retardo es L = 63 muestras, unos 1,3 ms. Un diseño equirrizado de Parks–McClellan necesitaría bastantes menos.
</details>

## Para profundizar

- [Apuntes del Tema 4](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Apuntes.pdf), sección 4 (Filtros FIR): «Método de las ventanas», «Fenómeno de Gibbs y ventanas fijas» y «Ventana de Kaiser».
- [Transparencias T4-04](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%2004%20-%20Filtros%20FIR.pdf), ventanas fijas y ventana de Kaiser.
- [Hoja de ejercicios del Tema 4](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Ejercicios.pdf), ejercicios 13 a 15, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T4/codigo/python/fir_ventana.py` y `fir_kaiser.py`, y sus versiones en Matlab.
- A. V. Oppenheim y R. W. Schafer, *Discrete-Time Signal Processing*, 3.ª ed., Pearson, 2010, apartados 7.5 y 7.6.
- J. F. Kaiser, «Nonrecursive digital filter design using the I₀-sinh window function», *Proc. IEEE Int. Symp. Circuits and Systems*, 1974.

## Relación con otros conceptos

- **Ventanas en el análisis espectral (Tema 3).** Las mismas ventanas, con el mismo compromiso entre lóbulo principal y secundarios. Herramienta: [Ventanas y fuga espectral](T3-ventanas.html).
- **Serie de Fourier (Tema 1).** El fenómeno de Gibbs aparece al truncar la serie de una onda cuadrada. Herramienta: [Serie de Fourier](T1-serie-fourier.html).
- **Fase lineal.** h[n] es simétrica: tipo I. Herramientas: [Tipos de FIR de fase lineal](T4-tipos-fir.html) y [Fase lineal y retardo de grupo](T4-fase-lineal.html).
- **Diseño óptimo.** Herramienta: [Parks–McClellan frente a ventanas](T4-parks-mcclellan.html).
- **Interpolación (Tema 2).** El filtro de un interpolador se diseña así. Herramienta: [Diezmado e interpolación](T2-diezmado-interpolacion.html).
