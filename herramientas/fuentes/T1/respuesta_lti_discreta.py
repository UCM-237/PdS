"""T1 · Respuesta de un sistema LTI discreto a una sinusoide."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div, Span
import pds_bokeh as pb

SISTEMAS = ["Media móvil de L muestras", "Primer orden (a)", "Diferencia"]

frec = ColumnDataSource(dict(W=[], m=[], f=[]))
ent = ColumnDataSource(dict(n=[], x=[], y=[]))

p1 = pb.figura("|H(e^jΩ)|", "Ω (rad/muestra)", "|H|", ancho=300, alto=180, x_range=(0, 3.1416))
p1.line("W", "m", source=frec, color=pb.AZUL, line_width=2)
p2 = pb.figura("∠H(e^jΩ)", "Ω (rad/muestra)", "fase (rad)", ancho=300, alto=180, x_range=p1.x_range)
p2.line("W", "f", source=frec, color=pb.AZUL, line_width=2)
m1 = Span(location=0.5, dimension="height", line_color=pb.NARANJA, line_dash="dashed")
m2 = Span(location=0.5, dimension="height", line_color=pb.NARANJA, line_dash="dashed")
p1.add_layout(m1); p2.add_layout(m2)
p3 = pb.figura("x[n] = cos(Ω₀n) y salida y[n]", "n", "", ancho=680, alto=200)
pb.tallos(p3, "n", "x", ent, color=pb.GRIS_CLARO, legend_label="x[n]")
pb.tallos(p3, "n", "y", ent, color=pb.ROJO, legend_label="y[n]")
pb.leyenda(p3, "below")

sis = pb.selector("Sistema", SISTEMAS)
W0 = pb.deslizador("Ω₀ (rad/muestra)", 0, 3.14, 0.5, 0.01)
L = pb.deslizador("L (media móvil)", 2, 16, 4, 1)
a = pb.deslizador("a (primer orden)", -0.95, 0.95, 0.8, 0.01)
info = Div(text="", width=240)

cb = pb.js("""
    function H(W) {
        const s = sis.value;
        if (s.startsWith("Media")) { let r = 0, i = 0; for (let k = 0; k < L.value; k++) { r += Math.cos(W * k); i -= Math.sin(W * k); } return [r / L.value, i / L.value]; }
        if (s.startsWith("Primer")) { const A = a.value, dr = 1 - A * Math.cos(W), di = A * Math.sin(W), d = dr * dr + di * di; return [(1 - A) * dr / d, -(1 - A) * di / d]; }
        return [1 - Math.cos(W), Math.sin(W)];
    }
    const Ws = rango(0, PI, 600), Hs = Ws.map(H);
    frec.data = {W: Ws, m: Hs.map(h => Math.hypot(h[0], h[1])), f: Hs.map(h => Math.atan2(h[1], h[0]))};
    const w = W0.value, h0 = H(w), A = Math.hypot(h0[0], h0[1]), ph = Math.atan2(h0[1], h0[0]);
    m1.location = w; m2.location = w;
    // Salida calculada con la ecuación en diferencias desde n = 0 (incluye el transitorio)
    const n = enteros(0, 40), x = n.map(k => Math.cos(w * k)), y = [];
    for (let k = 0; k < n.length; k++) {
        if (sis.value.startsWith("Media")) { let s = 0; for (let j = 0; j < L.value; j++) s += k - j >= 0 ? x[k - j] : 0; y.push(s / L.value); }
        else if (sis.value.startsWith("Primer")) y.push(a.value * (k ? y[k - 1] : 0) + (1 - a.value) * x[k]);
        else y.push(x[k] - (k ? x[k - 1] : 0));
    }
    ent.data = {n: n, x: x, y: y};
    info.text = `<p>|H(e<sup>jΩ₀</sup>)| = ${A.toFixed(3)} (${db(A).toFixed(1)} dB)<br>∠H = ${ph.toFixed(3)} rad</p>` +
                `<p>Pasado el transitorio, y[n] = ${A.toFixed(3)} cos(Ω₀n ${ph < 0 ? "−" : "+"} ${Math.abs(ph).toFixed(3)}).</p>`;
""", frec=frec, ent=ent, m1=m1, m2=m2, sis=sis, W0=W0, L=L, a=a, info=info)
pb.conectar(cb, sis, W0, L, a)

pb.pagina(__file__, "Respuesta de un sistema LTI discreto", tema=1,
          descripcion="En tiempo discreto, cos(Ω₀n) sale como |H(e<sup>jΩ₀</sup>)| cos(Ω₀n + ∠H) una vez "
                      "pasado el transitorio. La respuesta en frecuencia es periódica de periodo 2π y, "
                      "para un sistema real, basta verla en [0, π]. Sistemas: media móvil, y[n] = a y[n−1] + (1 − a) x[n] "
                      "e y[n] = x[n] − x[n−1].",
          controles=[sis, W0, L, a, info], graficas=[[p1, p2], p3], inicio=cb,
          referencia="Transparencias T1-03, «Exponenciales complejas: autofunciones de los sistemas LTI» · Apuntes del Tema 1, sección 8")
