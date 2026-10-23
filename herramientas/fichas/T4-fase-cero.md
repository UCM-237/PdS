## Introducción

### El problema del retardo

Un filtro causal siempre retrasa la señal: un FIR de fase lineal la retrasa (N − 1)/2 muestras y un IIR, un tiempo que además depende de la frecuencia. En tiempo real no hay alternativa, porque el filtro solo puede usar muestras pasadas. Pero si la señal ya está **grabada**, como un registro de ECG o un fichero de audio, se pueden usar también las muestras "futuras".

### Filtrar hacia delante y hacia atrás

El procedimiento de `filtfilt` (Matlab y SciPy) es:

1. Filtrar x[n] con H: v[n] = h[n] ∗ x[n].
2. Invertir el resultado en el tiempo, filtrarlo otra vez con H e invertirlo de nuevo.

Invertir en el tiempo conjuga la transformada de una señal real, así que la segunda pasada aplica H*(e^{jΩ}). En total:

> Y(e^{jΩ}) = H(e^{jΩ}) H*(e^{jΩ}) X(e^{jΩ}) = |H(e^{jΩ})|² X(e^{jΩ}).

La respuesta global es real y no negativa: **fase cero**. No hay retardo ni distorsión de fase, aunque H sea un IIR con fase muy no lineal.

### Consecuencias

- El módulo es |H|²: la atenuación en dB se **duplica**. En el corte de un Butterworth, −6 dB en lugar de −3 dB; la banda eliminada atenúa el doble. Si se quiere un corte en −3 dB hay que diseñar H con un corte algo mayor.
- La respuesta al impulso global, h[n] ∗ h[−n], es **simétrica respecto a n = 0**: no causal. Las oscilaciones de un filtro abrupto aparecen antes y después de cada flanco.
- Los bordes del registro necesitan tratamiento: `filtfilt` extiende la señal para reducir los transitorios.

Se usa mucho en análisis fuera de línea: biomedicina, sismología, procesado de imágenes (donde el "tiempo" es el espacio y no hay causalidad que respetar).

## Guía de uso

- **Señal** elige pulsos, escalones o un ECG simulado, con ruido de **desviación** ajustable.
- **Orden del Butterworth** y **Ωc/π** definen el paso bajo H.
- Arriba, la señal con ruido, la señal sin ruido (gris de puntos), la salida del filtro causal (rojo) y la de ida y vuelta (azul). Abajo, |H| y |H|², y la fase del causal frente a la fase cero.
- El recuadro da el retardo del filtro causal a bajas frecuencias.

## Ejercicios

**1. El retardo del causal.** Con los pulsos, orden 4 y Ωc/π = 0,08, ¿cuánto se retrasa la salida roja? ¿Y la azul? Sube Ωc/π a 0,2.

<details><summary>Solución</summary>
Unas 10 muestras con Ωc/π = 0,08: los picos rojos llegan tarde. La azul está alineada con la señal original. Con Ωc/π = 0,2, el retardo baja a unas 4 muestras: un filtro más ancho retrasa menos.
</details>

**2. Doble atenuación.** Compara |H| y |H|² en Ωc. ¿Cuántos dB atenúa cada uno? ¿Qué orden "equivalente" tiene el filtro de ida y vuelta?

<details><summary>Solución</summary>
|H(e^{jΩc})| = 0,707 (−3 dB) y |H|² = 0,5 (−6 dB). Lejos del corte, |H|² cae el doble de dB por década: como un Butterworth de orden 2N, pero con la fase nula.
</details>

**3. Orden alto.** Con los escalones y orden 8, compara las dos salidas. ¿Dónde aparecen las oscilaciones?

<details><summary>Solución</summary>
La roja se retrasa unas 20 muestras y oscila solo después de cada escalón, porque h[n] es causal. La azul no se retrasa y oscila a los dos lados del escalón, de forma simétrica, porque la respuesta global h[n] ∗ h[−n] es simétrica respecto a n = 0.
</details>

**4. El ECG.** Con el ECG simulado y ruido 0,15, ¿qué salida conserva la posición y la forma del complejo QRS (el pico estrecho)? ¿Por qué importa en medicina?

<details><summary>Solución</summary>
La de ida y vuelta: el pico queda en su sitio y con forma simétrica. El filtro causal lo retrasa y lo deforma de modo distinto que a las ondas lentas, porque el retardo de grupo depende de la frecuencia. En un ECG se miden intervalos entre ondas y su forma, y un filtro de fase no lineal falsearía esas medidas.
</details>

**5. El ejercicio 16 de la hoja.** Para F(z) = 0,2/(1 − 0,8z^{−1}), calcula la ganancia en Ω = 0 y en Ω = π con una pasada y con ida y vuelta, y el retardo en continua del filtro causal. ¿Se podría hacer en tiempo real?

<details><summary>Solución</summary>
F(1) = 1 y |F(−1)| = 0,2/1,8 = 0,111 (−19,1 dB). Con ida y vuelta, 1 y −38,2 dB, sin desfase. El retardo de grupo en continua de una pasada es a/(1 − a) = 4 muestras. No se puede en tiempo real: la pasada hacia atrás necesita toda la señal.
</details>

## Para profundizar

- [Apuntes del Tema 4](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Apuntes.pdf), sección 5 (Filtros especiales), «Fase cero».
- [Transparencias T4-05](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%2005%20-%20Filtros%20especiales.pdf), filtrado de fase cero.
- [Hoja de ejercicios del Tema 4](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Ejercicios.pdf), ejercicio 16, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T4/codigo/python/fase_cero.py` y su versión en Matlab.
- F. Gustafsson, «Determining the initial states in forward-backward filtering», *IEEE Transactions on Signal Processing*, 44(4), 1996.

## Relación con otros conceptos

- **Inversión temporal (Tema 1).** Invertir conjuga la transformada de una señal real. Herramientas: [Operaciones sobre la variable independiente](T1-variable-independiente.html) y [Propiedades de la transformada de Fourier](T1-propiedades-fourier.html).
- **Causalidad.** El filtro global no es causal. Herramienta: [Propiedades de los sistemas](T1-propiedades-sistemas.html).
- **Fase lineal y retardo de grupo.** Herramienta: [Fase lineal y retardo de grupo](T4-fase-lineal.html).
- **Butterworth discreto.** Herramienta: [Discretización de filtros IIR](T4-discretizacion-iir.html).
