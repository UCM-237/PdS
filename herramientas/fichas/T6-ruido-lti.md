## Introducción

### Media y autocorrelación de la salida

Si una señal estacionaria x[n] atraviesa un sistema LTI de respuesta al impulso h[n], la salida y = h ∗ x también es estacionaria, con

> μ_y = H(e^{j0}) μ_x,  φ_yy[l] = (h ∗ h̃ ∗ φ_xx)[l],  φ_yx[l] = (h ∗ φ_xx)[l],

donde h̃[n] = h[−n]. En frecuencia, con la **densidad espectral de potencia** Φ(e^{jΩ}), la DTFT de la autocorrelación:

> Φ_yy(e^{jΩ}) = |H(e^{jΩ})|² Φ_xx(e^{jΩ}),  Φ_yx(e^{jΩ}) = H(e^{jΩ}) Φ_xx(e^{jΩ}).

### Ruido coloreado

Si la entrada es ruido blanco de varianza σ², Φ_xx = σ² es plana y Φ_yy = σ²|H|²: la salida es **ruido coloreado** con la forma del filtro. Su potencia es σ² Σ h²[k] = (σ²/2π) ∫ |H|² dΩ. Así se modelan muchas señales: un AR(1) es ruido blanco filtrado por 1/(1 − az^{−1}); la voz, ruido o un tren de pulsos filtrado por el tracto vocal.

### Identificación de un sistema

Para conocer un sistema desconocido, se excita con ruido blanco y se mide la salida, normalmente con un ruido de medida v independiente: y = h ∗ x + v. Entonces φ_yx[l] = σ²h[l] y Φ_yx = H σ²: la correlación cruzada da directamente la respuesta al impulso y el cociente Φ_yx/Φ_xx da H con módulo y fase. El ruido de medida no influye, porque es independiente de x. En cambio, Φ_yy = |H|²σ² + Φ_vv: el cociente Φ_yy/Φ_xx da |H|² más el ruido y pierde la fase.

## Guía de uso

- **Sistema**: el H(z) del ejemplo de los apuntes, un Butterworth paso bajo de orden 4, un AR(1), una media móvil o un resonador. El significado del **parámetro** aparece en su título (Ω_c, a, L o Ω₀).
- **σ de la entrada**, **σ del ruido de medida v**, **N** y la longitud de los tramos de Welch con los que se estiman las DEP (Hann y 50 % de solapamiento).
- Arriba, la entrada y la salida, y la respuesta al impulso con la correlación cruzada φ̂_yx[l]/σ². En el centro, la DEP de la salida estimada y la teórica σ²|H|² + σ_v², y la fase de H. Abajo, |H| verdadera y sus dos estimaciones.
- El recuadro da la potencia de la salida medida y la teórica, la media de la salida y el número de tramos de Welch.

## Ejercicios

**1. La potencia de la salida.** Con el sistema de los apuntes y σ = 1, ¿qué potencia tiene la salida? ¿Por qué |H| es mayor que 1 en algunas frecuencias y, sin embargo, la potencia es menor que la de la entrada?

<details><summary>Solución</summary>
σ²Σh²[k] = 0,865 (medida, 0,875). Los polos están en 0,6 ± 0,6j (radio 0,85, ángulo π/4): hay un pico de |H| = 2,35 cerca de Ω = 0,77, pero |H| es pequeño en el resto (0,96 en Ω = 0 y 0,03 en Ω = π). La potencia es la media de σ²|H|² en [−π, π], no su máximo.
</details>

**2. Un AR(1).** Elige el AR(1) con a = 0,8 (parámetro 0,9). ¿Cuánto vale Φ_yy en Ω = 0 y en Ω = π? ¿Y la potencia de la salida?

<details><summary>Solución</summary>
Φ_yy = 1/|1 − 0,8e^{−jΩ}|²: 1/0,2² = 25 (14 dB) en Ω = 0 y 1/1,8² = 0,31 (−5 dB) en Ω = π. Es un ruido paso bajo. La potencia es 1/(1 − 0,64) = 2,78 (medida, 2,77). Es el ejercicio 15 de la hoja.
</details>

