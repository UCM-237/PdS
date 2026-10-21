# Hitos: Audio con ruido

Cada informe responde a las preguntas numeradas. Las figuras que se piden son el mínimo; añade las que necesites para justificar tus decisiones.

## Hito 1 · Señal y espectro (T1–T3, semana 6)

**Tareas**

1. Carga `audio_ruidoso.wav`, escúchalo y represéntalo en el tiempo: la señal completa y un detalle de unas decenas de milisegundos donde se vea algún clic.
2. Calcula el espectro del primer segundo (solo ruido) y el de la señal completa con la DFT. Usa una ventana y una escala en dB adecuadas.
3. Localiza las rayas del zumbido y mide su frecuencia y su amplitud.
4. Estima el nivel del soplido (su desviación típica σ) a partir de la PSD del primer segundo.
5. Calcula un espectrograma y localiza el silbido: instantes de inicio y fin y frecuencias.

**Preguntas**

1. ¿Qué resolución en frecuencia tiene la DFT del primer segundo? ¿Cuántas muestras necesitas como mínimo para separar dos rayas a 50 Hz? Compruébalo con distintas longitudes.
2. ¿Qué ventana has usado y por qué? ¿Qué pasa con las rayas débiles del zumbido si usas una ventana rectangular?
3. Estima la SNR sin usar la referencia limpia (con la potencia del primer segundo) y compárala con la real. ¿Por qué no coinciden?
4. ¿Hasta qué frecuencia llega la música? Esa frecuencia la necesitarás en el Hito 2.

**Figuras mínimas:** señal en el tiempo; espectro con las rayas marcadas; espectrograma.

## Hito 2 · Filtrado (T4, semana 9)

**Tareas**

1. Diseña un filtro para el zumbido: una cascada de muescas o un filtro peine. Elige el ancho de muesca a partir de la distancia entre las rayas del zumbido y las notas más cercanas.
2. Diseña un paso bajo para reducir el soplido por encima de la frecuencia máxima de la música (H1, pregunta 4), con dos métodos: un FIR (ventana de Kaiser u otro) y un IIR (Butterworth, Chebyshev o elíptico), con la misma especificación de banda de paso, banda de rechazo, rizado y atenuación.
3. Representa |H(f)|, el diagrama de polos y ceros de las muescas y el retardo de grupo de los dos paso bajo.
4. Aplica los filtros y mide la SNR tras cada etapa: con filtrado causal y con filtrado de fase cero.

**Preguntas**

1. ¿Qué radio de polo r has elegido y qué ancho de muesca da? ¿Qué pasaría con un bajo de 98 Hz si r fuese 0,99?
2. Compara las muescas con el filtro peine: ¿qué elimina cada uno que el otro no?
3. ¿Qué orden necesita cada tipo de filtro para tu especificación? ¿Por qué el elíptico necesita mucho menos orden que un Butterworth?
4. ¿Por qué el elíptico causal empeora la SNR aunque quite ruido? ¿Cómo lo arreglas y qué precio tiene en una aplicación en tiempo real?
5. ¿Por qué la mejora total de este hito es pequeña? ¿Qué ruidos quedan y por qué un filtro invariante no puede con ellos?

**Figuras mínimas:** respuesta de los filtros del zumbido; respuesta en módulo y retardo de grupo de los paso bajo; tabla de SNR.

## Hito 3 · Estadística y detección (T5, semana 13)

**Tareas**

1. Con el primer segundo, ya sin zumbido: histograma, media, varianza, curtosis, autocorrelación y PSD (periodograma y Welch). ¿Es un ruido blanco gaussiano?
2. Detecta los clics: calcula el residuo de un predictor lineal AR (Yule-Walker) y compáralo con un umbral robusto. Ten en cuenta que la música no es estacionaria.
3. Elige el umbral: representa sensibilidad y precisión frente al umbral. Para medirlas puedes marcar a mano los clics de un tramo o pedir al profesor la lista real al entregar el hito.
4. Repara los clics (interpolación) y decide en qué orden deben ir la reparación de clics y los filtros del Hito 2.
5. Diseña un filtro de Wiener con las PSD de Welch de la señal y del ruido, aplícalo y mide la SNR.

**Preguntas**

1. ¿Por qué el periodograma del ruido es tan irregular y el de Welch no? ¿Qué se gana y qué se pierde al promediar?
2. ¿Qué distribución tiene el residuo de predicción en la música y en los clics? ¿Por qué la curtosis es una buena pista?
3. ¿Qué orden AR y qué tamaño de bloque has usado y por qué?
4. Tras reparar los clics, ¿cambia la SNR? ¿Por qué? Propón una medida que sí refleje la mejora en los clics.
5. ¿Por qué el filtro de Wiener global mejora poco esta señal? ¿Qué hipótesis de su deducción no se cumple?

**Figuras mínimas:** histograma, autocorrelación y PSD del ruido; residuo con el umbral y los clics detectados; curva sensibilidad-precisión.

## Hito 4 · Tiempo-frecuencia y memoria final (T6, semana 16)

**Tareas**

1. Calcula la STFT de la señal tras el Hito 3. Elige la ventana y justifica el compromiso entre resolución en tiempo y en frecuencia con al menos tres longitudes.
2. Sigue la cresta del silbido trama a trama, ajusta su trayectoria y elimínala poniendo a cero (o atenuando) las celdas a su alrededor.
3. Aplica sustracción espectral con la potencia de ruido estimada en el primer segundo. Ajusta α y el suelo β.
4. Monta la cadena completa y mide la SNR y la SNR segmental tras cada etapa, frente a dos métodos base: solo paso bajo, y muescas más paso bajo.
5. Guarda `audio_restaurado.wav` y escúchalo.

**Preguntas**

1. ¿Por qué no se puede quitar el silbido con un filtro de banda eliminada fijo? Calcula cuánta música se perdería.
2. ¿Qué es el «ruido musical» de la sustracción espectral y cómo influyen α y β?
3. ¿Qué etapa aporta más mejora? ¿Coincide con lo que se oye?
4. ¿Qué limita el resultado final? ¿Qué harías con más tiempo?

**Entrega:** memoria final (plantilla en `04_Entrega_Final/`) que integre los cuatro hitos, código completo y audio restaurado.

## Criterios específicos por hito

| Hito | Imprescindible para aprobar | Para Excelente |
|---|---|---|
| H1 | Las seis rayas del zumbido medidas; σ del soplido; silbido localizado | Explica la diferencia entre la SNR estimada y la real y la resolución necesaria |
| H2 | Un filtro del zumbido y dos paso bajo con su especificación; tabla de SNR | Elige r con un criterio numérico y explica el efecto de la fase en la métrica |
| H3 | Modelo del ruido con PSD de Welch; detector de clics funcionando | Curva de umbral, orden de la cadena justificado y métrica propia para los clics |
| H4 | Silbido eliminado y tabla de SNR por etapa frente a una base | Compromiso de ventana con figuras, ajuste de α y β, análisis de límites |
