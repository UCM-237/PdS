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

from bokeh.document import Document
from bokeh.embed import file_html
from bokeh.events import DocumentReady
from bokeh.layouts import column, row
from bokeh.models import CustomJS, Div, InlineStyleSheet, RadioButtonGroup, Select, Slider
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

_CSS = f"""
:host {{ font-family: {FUENTE}; }}
.pds-tema {{ color: {GRIS}; font-size: 13px; margin: 0; }}
.pds-titulo {{ color: {AZUL}; font-size: 22px; font-weight: 600; margin: 2px 0 6px; }}
.pds-texto {{ max-width: 760px; font-size: 14px; line-height: 1.45; margin: 0; }}
.pds-ref {{ color: {GRIS}; font-size: 12px; margin-top: 6px; }}
"""


def figura(titulo: str, eje_x: str, eje_y: str, ancho: int = 520, alto: int = 260,
           **kw):
    """Figura con el estilo común; ``ancho`` y ``alto`` son los de la zona de datos."""
    kw.setdefault("tools", "pan,wheel_zoom,box_zoom,reset,save")
    p = _figure(title=titulo, x_axis_label=eje_x, y_axis_label=eje_y,
                frame_width=ancho, frame_height=alto, **kw)
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


def leyenda(p, lugar: str = "right") -> None:
    """Saca la leyenda fuera de los ejes; un clic en una entrada la oculta."""
    if not p.legend:
        return
    lg = p.legend[0]
    lg.click_policy = "hide"
    lg.label_text_font = FUENTE
    lg.label_text_font_size = "12px"
    lg.border_line_color = None
    lg.background_fill_alpha = 0.0
    if lugar in ("right", "below", "above", "left"):
        if lugar in ("below", "above"):
            lg.orientation = "horizontal"
        p.add_layout(lg, lugar)
    else:
        lg.location = lugar


def deslizador(titulo: str, inicio: float, fin: float, valor: float, paso: float,
               **kw) -> Slider:
    return Slider(title=titulo, start=inicio, end=fin, value=valor, step=paso,
                  width=kw.pop("width", 240), bar_color=AZUL, **kw)


def selector(titulo: str, opciones, valor=None, **kw) -> Select:
    """Lista desplegable; ``opciones`` es una lista de textos."""
    return Select(title=titulo, options=list(opciones), value=valor or opciones[0],
                  width=kw.pop("width", 240), **kw)


def botones(opciones, activo: int = 0, **kw) -> RadioButtonGroup:
    """Grupo de botones excluyentes (por ejemplo, escala lineal o en dB)."""
    return RadioButtonGroup(labels=list(opciones), active=activo, width=kw.pop("width", 240), **kw)


def tallos(p, x: str, y: str, fuente, color: str = AZUL, base: float = 0.0, **kw):
    """Gráfica de tallos (stem) para señales discretas."""
    p.segment(x0=x, y0=base, x1=x, y1=y, source=fuente, line_color=color, line_width=1.5)
    return p.scatter(x, y, source=fuente, size=6, color=color, **kw)


def editable(p, fuente, x: str = "n", y: str = "x", callback=None) -> None:
    """Permite cambiar los valores de una secuencia haciendo clic o arrastrando
    sobre la figura ``p``: el punto más cercano en ``x`` toma el valor de ``y``.
    ``callback`` se ejecuta después de cada cambio."""
    editar = CustomJS(args=dict(f=fuente, cx=x, cy=y, siguiente=callback), code="""
        const xs = f.data[cx], ys = f.data[cy].slice();
        let i = 0, mejor = Infinity;
        for (let j = 0; j < xs.length; j++) { const d = Math.abs(xs[j] - cb_obj.x); if (d < mejor) { mejor = d; i = j; } }
        if (mejor > 0.6) return;
        ys[i] = Math.round(cb_obj.y * 20) / 20;
        const nuevo = Object.assign({}, f.data); nuevo[cy] = ys; f.data = nuevo;
        if (siguiente) siguiente.execute(cb_obj);
    """)
    for evento in ("tap", "pan", "panstart"):
        p.js_on_event(evento, editar)
    p.toolbar.active_drag = None



def js(codigo: str, **args) -> CustomJS:
    """CustomJS con la biblioteca común ``JS`` (FFT, ventanas…) delante."""
    # El try/catch hace visible en la consola cualquier error del cálculo.
    return CustomJS(args=args, code=JS + "try {\n" + codigo + "\n} catch (e) { console.error('PDS: ' + e); }")


def conectar(callback, *controles) -> None:
    """Ejecuta ``callback`` cuando cambia cualquiera de los controles."""
    for c in controles:
        if isinstance(c, Slider):
            c.js_on_change("value", callback)
        elif isinstance(c, Select):
            c.js_on_change("value", callback)
        elif isinstance(c, RadioButtonGroup):
            c.js_on_change("active", callback)


