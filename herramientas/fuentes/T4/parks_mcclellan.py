"""T4 · Diseño equirrizado (Parks–McClellan) frente a diseño por ventanas."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
import numpy as np
from bokeh.models import BoxAnnotation, ColumnDataSource, Div
from scipy import signal
import pds_bokeh as pb

# Diseños de Parks–McClellan calculados con SciPy (remez) para una rejilla de longitudes,
# bordes de banda (en Ω/π) y pesos de la banda eliminada frente a la de paso.
LONG = [11, 15, 21, 25, 31, 41, 51]
OP = [0.2, 0.25, 0.3, 0.35, 0.4]
DT = [0.05, 0.1, 0.15, 0.2]
PESO = [1, 5, 10]
TABLA = {f"{M}-{p:.2f}-{d:.2f}-{w}": [round(float(v), 7) for v in
         signal.remez(M, [0, p / 2, (p + d) / 2, 0.5], [1, 0], weight=[1, w], fs=1)]
         for M in LONG for p in OP for d in DT for w in PESO}

F = ColumnDataSource(dict(W=[], pm=[], ve=[]))
FL = ColumnDataSource(dict(W=[], pm=[], ve=[]))
Hn = ColumnDataSource(dict(n=[], pm=[], ve=[]))

p1 = pb.figura("|H(e^jΩ)| (dB) con la misma longitud y los mismos bordes", "Ω/π", "dB", ancho=560, alto=280,
               x_range=(0, 1), y_range=(-100, 5))
paso = BoxAnnotation(left=0, right=0.3, fill_color=pb.VERDE, fill_alpha=0.10)
elim = BoxAnnotation(left=0.4, right=1, fill_color=pb.ROJO, fill_alpha=0.07)
p1.add_layout(paso); p1.add_layout(elim)
p1.line("W", "ve", source=F, color=pb.GRIS, line_width=2, legend_label="ventana")
p1.line("W", "pm", source=F, color=pb.AZUL, line_width=2, legend_label="Parks–McClellan")
pb.leyenda(p1, "below")
p2 = pb.figura("Detalle de la banda de paso (lineal)", "Ω/π", "", ancho=250, alto=280, x_range=(0, 0.45))
p2.line("W", "ve", source=FL, color=pb.GRIS, line_width=2)
p2.line("W", "pm", source=FL, color=pb.AZUL, line_width=2)
p3 = pb.figura("Respuestas al impulso", "n", "", ancho=820, alto=170)
p3.scatter("n", "ve", source=Hn, marker="square", size=8, line_color=pb.GRIS, fill_color=None, legend_label="ventana")
pb.tallos(p3, "n", "pm", Hn, color=pb.AZUL, legend_label="Parks–McClellan")
pb.leyenda(p3, "right")

M = pb.selector("Longitud M", [str(v) for v in LONG], valor="31")
Wp = pb.deslizador("Borde de la banda de paso Ωp/π", 0.2, 0.4, 0.3, 0.05)
Dt = pb.deslizador("Anchura de la transición (Ωs − Ωp)/π", 0.05, 0.2, 0.1, 0.05)
peso = pb.selector("Peso de la banda eliminada", ["1", "5", "10"])
vent = pb.selector("Ventana para comparar", ["Hamming", "Hann", "Blackman", "Rectangular"])
info = Div(text="", width=240)

cb = pb.js("""
    const m = Number(M.value), p = Math.round(Wp.value * 20) / 20, d = Math.round(Dt.value * 20) / 20;
    const h = T[`${m}-${p.toFixed(2)}-${d.toFixed(2)}-${peso.value}`];
    // Ventana: sinc ideal con corte en el centro de la transición, por la ventana elegida
    const c = (p + d / 2) * PI, D = (m - 1) / 2, w = ventana(vent.value, m);
    const hv = enteros(0, m - 1).map(n => c / PI * sinc(c / PI * (n - D)) * w[n]);
    const W = rango(0, 1, 1000), resp = b => W.map(x => cabs(b.reduce((s, v, n) => csum(s, cesc(v, cexp([0, -PI * x * n]))), [0, 0])));
    const Hp = resp(h), Hv = resp(hv);
    F.data = {W: W, pm: Hp.map(v => db(v, -120)), ve: Hv.map(v => db(v, -120))};
    FL.data = {W: W, pm: Hp, ve: Hv};
    Hn.data = {n: enteros(0, m - 1), pm: h, ve: hv};
    paso.right = p; elim.left = p + d;
    // Rizados medidos: desviación máxima de 1 en [0, Ωp] y máximo en [Ωs, π]
    const med = H => { let dp = 0, ds = 0; W.forEach((x, i) => { if (x <= p) dp = Math.max(dp, Math.abs(H[i] - 1)); if (x >= p + d) ds = Math.max(ds, H[i]); }); return [dp, ds]; };
    const [dpP, dsP] = med(Hp), [dpV, dsV] = med(Hv);
    const fila = (n, dp, ds) => `<li>${n}: δp = ${dp.toFixed(4)} (${(20 * Math.log10(1 + dp)).toFixed(2)} dB), δs = ${ds.toExponential(2)} (${db(ds).toFixed(1)} dB)</li>`;
    info.text = `<ul style="margin:0;padding-left:18px">${fila("Parks–McClellan", dpP, dsP)}${fila(vent.value, dpV, dsV)}</ul>` +
        `<p>Parks–McClellan: δp/δs = ${(dpP / dsP).toFixed(2)} (el peso pide ${peso.value}).</p>` +
        `<p>La ventana de ${vent.value} necesita una transición de unos ${({"Rectangular": 1.8, "Hann": 6.2, "Hamming": 6.6, "Blackman": 11})[vent.value]}π/M = ` +
        `${(({"Rectangular": 1.8, "Hann": 6.2, "Hamming": 6.6, "Blackman": 11})[vent.value] / m).toFixed(3)}π; aquí es de ${d.toFixed(2)}π.</p>` +
        "<p>El diseño equirrizado reparte el error por igual en cada banda y minimiza el máximo; con la ventana, " +
        "el error es mayor cerca de la transición y la atenuación la fija el tipo de ventana, no M.</p>";
""", F=F, Hn=Hn, T=TABLA, M=M, Wp=Wp, Dt=Dt, peso=peso, vent=vent, info=info, paso=paso, elim=elim, FL=FL)
pb.conectar(cb, M, Wp, Dt, peso, vent)

pb.pagina(__file__, "Parks–McClellan frente a ventanas", tema=4,
          descripcion="El algoritmo de Parks–McClellan busca el FIR de fase lineal de longitud M cuyo error máximo, ponderado, en "
                      "las bandas de paso y eliminada es el menor posible: el resultado tiene rizado constante (equirrizado). Se "
                      "compara con el diseño por ventanas de la misma longitud. Los diseños equirrizados se calculan con SciPy al "
                      "generar la página.",
          controles=[M, Wp, Dt, peso, vent, info], graficas=[[p1, p2], p3], inicio=cb,
          referencia="Transparencias T4-04, diseño de filtros FIR · Apuntes del Tema 4, sección 4")
