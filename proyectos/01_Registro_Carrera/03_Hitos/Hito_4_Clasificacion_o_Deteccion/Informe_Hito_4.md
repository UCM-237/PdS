# Hito 4 — Detección y clasificación

**Código:** `02_Codigo/carrera/deteccion.py`, `02_Codigo/carrera/sintetico.py` y `02_Codigo/hito4_deteccion.py` · **Resultados:** `resultados.md`, `deteccion_sesiones.csv`

He planteado la detección en tres niveles, de lo más local a lo más global:

1. **Estado en cada muestra**: parado / andando / corriendo.
2. **Cambios de ritmo** dentro de la sesión.
3. **Tipo de sesión**: rodaje, tempo, tirada larga o series.

## 1. Estados: parado / andando / corriendo

Regla con umbrales sobre la velocidad filtrada:

| Estado | Condición | Justificación |
|---|---|---|
| Parado | v < 2 km/h | el GPS en reposo marca 0–2 km/h de deriva |
| Andando | 2 ≤ v < 7 km/h | andar rápido son ~6 km/h |
| Corriendo | v ≥ 7 km/h | el trote más lento ronda 7–8 km/h |

Si se aplican los umbrales sin más, la etiqueta "parpadea" cuando la velocidad está cerca de un umbral. Para evitarlo, los tramos de menos de 20 s se absorben en el tramo vecino más largo (un filtro de duración mínima, parecido a una apertura morfológica).

**Resultado**: detecta la vuelta a la calma andando en 07/01 (min 48,5–49,7), 11/01 (min 88,9–91,1) y 15/01 (min 56,7–58,5), y en ninguna sesión hay paradas de más de 20 s. Las bajadas puntuales de velocidad (07/01 min 28 y 35, 15/01 min 25) duran menos de 20 s y no llegan a 7 km/h en la señal filtrada: son frenazos breves (un cruce, un giro), no paradas.

## 2. Cambios de ritmo

### 2.1 Método de partida: derivada + umbral MAD (`entrenamiento/main.py`)

Se suaviza con una EMA (τ = 10 s), se deriva y se marca un cambio donde |dv/dt| > k·MAD. Al revisar el código encontré varios problemas:

- **Cada muestra por encima del umbral cuenta como un cambio distinto.** Una sola transición genera 10–20 "cambios" (columna *Muestras > umbral* de la tabla). Lo he corregido agrupando las detecciones separadas menos de 30 s.
- En el dibujo de las líneas verticales se usa `df["time"]` (el vector entero) en lugar de cada instante `t`, y `get_segment_mean` avanza el índice con la comparación al revés, así que la media por tramo que se dibuja no corresponde a los tramos.
- La EMA es causal y retrasa el evento ~τ (Hito 2).
- La derivada amplifica el ruido de alta frecuencia: el umbral tiene que ser alto y entonces solo se detectan los cambios bruscos y grandes.

### 2.2 Método propuesto: segmentación binaria

Modelo: la velocidad es **constante a trozos más ruido**. La segmentación binaria busca el instante k que más reduce la suma de errores cuadráticos al partir la señal en dos medias distintas. Si la reducción supera una penalización, se acepta el corte y se repite el proceso en cada mitad.

- Penalización tipo BIC: β = 2σ²·log(n). σ se estima de forma robusta con la MAD de las diferencias de primer orden **en las muestras originales** (no en las interpoladas, que tienen menos varianza de la real).
- La segmentación se hace a 0,25 Hz (la frecuencia del muestreo original) para que las muestras sean aproximadamente independientes. A 1 Hz la interpolación crea correlación y salían muchos más cortes.
- Duración mínima de cada tramo: 45 s.
- Después se fusionan los tramos contiguos cuya media difiere menos de 1 km/h: aunque la diferencia sea estadísticamente significativa, no tiene interés deportivo.
- Se trabaja con la velocidad **sin filtrar**: el método ya promedia dentro de cada tramo, y así los bordes no se suavizan.

