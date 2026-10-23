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
import re

from bokeh.document import Document
from bokeh.embed import file_html
from bokeh.events import DocumentReady
from bokeh.layouts import column, row
from bokeh.models import CheckboxGroup, CustomJS, Div, InlineStyleSheet, RadioButtonGroup, Select, Slider
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
  .pds-ficha { max-width: 820px; font-size: 14.5px; line-height: 1.55; color: #222; margin-top: 28px;
                border-top: 2px solid #E3E4EC; padding-top: 8px; }
  .pds-ficha h1 { color: #2B3A8C; font-size: 20px; font-weight: 600; margin: 12px 0 4px; }
  .pds-ficha h2 { color: #2B3A8C; font-size: 17px; font-weight: 600; margin: 22px 0 6px; }
  .pds-ficha h3 { color: #222; font-size: 15px; font-weight: 600; margin: 16px 0 4px; }
  .pds-ficha p, .pds-ficha li { margin: 6px 0; }
  .pds-ficha blockquote { margin: 8px 0; padding: 4px 14px; border-left: 3px solid #2B3A8C; background: #F4F5FA; }
  .pds-ficha details { margin: 4px 0 14px; padding: 6px 12px; background: #F4F5FA; border-radius: 6px; }
  .pds-ficha summary { cursor: pointer; color: #1E7B4F; font-weight: 600; }
  .pds-ficha a { color: #2B3A8C; }
  .pds-ficha code { font-size: 13px; background: #F4F5FA; padding: 1px 4px; border-radius: 3px; }
  .pds-ficha table { border-collapse: collapse; margin: 8px 0; font-size: 14px; }
  .pds-ficha th, .pds-ficha td { text-align: left; padding: 4px 12px 4px 0; border-bottom: 1px solid #E3E4EC; vertical-align: top; }
</style>
{{ bokeh_css | indent(2) }}
{{ bokeh_js | indent(2) }}
</head>
<body>
{{ plot_div | indent(2) }}
{{ plot_script | indent(2) }}
{% if ficha %}
<section class="pds-ficha" id="ficha">
<h1>Ficha de uso</h1>
{{ ficha }}
</section>
{% endif %}
</body>
</html>
""")

_CSS = f"""
:host {{ font-family: {FUENTE}; }}
.pds-tema {{ color: {GRIS}; font-size: 13px; margin: 0; }}
.pds-titulo {{ color: {AZUL}; font-size: 22px; font-weight: 600; margin: 2px 0 6px; }}
.pds-texto {{ max-width: 760px; font-size: 14px; line-height: 1.45; margin: 0; }}
.pds-ref {{ color: {GRIS}; font-size: 12px; margin-top: 6px; }}
.pds-ref a {{ color: {AZUL}; }}
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


def casillas(opciones, activas=(), **kw) -> CheckboxGroup:
    """Casillas de verificación independientes."""
    return CheckboxGroup(labels=list(opciones), active=list(activas), width=kw.pop("width", 240), **kw)


def tallos(p, x: str, y: str, fuente, color: str = AZUL, base: float = 0.0, **kw):
    """Gráfica de tallos (stem) para señales discretas."""
    p.segment(x0=x, y0=base, x1=x, y1=y, source=fuente, line_color=color, line_width=1.5)
    kw.setdefault("size", 6)
    return p.scatter(x, y, source=fuente, color=color, **kw)


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



def plano_pz(p, fuente, modo, callback=None, real_tol: float = 0.04) -> None:
    """Polos y ceros editables en la figura ``p``.

    ``fuente`` tiene las columnas x, y, t ("polo" o "cero") y par (los dos de
    un par conjugado comparten número). ``modo`` es un selector con las
    opciones "Mover", "Añadir polo", "Añadir cero" y "Borrar": un clic
    añade o borra (los complejos van siempre con su conjugado) y arrastrar
    mueve un punto y su pareja. ``callback`` se ejecuta tras cada cambio.
    """
    from bokeh.models import CDSView, ColumnDataSource, GroupFilter
    estado = ColumnDataSource(dict(i=[-1]))
    for t, marca in (("polo", "x"), ("cero", "circle")):
        vista = CDSView(filter=GroupFilter(column_name="t", group=t))
        p.scatter("x", "y", source=fuente, view=vista, marker=marca, size=13, line_width=2.5,
                  line_color=ROJO if t == "polo" else AZUL, fill_color=None,
                  legend_label="polos" if t == "polo" else "ceros")
    comun = """
        const d = f.data, n = d.x.length, ancho = (p.x_range.end - p.x_range.start), tol = TOL * ancho;
        function cercano() {
            let i = -1, mejor = 0.06 * ancho;
            for (let j = 0; j < n; j++) { const r = Math.hypot(d.x[j] - cb_obj.x, d.y[j] - cb_obj.y); if (r < mejor) { mejor = r; i = j; } }
            return i;
        }
        function publicar(x, y, t, par) { f.data = {x: x, y: y, t: t, par: par}; if (siguiente) siguiente.execute(cb_obj); }
    """
    pulsar = CustomJS(args=dict(f=fuente, p=p, modo=modo, siguiente=callback, TOL=real_tol), code=comun + """
        const x = d.x.slice(), y = d.y.slice(), t = d.t.slice(), par = d.par.slice();
        if (modo.value === "Borrar") {
            const i = cercano(); if (i < 0) return;
            const q = par[i], keep = [...Array(n).keys()].filter(j => par[j] !== q);
            publicar(keep.map(j => x[j]), keep.map(j => y[j]), keep.map(j => t[j]), keep.map(j => par[j]));
        } else if (modo.value.startsWith("Añadir")) {
            const tipo = modo.value.endsWith("polo") ? "polo" : "cero", q = Math.max(0, ...par) + 1;
            const yy = Math.abs(cb_obj.y) < tol ? 0 : Math.abs(cb_obj.y);
            x.push(cb_obj.x); y.push(yy); t.push(tipo); par.push(q);
            if (yy !== 0) { x.push(cb_obj.x); y.push(-yy); t.push(tipo); par.push(q); }
            publicar(x, y, t, par);
        }
    """)
    empezar = CustomJS(args=dict(f=fuente, p=p, e=estado, modo=modo, siguiente=None, TOL=real_tol),
                       code=comun + 'e.data = {i: [modo.value === "Mover" ? cercano() : -1]};')
    arrastrar = CustomJS(args=dict(f=fuente, p=p, e=estado, siguiente=callback, TOL=real_tol), code=comun + """
        const i = e.data.i[0]; if (i < 0 || i >= n) return;
        const x = d.x.slice(), y = d.y.slice(), j = [...Array(n).keys()].find(k => k !== i && d.par[k] === d.par[i]);
        x[i] = cb_obj.x;
        if (j === undefined) y[i] = 0;
        else { const yy = Math.max(Math.abs(cb_obj.y), tol) * (cb_obj.y < 0 ? -1 : 1); y[i] = yy; x[j] = cb_obj.x; y[j] = -yy; }
        publicar(x, y, d.t.slice(), d.par.slice());
    """)
    p.js_on_event("tap", pulsar)
    p.js_on_event("panstart", empezar)
    p.js_on_event("pan", arrastrar)
    p.toolbar.active_drag = None


# Mapas de color: los de las figuras del Tema 5 (viridis para espectrogramas y
# escalogramas, magma para el módulo de una DFT 2D y grises para imágenes).
def _paleta(nombre: str):
    from bokeh.palettes import Greys256, Magma256, Viridis256
    return {"grises": Greys256, "viridis": Viridis256, "magma": Magma256}[nombre]


def figura_imagen(titulo: str, lado: int = 256, ancho: int = 260, ejes: bool = False):
    """Figura cuadrada para una imagen de ``lado``×``lado`` píxeles, con la fila 0
    arriba (como en Matlab y NumPy)."""
    from bokeh.models import Range1d
    p = figura(titulo, "", "", ancho=ancho, alto=ancho, x_range=Range1d(0, lado),
               y_range=Range1d(lado, 0), tools="pan,wheel_zoom,reset,save")
    p.grid.visible = False
    if not ejes:
        p.axis.visible = False
    return p


def imagen(p, fuente, x=0, y=0, dw=256, dh=256, paleta: str = "grises", bajo=0.0, alto=1.0,
           barra: bool = False):
    """Dibuja la columna ``img`` de ``fuente`` (una matriz, lista de filas) con un
    mapa de color; devuelve el ``LinearColorMapper`` para cambiar ``low`` y ``high``
    desde JS. ``x``, ``y``, ``dw`` y ``dh`` pueden ser columnas de la fuente."""
    from bokeh.models import ColorBar, LinearColorMapper
    mapa = LinearColorMapper(palette=_paleta(paleta), low=bajo, high=alto)
    p.image(image="img", x=x, y=y, dw=dw, dh=dh, source=fuente, color_mapper=mapa)
    if barra:
        cb = ColorBar(color_mapper=mapa, width=10, major_label_text_font=FUENTE,
                      major_label_text_font_size="11px", padding=4)
        p.add_layout(cb, "right")
    return mapa


def foto(titulo: str = "Foto propia (se procesa en el navegador)"):
    """Selector de fichero de imagen. Con ``foto_cargar`` de la biblioteca JS se
    convierte en una matriz de grises; la foto no sale del navegador."""
    from bokeh.models import FileInput
    return FileInput(title=titulo, accept="image/*", width=240)


def boton(texto: str, **kw):
    from bokeh.models import Button
    return Button(label=texto, width=kw.pop("width", 240), **kw)


def js(codigo: str, **args) -> CustomJS:
    """CustomJS con la biblioteca común ``JS`` (FFT, ventanas…) delante."""
    # Un argumento con el nombre de una función de JS la taparía (o al revés).
    choques = set(args) & set(re.findall(r"^(?:function|const)\s+(\w+)", JS, re.M))
    if choques:
        raise ValueError(f"argumentos con nombre de función de la biblioteca JS: {sorted(choques)}")
    # El try/catch hace visible en la consola cualquier error del cálculo.
    return CustomJS(args=args, code=JS + "try {\n" + codigo + "\n} catch (e) { console.error('PDS: ' + e); }")


def conectar(callback, *controles) -> None:
    """Ejecuta ``callback`` cuando cambia cualquiera de los controles."""
    for c in controles:
        if isinstance(c, Slider):
            c.js_on_change("value", callback)
        elif isinstance(c, Select):
            c.js_on_change("value", callback)
        elif isinstance(c, (RadioButtonGroup, CheckboxGroup)):
            c.js_on_change("active", callback)
        elif type(c).__name__ == "FileInput":
            c.js_on_change("value", callback)
        elif type(c).__name__ == "Button":
            c.js_on_event("button_click", callback)


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
// FFT inversa (misma longitud, potencia de 2); devuelve [re, im].
function ifft(re, im) {
    const n = re.length, [a, b] = fft(re, (im || new Array(n).fill(0)).map(v => -v));
    return [a.map(v => v / n), b.map(v => -v / n)];
}
// Convolución lineal directa.
function conv(x, h) {
    const y = new Array(x.length + h.length - 1).fill(0);
    for (let i = 0; i < x.length; i++) for (let j = 0; j < h.length; j++) y[i + j] += x[i] * h[j];
    return y;
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
// Números complejos como [re, im].
function cmul(a, b) { return [a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]]; }
function cdiv(a, b) { const d = b[0] * b[0] + b[1] * b[1]; return [(a[0] * b[0] + a[1] * b[1]) / d, (a[1] * b[0] - a[0] * b[1]) / d]; }
function csum(a, b) { return [a[0] + b[0], a[1] + b[1]]; }
function cres(a, b) { return [a[0] - b[0], a[1] - b[1]]; }
function cabs(a) { return Math.hypot(a[0], a[1]); }
function cexp(a) { const m = Math.exp(a[0]); return [m * Math.cos(a[1]), m * Math.sin(a[1])]; }
function cesc(k, a) { return [k * a[0], k * a[1]]; }
function csqrt(a) { const m = Math.sqrt(cabs(a)), f = Math.atan2(a[1], a[0]) / 2; return [m * Math.cos(f), m * Math.sin(f)]; }
// Coeficientes (de mayor a menor grado) del polinomio mónico con esas raíces.
function poli(raices) {
    let c = [[1, 0]];
    for (const r of raices) {
        const n = c.map(v => v.slice()); n.push([0, 0]);
        for (let i = 1; i < n.length; i++) n[i] = cres(n[i], cmul(r, c[i - 1]));
        c = n;
    }
    return c;
}
// Raíces de un polinomio real o complejo (coeficientes de mayor a menor grado),
// por el método de Durand–Kerner; los coeficientes iniciales nulos se descartan.
function raices(c) {
    c = c.map(v => Array.isArray(v) ? v : [v, 0]);
    const top = Math.max(...c.map(cabs)); while (c.length && cabs(c[0]) < 1e-9 * top) c = c.slice(1);
    const n = c.length - 1; if (n < 1) return [];
    const m = c.map(v => cdiv(v, c[0]));
    let r = enteros(0, n - 1).map(i => cexp([Math.log(0.9), 2 * PI * i / n + 0.4]));
    for (let it = 0; it < 500; it++) r = r.map((ri, i) => {
        let den = [1, 0]; r.forEach((rj, j) => { if (j !== i) den = cmul(den, cres(ri, rj)); });
        return cres(ri, cdiv(evalpoli(m, ri), den));
    });
    return r;
}
function polireal(raices) { return poli(raices).map(v => v[0]); }
function evalpoli(c, s) { let y = [0, 0]; for (const v of c) y = csum(cmul(y, s), Array.isArray(v) ? v : [v, 0]); return y; }
// k·Π(s − ceros)/Π(s − polos) en el punto complejo s.
function zpk(ceros, polos, k, s) {
    let y = [k, 0];
    for (const z of ceros) y = cmul(y, cres(s, z));
    for (const p of polos) y = cdiv(y, cres(s, p));
    return y;
}
// Ecuación en diferencias: a[0]y[n] = Σ b[k]x[n−k] − Σ a[k]y[n−k].
function filtrar(b, a, x) {
    const y = new Array(x.length).fill(0);
    for (let n = 0; n < x.length; n++) {
        let v = 0;
        for (let k = 0; k < b.length && k <= n; k++) v += b[k] * x[n - k];
        for (let k = 1; k < a.length && k <= n; k++) v -= a[k] * y[n - k];
        y[n] = v / a[0];
    }
    return y;
}
// Coeficientes en z^-1 de k·Π(z − ceros)/Π(z − polos) (más polos que ceros, o igual).
function ba(ceros, polos, k) {
    const b = new Array(polos.length - ceros.length).fill(0).concat(polireal(ceros).map(v => k * v));
    return [b, polireal(polos)];
}
function desenrollar(f) {
    const r = f.slice();
    for (let i = 1; i < r.length; i++) { let d = r[i] - r[i - 1]; d -= 2 * PI * Math.round(d / (2 * PI)); r[i] = r[i - 1] + d; }
    return r;
}
// Respuesta de H(s) = b(s)/a(s) (coeficientes de mayor a menor grado) en los
// instantes t (equiespaciados desde 0): "escalon" o "impulso" (sin la parte δ).
function continua(b, a, t, tipo) {
    const n = a.length - 1, a0 = a[0];
    const an = a.map(v => v / a0), bn = new Array(n + 1 - b.length).fill(0).concat(b.map(v => v / a0));
    const D = bn[0], c = []; for (let k = 1; k <= n; k++) c.push(bn[k] - an[k] * D);
    const u = tipo === "impulso" ? 0 : 1;
    const f = x => { const d = x.slice(1); let v = u; for (let k = 1; k <= n; k++) v -= an[k] * x[n - k]; d.push(v); return d; };
    const sal = x => { let y = u * D; for (let k = 1; k <= n; k++) y += c[k - 1] * x[n - k]; return y; };
    let x = new Array(n).fill(0); if (tipo === "impulso" && n > 0) x[n - 1] = 1;
    const rapido = Math.max(1, ...an.slice(1).map(v => Math.pow(Math.abs(v), 1 / n)));
    const T = t.length > 1 ? t[1] - t[0] : 0, pasos = Math.max(1, Math.ceil(T * rapido * 20)), h = T / pasos;
    const y = [];
    for (let i = 0; i < t.length; i++) {
        y.push(n ? sal(x) : (tipo === "impulso" ? 0 : D));
        for (let s = 0; s < pasos && n; s++) {
            const k1 = f(x), k2 = f(x.map((v, j) => v + h / 2 * k1[j])), k3 = f(x.map((v, j) => v + h / 2 * k2[j])), k4 = f(x.map((v, j) => v + h * k3[j]));
            x = x.map((v, j) => v + h / 6 * (k1[j] + 2 * k2[j] + 2 * k3[j] + k4[j]));
        }
    }
    return y;
}
// Polos del Butterworth analógico de orden N y pulsación de corte wc.
function polos_butter(N, wc = 1) {
    const p = []; for (let k = 1; k <= N; k++) p.push(cesc(wc, cexp([0, PI * (2 * k + N - 1) / (2 * N)])));
    return p;
}
// Butterworth digital paso bajo por transformación bilineal con predistorsión
// (Ωc en rad/muestra): devuelve [ceros, polos, k] en z con ganancia 1 en Ω = 0.
function butter_z(N, Wc) {
    const wc = 2 * Math.tan(Wc / 2), polos = polos_butter(N, wc).map(p => cdiv(csum([2, 0], p), cres([2, 0], p)));
    const ceros = new Array(N).fill(0).map(() => [-1, 0]);
    return [ceros, polos, 1 / cabs(zpk(ceros, polos, 1, [1, 0]))];
}
// Generador pseudoaleatorio con semilla (ruido reproducible), normal de varianza 1.
function ruido(L, semilla = 1) {
    let s = semilla >>> 0; const u = () => { s = (1664525 * s + 1013904223) >>> 0; return (s + 0.5) / 4294967296; };
    const r = []; for (let i = 0; i < L; i++) r.push(Math.sqrt(-2 * Math.log(u())) * Math.cos(2 * PI * u()));
    return r;
}
// ---- Temas 5 y 6 -----------------------------------------------------
// Generador con semilla (mulberry32): devuelve una función que da uniformes en (0, 1).
function generador(semilla = 1) {
    let s = (semilla >>> 0) || 1;
    return function () {
        s = (s + 0x6D2B79F5) >>> 0; let t = s;
        t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
        return (((t ^ (t >>> 14)) >>> 0) + 0.5) / 4294967296;
    };
}
// Muestra N(0, 1) a partir de un generador de uniformes (Box-Muller).
function gauss(u) { return Math.sqrt(-2 * Math.log(u())) * Math.cos(2 * PI * u()); }
function media(x) { let s = 0; for (const v of x) s += v; return s / x.length; }
function varianza(x) { const m = media(x); let s = 0; for (const v of x) s += (v - m) * (v - m); return s / (x.length - 1); }
function maximo(x) { let m = -Infinity; for (const v of x) if (v > m) m = v; return m; }
function minimo(x) { let m = Infinity; for (const v of x) if (v < m) m = v; return m; }
// Histograma normalizado como densidad (área 1 sobre las N muestras) en nb
// intervalos de [a, b]: {c: centros, d: alturas, ancho}.
function histo(x, a, b, nb) {
    const ancho = (b - a) / nb, n = new Array(nb).fill(0);
    for (const v of x) { const i = Math.floor((v - a) / ancho); if (i >= 0 && i < nb) n[i]++; else if (v === b) n[nb - 1]++; }
    return {c: n.map((_, i) => a + (i + 0.5) * ancho), d: n.map(v => v / (x.length * ancho)), ancho: ancho};
}
function pot2(n) { let p = 1; while (p < n) p <<= 1; return p; }
// FFT 2D de una matriz M×N (lista de filas; M y N potencias de 2); devuelve [re, im].
function fft2d(re, im, inversa = false) {
    const M = re.length, N = re[0].length, f = inversa ? ifft : fft;
    const R = [], I = [];
    for (let m = 0; m < M; m++) { const [a, b] = f(re[m], im ? im[m] : null); R.push(a); I.push(b); }
    for (let n = 0; n < N; n++) {
        const [a, b] = f(R.map(r => r[n]), I.map(r => r[n]));
        for (let m = 0; m < M; m++) { R[m][n] = a[m]; I[m][n] = b[m]; }
    }
    return [R, I];
}
function ifft2d(re, im) { return fft2d(re, im, true); }
// Lleva el origen de frecuencias al centro (fftshift 2D).
function centrar2d(A) {
    const M = A.length, N = A[0].length;
    return enteros(0, M - 1).map(m => enteros(0, N - 1).map(n => A[(m + M / 2) % M][(n + N / 2) % N]));
}
// Convolución 2D con salida del tamaño de f ('same'); h es K×K con K impar y el
// borde se completa con "ceros", repitiendo el borde ("repetir") o reflejando ("reflejar").
function conv2d(f, h, borde = "repetir") {
    const M = f.length, N = f[0].length, K = h.length, c = (K - 1) / 2;
    const idx = (i, L) => borde === "repetir" ? Math.min(Math.max(i, 0), L - 1)
        : borde === "reflejar" ? (i < 0 ? -i - 1 : i >= L ? 2 * L - i - 1 : i) : i;
    const g = [];
    for (let m = 0; m < M; m++) {
        const fila = new Array(N).fill(0);
        for (let i = 0; i < K; i++) {
            const mm = idx(m - (i - c), M); if (mm < 0 || mm >= M) continue;
            const fm = f[mm], hi = h[i];
            for (let j = 0; j < K; j++) {
                const hij = hi[j]; if (hij === 0) continue;
                for (let n = 0; n < N; n++) {
                    const nn = idx(n - (j - c), N); if (nn < 0 || nn >= N) continue;
                    fila[n] += hij * fm[nn];
                }
            }
        }
        g.push(fila);
    }
    return g;
}
// STFT de x con la ventana w (L muestras), salto R y DFT de N puntos (potencia
// de 2): {S: |X[m,k]|² de cada tramo para k = 0..N/2, ini: muestra inicial de cada tramo}.
function stft_pot(x, w, R, N) {
    const L = w.length, S = [], ini = [];
    for (let s = 0; s + L <= x.length; s += R) {
        const re = new Array(N).fill(0);
        for (let r = 0; r < L; r++) re[r] = x[s + r] * w[r];
        const [a, b] = fft(re); S.push(a.slice(0, N / 2 + 1).map((v, k) => v * v + b[k] * b[k])); ini.push(s);
    }
    return {S: S, ini: ini};
}
// Filtros paso bajo h0 de la DWT ortogonal (los de reconstrucción de PyWavelets).
const DWT_H0 = {
    "Haar": [Math.SQRT1_2, Math.SQRT1_2],
    "db2": [0.48296291314453416, 0.8365163037378079, 0.2241438680420134, -0.12940952255126037],
    "db4": [0.2303778133088965, 0.7148465705529157, 0.6308807679298589, -0.027983769416859854,
            -0.18703481171909309, 0.030841381835560764, 0.0328830116668852, -0.010597401785069032],
};
function dwt_h1(h0) { const L = h0.length; return h0.map((_, n) => (n % 2 ? -1 : 1) * h0[L - 1 - n]); }
// Un nivel de la DWT con extensión periódica: a[k] = Σ h0[n] x[2k+n−o], d[k] = Σ h1[n] x[2k+n−o],
// con o = L/2 − 1 (0 en Haar), el mismo origen que el modo "periodization" de PyWavelets.
function dwt_nivel(x, h0) {
    const N = x.length, h1 = dwt_h1(h0), o = h0.length / 2 - 1, a = [], d = [];
    for (let k = 0; k < N / 2; k++) {
        let sa = 0, sd = 0;
        for (let n = 0; n < h0.length; n++) { const v = x[mod(2 * k + n - o, N)]; sa += h0[n] * v; sd += h1[n] * v; }
        a.push(sa); d.push(sd);
    }
    return [a, d];
}
// Inversa de un nivel: x[m] = Σ_k a[k] h0[m − 2k + o] + d[k] h1[m − 2k + o].
function idwt_nivel(a, d, h0) {
    const N = 2 * a.length, h1 = dwt_h1(h0), o = h0.length / 2 - 1, x = new Array(N).fill(0);
    for (let k = 0; k < a.length; k++)
        for (let n = 0; n < h0.length; n++) { const m = mod(2 * k + n - o, N); x[m] += h0[n] * a[k] + h1[n] * d[k]; }
    return x;
}
// DWT de J niveles: {a: aproximación a_J, d: [d_1, …, d_J]} (longitud de x divisible por 2^J).
function dwt_dec(x, nombre, J) {
    const h0 = DWT_H0[nombre], d = []; let a = x.slice();
    for (let j = 0; j < J; j++) { const [aa, dd] = dwt_nivel(a, h0); d.push(dd); a = aa; }
    return {a: a, d: d};
}
function dwt_rec(c, nombre) {
    const h0 = DWT_H0[nombre]; let a = c.a.slice();
    for (let j = c.d.length - 1; j >= 0; j--) a = idwt_nivel(a, c.d[j], h0);
    return a;
}
// Componentes de la descomposición, cada una de la longitud de la señal:
// {A: A_J, D: [D_1, …, D_J]}, con x = A_J + D_J + … + D_1.
function dwt_componentes(c, nombre) {
    const cero = v => v.map(() => 0);
    const A = dwt_rec({a: c.a, d: c.d.map(cero)}, nombre);
    const D = c.d.map((_, j) => dwt_rec({a: cero(c.a), d: c.d.map((v, i) => i === j ? v : cero(v))}, nombre));
    return {A: A, D: D};
}
// Wavelets madre continuas: valor complejo [re, im] en t.
function wavelet(nombre, t) {
    if (nombre === "Morlet") { const g = Math.pow(PI, -0.25) * Math.exp(-t * t / 2); return [g * Math.cos(6 * t), g * Math.sin(6 * t)]; }
    return [2 / (Math.sqrt(3) * Math.pow(PI, 0.25)) * (1 - t * t) * Math.exp(-t * t / 2), 0];
}
// Frecuencia (Hz) equivalente a la escala a (s): ω₀/(2πa) para Morlet y √2/(2πa) para el sombrero mexicano.
function wavelet_frec(nombre, a) { return (nombre === "Morlet" ? 6 : Math.SQRT2) / (2 * PI * a); }
// CWT W(a, b) = (1/√a) ∫ x(t) ψ*((t − b)/a) dt de x muestreada con periodo T, para
// cada escala de "escalas" (s) y cada b = nT; devuelve |W|² (una fila por escala).
function cwt_pot(x, T, escalas, nombre) {
    const L = x.length, P = pot2(2 * L), xr = new Array(P).fill(0);
    for (let n = 0; n < L; n++) xr[n] = x[n];
    const [Xr, Xi] = fft(xr);
    return escalas.map(a => {
        // g[n] = (T/√a) ψ*(−nT/a), con los índices negativos al final (correlación = convolución con g)
        const gr = new Array(P).fill(0), gi = new Array(P).fill(0), M = Math.min(P / 2 - 1, Math.ceil(6 * a / T));
        for (let n = -M; n <= M; n++) { const v = wavelet(nombre, -n * T / a), i = mod(n, P); gr[i] = T / Math.sqrt(a) * v[0]; gi[i] = -T / Math.sqrt(a) * v[1]; }
        const [Gr, Gi] = fft(gr, gi);
        const [wr, wi] = ifft(Xr.map((v, k) => v * Gr[k] - Xi[k] * Gi[k]), Xr.map((v, k) => v * Gi[k] + Xi[k] * Gr[k]));
        return wr.slice(0, L).map((v, n) => v * v + wi[n] * wi[n]);
    });
}
// Imagen de prueba de los apuntes del Tema 5 (N×N, valores en [0, 1], fila 0 arriba).
function imagen_prueba(N = 256) {
    const f = [];
    for (let i = 0; i < N; i++) {
        const y = i / N, fila = [];
        for (let j = 0; j < N; j++) {
            const x = j / N; let v = 0.35 + 0.25 * x;
            if ((x - 0.3) ** 2 + (y - 0.32) ** 2 < 0.18 ** 2) v = 0.85;
            if (x > 0.58 && x < 0.9 && y > 0.12 && y < 0.45) v = 0.12;
            if (y > 0.6 && y < 0.9 && x > 0.08 && x < 0.48) v = 0.5 + 0.4 * Math.cos(2 * PI * 16 * x);
            const r = Math.hypot(x - 0.73, y - 0.75);
            if (r < 0.16) v = 0.5 + 0.4 * Math.cos(2 * PI * 120 * r * r);
            fila.push(v);
        }
        f.push(fila);
    }
    return f;
}
// Otras imágenes generadas: "Tablero", "Anillos" (frecuencia espacial creciente
// desde el centro), "Rayas" (finas, oblicuas) y "Texto".
function imagen_patron(nombre, N = 256) {
    if (nombre === "Prueba") return imagen_prueba(N);
    if (nombre === "Texto" && typeof document !== "undefined") {
        const cv = document.createElement("canvas"); cv.width = cv.height = N;
        const cx = cv.getContext("2d"); cx.fillStyle = "#fff"; cx.fillRect(0, 0, N, N); cx.fillStyle = "#000";
        cx.font = `600 ${Math.round(N / 4.2)}px Fira Sans, Helvetica, sans-serif`; cx.textAlign = "center"; cx.textBaseline = "middle";
        cx.fillText("Señales", N / 2, N * 0.32); cx.font = `${Math.round(N / 9)}px Fira Sans, Helvetica, sans-serif`;
        cx.fillText("Procesamiento de", N / 2, N * 0.62); cx.fillText("señales · UCM", N / 2, N * 0.8);
        const d = cx.getImageData(0, 0, N, N).data;
        return enteros(0, N - 1).map(i => enteros(0, N - 1).map(j => d[4 * (i * N + j)] / 255));
    }
    return enteros(0, N - 1).map(i => enteros(0, N - 1).map(j => {
        const x = (j + 0.5) / N - 0.5, y = (i + 0.5) / N - 0.5;
        if (nombre === "Tablero") return (Math.floor(8 * (x + 0.5)) + Math.floor(8 * (y + 0.5))) % 2 ? 0.85 : 0.15;
        if (nombre === "Anillos") return 0.5 + 0.5 * Math.cos(PI * N * (x * x + y * y));
        return 0.5 + 0.5 * Math.cos(2 * PI * 0.42 * N * (0.8 * x + 0.6 * y));
    }));
}
// Lee la foto de un FileInput, la recorta al cuadrado central, la reduce a N×N en
// grises ([0, 1]) y llama a siguiente(imagen). La foto no sale del navegador.
function foto_cargar(fi, N, siguiente) {
    if (!fi.value) return;
    const img = new Image();
    img.onload = () => {
        const cv = document.createElement("canvas"); cv.width = cv.height = N;
        const cx = cv.getContext("2d"), lado = Math.min(img.width, img.height);
        cx.drawImage(img, (img.width - lado) / 2, (img.height - lado) / 2, lado, lado, 0, 0, N, N);
        const d = cx.getImageData(0, 0, N, N).data;
        siguiente(enteros(0, N - 1).map(i => enteros(0, N - 1).map(j => {
            const k = 4 * (i * N + j); return (0.299 * d[k] + 0.587 * d[k + 1] + 0.114 * d[k + 2]) / 255;
        })));
    };
    img.src = "data:" + (fi.mime_type || "image/png") + ";base64," + fi.value;
}
// Método de Welch con tramos de L muestras que avanzan R, ventana w y DFT de N ≥ L
// puntos: estima la DEP bilateral Φ_xx(e^{jΩ}) en Ω_k = 2πk/N, k = 0..N/2 (y, si se da
// y, también Φ_yy y la cruzada Φ_yx, que promedia Y·X*). Sin restar la media.
function welch(x, y, w, R, N) {
    const L = w.length, U = w.reduce((a, v) => a + v * v, 0), K = N / 2 + 1;
    const Pxx = new Array(K).fill(0), Pyy = new Array(K).fill(0), Cr = new Array(K).fill(0), Ci = new Array(K).fill(0);
    let M = 0;
    for (let s = 0; s + L <= x.length; s += R) {
        const a = new Array(N).fill(0); for (let r = 0; r < L; r++) a[r] = x[s + r] * w[r];
        const [Xr, Xi] = fft(a);
        let Yr, Yi;
        if (y) { const b = new Array(N).fill(0); for (let r = 0; r < L; r++) b[r] = y[s + r] * w[r]; [Yr, Yi] = fft(b); }
        for (let k = 0; k < K; k++) {
            Pxx[k] += Xr[k] * Xr[k] + Xi[k] * Xi[k];
            if (y) { Pyy[k] += Yr[k] * Yr[k] + Yi[k] * Yi[k]; Cr[k] += Yr[k] * Xr[k] + Yi[k] * Xi[k]; Ci[k] += Yi[k] * Xr[k] - Yr[k] * Xi[k]; }
        }
        M++;
    }
    const e = v => v.map(z => z / (M * U));
    return {W: enteros(0, K - 1).map(k => 2 * PI * k / N), Pxx: e(Pxx), Pyy: e(Pyy), Pyx: [e(Cr), e(Ci)], tramos: M};
}
// Matriz (lista de filas) en el formato que necesita el glifo image de Bokeh.
function matriz(A) {
    const M = A.length, N = M ? A[0].length : 0, f = new Float32Array(M * N);
    for (let m = 0; m < M; m++) for (let n = 0; n < N; n++) f[m * N + n] = A[m][n];
    return Bokeh.require("core/util/ndarray").ndarray(f.buffer, {dtype: "float32", shape: [M, N]});
}
// Reproduce x (frecuencia de muestreo fs) por los altavoces, normalizada.
function sonar(x, fs) {
    const C = window.AudioContext || window.webkitAudioContext; if (!C) return;
    const ctx = window.__pds_audio || (window.__pds_audio = new C());
    if (ctx.state === "suspended") ctx.resume();
    let m = 1e-9; for (const v of x) m = Math.max(m, Math.abs(v));
    const b = ctx.createBuffer(1, x.length, fs), d = b.getChannelData(0);
    for (let i = 0; i < x.length; i++) d[i] = 0.8 * x[i] / m;
    const s = ctx.createBufferSource(); s.buffer = b; s.connect(ctx.destination); s.start();
}
"""


FICHAS = RAIZ / "fichas"


def _ficha(tema: int, nombre: str) -> str:
    """HTML de ``fichas/T<tema>-<nombre>.md`` si existe (introducción teórica,
    guía de uso, ejercicios, recursos y relación con otros conceptos)."""
    fichero = FICHAS / f"T{tema}-{nombre}.md"
    if not fichero.exists():
        return ""
    import markdown
    # Los exponentes se escriben e^{…} en el Markdown y se muestran como superíndices
    texto = re.sub(r"\^\{([^{}]*)\}", r"<sup>\1</sup>", fichero.read_text(encoding="utf-8"))
    texto = re.sub(r"_\{([^{}]*)\}", r"<sub>\1</sub>", texto)
    return markdown.markdown(texto, extensions=["tables", "md_in_html"])


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
    ficha = _ficha(tema, nombre)
    if referencia or ficha:
        enlace = ' · <a href="#ficha">Ficha de uso: teoría, guía, ejercicios y recursos ↓</a>' if ficha else ""
        cab += f'<p class="pds-ref">{html.escape(referencia)}{enlace}</p>'
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
                                 template_variables={"fuente": FUENTE, "ficha": ficha}),
                       encoding="utf-8")
    indice = SALIDA / "indice"
    indice.mkdir(exist_ok=True)
    (indice / f"T{tema}-{nombre}.json").write_text(json.dumps(
        {"tema": tema, "titulo": titulo, "archivo": destino.name,
         "descripcion": descripcion}, ensure_ascii=False, indent=1), encoding="utf-8")
    return destino
