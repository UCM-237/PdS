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
| `html/` | Páginas generadas (`Tn-nombre.html`) e índice (`index.html`) |
| `server/` | Apps que necesitan Python en marcha (`bokeh serve`), como el filtrado de audio |
| `standalone/`, `notebook/` | Herramientas antiguas, pendientes de pasar a `fuentes/` |

## Uso

```bash
pip install -r requirements.txt
make            # genera html/ con Bokeh desde la CDN (para publicar)
make sin-red    # igual, con Bokeh incrustado en cada página (para clase sin red)
```

Las apps de `server/` se lanzan con `bokeh serve --show server/<app>.py`.
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
4. `make` y comprueba la página en el navegador.

Notación: ω (rad/s) y f (Hz) en tiempo continuo; Ω (rad/muestra) y
F (ciclos/muestra) en tiempo discreto.

## Publicación

El flujo `.github/workflows/herramientas.yml` publica `herramientas/html`
en GitHub Pages cada vez que cambia en `main`. Hay que activarlo una vez en
*Settings → Pages → Build and deployment → Source: GitHub Actions*.
