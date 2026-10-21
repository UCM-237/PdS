# Proyectos de evaluación

Cinco proyectos para los «trabajos específicos de carácter individual» de la evaluación continua (Nec, 25 % según la guía docente). Cada estudiante elige uno y lo desarrolla en cuatro hitos ligados a los temas de teoría; todos tienen código de partida equivalente en Matlab y en Python.

| Proyecto | Señales | Técnicas principales | Dificultad |
|---|---|---|---|
| [01 · Registro de carrera](01_Registro_Carrera/README.md) | Velocidad GPS, FC y altitud de Strava (reales) y sesiones sintéticas | Remuestreo, EMA y Butterworth de fase cero, Hampel, segmentación, STFT | Media-baja |
| [02 · Audio con ruido](02_Audio_Con_Ruido/README.md) | Grabación de 10 s con zumbido, soplido, clics y silbido | Muescas y peine, FIR/IIR, predicción AR, Wiener, STFT, sustracción espectral | Media |
| [03 · Códigos de barras](03_Imagen_Codigos_de_Barras/README.md) | Fotos de códigos EAN-13 giradas, con ruido y desenfoque | Muestreo y aliasing, filtros separables, Otsu, DFT 2D, deconvolución | Media |
| [04 · ECG](04_ECG/README.md) | Dos registros de holter de 3 min | Línea base, Pan-Tompkins, HRV, wavelets, clasificación de latidos | Media-alta |
| [05 · Imagen con ruido](05_Imagen_Con_Ruido/README.md) | Seis fotos con ruido gaussiano, impulsivo, periódico, de Poisson y desenfoque | Filtros separables, mediana, Wiener local, muescas 2D, deconvolución | Media |

El material común (calendario, rúbrica, plantillas, normas y guía del profesor) está en [`00_Comun/`](00_Comun/README.md). La solución de cada proyecto (`05_Solucion/`) no está en este repositorio.
