## Introducción

### Eco, retardo y ruido

Un radar, un sonar o un medidor de distancia por ultrasonidos emite un pulso x[n] y recibe un eco atenuado y retrasado, con ruido:

> y[n] = α x[n − D] + v[n].

El retardo D es lo que interesa: da la distancia (D/f_s por la velocidad de propagación, entre dos). Lo mismo pasa al alinear las señales de dos micrófonos o al sincronizar un receptor GPS con el código de un satélite.

### La correlación cruzada

La **correlación cruzada** compara el eco con el pulso desplazado l muestras:

> r_yx[l] = Σ_n y[n] x[n − l] = α r_xx[l − D] + Σ_n v[n] x[n − l].

El primer término es la autocorrelación del pulso, centrada en l = D, y su máximo vale α‖x‖², con ‖x‖² = Σ x²[n] la energía del pulso. El segundo es ruido de media nula y desviación σ‖x‖. El retardo se estima con la posición del máximo de r_yx. Es el **filtro adaptado**: la correlación con el pulso conocido es el filtro lineal que maximiza la relación señal-ruido a la salida, α²‖x‖²/σ².

### Qué pulso usar

- La **energía** del pulso fija la SNR a la salida: un pulso largo de poca amplitud funciona tan bien como uno corto y fuerte. Por eso se detectan ecos que no se ven en la señal.
- La **forma** de r_xx fija la precisión y la ambigüedad. Un pulso de **banda ancha** (ruido, un chirp) tiene una autocorrelación estrecha y sin picos secundarios: el máximo es nítido y único. Un pulso rectangular tiene un triángulo ancho; una sinusoide tiene muchos picos casi iguales, y el ruido puede hacer que gane uno equivocado.

## Guía de uso

- **Pulso emitido**: ruido blanco, un chirp, un pulso sinc, un pulso rectangular o una sinusoide, de **longitud L**.
- **Retardo verdadero D**, **atenuación α**, **σ del ruido** y **realización**. La señal recibida tiene 1024 muestras.
- Arriba, el pulso y la señal recibida, con el eco sin ruido en azul. Abajo, la autocorrelación del pulso y la correlación cruzada normalizada por ‖x‖², con el retardo verdadero (verde) y el estimado (rojo).
- El recuadro da el retardo estimado (en verde si acierta), la altura del pico sin ruido, la desviación del ruido de la correlación, la SNR a la salida y por muestra, y la anchura y el pico secundario de r_xx.

## Ejercicios

**1. Un eco que no se ve.** Con los valores de partida (ruido blanco, L = 128, α = 0,5, σ = 1), ¿se ve el eco en y[n]? ¿Qué SNR hay por muestra y a la salida del correlador? ¿Acierta?

<details><summary>Solución</summary>
No se ve: la SNR por muestra es −6 dB (el pulso tiene potencia 1 y amplitud α = 0,5, frente a un ruido de varianza 1). Pero a la salida es α²‖x‖²/σ² = 14,9 dB: el pico vale 0,5 y el ruido de la correlación tiene desviación σ/‖x‖ = 0,09. Acierta: D̂ = 300. La correlación suma de forma coherente las 128 muestras del eco.
</details>

**2. Más ruido.** Sube σ a 3 con L = 128. ¿Acierta? ¿Y con L = 32 y L = 256? ¿Qué SNR a la salida hace falta, más o menos?

<details><summary>Solución</summary>
Con σ = 3 la SNR a la salida baja a 5,4 dB y falla (D̂ = 309). Con L = 32 baja a 0,3 dB y falla de lejos; con L = 256 sube a 8,8 dB, pero entre las casi 800 posiciones posibles alguna de ruido supera aún al pico. Para acertar casi siempre hace falta que el pico supere al ruido unas 4 o 5 desviaciones típicas, unos 13 dB de SNR a la salida, porque se elige el máximo entre muchos valores.
</details>

**3. La forma del pulso.** Con σ = 1 y L = 128, compara el ruido blanco, el chirp y el pulso rectangular. ¿Cómo es r_xx en cada caso? ¿Qué precisión da cada uno?

<details><summary>Solución</summary>
El ruido blanco da un pico de una muestra (anchura 0 a media altura) con lóbulos secundarios de 0,15; el chirp, un pico de ±1 muestra; el rectangular, un triángulo de ±63 muestras a media altura. Los tres aciertan aquí (300, 300 y 302), pero con el rectangular el máximo está en una meseta suave y el ruido lo desplaza varias muestras: precisión mucho peor. El chirp es lo que usan los radares: banda ancha con amplitud constante.
</details>

**4. La sinusoide.** Con la sinusoide (L = 128, σ = 1), ¿cómo es r_xx? ¿Cuánto vale el pico secundario? Sube σ y cambia de realización: ¿qué errores aparecen?

<details><summary>Solución</summary>
r_xx es una cosinusoide con envolvente triangular y el pico secundario vale 0,90, a un periodo de distancia (unas 7 muestras). Con más ruido, el máximo salta a uno de los picos vecinos: el error es casi siempre un múltiplo del periodo. Es la ambigüedad de una señal de banda estrecha, el mismo problema que tendría un AR(1) con a = 0,95 en el ejercicio 14 de la hoja.
</details>

**5. La energía, no la amplitud.** Con L = 128 y σ = 1, ¿por qué el pulso sinc falla y el ruido blanco no, si los dos tienen amplitud máxima del orden de 1? ¿Qué α hace falta con ruido blanco para bajar a 4,5 dB?

<details><summary>Solución</summary>
El sinc de este ejemplo solo tiene unas 4 muestras grandes y su energía es ‖x‖² ≈ 4, frente a 128 del ruido: la SNR a la salida es 0 dB y falla. El ruido blanco tiene amplitud media 1 en todas las muestras. Con ruido blanco y α = 0,15, α²‖x‖²/σ² = 0,0225 · 125 ≈ 4,5 dB, y vuelve a fallar. Lo que cuenta es la energía del eco, α²‖x‖².
</details>

## Para profundizar

- [Apuntes del Tema 6](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%20Apuntes.pdf), sección 3, «Correlación cruzada».
- [Transparencias T6-03](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%2003%20-%20Se%C3%B1ales%20aleatorias.pdf), correlación cruzada y estimación de retardos.
- [Hoja de ejercicios del Tema 6](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%20Ejercicios.pdf), ejercicio 14, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T6%20-%20Ejercicios%20resueltos.pdf).
- M. A. Richards, *Fundamentals of Radar Signal Processing*, 2.ª ed., McGraw-Hill, 2014, capítulos 4 y 5 (filtro adaptado y compresión de pulsos).
- S. M. Kay, *Fundamentals of Statistical Signal Processing, vol. II: Detection Theory*, Prentice Hall, 1998, capítulo 4.

## Relación con otros conceptos

- **La autocorrelación.** Herramienta: [Estimación de la autocorrelación](T6-autocorrelacion.html).
- **Convolución (Tema 1).** La correlación es la convolución con el pulso invertido en el tiempo. Herramienta: [Convolución discreta](T1-convolucion-discreta.html).
- **Detección de tonos (Tema 5).** Goertzel también correla con una señal conocida. Herramienta: [Marcación por tonos (DTMF)](T5-dtmf.html).
- **Identificación.** La correlación entrada-salida da h[l]. Herramienta: [Ruido a través de un sistema LTI](T6-ruido-lti.html).
