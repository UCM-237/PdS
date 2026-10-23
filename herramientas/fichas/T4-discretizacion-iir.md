## Introducción

### De un filtro analógico a uno digital

El diseño clásico de filtros IIR aprovecha todo lo que se sabe de filtros analógicos: se diseña un prototipo H_a(s) (Butterworth, Chebyshev, elíptico) y se transforma en un H(z). La transformación debe llevar el semiplano izquierdo de s al interior de la circunferencia unidad, para conservar la estabilidad, y el eje jω a la circunferencia, para conservar la forma de la respuesta en frecuencia. Ningún método lo consigue todo a la vez.

### Invarianza al impulso

Se pide que h[n] sean las muestras de h_a(t): h[n] = T h_a(nT). Con H_a en fracciones simples,

> H_a(s) = Σ r_k/(s − p_k)  →  H(z) = Σ T r_k/(1 − e^{p_kT} z^{−1}).

Los polos van a **z = e^{pT}**: un polo estable da un polo dentro de la circunferencia. La respuesta temporal se conserva en los instantes de muestreo, pero en frecuencia

> H(e^{jωT}) = Σ_m H_a(j(ω − 2πm/T)):

el espectro se repite cada ω_s = 2π/T y se **solapa** (aliasing), porque ningún filtro analógico tiene banda limitada. Funciona bien con paso bajos muy atenuados por encima de ω_s/2; no sirve para paso altos.

### Transformación bilineal

Se sustituye

> s = (2/T)(1 − z^{−1})/(1 + z^{−1}).

Todo el eje jω, de 0 a ∞, va a la circunferencia, de Ω = 0 a π: no hay aliasing. A cambio, el eje se **comprime** de forma no lineal:

> Ω = 2 arctan(ωT/2),  ω = (2/T) tan(Ω/2).

A bajas frecuencias Ω ≈ ωT, pero cerca de ω_s/2 la compresión es fuerte. Se corrige **predistorsionando** las frecuencias críticas: se diseña el analógico con ω = (2/T) tan(Ω/2) para que, tras la bilineal, los bordes queden en las Ω pedidas. Es el método habitual.

### Otros métodos

- **Correspondencia de polos y ceros**: polos y ceros finitos a e^{pT}; los ceros en infinito, a z = −1; se ajusta la ganancia.
- **Euler hacia atrás**, s = (1 − z^{−1})/T: siempre estable, pero deforma la respuesta si T no es pequeño.
- **Euler hacia delante**, s = (z − 1)/T: un polo estable puede quedar fuera de la circunferencia. No se debe usar.

## Guía de uso

- **Método** elige la transformación. El prototipo es un Butterworth de **orden N** y corte **ωc**, discretizado con **periodo T**.
- Arriba, los polos del prototipo en el plano s y los polos y ceros de H(z). Después, el módulo analógico (gris) y el digital (azul) hasta ω_s/2 = π/T, en **Lineal o dB**.
- Abajo, la respuesta al **escalón** o al **impulso** (h[n]/T, para compararla con h(t)): analógica continua y digital en t = nT.
- El recuadro da ω_s/2, ωc·T, la estabilidad y la ganancia en continua y en Ω = π.

## Ejercicios

**1. Invarianza al impulso: la ganancia.** Con N = 1, ωc = 1 y la invarianza al impulso, ¿cuánto vale la ganancia en continua con T = 0,05, 0,5 y 2? ¿Por qué no es 1?

<details><summary>Solución</summary>
H(1) = T/(1 − e^{−T}): 1,03, 1,27 y 2,31. Es el aliasing: H(e^{j0}) suma las copias de H_a(jω) desplazadas múltiplos de ω_s, y la del primer orden cae despacio. Con T pequeño las copias están lejos y la ganancia tiende a 1. En el ejercicio 8 de la hoja, con T = 0,1, sale 0,4992 en vez de 0,5.
</details>

**2. Lo que se conserva.** Con N = 2, ωc = 1, T = 0,5 y la respuesta al impulso, compara h[n]/T con h(t). Cambia a la bilineal: ¿siguen coincidiendo?

