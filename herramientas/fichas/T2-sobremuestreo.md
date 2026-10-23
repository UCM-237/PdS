## Introducción

### La idea: repartir el ruido en más banda

El ruido de cuantificación de un cuantificador de paso Δ tiene potencia Δ²/12 y, con el modelo de ruido blanco, se reparte por igual en toda la banda [0, π] de la señal discreta, es decir, entre 0 y fs/2. Si la señal útil solo ocupa hasta f_B y se muestrea con fs = 2R f_B, siendo R el **factor de sobremuestreo**, solo la fracción 1/R del ruido cae en la banda útil. Un filtro digital paso bajo elimina el resto y después se diezma por R. La SQNR en la banda mejora en

> 10 log₁₀ R dB:

3 dB, medio bit, cada vez que se duplica R. Para ganar 4 bits haría falta R ≈ 256: el sobremuestreo solo es caro.

### Conformado de ruido

Los conversores **sigma-delta** hacen algo más: realimentan el error de cuantificación para que el ruido no sea blanco, sino que se acumule en las frecuencias altas, fuera de la banda útil. Con realimentación de primer orden, la salida es

> y[n] = x[n] + e[n] − e[n − 1],

así que el ruido se filtra con 1 − z^{−1}, que vale 0 en Ω = 0 y 2 en Ω = π. La potencia de ruido que queda en la banda |Ω| < π/R se reduce mucho más: la mejora sobre el caso sin sobremuestrear es

> 10 log₁₀(3R³/π²) dB (primer orden),  10 log₁₀(5R⁵/π⁴) dB (segundo orden, ruido filtrado con (1 − z^{−1})²),

unos 9 dB por cada duplicación de R con primer orden y 15 dB con segundo. En general, con orden L, unos 3(2L + 1) dB por duplicación.

### En la práctica

Así es como un conversor con un cuantificador de 1 o pocos bits, muy rápido, consigue 16 o 24 bits efectivos en audio: sobremuestreo alto, conformado de orden elevado y un filtro de diezmado digital. El precio es que la frecuencia de muestreo interna es muy alta y que los conformadores de orden alto pueden volverse inestables si el cuantificador satura.

## Guía de uso

- **R** es el factor de sobremuestreo: la banda de la señal es Ω < π/R (sombreada en verde).
- **B** es el número de bits del cuantificador y **Amplitud**, la del tono de prueba, situado al 30 % de la banda de la señal.
- **Sin conformar, 1.er orden o 2.º orden** elige la realimentación del error.
- Arriba, la entrada y la salida cuantificada. Abajo a la izquierda, el espectro de la salida y el del error (suavizado), con el eje de frecuencias en escala logarítmica. Abajo a la derecha, la SQNR teórica en la banda frente a R para los tres casos y, en rojo, la medida.
- La entrada lleva un ruido muy pequeño (σ = Δ/3) para que el error se comporte como el modelo; la SQNR solo mide el error de cuantificación.

## Ejercicios

**1. Tres decibelios por duplicación.** Sin conformar, con B = 4 y amplitud 0,5, mide la SQNR para R = 1, 2, 4, 8 y 16. ¿Cuánto sube cada vez?

<details><summary>Solución</summary>
Unos 3 dB por duplicación: de R = 1 a R = 16, unos 12 dB, que equivalen a 2 bits. El ruido total es el mismo; lo que baja es la fracción que cae en la banda.
</details>

**2. Primer orden.** Repite con conformado de 1.er orden. ¿Cuánto sube ahora por duplicación? Mira la forma del espectro del error.

<details><summary>Solución</summary>
Unos 9 dB por duplicación (para R grande). El error ya no es plano: crece con la frecuencia, unos 20 dB por década, y es muy pequeño dentro de la banda verde. Con R = 1 el conformado no ayuda (incluso empeora), porque no hay banda libre donde empujar el ruido.
</details>

**3. Segundo orden.** Con B = 4, R = 64 y conformado de 2.º orden, ¿qué SQNR se obtiene? ¿A cuántos bits equivale?

<details><summary>Solución</summary>
Más de 70 dB, frente a unos 20 dB sin sobremuestrear: unos 9 bits más, como un cuantificador de unos 13 bits. El recuadro da los bits efectivos.
</details>

**4. El ejercicio 16 b de la hoja.** Un conversor de 12 bits sobremuestrea por 16 sin conformar. Configúralo con amplitud 0,9 y compara la SQNR medida con 6,02·12 + 1,76 + 10 log₁₀ 16 = 86 dB.

<details><summary>Solución</summary>
Sale unos 85 dB: 1 dB menos porque la amplitud es 0,9 y no 1 (20 log₁₀ 0,9 ≈ −0,9 dB). La ganancia de 12 dB equivale a 2 bits: el conversor se comporta como uno de 14 bits.
</details>

**5. Pocos bits.** Con B = 2 y conformado de 2.º orden, sube la amplitud hasta 0,9. ¿Qué ocurre?

<details><summary>Solución</summary>
La realimentación hace que la entrada del cuantificador supere el margen y se sature: el error deja de ser pequeño y la SQNR se hunde. Los conformadores de orden alto necesitan limitar la amplitud de entrada, y por eso los sigma-delta reales trabajan por debajo del fondo de escala.
</details>

## Para profundizar

- [Apuntes del Tema 2](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%20Apuntes.pdf), sección 6, «Conversores con sobremuestreo».
- [Transparencias T2-04](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%2004%20-%20Muestreo%20discreto.pdf), conversores con sobremuestreo.
- [Hoja de ejercicios del Tema 2](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%20Ejercicios.pdf), ejercicio 16, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%20Ejercicios%20resueltos.pdf).
- A. V. Oppenheim y R. W. Schafer, *Discrete-Time Signal Processing*, 3.ª ed., Pearson, 2010, apartado 4.9.
- R. Schreier y G. C. Temes, *Understanding Delta-Sigma Data Converters*, IEEE Press y Wiley, 2005, capítulos 1 y 2.

## Relación con otros conceptos

- **Cuantificación.** El ruido Δ²/12 y la fórmula de 6 dB por bit. Herramienta: [Cuantificación y SQNR](T2-cuantificacion.html).
- **Diezmado.** Tras sobremuestrear se filtra y se diezma. Herramienta: [Diezmado e interpolación](T2-diezmado-interpolacion.html).
- **Filtros FIR.** 1 − z^{−1} es la diferencia, un paso alto con un cero en z = 1. Herramienta: [Respuesta de un sistema LTI discreto](T1-respuesta-lti-discreta.html).
- **Densidad espectral de potencia (Tema 6).** El ruido conformado tiene una PSD |1 − e^{−jΩ}|²Δ²/12.
