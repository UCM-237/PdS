# ECG

Dos registros de holter de 3 minutos (360 Hz) con deriva de la línea base, red, ruido muscular y artefactos de movimiento; uno de ellos con una taquicardia transitoria y extrasístoles ventriculares. Se limpia la señal sin deformar el segmento ST, se detectan los latidos con Pan-Tompkins, se analiza la variabilidad del ritmo y se clasifican los latidos con ayuda de la transformada wavelet.

| Parte | Herramienta | Tema | Hito |
|---|---|---|---|
| Bandas del ECG y FC | PSD de Welch, autocorrelación | T2, T3, T5 | H1 |
| Línea base, red, EMG | IIR causal / fase cero, FIR, medianas, muesca | T4 | H2 |
| Latidos y HRV | Pan-Tompkins, Se/VPP, PSD del tacograma | T5 | H3 |
| Escalas del QRS, latidos V, alarma | Transformada wavelet *à trous* | T6 | H4 |

**Dificultad:** media-alta. **Datos:** sintéticos; el profesor puede generar una versión distinta por alumno con el generador de la solución. El registro A viene anotado; las anotaciones de B las guarda el profesor para evaluar.

## Contenido

- [`00_Enunciado/Enunciado.md`](00_Enunciado/Enunciado.md) y [`Info.md`](00_Enunciado/Info.md): contexto, teoría y evaluación.
- `01_Datos/`: registros y anotaciones de A.
- `02_Codigo/python/` y `02_Codigo/matlab/`: código de partida equivalente.
- [`03_Hitos/Hitos.md`](03_Hitos/Hitos.md): tareas y preguntas de cada hito.
- `04_Entrega_Final/`: plantilla de la memoria.