Las sumas de cuadrados se calculan con sumas acumuladas, así que el coste de cada tramo es O(1) y todo el algoritmo es O(n log n).

### 2.3 Validación con señales sintéticas

Las sesiones reales no traen etiquetas, así que para medir precisión y sensibilidad he generado **30 sesiones sintéticas de series** (`carrera/sintetico.py`) con:

- 4–8 repeticiones de 1–4 min a 13–16 km/h, recuperaciones de 1–2 min a 7,5–9,5 km/h, calentamiento, vuelta a la calma y un tramo final andando;
- ruido AR(1) con σ ∈ {0,5; 1; 1,5} km/h y autocorrelación 0,4 (como en los datos reales, Hito 2);
- muestreo irregular de 2–6 s, un salto de GPS y un hueco de ~30 s.

Un cambio cuenta como acierto si se detecta a menos de 20 s del real.

![Validación sintética](figuras/h4_validacion_sintetica.png)

| Método | TP | FP | FN | Precisión | Sensibilidad | F1 | Error medio (s) |
|---|---|---|---|---|---|---|---|
| Derivada + MAD (corregido) | 223 | 0 | 175 | 1,00 | 0,56 | 0,72 | 5,3 |
| **Segmentación binaria** | 395 | 63 | 3 | 0,86 | **0,99** | **0,92** | 4,5 |

F1 según el nivel de ruido:

| Método | σ = 0,5 | σ = 1,0 | σ = 1,5 |
|---|---|---|---|
| Derivada + MAD | 0,99 | 0,60 | 0,21 |
| Segmentación binaria | 0,98 | 0,92 | 0,88 |

- Con poco ruido los dos métodos funcionan igual de bien. Con el ruido real (σ ≈ 1 km/h) el de la derivada **se pierde casi la mitad de los cambios**, y con σ = 1,5 casi todos.
- La segmentación binaria apenas pierde cambios (3 de 398). De sus 63 falsos positivos, 49 son cortes de más que parten una repetición o una recuperación en dos: el ruido está autocorrelacionado y a veces produce una diferencia de medias aparente de más de 1 km/h (sobre todo con σ = 1,5). Los otros 14 están junto al hueco de 30 s (8) o en la vuelta a la calma (6). Estos cortes de más no afectan al conteo de repeticiones (apartado 3), porque los tramos rápidos seguidos se agrupan.
- El error de localización es de 4–5 s, del orden del periodo de muestreo (4 s), así que no se puede pedir mucho más.

### 2.4 Resultado en las sesiones reales

![Sesiones reales](figuras/h4_sesiones_reales.png)

| Actividad | Andando/parado (min) | Cambios de ritmo (min) | Derivada+MAD | Muestras > umbral (sin agrupar, como en main.py) |
|---|---|---|---|---|
| 07/01 | 48,5–49,7 | 1,1 · 2,5 · 36,9 · 42,3 · 48,5 | 1 | 11 |
| 09/01 | – | 0,7 · 1,5 · 2,6 | 1 | 10 |
| 11/01 | 88,9–91,1 | 28,3 · 29,3 · 80,9 · 81,8 · 88,9 | 1 | 19 |
| 14/01 | – | 1,0 · 2,5 · 25,9 | 1 | 19 |
| 15/01 | 56,7–58,5 | 0,7 · 43,6 · 45,1 · 56,7 · 57,4 | 4 | 21 |

Cómo interpreto los cortes:

