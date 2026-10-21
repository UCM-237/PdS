# Audio con ruido

## Contexto

Se ha digitalizado una grabación musical antigua de 10 s. El sistema de grabación y la copia han dejado cuatro tipos de ruido superpuestos, que es habitual encontrar juntos en restauración de audio:

- **zumbido** de la red eléctrica, con sus armónicos;
- **soplido** de banda ancha de la cinta o del preamplificador;
- **clics** cortos e intensos, como los de un disco de vinilo rayado;
- un **silbido** de frecuencia variable que aparece durante unos segundos.

El primer segundo de la grabación es silencio musical: solo contiene ruido. Tu trabajo es caracterizar cada ruido, diseñar el procesado adecuado para cada uno y medir cuánto mejora la señal.

## Objetivos de aprendizaje

Al terminar el proyecto deberías ser capaz de:

1. Leer el espectro de una señal real: resolución, ventana, escala en dB, rayas frente a ruido de banda ancha (T2, T3).
2. Traducir lo que ves en el espectro a una especificación de filtro y diseñar filtros IIR y FIR que la cumplan (T4).
3. Explicar las consecuencias de la fase de un filtro: retardo, distorsión y filtrado de fase cero (T4).
4. Modelar un ruido con herramientas estadísticas (histograma, autocorrelación, PSD) y usar ese modelo para detectar eventos y para diseñar un filtro de Wiener (T5).
5. Reconocer cuándo un problema no se puede resolver con un filtro invariante y resolverlo en el plano tiempo-frecuencia con la STFT (T6).
6. Validar un procesado con métricas cuantitativas y conocer sus límites.

## Datos

En `01_Datos/`:

| Fichero | Contenido |
|---|---|
| `audio_ruidoso.wav` | La señal que tienes que procesar: mono, 16 bits, fs = 16 kHz, 10 s |
| `audio_limpio.wav` | La misma música sin ruido. **Solo** puede usarse para medir el resultado (SNR), nunca como entrada del procesado |

La SNR de una señal procesada y frente a la referencia limpia s es

```
SNR = 10 log10( Σ s[n]² / Σ (y[n] − s[n])² )   (dB)
```

Fíjate en que penaliza cualquier diferencia con s: también un retardo o una distorsión de fase que no se oiría.

## Teoría mínima

**Zumbido de red.** La red es de 50 Hz y las no linealidades de la fuente de alimentación generan armónicos en 100, 150, … Hz. Cada raya se puede eliminar con una **muesca** de segundo orden, con ceros en e^{±jω₀} y polos en r·e^{±jω₀}:

```
H(z) = (1 − 2cos(ω₀) z⁻¹ + z⁻²) / (1 − 2r cos(ω₀) z⁻¹ + r² z⁻²)
```

El ancho de la muesca a −3 dB es aproximadamente (1 − r)·fs/π Hz. Otra opción es el **filtro peine** H(z) = (1 − z⁻ᴺ)/(1 − ρz⁻ᴺ) con N = fs/50, que anula a la vez todos los múltiplos de 50 Hz (ver T4, «Filtros peine»).

**Clics.** Un clic dura unas pocas muestras, así que su espectro es casi plano y no se puede separar de la música con un filtro. Lo que sí lo distingue es que **no es predecible**: si se predice cada muestra a partir de las anteriores con un modelo autorregresivo (AR), el error de predicción

```
e[n] = x[n] − Σ_{k=1..p} a_k x[n−k]
```

es pequeño en la música y muy grande en los clics. Los coeficientes a_k salen de las ecuaciones de Yule-Walker con la autocorrelación estimada (T5).

**Filtro de Wiener.** Si señal y ruido son incorrelados, el filtro lineal que minimiza el error cuadrático medio es H(f) = S_s(f) / (S_s(f) + S_n(f)) = (S_x(f) − S_n(f)) / S_x(f), con S_x la PSD de la señal ruidosa y S_n la del ruido, ambas estimadas (por ejemplo con el método de Welch).

**STFT y sustracción espectral.** Un filtro invariante aplica la misma H(f) todo el tiempo; si el ruido cambia de frecuencia con el tiempo, hace falta trabajar en el plano tiempo-frecuencia. La STFT divide la señal en tramas enventanadas y calcula la DFT de cada una; tras modificar los coeficientes, la señal se reconstruye por solape y suma. La **sustracción espectral** aplica a cada celda la ganancia G = √max(1 − α·P_n/|X|², β²), con P_n la potencia media del ruido en esa frecuencia.

## Desarrollo

El proyecto se hace en cuatro hitos, cada uno después del tema en que se apoya. Las tareas y preguntas concretas están en [`03_Hitos/Hitos.md`](../03_Hitos/Hitos.md).

| Hito | Qué haces | Temas | Entrega |
|---|---|---|---|
| H1 · Señal y espectro | Identificar y medir los cuatro ruidos | T1–T3 | Semana 6 |
| H2 · Filtrado | Muescas o peine para el zumbido, paso bajo para el soplido; IIR frente a FIR | T4 | Semana 9 |
| H3 · Estadística y detección | Modelo del ruido, detector de clics, filtro de Wiener | T5 | Semana 13 |
| H4 · Tiempo-frecuencia y memoria | Eliminar el silbido con la STFT, sustracción espectral, cadena completa | T6 | Semana 16 |

## Código de partida

`02_Codigo/python/` y `02_Codigo/matlab/` contienen lo mismo en los dos lenguajes: funciones para leer el audio, calcular la SNR, dibujar el espectro y la STFT, y un esqueleto por hito con las partes que tienes que completar marcadas con `TODO`. Elige un lenguaje y úsalo en todo el proyecto.

## Entregables

- Un informe por hito (plantilla en `00_Comun/Plantilla/Plantilla_Hito.md`, máximo 4 páginas) con su código.
- La memoria final (plantilla en `04_Entrega_Final/`), el código completo y el fichero `audio_restaurado.wav`.

## Evaluación

Rúbrica común en `00_Comun/Rubrica/Rubrica.md`. Lo específico de este proyecto:

- **C1 Comprensión:** identificas los cuatro ruidos y das sus parámetros medidos (frecuencias, nivel, instantes), no solo su nombre.
- **C2 Fundamento:** el ancho de las muescas, las bandas del paso bajo, el umbral del detector y la ventana de la STFT salen de medidas tuyas.
- **C3 Implementación:** las comparaciones de SNR se hacen sin retardos ni desfases que falseen la métrica.
- **C4 Validación:** tabla de SNR por etapa frente a un método base, y una medida específica para los clics (la SNR casi no los ve).
- **C5 Comunicación:** espectros y espectrogramas con ejes y escalas útiles; se oye la diferencia en el audio entregado.

Como referencia, una solución completa consigue mejorar la SNR en más de 10 dB.

## Referencias

- S. J. Godsill, P. J. W. Rayner, *Digital Audio Restoration*, Springer, 1998 (caps. 4–5: clics y ruido de banda ancha).
- S. F. Boll, «Suppression of acoustic noise in speech using spectral subtraction», *IEEE Trans. ASSP*, 27(2), 1979.
- A. V. Oppenheim, R. W. Schafer, *Discrete-Time Signal Processing*, 3.ª ed., Pearson, 2010 (cap. 7: diseño de filtros; cap. 10: STFT).