**3. La media móvil.** Con la media móvil de 3 muestras y σ ≈ √2, ¿qué potencia tiene la salida y dónde se anula su DEP? ¿Cómo es φ̂_yx[l]?

<details><summary>Solución</summary>
σ² Σh² = 2 · 3 · (1/9) = 2/3 (con σ = 1,41, 0,663). Φ_yy = (2/9)(1 + 2cos Ω)², que se anula en Ω = 2π/3: en dB la DEP estimada cae hacia el suelo del ruido de medida. φ̂_yx[l]/σ² reproduce h[l] = 1/3 en l = 0, 1, 2 y 0 en el resto. Es el ejercicio 16 de la hoja.
</details>

**4. Identificar con ruido de medida.** Con el sistema de los apuntes y σ_v = 0,3, compara las dos estimaciones de |H| cerca de Ω = π. ¿Por qué falla √(Φ̂_yy/Φ̂_xx)? ¿Qué pasa con σ_v = 0?

<details><summary>Solución</summary>
|H(e^{jπ})| = 0,034 (−29 dB). El cociente cruzado lo estima bien, con algo de ruido. √(Φ̂_yy/Φ̂_xx) = √(|H|² + σ_v²/σ²) se queda en unos 0,3 (−10,5 dB), porque el ruido de medida tiene más potencia que la señal filtrada en esas frecuencias. Con σ_v = 0 las dos coinciden. Es el ejercicio 17 de la hoja.
</details>

**5. La fase y la respuesta al impulso.** ¿Qué información da el cociente cruzado que no da Φ_yy? Compara la fase estimada con la verdadera y φ̂_yx[l]/σ² con h[l].

<details><summary>Solución</summary>
La fase: Φ_yx es complejo y su argumento es el de H, mientras que Φ_yy es real y positivo. La fase estimada sigue a la verdadera salvo donde |H| es tan pequeño que el ruido domina. Del mismo modo, φ̂_yx[l]/σ² reproduce h[l] (0,2, 0,54, 0,50…), con un error del orden de 1/√N.
</details>

**6. Tramos de Welch.** Con el Butterworth de Ω_c = 0,3π y N = 16 384, compara tramos de 64 y de 1024 muestras. ¿Qué cambia en las DEP estimadas?

<details><summary>Solución</summary>
Con 64 muestras hay 511 tramos: la estimación es muy suave (poca varianza), pero con poca resolución, y la caída del filtro se ve redondeada. Con 1024 hay 31 tramos: se resuelve bien la caída, pero la estimación es más ruidosa. Es el compromiso entre sesgo y varianza de [Periodograma y método de Welch](T6-periodograma-welch.html).
</details>

## Para profundizar

- [Apuntes del Tema 6](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%20Apuntes.pdf), sección 4, «Densidad espectral de potencia» y «Respuesta de un sistema LTI».
- [Transparencias T6-04](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%2004%20-%20An%C3%A1lisis%20espectral.pdf), sistema LTI, ruido coloreado e identificación de sistemas.
- [Hoja de ejercicios del Tema 6](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%20Ejercicios.pdf), ejercicios 15 a 17, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%20Ejercicios%20resueltos.pdf).
- J. S. Bendat y A. G. Piersol, *Random Data: Analysis and Measurement Procedures*, 4.ª ed., Wiley, 2010, capítulos 6 y 9.
- L. Ljung, *System Identification: Theory for the User*, 2.ª ed., Prentice Hall, 1999, capítulo 6.

## Relación con otros conceptos

- **Respuesta en frecuencia (Tema 4).** Herramienta: [Polos y ceros en el plano z](T4-polos-ceros-z.html).
- **Estimar la DEP.** Herramienta: [Periodograma y método de Welch](T6-periodograma-welch.html).
- **La autocorrelación del AR(1).** Herramienta: [Estimación de la autocorrelación](T6-autocorrelacion.html).
- **Correlación cruzada y retardos.** Herramienta: [Estimación de un retardo por correlación](T6-retardo-correlacion.html).
