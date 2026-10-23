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
# Plantilla: zonas prohibidas en la banda de paso (por debajo de −Rp hasta ωp = 1) y en la de supresión (por encima de −Rs desde ωs)
Pl = ColumnDataSource(dict(left=[], right=[], top=[], bottom=[]))
p1.quad(left="left", right="right", top="top", bottom="bottom", source=Pl, fill_color=pb.GRIS_CLARO, fill_alpha=0.35, line_color=None)
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
Ws = pb.deslizador("ωs (rad/s), borde de la banda eliminada", 1.05, 5, 2, 0.05)
ajuste = pb.botones(["Normalizados", "Ajustados a la plantilla"])
info = Div(text="", width=240)

cb = pb.js("""
    const n = N.value, rp = Rp.value, rs = Rs.value, w = Array.from(F.data.w);
    const clave = {"Butterworth": "B" + n, "Chebyshev I": `C1-${n}-${rp}`, "Chebyshev II": `C2-${n}-${rs}`, "Elíptico": `E-${n}-${rp}-${rs}`};
    // Escala de frecuencias: con «ajustados», Butterworth da −Rp en ωp = 1 y Chebyshev II da −Rs en ωs
    const aj = ajuste.active === 1, fac = {"Butterworth": aj ? (10 ** (rp / 10) - 1) ** (-1 / (2 * n)) : 1, "Chebyshev I": 1,
                                         "Chebyshev II": aj ? Ws.value : 1, "Elíptico": 1};
    const nom = {}; for (const c in clave) nom[clave[c]] = c;
    const resp = c => { const [z, p, k] = T[c], a = fac[nom[c]]; return w.map(v => zpk(z, p, k, [0, v / a])); };
    const d = {w: w};
    for (const [nombre, col] of [["Butterworth", "B"], ["Chebyshev I", "C1"], ["Chebyshev II", "C2"], ["Elíptico", "E"]])
        d[col] = resp(clave[nombre]).map(h => db(cabs(h), -200));
    const Hs = resp(clave[tipo.value]), f = desenrollar(Hs.map(h => Math.atan2(h[1], h[0])));
    d.sel = Hs.map(cabs);
    d.g = w.map((_, i) => { const j = Math.min(Math.max(i, 1), w.length - 2); return -(f[j + 1] - f[j - 1]) / (w[j + 1] - w[j - 1]); });
    d.f = f; F.data = d;
    const [z, p, k] = T[clave[tipo.value]], a = fac[tipo.value];
    PZ.data = {px: p.map(v => a * v[0]), py: p.map(v => a * v[1])};
    ZZ.data = {zx: z.map(v => a * v[0]), zy: z.map(v => a * v[1])};
    ws.location = Ws.value;
    Pl.data = {left: [0.1, Ws.value], right: [1, 10], top: [-rp, 5], bottom: [-100, -rs]};
    const at = (c, x) => { const [z, p, k] = T[clave[c]]; return -db(cabs(zpk(z, p, k, [0, x / fac[c]])), -300); };
    // Orden mínimo para ωp = 1, Rp, ωs y Rs (fórmulas de buttord, cheb1ord, cheb2ord y ellipord)
    const K = m => { let x = 1, y = Math.sqrt(1 - m * m); for (let i = 0; i < 30; i++) [x, y] = [(x + y) / 2, Math.sqrt(x * y)]; return PI / (2 * x); };
    const D = (10 ** (rs / 10) - 1) / (10 ** (rp / 10) - 1), wsv = Ws.value, k1 = 1 / Math.sqrt(D), kk = 1 / wsv;
    const nmin = {"Butterworth": Math.log10(D) / (2 * Math.log10(wsv)), "Chebyshev I": Math.acosh(Math.sqrt(D)) / Math.acosh(wsv),
                  "Chebyshev II": Math.acosh(Math.sqrt(D)) / Math.acosh(wsv), "Elíptico": K(kk) * K(Math.sqrt(1 - k1 * k1)) / (K(k1) * K(Math.sqrt(1 - kk * kk)))};
    const cumple = c => at(c, 1) <= rp + 1e-6 && at(c, wsv) >= rs - 1e-6;
    info.text = `<p>Plantilla: ωp = 1, Rp = ${rp} dB, ωs = ${wsv.toFixed(2)}, Rs = ${rs} dB.</p><ul style="margin:0;padding-left:18px">` +
        ["Butterworth", "Chebyshev I", "Chebyshev II", "Elíptico"].map(c => `<li>${c}: N mínimo ${Math.ceil(nmin[c] - 1e-9)}; con N = ${n}, ` +
            `${at(c, wsv).toFixed(1)} dB en ωs${aj ? (cumple(c) ? " ✓" : " ✗") : ""}</li>`).join("") + "</ul>" +
        (aj ? "<p>Ajustados: Butterworth, Chebyshev I y elíptico dan −Rp en ωp = 1; Chebyshev II da −Rs en ωs. ✓ si cumple la plantilla.</p>"
            : "<p>Normalizados: Butterworth, ωc = 1 (−3 dB). Chebyshev I y elíptico: ωp = 1 (−Rp dB). Chebyshev II: ωs = 1 (−Rs dB).</p>") +
        `<p>${tipo.value}: ${p.length} polos${z.length ? " y " + z.length + " ceros en el eje imaginario" : ", sin ceros finitos"}.</p>`;
""", F=F, PZ=PZ, ZZ=ZZ, T=TABLA, tipo=tipo, N=N, Rp=Rp, Rs=Rs, Ws=Ws, ws=ws, info=info, Pl=Pl, ajuste=ajuste)
pb.conectar(cb, tipo, N, Rp, Rs, Ws, ajuste)

pb.pagina(__file__, "Aproximaciones de filtros analógicos", tema=4,
          descripcion="Con el mismo orden N, Butterworth es máximamente plano; Chebyshev I admite rizado en la banda "
                      "de paso y Chebyshev II en la de supresión a cambio de una transición más abrupta; el elíptico "
                      "tiene rizado en las dos y la transición más estrecha. Los polos de Butterworth están en una "
                      "circunferencia y los de Chebyshev en una elipse; los ceros, sobre el eje jω. La zona gris es la plantilla: "
                      "para cada aproximación se indica el orden mínimo que la cumple.",
          controles=[tipo, N, Rp, Rs, Ws, ajuste, info], graficas=[p1, [p2, p3, p4]], inicio=cb,
          referencia="Transparencias T4-02, filtros continuos · Apuntes del Tema 4, sección 2")
