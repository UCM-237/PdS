# Procesamiento de Señales

Material docente de la asignatura **Procesamiento de Señales** del Grado en
Ingeniería Electrónica de Comunicaciones (GIEC) de la Universidad Complutense
de Madrid.

El repositorio reúne en un solo sitio todo lo que se usa en la asignatura:
transparencias, apuntes y hojas de ejercicios de los seis temas, ejemplos de
código en Python y en Matlab, herramientas interactivas para experimentar con
los conceptos en el navegador y los proyectos de evaluación continua. Todo el
material comparte notación, paleta y estilo, y se genera a partir de sus
fuentes (LaTeX y Python), de modo que se puede corregir y actualizar cada
curso.

**Herramientas interactivas:** <https://ucm-237.github.io/PdS/>

## Temas

| Tema | Contenido | Transparencias |
| --- | --- | --- |
| T1 | Señales y sistemas | Señales · Operaciones · Sistemas · Aplicaciones |
| T2 | Muestreo | Muestreo · Reconstrucción · Cuantificación · Muestreo discreto |
| T3 | Transformada discreta de Fourier | DFT · Propiedades · Análisis espectral · FFT |
| T4 | Filtros | Introducción · Filtros continuos · Filtros IIR · Filtros FIR · Filtros especiales · Mediana |
| T5 | Aplicaciones | STFT · Wavelets · Imágenes · Deconvolución · Sustracción espectral |
| T6 | Señales aleatorias | Variables aleatorias · Varias variables · Señales aleatorias · Análisis espectral · Estimadores robustos · Predicción y Wiener · Detección |

Cada tema tiene sus transparencias (una presentación por clase, más cápsulas cortas con las técnicas que piden los proyectos), unos apuntes
que las desarrollan, una hoja de ejercicios con su versión resuelta, ejemplos
de código y las herramientas interactivas correspondientes.

## Contenido del repositorio

```
teoría/            material de teoría
├── clase/         PDF listos para usar: transparencias, apuntes, ejercicios
│                  (con y sin solución) y el documento completo
├── T1/ … T6/      fuentes de cada tema
│   ├── transparencias/   presentaciones (beamer)
│   ├── apuntes/          apuntes del tema
│   ├── ejercicios/       hoja de ejercicios y hoja resuelta
│   ├── figuras/          figuras y el script que las genera
│   └── codigo/           ejemplos en python/ y matlab/ en paralelo
├── comun/         estilo, notación y datos comunes (ver comun/README.md)
├── src/           descripción de la asignatura y prácticas anteriores
├── archivo/       fuentes antiguas, solo como referencia
└── Makefile       compila, genera figuras, prueba el código y publica en clase/

herramientas/      herramientas interactivas (Bokeh) con sus fichas de uso
├── fuentes/T1…T6/ un script de Python por herramienta
├── fichas/        ficha de uso de cada herramienta (Markdown)
├── comun/         estilo y biblioteca común
├── server/        filtrado de audio en vivo (necesita bokeh serve)
└── generar.py     genera las páginas HTML y el índice

proyectos/         proyectos de evaluación continua
├── 00_Comun/      calendario, normas, rúbrica, plantillas y guía del profesor
├── 01_Registro_Carrera/
├── 02_Audio_Con_Ruido/
├── 03_Imagen_Codigos_de_Barras/
├── 04_ECG/
├── 05_Imagen_Con_Ruido/
└── TEC/           trabajo con Raspberry Pi Pico (generación, adquisición y FFT)
```

### Herramientas interactivas

Más de sesenta páginas web, organizadas por tema, que permiten mover
parámetros y ver el efecto al instante: exponenciales, convolución, series de
Fourier, aliasing, reconstrucción, cuantificación, DFT y ventanas, FFT,
polos y ceros, diseño de filtros IIR y FIR, STFT, wavelets, procesado de
imágenes, distribuciones, autocorrelación, periodograma y Welch, entre otras.
Cada página funciona sin instalar nada y lleva al pie su **ficha de uso**:
introducción, guía paso a paso, ejercicios con solución desplegable, recursos
y relación con otros conceptos. Las transparencias y los apuntes enlazan
directamente a la herramienta de cada concepto.

Están publicadas en <https://ucm-237.github.io/PdS/>; el flujo
`.github/workflows/herramientas.yml` las regenera y publica cada vez que
cambia `herramientas/` en `main`. Más detalles en
[`herramientas/README.md`](herramientas/README.md).

### Proyectos de evaluación continua

