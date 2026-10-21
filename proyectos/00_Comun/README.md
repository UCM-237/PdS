# Proyectos de evaluación: material común

Los proyectos son los «trabajos específicos de carácter individual» de la evaluación continua (**Nec, 25 % de la nota final** según la guía docente). Cada estudiante elige **uno** de los cinco proyectos al inicio del curso y lo desarrolla en **cuatro hitos**, cada uno ligado al bloque de teoría que se acaba de ver.

| Fichero | Contenido |
|---|---|
| [`Calendario.md`](Calendario.md) | Hitos, semanas y temas de teoría de cada uno |
| [`Rubrica/Rubrica.md`](Rubrica/Rubrica.md) | Criterios, niveles y pesos (común a los cinco proyectos) |
| [`Plantilla/Plantilla_Hito.md`](Plantilla/Plantilla_Hito.md) | Esqueleto del informe de cada hito |
| [`Plantilla/Plantilla_Entrega.md`](Plantilla/Plantilla_Entrega.md) | Esqueleto de la memoria final |
| [`Normas.md`](Normas.md) | Lenguaje (Matlab o Python), formato de entrega, reproducibilidad, uso de IA |
| [`Guia_Profesor.md`](Guia_Profesor.md) | Cómo corregir, qué hay en `05_Solucion/` y cómo regenerar datos |
| `Utilidades/` | Cuaderno de descarga de datos reales de PhysioNet (opcional) |

## Estructura de cada proyecto

```
NN_Proyecto/
├── README.md            resumen, temas implicados y nivel de dificultad
├── 00_Enunciado/        enunciado completo (contexto, objetivos, teoría mínima, tareas)
├── 01_Datos/            datos del alumno (generados por 05_Solucion/generar_datos.py)
├── 02_Codigo/
│   ├── matlab/          código de partida en Matlab
│   └── python/          el mismo código de partida en Python
├── 03_Hitos/Hitos.md    tareas, preguntas y entregables de cada hito
├── 04_Entrega_Final/    plantilla de la memoria final
└── 05_Solucion/         solución del profesor (no se distribuye a los alumnos)
```

El alumno recibe todo salvo `05_Solucion/`.
