# Rúbrica común

La misma rúbrica sirve para los cinco proyectos y para cada hito; cada enunciado concreta qué significa cada criterio en su caso (sección «Criterios específicos» de `03_Hitos/Hitos.md`). La nota de un hito es la media ponderada de sus criterios, con los niveles convertidos a 10 / 8 / 6 / 3 / 0.

## Criterios y pesos

| Criterio | Qué se valora | Peso |
|---|---|---|
| C1 · Comprensión de la señal | Describe correctamente el origen, el muestreo, las unidades y el contenido espectral; identifica los problemas que hay que resolver | 20 % |
| C2 · Fundamento teórico | Las decisiones (frecuencias de corte, orden, ventana, umbrales) se justifican con la teoría y con medidas, no por prueba y error | 20 % |
| C3 · Implementación | El código es correcto, reproducible y legible; usa las funciones adecuadas y no tiene errores de fase, escala o índices | 25 % |
| C4 · Validación | Hay métricas cuantitativas, comparación con una referencia o un método base, y análisis de los casos en que falla | 25 % |
| C5 · Comunicación | Figuras con ejes, unidades y leyenda; texto claro y conciso; conclusiones apoyadas en los resultados | 10 % |

## Niveles

| Nivel | C1 · Comprensión | C2 · Fundamento | C3 · Implementación | C4 · Validación | C5 · Comunicación |
|---|---|---|---|---|---|
| **Excelente (10)** | Caracteriza la señal con medidas propias y descubre problemas no mencionados en el enunciado | Cada parámetro se deriva de una especificación medida; discute alternativas y sus compromisos | Correcto, modular y reproducible con un solo comando; tiene en cuenta fase, bordes y escalas | Métricas adecuadas, método base, varios casos y análisis de errores | Figuras de calidad de publicación; el lector entiende el resultado solo con las figuras |
| **Notable (8)** | Caracteriza bien la señal y los problemas del enunciado | Justifica los parámetros principales con la teoría | Correcto y reproducible; algún detalle mejorable (bordes, retardo) | Métricas adecuadas y comparación con una referencia | Figuras y texto claros, con algún detalle menor |
| **Aprobado (6)** | Describe la señal de forma correcta pero superficial | Justificación genérica («se usa un Butterworth porque es habitual») | Funciona pero con errores menores o poco organizado | Alguna métrica, sin comparación o con un solo caso | Se entiende, pero faltan unidades, leyendas o hay texto de relleno |
| **Insuficiente (3)** | Errores de concepto en la descripción (unidades, frecuencias, muestreo) | Parámetros sin justificar o justificados con argumentos erróneos | No reproducible o con errores que invalidan el resultado | Solo valoración visual | Difícil de seguir; figuras sin ejes o sin explicar |
| **No presentado (0)** | | | | | |

## Reglas generales

- Si el código no se ejecuta con los datos entregados, C3 y C4 se califican como máximo con Aprobado.
- Si el alumno no sabe explicar en la defensa una parte de su trabajo, esa parte no puntúa.
- Los resultados numéricos clave del enunciado (por ejemplo, la SNR conseguida o el número de latidos) se comparan con la solución; una diferencia grande no penaliza si está justificada.
