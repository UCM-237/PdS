# Audio con ruido

Restauración de una grabación musical con cuatro ruidos superpuestos: zumbido de red con armónicos, soplido blanco, clics impulsivos y un silbido de frecuencia variable. Cada ruido pide una herramienta de un tema distinto, así que el proyecto recorre toda la asignatura.

| Ruido | Herramienta | Tema | Hito |
|---|---|---|---|
| Zumbido 50 Hz + armónicos | Muescas IIR o filtro peine | T4 | H2 |
| Soplido de banda ancha | Paso bajo FIR/IIR, Wiener, sustracción espectral | T4, T5, T6 | H2–H4 |
| Clics | Predicción lineal AR + umbral robusto | T5 | H3 |
| Silbido de frecuencia variable | STFT y seguimiento de la cresta | T6 | H4 |

**Dificultad:** media. **Datos:** sintéticos; el profesor puede generar una versión distinta por alumno con el generador de la solución.

## Contenido

- [`00_Enunciado/Enunciado.md`](00_Enunciado/Enunciado.md): contexto, objetivos, teoría mínima y evaluación.
- `01_Datos/`: audio ruidoso y referencia limpia.
- `02_Codigo/python/` y `02_Codigo/matlab/`: código de partida equivalente en los dos lenguajes.
- [`03_Hitos/Hitos.md`](03_Hitos/Hitos.md): tareas y preguntas de cada hito.
- `04_Entrega_Final/`: plantilla de la memoria.
- `05_Solucion/`: solución del profesor en Python y Matlab (no se distribuye).
