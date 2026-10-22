"""Estilo común de las herramientas interactivas (Bokeh).

Cada herramienta es un script en ``fuentes/Tn/`` que construye sus gráficas
y controles con este módulo y termina llamando a ``pagina()``, que escribe
una página HTML autónoma en ``html/``. Los cálculos que dependen de los
controles se hacen en el navegador (``CustomJS``), así que la página se abre
sin Python, también desde el enlace de una transparencia.

    import pds_bokeh as pb
    p = pb.figura("Señal", "t (s)", "x(t)")
    f = pb.deslizador("f (Hz)", 0.1, 4, 1, 0.1)
    ...
    pb.pagina(__file__, "Exponencial compleja", tema=1,
              descripcion="...", controles=[f], graficas=[p])

``generar.py`` ejecuta todas las fuentes y escribe el índice por temas.
La paleta y la notación son las de ``teoría/comun`` (transparencias,
apuntes y figuras).
"""

from __future__ import annotations

import html
import json
import os
import pathlib

from bokeh.embed import file_html
from bokeh.layouts import column, row
from bokeh.models import Div, Slider, InlineStyleSheet
from bokeh.plotting import figure as _figure
from bokeh.resources import CDN, INLINE
from jinja2 import Template

# Paleta de teoría/comun/pds_estilo.py
AZUL = "#2B3A8C"
ROJO = "#C0392B"
VERDE = "#1E7B4F"
NARANJA = "#D9822B"
GRIS = "#5A5A66"
GRIS_CLARO = "#B8BAC6"
REJILLA = "#E3E4EC"
CICLO = [AZUL, ROJO, VERDE, NARANJA, GRIS]

FUENTE = "Fira Sans, Helvetica, Arial, sans-serif"

TEMAS = {
    1: "Señales y sistemas",
    2: "Muestreo y reconstrucción",
    3: "Transformada discreta de Fourier",
    4: "Filtros",
    5: "Aplicaciones",
    6: "Señales aleatorias",
}

# PDS_INLINE=1 incrusta Bokeh en cada página (unos 1,5 MB) para usarla sin red.
RECURSOS = INLINE if os.environ.get("PDS_INLINE") else CDN

RAIZ = pathlib.Path(__file__).resolve().parents[1]
SALIDA = RAIZ / "html"

_PLANTILLA = Template("""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fira+Sans:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<style>
  body { margin: 0; padding: 16px 24px; font-family: {{ fuente }}; color: #222;
         background: #fff; }
</style>
{{ bokeh_css | indent(2) }}
{{ bokeh_js | indent(2) }}
</head>
<body>
{{ plot_div | indent(2) }}
{{ plot_script | indent(2) }}
</body>
</html>
""")

_CSS = InlineStyleSheet(css=f"""
:host {{ font-family: {FUENTE}; }}
.pds-tema {{ color: {GRIS}; font-size: 13px; margin: 0; }}
.pds-titulo {{ color: {AZUL}; font-size: 22px; font-weight: 600; margin: 2px 0 6px; }}
.pds-texto {{ max-width: 760px; font-size: 14px; line-height: 1.45; margin: 0; }}
.pds-ref {{ color: {GRIS}; font-size: 12px; margin-top: 6px; }}
""")


def figura(titulo: str, eje_x: str, eje_y: str, ancho: int = 520, alto: int = 280,
           **kw):
    """Figura con el estilo común: sin borde, rejilla suave, Fira Sans."""
    kw.setdefault("tools", "pan,wheel_zoom,box_zoom,reset,save")
    p = _figure(title=titulo, x_axis_label=eje_x, y_axis_label=eje_y,
                width=ancho, height=alto, **kw)
    p.toolbar.logo = None
    p.outline_line_color = None
    p.title.text_font = FUENTE
    p.title.text_font_size = "14px"
    p.title.text_font_style = "normal"
    p.title.text_color = AZUL
    for eje in (p.xaxis, p.yaxis):
        eje.axis_label_text_font = FUENTE
        eje.axis_label_text_font_size = "13px"
        eje.axis_label_text_font_style = "normal"
        eje.major_label_text_font = FUENTE
        eje.major_label_text_font_size = "12px"
        eje.axis_line_color = GRIS
        eje.major_tick_line_color = GRIS
        eje.minor_tick_line_color = None
    p.grid.grid_line_color = REJILLA
    return p


def deslizador(titulo: str, inicio: float, fin: float, valor: float, paso: float,
               **kw) -> Slider:
    return Slider(title=titulo, start=inicio, end=fin, value=valor, step=paso,
                  width=kw.pop("width", 240), bar_color=AZUL, **kw)


def pagina(fuente: str, titulo: str, tema: int, descripcion: str, controles,
           graficas, referencia: str = "", columnas: int = 1) -> pathlib.Path:
    """Escribe html/<nombre de la fuente>.html y su entrada del índice.

    ``graficas`` es una lista de figuras (o de filas ya montadas) que se
    colocan en ``columnas`` columnas; ``controles`` va a la izquierda.
    """
    nombre = pathlib.Path(fuente).stem.replace("_", "-")
    cab = (f'<p class="pds-tema">Tema {tema} · {html.escape(TEMAS[tema])}</p>'
           f'<p class="pds-titulo">{html.escape(titulo)}</p>'
           f'<p class="pds-texto">{descripcion}</p>')
    if referencia:
        cab += f'<p class="pds-ref">{html.escape(referencia)}</p>'
    cabecera = Div(text=cab, stylesheets=[_CSS])
    filas = [row(*graficas[i:i + columnas]) for i in range(0, len(graficas), columnas)]
    cuerpo = row(column(*controles, width=260), column(*filas))
    doc = column(cabecera, cuerpo)
    SALIDA.mkdir(exist_ok=True)
    destino = SALIDA / f"T{tema}-{nombre}.html"
    destino.write_text(file_html(doc, RECURSOS, title=f"PdS · {titulo}", template=_PLANTILLA,
                                 template_variables={"fuente": FUENTE}),
                       encoding="utf-8")
    indice = SALIDA / "indice"
    indice.mkdir(exist_ok=True)
    (indice / f"T{tema}-{nombre}.json").write_text(json.dumps(
        {"tema": tema, "titulo": titulo, "archivo": destino.name,
         "descripcion": descripcion}, ensure_ascii=False, indent=1), encoding="utf-8")
    return destino
