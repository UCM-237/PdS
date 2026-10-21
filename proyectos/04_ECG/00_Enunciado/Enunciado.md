# ECG

## Contexto

Un holter ha registrado dos tramos de 3 minutos de electrocardiograma (ECG) de una derivación. Los registros tienen los problemas habituales de un ECG ambulatorio: deriva de la línea base por la respiración y el movimiento, interferencia de la red eléctrica, ruido muscular y, en uno de ellos, saltos por movimiento del electrodo. Además, uno de los pacientes tiene un episodio de taquicardia y algunas extrasístoles ventriculares.

Tu trabajo es limpiar la señal sin deformar la información clínica, detectar los latidos, medir la frecuencia cardiaca y su variabilidad, y proponer un sistema de alarma sencillo. Ajustarás el método con el registro A, que viene anotado, y el profesor lo evaluará con las anotaciones del registro B, que tú no tienes.

## Objetivos de aprendizaje

1. Relacionar las ondas del ECG con su contenido espectral y localizar cada artefacto en el espectro (T2, T3).
2. Elegir entre filtros FIR, IIR y no lineales según su efecto sobre la forma de onda, no solo sobre el módulo de H(f) (T4).
3. Implementar un detector de eventos con umbral adaptativo y validarlo con sensibilidad y valor predictivo positivo (T5).
4. Tratar el ritmo cardiaco como una señal aleatoria: estadística de los intervalos RR y PSD del tacograma (T5).
5. Analizar la señal en varias escalas con la transformada wavelet diádica (T6).

## Teoría mínima

Un ECG típico presenta las ondas P, QRS y T (ver [`Info.md`](Info.md) para la fisiología y las referencias). En procesado:

| Componente | Duración típica | Banda aproximada |
|---|---|---|
| Onda P | 80–100 ms | 0,5–10 Hz |
| Complejo QRS | 60–100 ms (normal), > 120 ms (ventricular) | 5–30 Hz, máximo en 10–15 Hz |
| Onda T y segmento ST | 200–300 ms | 0,5–8 Hz |
| Deriva de la línea base | | < 0,5 Hz |
| Red eléctrica | | 50 Hz y armónicos |
| Ruido muscular (EMG) | ráfagas de segundos | 20–150 Hz |

**Línea base.** Un paso alto de 0,5 Hz la quita, pero el segmento ST tiene información clínica de muy baja frecuencia: un filtro con fase no lineal lo deforma y puede simular una isquemia. Por eso se usan filtros de fase cero, FIR de fase lineal o estimadores no lineales de la línea base (medianas).

**Detector de Pan-Tompkins.** Paso banda 5–15 Hz, derivada, cuadrado e integración en una ventana de unos 150 ms, seguidos de un umbral que se adapta al nivel de los picos de señal (SPK) y de ruido (NPK): umbral = NPK + 0,25·(SPK − NPK).

**Validación de un detector.** Con una tolerancia (típicamente 150 ms), cada latido anotado se empareja con como mucho una detección: Se = VP/(VP + FN) y VPP = VP/(VP + FP).

**Variabilidad del ritmo (HRV).** Los intervalos RR forman una señal aleatoria muestreada de forma irregular. Se describen con la media, la desviación típica (SDNN) y la raíz cuadrática media de sus diferencias (RMSSD), y con su PSD tras remuestrearlos a una rejilla uniforme (4 Hz). La banda HF (0,15–0,4 Hz) recoge la arritmia sinusal respiratoria, y la LF (0,04–0,15 Hz) la regulación de la presión arterial.

**Transformada wavelet diádica.** Con un par de filtros paso bajo h y paso alto g, dilatados en cada nivel (algoritmo *à trous*), se obtiene la señal en las escalas 2¹, 2², … sin diezmar. Cada escala es un paso banda una octava más grave que la anterior, y el QRS se concentra en las escalas 2³–2⁴.

## Datos

En `01_Datos/`, todos a fs = 360 Hz y en mV:

| Fichero | Contenido |
|---|---|
| `ecg_A.csv` | Registro A (desarrollo): ritmo sinusal, ruido moderado |
| `ecg_A_anotaciones.csv` | Instante, muestra (desde 0) y tipo (N normal, V ventricular) de cada latido de A |
| `ecg_A_limpio.csv` | Registro A sin ruido. **Solo** para medir la distorsión de los filtros (H2) |
| `ecg_B.csv` | Registro B (prueba): más ruido, taquicardia y extrasístoles. Sin anotaciones |

## Desarrollo

| Hito | Qué haces | Temas | Entrega |
|---|---|---|---|
| H1 · Señal y espectro | Identificar ondas y artefactos; FC por el espectro y la autocorrelación | T1–T3 | Semana 6 |
| H2 · Filtrado | Línea base, red y alta frecuencia; IIR causal, fase cero, FIR y medianas | T4 | Semana 9 |
| H3 · Detección y HRV | Pan-Tompkins, Se y VPP en A, estadística y PSD de los RR | T5 | Semana 13 |
| H4 · Wavelets, clasificación y memoria | Análisis multiescala, latidos ventriculares, alarma, resultados en B | T6 | Semana 16 |

Tareas y preguntas de cada hito en [`03_Hitos/Hitos.md`](../03_Hitos/Hitos.md).

## Código de partida

`02_Codigo/python/` y `02_Codigo/matlab/` contienen lo mismo: lectura de los registros y las anotaciones, la función de validación (Se, VPP) y un esqueleto por hito con las partes a completar marcadas con `TODO`.

## Entregables

- Un informe por hito (plantilla en `00_Comun/Plantilla/Plantilla_Hito.md`) con su código.
- La memoria final, el código completo y el fichero `ecg_B_latidos.csv` con tus detecciones del registro B: una fila por latido con `muestra,tipo`. Con él el profesor calcula tu Se y VPP en B.

## Evaluación

Rúbrica común en `00_Comun/Rubrica/Rubrica.md`. Lo específico de este proyecto:

- **C1 Comprensión:** relacionas cada artefacto con su banda y das la FC con dos métodos independientes.
- **C2 Fundamento:** eliges el filtro de la línea base midiendo su efecto en el segmento ST, no solo por su |H(f)|.
- **C3 Implementación:** el detector no usa información del registro B para ajustar parámetros.
- **C4 Validación:** Se y VPP en A con su tolerancia; en B el profesor mide los mismos índices con tu `ecg_B_latidos.csv`.
- **C5 Comunicación:** figuras con ondas reconocibles, escalas en mV y ms, y conclusiones clínicas prudentes.

Como referencia, una buena solución consigue Se y VPP por encima de 0,99 en los dos registros.

## Referencias

- J. Pan, W. J. Tompkins, «A real-time QRS detection algorithm», *IEEE Trans. Biomed. Eng.*, 32(3), 1985.
- J. P. Martínez et al., «A wavelet-based ECG delineator: evaluation on standard databases», *IEEE Trans. Biomed. Eng.*, 51(4), 2004.
- Task Force of the ESC and NASPE, «Heart rate variability: standards of measurement», *Circulation*, 93(5), 1996.
- Datos reales para ampliar el proyecto: MIT-BIH Arrhythmia Database en PhysioNet (cuaderno en `00_Comun/Utilidades/`).
