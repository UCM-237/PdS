# Hitos: Registro de carrera

Cada informe responde a las preguntas numeradas. Las figuras que se piden son el mínimo.

## Hito 1 · Señal y espectro (T1–T3, semana 6)

**Tareas**

1. Carga las cinco actividades reales y representa velocidad (km/h), FC y altitud frente al tiempo en minutos.
2. Estudia el muestreo: histograma de los intervalos entre muestras, valores típicos y máximos, huecos de más de 15 s.
3. Busca anomalías: velocidades imposibles, saltos de la distancia acumulada, tramos en los que la FC se queda congelada.
4. Remuestrea a una rejilla uniforme y justifica la frecuencia elegida.
5. Calcula la densidad espectral de potencia (Welch) de la velocidad y de la FC de cada sesión.

**Preguntas**

1. ¿Por qué no se puede aplicar directamente la FFT a los datos tal como vienen? ¿Hasta qué frecuencia hay información de verdad?
2. ¿Qué anomalías has encontrado y qué sensor las causa? ¿Cuáles afectan a la distancia total?
3. ¿En qué banda está la información de los cambios de ritmo y en qué banda el ruido del GPS? Relaciónalo con la duración mínima de un tramo que te interese detectar.

**Figuras mínimas:** señales de una sesión; histograma de intervalos; anomalías marcadas; PSD de velocidad y FC.

## Hito 2 · Filtrado (T4, semana 9)

**Tareas**

1. La aplicación de `entrenamiento/main.py` suaviza con una EMA de τ = 10 s. Escribe su H(z) para Δt = 1 s, representa su respuesta en frecuencia y calcula su frecuencia de corte y su retardo.
2. Diseña un Butterworth paso bajo con la frecuencia de corte que justificaste en el H1 y aplícalo con fase cero. Compara con la EMA (τ = 10 y 30 s) y con una mediana móvil.
3. Mide en las sesiones sintéticas de desarrollo el retardo de cada filtro en los cambios de ritmo conocidos.
4. Calcula el desnivel positivo de cada sesión real sumando las subidas de la altitud sin filtrar, filtrada y filtrada con histéresis.

**Preguntas**

1. ¿Qué retardo introduce la EMA y por qué importa para localizar un cambio de ritmo?
2. ¿Qué ventaja tiene la mediana frente a los filtros lineales con los saltos del GPS?
3. ¿Por qué el desnivel sin filtrar sale mayor? ¿Qué valor das por bueno y por qué?

**Figuras mínimas:** respuesta en frecuencia de la EMA y del Butterworth; comparación de filtros en una sesión; tabla de retardos; desnivel según el tratamiento.

## Hito 3 · Ruido, atípicos y cambios de ritmo (T5, semana 13)

**Tareas**

1. Modela el ruido de la velocidad en tramos de ritmo estable: histograma, σ y autocorrelación. Compara con la σ de `desarrollo_verdad.csv`.
2. Programa un detector de atípicos (Hampel u otro basado en MAD) y una regla para la FC congelada. Limpia las señales y corrige la distancia.
3. Detecta los cambios de ritmo con dos métodos: umbral sobre la derivada de la velocidad filtrada, y segmentación binaria con penalización. Mide precisión, sensibilidad y F1 en las diez sesiones de desarrollo (tolerancia ±20 s).
4. Calcula indicadores de cada sesión real: distancia corregida, tiempo corriendo, ritmo, FC media, tiempo en zonas de FC, desnivel, desacoplamiento aeróbico (deriva de la FC a ritmo constante).

**Preguntas**

1. ¿Es blanco el ruido de la velocidad? ¿Qué implica la autocorrelación para el umbral de un detector?
2. ¿Por qué la MAD y no la desviación típica para fijar el umbral de atípicos?
3. ¿Qué controla la penalización de la segmentación? ¿Qué pasa si la tomas demasiado pequeña o demasiado grande?
4. ¿Qué método de cambios de ritmo eliges y por qué? ¿Qué tipo de error comete?

**Figuras mínimas:** estadística del ruido; atípicos marcados; cambios detectados frente a reales en una sesión de desarrollo; tabla de indicadores.

## Hito 4 · Series, clasificación y memoria final (T6, semana 16)

**Tareas**

1. Calcula la STFT de la velocidad de una sesión de series. Elige la ventana y la banda de las series y localiza el bloque de series en el tiempo.
2. Mide el periodo de las repeticiones con la autocorrelación en ese bloque y compáralo con la verdad.
3. Clasifica cada muestra como parado, andando o corriendo, sin parpadeos en los umbrales.
4. Diseña reglas para el tipo de sesión (Series, Progresivo, Tempo, Rodaje, Tirada larga) con las medidas de los hitos anteriores. Valídalas en las sintéticas de desarrollo y aplícalas a las reales y a las de prueba.
5. Monta la cadena completa y genera `prueba.csv`.

**Preguntas**

1. ¿Qué longitud de ventana necesitas en la STFT para ver series de 1,5 a 8 minutos? ¿Qué pierdes en resolución temporal?
2. ¿Por qué la autocorrelación puede dar el doble del periodo? ¿Cómo lo evitas?
3. ¿Qué sesión real es más difícil de clasificar y por qué?

**Entrega:** memoria final, código completo y `prueba.csv`.

## Criterios específicos por hito

| Hito | Imprescindible para aprobar | Para Excelente |
|---|---|---|
| H1 | Intervalos de muestreo, anomalías y remuestreo | PSD con la banda útil razonada a partir de la duración de un tramo |
| H2 | EMA y Butterworth comparados con figuras | H(z) de la EMA, retardos medidos en las sintéticas y desnivel con histéresis |
| H3 | Ruido caracterizado y un detector de cambios con su F1 | Comparación de dos detectores, penalización justificada con σ e indicadores fisiológicos |
| H4 | Clasificación de las sesiones y `prueba.csv` | Bloque de series con la STFT y periodo con la autocorrelación |