Cinco proyectos con datos reales o sintéticos, de los que cada estudiante
elige uno y lo desarrolla en cuatro hitos ligados a los bloques de teoría:

| Proyecto | Resumen |
| --- | --- |
| [Registro de carrera](proyectos/01_Registro_Carrera) | Sesiones de carrera (GPS, pulso, altitud): remuestreo, filtrado, detección de cambios de ritmo y clasificación |
| [Audio con ruido](proyectos/02_Audio_Con_Ruido) | Restauración de una grabación con zumbido de red, soplido, clics y un silbido de frecuencia variable |
| [Códigos de barras](proyectos/03_Imagen_Codigos_de_Barras) | Lectura de códigos EAN-13 en fotos giradas, ruidosas o desenfocadas |
| [ECG](proyectos/04_ECG) | Limpieza de registros de holter, detección de latidos, variabilidad del ritmo y clasificación |
| [Imagen con ruido](proyectos/05_Imagen_Con_Ruido) | Diagnóstico y restauración de imágenes con distintos tipos de ruido y desenfoque |

Cada proyecto incluye enunciado, datos, código de partida en Matlab y en
Python, la descripción de los hitos y la plantilla de la memoria final. El
calendario, la rúbrica y las normas comunes están en
[`proyectos/00_Comun`](proyectos/00_Comun).

## Para estudiantes

- **Material de clase.** Los PDF de cada tema están en
  [`teoría/clase/`](teoría/clase): transparencias, apuntes, ejercicios y
  ejercicios resueltos. *PdS - Apuntes y ejercicios.pdf* reúne los apuntes y
  los ejercicios resueltos de toda la asignatura en un solo documento.
- **Estudio.** Una forma de trabajar cada tema: repasar las transparencias,
  leer los apuntes, intentar la hoja de ejercicios y solo después consultar
  la versión resuelta.
- **Herramientas interactivas.** Abre <https://ucm-237.github.io/PdS/>, elige
  el tema y la herramienta, sigue la guía de su ficha y haz sus ejercicios.
  Son útiles para comprobar la intuición antes de hacer cuentas y para
  verificar resultados de la hoja de ejercicios.
- **Código.** En `teoría/Tn/codigo/` están los ejemplos de las transparencias
  en Python (`numpy`, `scipy`, `matplotlib`) y en Matlab. Ejecútalos y cambia
  sus parámetros.
- **Proyecto.** Lee las [normas](proyectos/00_Comun/Normas.md) y el
  [calendario](proyectos/00_Comun/Calendario.md), elige un proyecto y usa la
  plantilla de cada hito. Puedes trabajar en Matlab o en Python.

## Para profesores

- **Compilar el material de teoría.** Desde `teoría/`:

  ```bash
  make T1             # un tema (también T2 … T6, o make para todos)
  make completo       # documento único con apuntes y ejercicios resueltos
  make figuras        # regenera las figuras (Python)
  make prueba-codigo  # ejecuta los ejemplos en Python y en Octave
  make publicar       # compila todo y copia los PDF a clase/
  make ERRATAS=1 T1   # versión con las notas de erratas, en PDF aparte
  ```

  Hace falta TeX Live con XeLaTeX y `latexmk`, las fuentes Fira y Libertinus,
  Python 3 con `numpy`, `scipy` y `matplotlib`, y Octave con los paquetes
  `signal` y `control` para probar el código Matlab. Los datos del curso
  (asignatura, grado, autores) se cambian en `teoría/comun/datos.tex`, y los
  convenios de formato y notación están en
  [`teoría/comun/README.md`](teoría/comun/README.md).
- **Herramientas interactivas.** Desde `herramientas/`, `make` genera las
  páginas con Bokeh desde la CDN y `make sin-red` las genera con Bokeh
  incrustado, para usarlas en clase sin conexión. Para añadir una herramienta
  y su ficha, sigue los pasos de
  [`herramientas/README.md`](herramientas/README.md). En clase se pueden
  proyectar mientras se explica el concepto, y las fichas sirven como
  actividad guiada.
- **Proyectos.** La [guía del profesor](proyectos/00_Comun/Guia_Profesor.md)
  explica cómo corregir con la [rúbrica](proyectos/00_Comun/Rubrica/Rubrica.md)
  y cómo generar datos distintos para cada estudiante. Las soluciones
  (`05_Solucion/` de cada proyecto) no están en este repositorio público:
  se guardan en el repositorio privado `UCM-237/PdS-soluciones`.

## Licencia

GNU General Public License v3.0. Ver [`LICENSE`](LICENSE).
