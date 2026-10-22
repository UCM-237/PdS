"""T1 · Respuesta de un sistema LTI continuo a una sinusoide."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div, Span
import pds_bokeh as pb

SISTEMAS = ["Paso bajo de primer orden", "Paso alto de primer orden", "Segundo orden (ωn, ζ)"]

frec = ColumnDataSource(dict(w=[], m=[], f=[]))
tiempo = ColumnDataSource(dict(t=[], x=[], y=[]))

p1 = pb.figura("|H(jω)|", "ω (rad/s)", "|H|", ancho=300, alto=180, x_axis_type="log")
p1.line("w", "m", source=frec, color=pb.AZUL, line_width=2)
p2 = pb.figura("∠H(jω)", "ω (rad/s)", "fase (rad)", ancho=300, alto=180, x_axis_type="log", x_range=p1.x_range)
p2.line("w", "f", source=frec, color=pb.AZUL, line_width=2)
m1 = Span(location=1, dimension="height", line_color=pb.NARANJA, line_dash="dashed")
m2 = Span(location=1, dimension="height", line_color=pb.NARANJA, line_dash="dashed")
p1.add_layout(m1); p2.add_layout(m2)
p3 = pb.figura("Entrada x(t) = cos(ω₀t) y salida en régimen permanente", "t (s)", "", ancho=680, alto=200)
p3.line("t", "x", source=tiempo, color=pb.GRIS, line_width=1.5, legend_label="x(t)")
p3.line("t", "y", source=tiempo, color=pb.ROJO, line_width=2, legend_label="y(t) = |H| cos(ω₀t + ∠H)")
pb.leyenda(p3, "below")

sis = pb.selector("Sistema", SISTEMAS)
w0 = pb.deslizador("log₁₀ ω₀ (ω₀ en rad/s)", -1, 2, 0, 0.02)
wc = pb.deslizador("ωc o ωn (rad/s)", 0.5, 20, 2, 0.1)
z = pb.deslizador("ζ (solo segundo orden)", 0.05, 2, 0.3, 0.01)
info = Div(text="", width=240)

cb = pb.js("""
    function H(w) {   // devuelve [re, im]
        const c = wc.value, Z = z.value, s = sis.value;
        if (s.startsWith("Paso bajo")) { const d = 1 + (w / c) ** 2; return [1 / d, -(w / c) / d]; }
        if (s.startsWith("Paso alto")) { const d = 1 + (w / c) ** 2; return [(w / c) ** 2 / d, (w / c) / d]; }
        const a = c * c - w * w, b = 2 * Z * c * w, d = a * a + b * b; return [c * c * a / d, -c * c * b / d];
    }
    const lw = rango(-1, 2, 600), w = lw.map(v => Math.pow(10, v));
    const Hs = w.map(H), f = Hs.map(h => Math.atan2(h[1], h[0]));
    // Fase continua (sin saltos de 2π)
    for (let i = 1; i < f.length; i++) { while (f[i] - f[i - 1] > PI) f[i] -= 2 * PI; while (f[i] - f[i - 1] < -PI) f[i] += 2 * PI; }
    frec.data = {w: w, m: Hs.map(h => Math.hypot(h[0], h[1])), f: f};
    const W0 = Math.pow(10, w0.value), h0 = H(W0), A = Math.hypot(h0[0], h0[1]), ph = Math.atan2(h0[1], h0[0]);
    m1.location = W0; m2.location = W0;
    const t = rango(0, 4 * 2 * PI / W0, 800);
    tiempo.data = {t: t, x: t.map(u => Math.cos(W0 * u)), y: t.map(u => A * Math.cos(W0 * u + ph))};
    info.text = `<p>ω₀ = ${W0.toFixed(3)} rad/s</p><p>|H(jω₀)| = ${A.toFixed(3)} (${db(A).toFixed(1)} dB)<br>∠H(jω₀) = ${ph.toFixed(3)} rad</p>` +
                `<p>La salida es la misma sinusoide, escalada por ${A.toFixed(3)} y retrasada ${(-ph / W0).toFixed(3)} s.</p>`;
""", frec=frec, tiempo=tiempo, m1=m1, m2=m2, sis=sis, w0=w0, wc=wc, z=z, info=info)
pb.conectar(cb, sis, w0, wc, z)

pb.pagina(__file__, "Respuesta de un sistema LTI continuo", tema=1,
          descripcion="Las exponenciales complejas son autofunciones de los sistemas LTI: la entrada "
                      "cos(ω₀t) sale como |H(jω₀)| cos(ω₀t + ∠H(jω₀)). La respuesta en frecuencia "
                      "dice cuánto se escala y se desfasa cada frecuencia. Sistemas: 1/(1 + s/ωc), (s/ωc)/(1 + s/ωc) "
                      "y ωn²/(s² + 2ζωn s + ωn²).",
          controles=[sis, w0, wc, z, info], graficas=[[p1, p2], p3], inicio=cb,
          referencia="Transparencias T1-03, «Exponenciales complejas: autofunciones de los sistemas LTI» · Apuntes del Tema 1, sección 8")
