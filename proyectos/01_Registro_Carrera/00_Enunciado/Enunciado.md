# Registro de carrera

## Contexto

Un reloj deportivo con GPS y una banda de pecho registran la velocidad, la frecuencia cardiaca (FC) y la altitud de un corredor. El reloj no guarda las muestras a intervalos fijos, el GPS da saltos de vez en cuando y la banda tarda en engancharse al empezar. Con esas señales queremos saber qué entrenamiento se hizo: cuándo cambió el ritmo, si hubo series y cuántas, cuánto se subió de verdad y cómo respondió el corazón.

Tienes cinco sesiones reales del mismo corredor, sin etiquetas, y trece sesiones sintéticas generadas con el mismo tipo de ruido. Diez sintéticas traen los instantes reales de los cambios de ritmo y el tipo de sesión, para que ajustes y valides tus detectores; las otras tres son de prueba.

## Objetivos de aprendizaje

1. Describir el muestreo de una señal real (irregular, con huecos) y remuestrearla de forma justificada; leer su espectro (T1–T3).
2. Analizar un filtro IIR de primer orden como el de una aplicación real, y compararlo con un Butterworth de fase cero y con la mediana (T4).
3. Modelar el ruido de la velocidad, detectar atípicos con estadística robusta y formular la detección de cambios de ritmo como un problema estadístico (T5).
4. Usar la STFT y la autocorrelación para localizar un bloque de series y medir su periodo (T6).

## Teoría mínima

**Muestreo irregular.** Un filtro digital y la DFT suponen un periodo de muestreo constante. Si las muestras llegan cada 2–6 s, primero hay que interpolar a una rejilla uniforme. Interpolar a 1 Hz no añade información: el contenido útil sigue limitado por el periodo típico original (unos 4 s, es decir, hasta unos 0,125 Hz).

**Media móvil exponencial (EMA).** y[k] = y[k−1] + α·(x[k] − y[k−1]), con α = 1 − e^(−Δt/τ). Con Δt constante es un IIR de primer orden, H(z) = α / (1 − (1 − α)·z⁻¹), con retardo de grupo en continua de aproximadamente τ.

**Filtrado de fase cero.** Filtrar hacia delante y hacia atrás (`filtfilt`) eleva al cuadrado el módulo de la respuesta y anula la fase: los eventos no se desplazan en el tiempo, pero el filtro deja de ser causal.

**Estimación robusta.** La desviación absoluta mediana MAD = mediana(|x − mediana(x)|) no se ve afectada por unos pocos atípicos; para ruido gaussiano, σ ≈ 1,4826·MAD. El filtro de Hampel marca la muestra que se aleja más de k·1,4826·MAD de la mediana de su ventana. Con las diferencias de primer orden, σ ≈ 1,4826·mediana(|Δx|)/√2 apenas se ve afectada por los escalones de la señal.

**Cambios de media.** Si la velocidad es constante a trozos más ruido, un corte en k reduce la suma de cuadrados respecto a la media. La segmentación binaria busca el mejor corte, lo acepta si la reducción supera una penalización (por ejemplo 2σ²·log n) y repite en cada mitad.

**STFT.** Una sesión de series es casi periódica: rápido–lento–rápido... con periodo T de 1,5 a 8 minutos. Su espectrograma muestra energía en la banda alrededor de 1/T solo mientras duran las series. La autocorrelación en ese tramo tiene máximos en múltiplos de T.

## Datos

En `01_Datos/`:

| Fichero | Contenido |
|---|---|
| `actividad_AAAA-MM-DD.csv` | Cinco sesiones reales. Columnas: `time` (s), `distance` (m, acumulada), `heartrate` (ppm), `velocity` (m/s, ya suavizada por Strava), `altitude` (m); `distance_km` y `speed_kmh` son derivadas |
| `sinteticas/desarrollo_01.csv` … `desarrollo_10.csv` | Sesiones sintéticas con el mismo formato |
| `sinteticas/desarrollo_verdad.csv` | Tipo de cada sesión de desarrollo, σ del ruido de la velocidad e instantes (s) de los cambios de ritmo |
| `sinteticas/prueba_1.csv` … `prueba_3.csv` | Sesiones de prueba, sin etiquetas |

Los tipos de sesión son: Series, Progresivo (tramos cada vez más rápidos), Tempo (ritmo alto sostenido), Rodaje y Tirada larga.

## Desarrollo

| Hito | Qué haces | Temas | Entrega |
|---|---|---|---|
| H1 · Señal y espectro | Muestreo, anomalías, remuestreo, espectro | T1–T3 | Semana 6 |
| H2 · Filtrado | EMA, Butterworth de fase cero, mediana, desnivel | T4 | Semana 9 |
| H3 · Ruido, atípicos y cambios de ritmo | Modelo de ruido, Hampel, segmentación, indicadores | T5 | Semana 13 |
| H4 · Series, clasificación y memoria | STFT, periodo, estados, clasificación | T6 | Semana 16 |

Tareas y preguntas en [`03_Hitos/Hitos.md`](../03_Hitos/Hitos.md).

## Código de partida

`02_Codigo/python/` y `02_Codigo/matlab/` contienen lo mismo: lectura de actividades y de la verdad de las sintéticas, la métrica para evaluar detecciones y un esqueleto por hito con `TODO`. El código de Matlab no necesita toolboxes.

## Entregables

- Un informe por hito y su código.
- La memoria final, el código completo y `prueba.csv` con una fila por sesión de prueba: `sesion,tipo,cambios_s` (instantes separados por espacios).

## Evaluación

Rúbrica común en `00_Comun/Rubrica/Rubrica.md`. Lo específico de este proyecto:

- **C1 Comprensión:** explicas el muestreo irregular, qué hace el EMA en frecuencia y por qué el ruido de la velocidad no es blanco.
- **C2 Fundamento:** la frecuencia de corte, la ventana de Hampel, la penalización y la banda de la STFT salen de medidas (espectro, σ, duración mínima de un tramo).
- **C3 Implementación:** la misma cadena para las sesiones reales y las sintéticas, sin ajustes por sesión.
- **C4 Validación:** precisión y sensibilidad de los cambios de ritmo en las sesiones de desarrollo; clase y cambios de las de prueba.
- **C5 Comunicación:** figuras con el tiempo en minutos y las unidades del deporte (km/h, min/km, ppm).

Como referencia, la solución del profesor clasifica bien las trece sesiones sintéticas y las cinco reales, y detecta los cambios de ritmo con F1 = 0,85 (tolerancia ±20 s).

## Referencias

- R. Killick, P. Fearnhead, I. A. Eckley, «Optimal detection of changepoints with a linear computational cost», *JASA*, 107(500), 2012.
- R. K. Pearson, «Outliers in process modeling and identification», *IEEE Trans. Control Systems Technology*, 10(1), 2002 (filtro de Hampel).
- Strava API v3, *Streams*: https://developers.strava.com/docs/reference/#api-Streams
