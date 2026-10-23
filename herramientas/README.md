# Herramientas interactivas

Páginas web interactivas que acompañan a las transparencias de teoría. Cada
herramienta es una página HTML autónoma: se abre en el navegador, desde el
enlace de la transparencia o desde el índice, sin instalar Python. Los
cálculos que dependen de los controles se hacen en el propio navegador.

Índice publicado: `https://ucm-237.github.io/PdS/` (ver «Publicación»).

## Estructura

| Carpeta | Contenido |
| --- | --- |
| `fuentes/Tn/` | Un script de Python por herramienta, ordenados por tema |
| `comun/pds_bokeh.py` | Estilo común (paleta y notación de `teoría/comun`), controles y plantilla de página |
| `generar.py` | Ejecuta todas las fuentes y escribe el índice |
| `fichas/` | Ficha de uso de cada herramienta (`Tn-nombre.md`): introducción, guía de uso, ejercicios, recursos y relación con otros conceptos; se añade al pie de la página |
| `html/` | Páginas generadas (`Tn-nombre.html`) e índice (`index.html`) |
| `server/` | Filtrado de audio (T4), la única app que necesita Python en marcha (`bokeh serve`) porque reproduce sonido filtrado |

## Uso

```bash
pip install -r requirements.txt
make            # genera html/ con Bokeh desde la CDN (para publicar)
make sin-red    # igual, con Bokeh incrustado en cada página (para clase sin red)
```

Para comprobar una página sin red, genera con `make sin-red` y ábrela con el navegador.
La app de `server/` se lanza con `bokeh serve --show server/T4_05_FIR_Audio.py`.
No guardan nada salvo que se pida con `PDS_REGISTRO=1`, que escribe un
registro de interacciones en `logs/`; si se usa con alumnos, hay que
avisarles.

## Añadir una herramienta

1. Crea `fuentes/Tn/nombre.py` a partir de `fuentes/T1/exponencial_continua.py`.
2. Construye las figuras con `pb.figura()` y los controles con
   `pb.deslizador()`; actualiza los datos con `CustomJS`, no con callbacks
   de Python, para que la página funcione sin servidor.
3. Termina con `pb.pagina(__file__, titulo, tema=n, descripcion=…,
   controles=[…], graficas=[…], referencia=…)`. La referencia indica la
   transparencia y la sección de los apuntes que la usan.
4. Escribe su ficha en `fichas/Tn-nombre.md` (Markdown) con los apartados de
   `fichas/T2-aliasing.md`. Las soluciones de los ejercicios van dentro de
   `<details><summary>Solución</summary>…</details>`.
5. `make` y comprueba la página en el navegador.

La biblioteca de JavaScript de `pds_bokeh.JS` está disponible en todos los
`pb.js(...)`: FFT y DFT, ventanas, números complejos (`cmul`, `cdiv`,
`cexp`…), polinomios y sus raíces, `zpk`, `filtrar` (ecuación en
diferencias), `continua` (respuesta de H(s) al escalón o al impulso) y
Butterworth analógico y digital. Un argumento de `pb.js` no puede llamarse
como una de esas funciones. `pb.editable()` deja modificar una secuencia
con el ratón y `pb.plano_pz()`, mover, añadir y borrar polos y ceros.

Notación: ω (rad/s) y f (Hz) en tiempo continuo; Ω (rad/muestra) y
F (ciclos/muestra) en tiempo discreto.

## Publicación

El flujo `.github/workflows/herramientas.yml` publica `herramientas/html`
en GitHub Pages cada vez que cambia en `main`. Hay que activarlo una vez en
*Settings → Pages → Build and deployment → Source: GitHub Actions*.