<details><summary>Solución</summary>
Con la invarianza al impulso, h[n]/T cae exactamente sobre h(t) en cada t = nT: es lo que define el método. Con la bilineal, la respuesta al impulso es parecida pero no igual, y en n = 0 tiene un valor distinto, porque la bilineal añade ceros en z = −1.
</details>

**3. Deformación del eje.** Con N = 2, ωc = 1, T = 1 y la bilineal sin predistorsión, ¿cuánto vale |H| en ω = 1 (Ω = 1)? Cambia a bilineal con predistorsión.

<details><summary>Solución</summary>
Unos 0,64 en lugar de 0,707: el corte digital ha quedado en Ω = 2 arctan(0,5) = 0,93, por debajo de lo pedido. Con predistorsión, el analógico se diseña con ωc = 2 tan(0,5) = 1,09 y el digital da exactamente 0,707 en Ω = 1. Con T = 2 el error sin predistorsionar es mucho mayor: |H| = 0,38 en ω = 1. Es el ejercicio 10 de la hoja.
</details>

**4. Euler hacia delante.** Con N = 2, ωc = 5 y Euler hacia delante, sube T desde 0,05. ¿A partir de qué T se vuelve inestable? ¿Pasa lo mismo con Euler hacia atrás?

<details><summary>Solución</summary>
Los polos van a z = 1 + pT. Con p = 5e^{±j3π/4}, |1 + pT| = 1 cuando T = −2 Re p/|p|² ≈ 0,28. Con T = 0,5 los polos están en |z| ≈ 1,93. Con Euler hacia atrás, z = 1/(1 − pT) siempre queda dentro de la circunferencia si Re p < 0: es estable para cualquier T, aunque muy deformado.
</details>

**5. Todos se parecen con T pequeño.** Con N = 3, ωc = 1 y T = 0,05, compara los seis métodos en la respuesta al escalón. Repite con T = 1.

<details><summary>Solución</summary>
Con T = 0,05 (ωcT = 0,05, unas 125 muestras por periodo de la frecuencia de corte) todos coinciden prácticamente con el analógico. Con T = 1 se separan. La invarianza al impulso sigue las muestras de la respuesta analógica. La bilineal se adelanta un poco, porque sus ceros en z = −1 dejan pasar algo de la entrada desde n = 0. Euler hacia atrás pierde la sobreoscilación y sube suavemente. Euler hacia delante lleva dos polos justo a la circunferencia unidad (|1 + pT| = 1) y la salida oscila sin amortiguarse: la herramienta lo marca como inestable. Discretizar bien exige una frecuencia de muestreo holgada.
</details>

## Para profundizar

- [Apuntes del Tema 4](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Apuntes.pdf), sección 3 (Filtros IIR): «Invarianza al impulso», «Transformada bilineal» y «Procedimiento de diseño».
- [Transparencias T4-03](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%2003%20-%20Filtros%20IIR.pdf), filtros IIR.
- [Hoja de ejercicios del Tema 4](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Ejercicios.pdf), ejercicios 8 a 11, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T4/codigo/python/iir_bilineal.py` y su versión en Matlab.
- A. V. Oppenheim y R. W. Schafer, *Discrete-Time Signal Processing*, 3.ª ed., Pearson, 2010, apartados 7.1 a 7.3.

## Relación con otros conceptos

- **Aliasing (Tema 2).** La invarianza al impulso es muestrear h(t). Herramienta: [Aliasing](T2-aliasing.html).
- **Prototipos.** Herramienta: [Aproximaciones de filtros analógicos](T4-filtros-continuos.html).
- **Transformaciones en frecuencia.** Paso alto y paso banda discretos con la bilineal. Herramienta: [Transformaciones en frecuencia](T4-transformaciones-frecuencia.html).
- **Estabilidad (Tema 1).** Del semiplano izquierdo al interior de la circunferencia. Herramienta: [Región de convergencia](T1-region-convergencia.html).
- **Implementación.** Herramienta: [Cuantificación de coeficientes](T4-cuantificacion-coeficientes.html).