- **Primeros 3 min** (todas): arranque. En 09/01 y 14/01 el corredor sale fuerte (12–13 km/h durante 1 min), afloja y luego se pone a ritmo. En 07/01 hay un tramo lento (7,7 km/h) entre los min 1 y 2,5, que puede ser un semáforo o un tramo con gente.
- **07/01, min 36,9–42,3**: bloque de 5,4 min a 11,2 km/h, +1,2 km/h sobre el resto. Es un **progresivo o cambio de ritmo** dentro del rodaje, y explica en parte por qué esta sesión tiene tanto tiempo en Z4.
- **11/01, min 28 y 81**: dos aceleraciones cortas (~1 min, +1 km/h).
- **15/01, min 43,6–45,1**: bajada de ritmo justo después de coronar la subida (recuperación). El tramo algo más rápido de la subida (min 38–43, Hito 3) **no** sale como tramo propio: la diferencia es de ~1 km/h, del orden del ruido, y la segmentación no la separa. Es el límite de sensibilidad del método con la penalización elegida.
- **Final**: paso a andar (coincide con el detector de estados).

## 3. Clasificación de la sesión

Regla sencilla con prioridad, a partir de las características del Hito 3. Los umbrales de velocidad son **relativos al propio corredor** (v_ref = mediana de su velocidad en carrera en todas las sesiones = 10,16 km/h), para que la regla sirva también para corredores de otro nivel:

```
si   nº repeticiones ≥ 3                       → Series
sino si distancia ≥ 12 km o t corriendo ≥ 75 min → Tirada larga
sino si v ≥ 1,05·v_ref y %tiempo Z4–Z5 ≥ 40 %  → Tempo
sino                                            → Rodaje
```

**Repeticiones**: cada tramo de la segmentación se etiqueta como *rápido* si su media supera en ≥ 1 km/h la mediana de la velocidad en carrera. Los tramos rápidos seguidos se agrupan en un bloque, y se cuentan los bloques que tienen un tramo lento a cada lado. La primera versión contaba tramos sueltos ("rápido entre dos lentos") y fallaba cuando la segmentación partía una repetición en dos (contaba 2 de 4 en un caso). Agrupando, el conteo es exacto en todos los sintéticos probados.

**Validación en sesiones reales** (etiqueta manual puesta mirando las gráficas del Hito 1, antes de diseñar la regla):

| Actividad | Clase detectada | Etiqueta manual | Motivo |
|---|---|---|---|
| 07/01 | Rodaje | Rodaje | v = 10,0 km/h (< 105 % ref.), 1 bloque rápido |
| 09/01 | Tempo | Tempo | v = 11,2 km/h (110 % ref.), 76 % en Z4 |
| 11/01 | Tirada larga | Tirada larga | 15,1 km |
| 14/01 | Tempo | Tempo | v = 11,3 km/h (111 % ref.), 63 % en Z4 |
| 15/01 | Rodaje | Rodaje | v = 9,6 km/h, 9 % en Z4 |

5/5 aciertos, pero con solo 5 sesiones (y con umbrales que he elegido viendo estas mismas sesiones) eso no demuestra mucho. Por eso lo he probado también con **30 sesiones sintéticas** (10 de cada tipo, con distinta duración, velocidad y nº de repeticiones):

| Real \ Predicho | Rodaje | Series | Tirada larga |
|---|---|---|---|
| Rodaje | 10 | 0 | 0 |
| Series | 0 | 10 | 0 |
| Tirada larga | 0 | 0 | 10 |

(En los sintéticos no hay sesiones *Tempo* porque el modelo de FC del generador es muy simple y no reproduce bien las zonas.)

## 4. Limitaciones

- **07/01** se queda cerca del límite Rodaje/Tempo: el 58 % del tiempo está en Z4, pero la velocidad media no llega al 105 %. Con otra FCmáx (la supongo en 190 ppm) podría cambiar de clase.
- Los umbrales (2/7 km/h, 105 %, 40 %, 12 km, 1 km/h) se han elegido a mano. Con más sesiones etiquetadas se podrían ajustar con un árbol de decisión, que tendría la misma forma de reglas.
- La segmentación supone que el ritmo es constante a trozos. Una aceleración progresiva (un *fartlek* suave o un progresivo continuo) se partiría en varios escalones.
- No hay cadencia, que ayudaría a separar andar de correr y a detectar los cambios de ritmo antes (la cadencia responde más rápido que el GPS).
