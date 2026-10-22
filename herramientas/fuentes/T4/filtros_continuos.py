"""T4 · Aproximaciones de filtros analógicos: Butterworth, Chebyshev y elíptico."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
import numpy as np
from bokeh.models import ColumnDataSource, Div, Span
from scipy import signal
import pds_bokeh as pb

# Prototipos paso bajo normalizados (ωp = 1 rad/s; en Chebyshev II, ωs = 1) para
# N = 1..10, Rp = 0,5..3 dB y Rs = 20..80 dB. Se calculan aquí con SciPy y la
# página sólo evalúa H(jω) a partir de ceros, polos y ganancia.
RP = [0.5, 1, 1.5, 2, 2.5, 3]
RS = list(range(20, 81, 10))


def zpk(z, p, k):
    z, p = np.atleast_1d(z), np.atleast_1d(p)
    return [[[float(c.real), float(c.imag)] for c in z], [[float(c.real), float(c.imag)] for c in p], float(k)]


TABLA = {}
for N in range(1, 11):
    TABLA[f"B{N}"] = zpk(*signal.buttap(N))
    for rp in RP:
        TABLA[f"C1-{N}-{rp}"] = zpk(*signal.cheb1ap(N, rp))
    for rs in RS:
        TABLA[f"C2-{N}-{rs}"] = zpk(*signal.cheb2ap(N, rs))
        for rp in RP:
            TABLA[f"E-{N}-{rp}-{rs}"] = zpk(*signal.ellipap(N, rp, rs))

w = np.logspace(-1, 1, 500)
F = ColumnDataSource(dict(w=w, B=w * 0, C1=w * 0, C2=w * 0, E=w * 0, sel=w * 0, f=w * 0, g=w * 0))
PZ = ColumnDataSource(dict(px=[], py=[]))
ZZ = ColumnDataSource(dict(zx=[], zy=[]))

p1 = pb.figura("Módulo |H(jω)| (dB) de las cuatro aproximaciones con el mismo N", "ω (rad/s)", "dB",
               ancho=560, alto=260, x_axis_type="log", y_range=(-100, 5))
for col, color, nombre in (("B", pb.AZUL, "Butterworth"), ("C1", pb.ROJO, "Chebyshev I"),
                           ("C2", pb.VERDE, "Chebyshev II"), ("E", pb.NARANJA, "Elíptico")):
    p1.line("w", col, source=F, color=color, line_width=2, legend_label=nombre)
ws = Span(location=2, dimension="height", line_color=pb.GRIS, line_dash="dashed")
p1.add_layout(ws)
pb.leyenda(p1, "right")
p2 = pb.figura("Polos (×) y ceros (○) del seleccionado", "Re s", "Im s", ancho=240, alto=240,
               x_range=(-2, 0.5), y_range=(-2.5, 2.5), match_aspect=False)
p2.scatter("px", "py", source=PZ, marker="x", size=12, line_width=2.5, color=pb.ROJO)
p2.scatter("zx", "zy", source=ZZ, marker="circle", size=11, line_width=2, line_color=pb.AZUL, fill_color=None)
p2.line(x=[0, 0], y=[-10, 10], color=pb.GRIS, line_width=1)
p3 = pb.figura("Módulo lineal del seleccionado", "ω (rad/s)", "", ancho=225, alto=200, x_range=(0, 3))
p3.line("w", "sel", source=F, color=pb.AZUL, line_width=2)
p4 = pb.figura("Retardo de grupo del seleccionado", "ω (rad/s)", "s", ancho=225, alto=200, x_range=(0, 3))
p4.line("w", "g", source=F, color=pb.VERDE, line_width=2)

tipo = pb.selector("Aproximación seleccionada", ["Butterworth", "Chebyshev I", "Chebyshev II", "Elíptico"])
N = pb.deslizador("Orden N", 1, 10, 4, 1)
Rp = pb.deslizador("Rp, rizado en la banda de paso (dB)", 0.5, 3, 1, 0.5)
Rs = pb.deslizador("Rs, atenuación mínima (dB)", 20, 80, 40, 10)
Ws = pb.deslizador("ωs (rad/s) para medir la atenuación", 1.05, 5, 2, 0.05)
info = Div(text="", width=240)

cb = pb.js("""
    const n = N.value, rp = Rp.value, rs = Rs.value, w = Array.from(F.data.w);
    const clave = {"Butterworth": "B" + n, "Chebyshev I": `C1-${n}-${rp}`, "Chebyshev II": `C2-${n}-${rs}`, "Elíptico": `E-${n}-${rp}-${rs}`};
    const resp = c => { const [z, p, k] = T[c]; return w.map(v => zpk(z, p, k, [0, v])); };
    const d = {w: w};
    for (const [nombre, col] of [["Butterworth", "B"], ["Chebyshev I", "C1"], ["Chebyshev II", "C2"], ["Elíptico", "E"]])
        d[col] = resp(clave[nombre]).map(h => db(cabs(h), -200));
    const Hs = resp(clave[tipo.value]), f = desenrollar(Hs.map(h => Math.atan2(h[1], h[0])));
    d.sel = Hs.map(cabs);
    d.g = w.map((_, i) => { const j = Math.min(Math.max(i, 1), w.length - 2); return -(f[j + 1] - f[j - 1]) / (w[j + 1] - w[j - 1]); });
    d.f = f; F.data = d;
    const [z, p, k] = T[clave[tipo.value]];
    PZ.data = {px: p.map(v => v[0]), py: p.map(v => v[1])};
    ZZ.data = {zx: z.map(v => v[0]), zy: z.map(v => v[1])};
    ws.location = Ws.value;
    const at = c => { const [z, p, k] = T[clave[c]]; return -db(cabs(zpk(z, p, k, [0, Ws.value])), -300); };
    info.text = `<p>Atenuación en ωs = ${Ws.value.toFixed(2)} rad/s:</p><ul style="margin:0;padding-left:18px">` +
        ["Butterworth", "Chebyshev I", "Chebyshev II", "Elíptico"].map(c => `<li>${c}: ${at(c).toFixed(1)} dB</li>`).join("") + "</ul>" +
        `<p>Butterworth: ωc = 1 (−3 dB). Chebyshev I y elíptico: ωp = 1 (−Rp dB). Chebyshev II: ωs = 1 (−Rs dB).</p>` +
        `<p>${tipo.value}: ${p.length} polos${z.length ? " y " + z.length + " ceros en el eje imaginario" : ", sin ceros finitos"}.</p>`;
""", F=F, PZ=PZ, ZZ=ZZ, T=TABLA, tipo=tipo, N=N, Rp=Rp, Rs=Rs, Ws=Ws, ws=ws, info=info)
pb.conectar(cb, tipo, N, Rp, Rs, Ws)

pb.pagina(__file__, "Aproximaciones de filtros analógicos", tema=4,
          descripcion="Con el mismo orden N, Butterworth es máximamente plano; Chebyshev I admite rizado en la banda "
                      "de paso y Chebyshev II en la de supresión a cambio de una transición más abrupta; el elíptico "
                      "tiene rizado en las dos y la transición más estrecha. Los polos de Butterworth están en una "
                      "circunferencia y los de Chebyshev en una elipse; los ceros, sobre el eje jω.",
          controles=[tipo, N, Rp, Rs, Ws, info], graficas=[p1, [p2, p3, p4]], inicio=cb,
          referencia="Transparencias T4-02, filtros continuos · Apuntes del Tema 4, sección 2")
