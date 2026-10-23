"""T5 · Operaciones puntuales, histograma y ecualización de una imagen."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div, LinearAxis, Range1d
import pds_bokeh as pb

LADO = 256

F0 = ColumnDataSource(dict(img=[]))
G0 = ColumnDataSource(dict(img=[]))
H1 = ColumnDataSource(dict(r=[], h=[], F=[]))
H2 = ColumnDataSource(dict(r=[], h=[], F=[]))
Tr = ColumnDataSource(dict(r=[], s=[]))
Foto = ColumnDataSource(dict(f=[]))

p1 = pb.figura_imagen("Imagen original", LADO, ancho=230)
pb.imagen(p1, F0, dw=LADO, dh=LADO)
p2 = pb.figura_imagen("Imagen transformada s = T(r)", LADO, ancho=230)
pb.imagen(p2, G0, dw=LADO, dh=LADO)
p2.x_range = p1.x_range
p2.y_range = p1.y_range
p3 = pb.figura("Transformación T(r)", "r (nivel de entrada)", "s", ancho=200, alto=200, x_range=(0, 255), y_range=(0, 255))
p3.line("r", "s", source=Tr, color=pb.AZUL, line_width=2)


def hist(titulo, fuente):
    p = pb.figura(titulo, "nivel r", "proporción de píxeles p[r]", ancho=350, alto=200, x_range=(-1, 256))
    barras = p.vbar(x="r", top="h", width=1, source=fuente, fill_color=pb.GRIS, line_color=None)
    p.y_range.renderers = [barras]
    p.extra_y_ranges = {"F": Range1d(0, 1.02)}
    p.add_layout(LinearAxis(y_range_name="F", axis_label="F(r)"), "right")
    p.line("r", "F", source=fuente, color=pb.ROJO, line_width=2, y_range_name="F")
    return p


p4 = hist("Histograma original y F(r)", H1)
p5 = hist("Histograma transformado", H2)

imagen = pb.selector("Imagen", ["Prueba con poco contraste", "Prueba", "Oscura", "Texto", "Foto propia"])
fi = pb.foto()
op = pb.selector("Operación", ["Ninguna", "Negativo", "Corrección gamma", "Estiramiento lineal de [r₁, r₂]",
                               "Umbralización", "Ecualización"], "Ecualización")
gam = pb.deslizador("γ", 0.2, 3, 0.5, 0.05)
r1 = pb.deslizador("r₁ (nivel que pasa a 0)", 0, 254, 90, 1)
r2 = pb.deslizador("r₂ (nivel que pasa a 255)", 1, 255, 170, 1)
u = pb.deslizador("Umbral u", 0, 255, 128, 1)
info = Div(text="", width=250)

cb = pb.js("""
    const N = LADO;
    let f;
    if (imagen.value === "Foto propia" && Foto.data.f.length) f = Foto.data.f[0];
    else if (imagen.value === "Texto") f = imagen_patron("Texto", N);
    else { f = imagen_prueba(N); if (imagen.value.includes("poco")) f = f.map(r => r.map(v => 0.4 + 0.25 * v)); else if (imagen.value === "Oscura") f = f.map(r => r.map(v => 0.6 * v ** 2.2)); }
    // Niveles enteros de 0 a 255
    const q = f.map(r => r.map(v => Math.min(255, Math.max(0, Math.round(255 * v)))));
    const cuenta = img => { const h = new Array(256).fill(0); for (const r of img) for (const v of r) h[v]++; return h.map(v => v / (N * N)); };
    const acum = p => { let s = 0; return p.map(v => (s += v)); };
    const p = cuenta(q), F = acum(p), o = op.value;
    let T;
    if (o === "Negativo") T = enteros(0, 255).map(r => 255 - r);
    else if (o.startsWith("Corrección")) T = enteros(0, 255).map(r => Math.round(255 * Math.pow(r / 255, gam.value)));
    else if (o.startsWith("Estiramiento")) { const a = Math.min(r1.value, r2.value - 1), b = Math.max(r2.value, a + 1); T = enteros(0, 255).map(r => Math.round(255 * Math.min(1, Math.max(0, (r - a) / (b - a))))); }
    else if (o === "Umbralización") T = enteros(0, 255).map(r => r > u.value ? 255 : 0);
    else if (o === "Ecualización") T = F.map(v => Math.round(255 * v));
    else T = enteros(0, 255);
    const g = q.map(r => r.map(v => T[v])), pg = cuenta(g), Fg = acum(pg);
    F0.data = {img: [matriz(q.map(r => r.map(v => v / 255)))]}; G0.data = {img: [matriz(g.map(r => r.map(v => v / 255)))]};
    H1.data = {r: enteros(0, 255), h: p, F: F}; H2.data = {r: enteros(0, 255), h: pg, F: Fg};
    Tr.data = {r: enteros(0, 255), s: T};
    const ocupa = h => h.filter(v => v > 0).length, ext = h => { const i = h.findIndex(v => v > 0); let j = 255; while (j > 0 && !h[j]) j--; return [i, j]; };
    const m = h => h.reduce((a, v, r) => a + v * r, 0), sd = h => { const mu = m(h); return Math.sqrt(h.reduce((a, v, r) => a + v * (r - mu) ** 2, 0)); };
    info.text = `<p>Original: niveles de ${ext(p)[0]} a ${ext(p)[1]}, ${ocupa(p)} niveles distintos; media ${m(p).toFixed(1)}, desviación ${sd(p).toFixed(1)}</p>` +
        `<p>Transformada: niveles de ${ext(pg)[0]} a ${ext(pg)[1]}, ${ocupa(pg)} niveles distintos; media ${m(pg).toFixed(1)}, desviación ${sd(pg).toFixed(1)}</p>` +
        (o === "Ecualización" ? "<p>T(r) = round(255·F(r)): la F de la imagen ecualizada es casi una recta, pero los píxeles de un mismo nivel van todos al mismo nivel nuevo y el histograma no queda plano</p>" : "");
""", F0=F0, G0=G0, H1=H1, H2=H2, Tr=Tr, Foto=Foto, imagen=imagen, op=op, gam=gam, r1=r1, r2=r2, u=u, info=info, LADO=LADO)
pb.conectar(cb, imagen, op, gam, r1, r2, u)
fi.js_on_change("value", pb.js("""
    foto_cargar(fi, LADO, img => { Foto.data = {f: [img]}; if (imagen.value === "Foto propia") cb.execute(); else imagen.value = "Foto propia"; });
""", fi=fi, Foto=Foto, imagen=imagen, cb=cb, LADO=LADO))

pb.pagina(__file__, "Histograma y operaciones puntuales", tema=5,
          descripcion="Una operación puntual cambia cada píxel con una función de su propio nivel, s = T(r). El histograma "
                      "cuenta los píxeles de cada nivel: uno estrecho corresponde a una imagen con poco contraste. La "
                      "ecualización usa T(r) = 255·F(r), con F la proporción acumulada, para repartir los niveles por todo el "
                      "rango. Puedes cargar una foto propia; se procesa en el navegador.",
          controles=[imagen, fi, op, gam, r1, r2, u, info], graficas=[[p1, p2, p3], [p4, p5]], inicio=cb,
          referencia="Transparencias T5-03, operaciones puntuales, histograma y ecualización · Apuntes del Tema 5, sección 3")
