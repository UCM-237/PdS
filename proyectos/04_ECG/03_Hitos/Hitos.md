# Hitos: ECG

Cada informe responde a las preguntas numeradas. Las figuras que se piden son el mínimo.

## Hito 1 · Señal y espectro (T1–T3, semana 6)

**Tareas**

1. Carga los dos registros y represéntalos completos y en tramos de pocos segundos. Señala las ondas P, QRS y T de un latido.
2. Calcula la PSD del registro A con el método de Welch y localiza la línea base, la red, el QRS y el ruido muscular.
3. Estima la frecuencia cardiaca media de A de dos formas: con las rayas del espectro en 0–6 Hz y con la autocorrelación. Compáralas con la de las anotaciones.
4. Mide la amplitud de la interferencia de red.

**Preguntas**

1. ¿Por qué el espectro de un ECG tiene rayas en múltiplos de la FC? ¿Qué longitud de ventana necesitas para verlas?
2. ¿Qué ocurre con esas rayas en el registro B, donde la FC cambia? ¿Qué te dice eso de la estacionariedad?
3. ¿Qué fracción de la potencia está por debajo de 0,5 Hz? ¿Es información o ruido?

**Figuras mínimas:** registros en el tiempo con las ondas señaladas; PSD con las bandas marcadas; autocorrelación.

## Hito 2 · Filtrado (T4, semana 9)

**Tareas**

1. Elimina la línea base con cuatro métodos: Butterworth paso alto de 0,5 Hz causal, el mismo con fase cero, FIR de fase lineal con la misma especificación y un estimador de medianas.
2. Elimina la red con una muesca de segundo orden y el ruido de alta frecuencia con un paso bajo de unos 40 Hz.
3. Mide con `ecg_A_limpio.csv` el error RMS de cada opción y el error en el segmento ST (80–120 ms después del pico R).
4. Elige una cadena y aplícala a los dos registros.

**Preguntas**

1. ¿Por qué el Butterworth causal deprime el segmento ST? Relaciónalo con su retardo de grupo.
2. ¿Cuántos coeficientes necesita el FIR? ¿Es viable en un holter que procesa en tiempo real? ¿Y el filtrado de fase cero?
3. El filtro de medianas no es lineal: ¿qué propiedades de los filtros LTI pierde y qué gana?
4. ¿Qué radio de polos has elegido para la muesca y qué ancho tiene?

**Figuras mínimas:** comparación de los métodos de línea base sobre dos latidos; respuestas en frecuencia; tabla de errores.

## Hito 3 · Detección y variabilidad (T5, semana 13)

**Tareas**

1. Implementa el detector de Pan-Tompkins y representa sus etapas.
2. Valida el detector en A con las anotaciones: VP, FP, FN, Se y VPP con una tolerancia de 150 ms, y el error de posición del pico R.
3. Aplícalo a B. Revisa a ojo los tramos difíciles (ráfagas musculares, saltos) y anota qué falla.
4. Calcula en A la FC media, SDNN y RMSSD, el histograma de los RR y la PSD del tacograma remuestreado a 4 Hz, con las potencias LF y HF.

**Preguntas**

1. ¿Qué papel tiene cada etapa de Pan-Tompkins? ¿Qué pasa si quitas el cuadrado o cambias la ventana de integración?
2. ¿Cómo se adapta el umbral? ¿Por qué hace falta la búsqueda hacia atrás?
3. ¿Por qué hay que remuestrear los RR antes de calcular su PSD? ¿Qué pasaría con la FFT de los RR tal cual?
4. ¿A qué frecuencia aparece el pico de HF y qué fenómeno fisiológico representa?

**Figuras mínimas:** etapas del detector; tacograma, histograma y PSD de los RR; tabla de Se y VPP.

## Hito 4 · Wavelets, clasificación y memoria final (T6, semana 16)

**Tareas**

1. Implementa la transformada wavelet diádica *à trous* con los filtros de spline cuadrática (h = [1 3 3 1]/8, g = [2 −2]) y representa las escalas 2¹–2⁵ de unos latidos. Calcula la respuesta en frecuencia equivalente de cada escala.
2. Construye un segundo detector de QRS con la escala que concentre más energía del QRS y compáralo con Pan-Tompkins en B sin preprocesar.
3. Clasifica cada latido de B como normal (N) o ventricular (V) con dos características: anchura del QRS y adelanto respecto a los RR vecinos.
4. Diseña una alarma de taquicardia (FC > 100 lpm sostenida) y aplícala a B.
5. Genera `ecg_B_latidos.csv` (`muestra,tipo`, una fila por latido detectado).

**Preguntas**

1. ¿Qué banda cubre cada escala? ¿Por qué la transformada no diezmada es mejor que la diezmada para localizar el QRS?
2. ¿Qué diferencias de forma tiene un latido ventricular y cómo las ves en las escalas wavelet?
3. ¿Qué índices de HRV dejan de tener sentido en B y por qué?
4. Si tuvieras que llevar el sistema a un dispositivo real, ¿qué cambiarías?

**Entrega:** memoria final (plantilla en `04_Entrega_Final/`), código completo y `ecg_B_latidos.csv`.

## Criterios específicos por hito

| Hito | Imprescindible para aprobar | Para Excelente |
|---|---|---|
| H1 | Bandas de cada componente y FC por dos métodos | Explica la estructura armónica y su pérdida con FC variable |
| H2 | Cadena aplicada con su justificación y error frente a la limpia | Mide el error en el ST y relaciona la deformación con el retardo de grupo |
| H3 | Detector funcionando con Se y VPP en A; FC, SDNN y RMSSD | PSD del tacograma con el pico respiratorio identificado y análisis de fallos en B |
| H4 | Clasificación N/V y alarma aplicadas a B; fichero de latidos | Detector wavelet comparado con Pan-Tompkins y Se, VPP ≥ 0,99 en B |