# Funciones de JavaScript que comparten las herramientas.
JS = r"""
const PI = Math.PI;
function rango(a, b, n) { const r = []; for (let i = 0; i < n; i++) r.push(a + (b - a) * i / (n - 1)); return r; }
function enteros(a, b) { const r = []; for (let i = a; i <= b; i++) r.push(i); return r; }
function sinc(x) { return Math.abs(x) < 1e-12 ? 1 : Math.sin(PI * x) / (PI * x); }
function db(x, suelo = -120) { return Math.max(20 * Math.log10(Math.max(x, 1e-300)), suelo); }
function mod(a, n) { return ((a % n) + n) % n; }
// FFT de base 2 (re, im de longitud potencia de 2); devuelve [re, im].
function fft(re, im) {
    const n = re.length; re = re.slice(); im = im ? im.slice() : new Array(n).fill(0);
    for (let i = 1, j = 0; i < n; i++) {
        let bit = n >> 1; for (; j & bit; bit >>= 1) j ^= bit; j ^= bit;
        if (i < j) { [re[i], re[j]] = [re[j], re[i]]; [im[i], im[j]] = [im[j], im[i]]; }
    }
    for (let len = 2; len <= n; len <<= 1) {
        const a = -2 * PI / len, wr = Math.cos(a), wi = Math.sin(a);
        for (let i = 0; i < n; i += len) {
            let cr = 1, ci = 0;
            for (let k = 0; k < len / 2; k++) {
                const ur = re[i + k], ui = im[i + k];
                const vr = re[i + k + len / 2] * cr - im[i + k + len / 2] * ci;
                const vi = re[i + k + len / 2] * ci + im[i + k + len / 2] * cr;
                re[i + k] = ur + vr; im[i + k] = ui + vi;
                re[i + k + len / 2] = ur - vr; im[i + k + len / 2] = ui - vi;
                const t = cr * wr - ci * wi; ci = cr * wi + ci * wr; cr = t;
            }
        }
    }
    return [re, im];
}
// DFT directa de N puntos (cualquier N); devuelve [re, im].
function dft(x, N) {
    const re = [], im = [];
    for (let k = 0; k < N; k++) {
        let a = 0, b = 0;
        for (let n = 0; n < x.length; n++) { const w = -2 * PI * k * n / N; a += x[n] * Math.cos(w); b += x[n] * Math.sin(w); }
        re.push(a); im.push(b);
    }
    return [re, im];
}
// DTFT de x[0..L-1] en M frecuencias de [0, 2π) mediante FFT con ceros.
function dtft(x, M = 2048) {
    const re = new Array(M).fill(0); for (let n = 0; n < x.length; n++) re[n % M] += x[n];
    return fft(re);
}
function ventana(tipo, L) {
    const w = [];
    for (let n = 0; n < L; n++) {
        const c = L > 1 ? 2 * PI * n / (L - 1) : 0;
        if (tipo === "Hann") w.push(0.5 - 0.5 * Math.cos(c));
        else if (tipo === "Hamming") w.push(0.54 - 0.46 * Math.cos(c));
        else if (tipo === "Blackman") w.push(0.42 - 0.5 * Math.cos(c) + 0.08 * Math.cos(2 * c));
        else w.push(1);
    }
    return w;
}
"""


def pagina(fuente: str, titulo: str, tema: int, descripcion: str, controles,
           graficas, referencia: str = "", columnas: int = 1, inicio=None) -> pathlib.Path:
    """Escribe html/<nombre de la fuente>.html y su entrada del índice.

    ``graficas`` es una lista de figuras (una lista dentro de ella es una
    fila) que se colocan en ``columnas`` columnas; ``controles`` va a la izquierda.
    ``inicio`` es un CustomJS que se ejecuta al abrir la página (suele ser el
    mismo que el de los controles, para no repetir el cálculo en Python).
    """
    nombre = pathlib.Path(fuente).stem.replace("_", "-")
    cab = (f'<p class="pds-tema">Tema {tema} · {html.escape(TEMAS[tema])}</p>'
           f'<p class="pds-titulo">{html.escape(titulo)}</p>'
           f'<p class="pds-texto">{descripcion}</p>')
    if referencia:
        cab += f'<p class="pds-ref">{html.escape(referencia)}</p>'
    cabecera = Div(text=cab, stylesheets=[InlineStyleSheet(css=_CSS)])
    graficas = [row(*g) if isinstance(g, (list, tuple)) else g for g in graficas]
    filas = [row(*graficas[i:i + columnas]) for i in range(0, len(graficas), columnas)]
    cuerpo = row(column(*controles, width=260), column(*filas))
    doc = Document()
    doc.add_root(column(cabecera, cuerpo))
    if inicio is not None:
        doc.js_on_event(DocumentReady, inicio)
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
