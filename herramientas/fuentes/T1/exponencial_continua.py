"""T1 · Parte real de una exponencial compleja continua."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
import numpy as np
from bokeh.models import ColumnDataSource, CustomJS
import pds_bokeh as pb

t = np.linspace(0, 5, 500)
r, f, th = 0.3, 1.0, 0.0
env = np.exp(r * t)
datos = ColumnDataSource(dict(t=t, x=env * np.cos(2 * np.pi * f * t + th), sup=env, inf=-env))

p = pb.figura("x(t) = Re{C·exp(st)} = exp(σt)·cos(2πft + θ)", "t (s)", "x(t)")
p.line("t", "sup", source=datos, color=pb.GRIS_CLARO, line_dash="dashed", legend_label="±exp(σt)")
p.line("t", "inf", source=datos, color=pb.GRIS_CLARO, line_dash="dashed")
p.line("t", "x", source=datos, color=pb.AZUL, line_width=2, legend_label="x(t)")
pb.leyenda(p, "below")

sigma = pb.deslizador("σ (1/s)", -1, 1, r, 0.05)
frec = pb.deslizador("f (Hz)", 0, 4, f, 0.1)
fase = pb.deslizador("θ (rad)", -np.pi, np.pi, th, 0.05)

cb = CustomJS(args=dict(d=datos, s=sigma, f=frec, th=fase), code="""
    const t = d.data.t, x = [], sup = [], inf = [];
    for (let i = 0; i < t.length; i++) {
        const e = Math.exp(s.value * t[i]);
        x.push(e * Math.cos(2 * Math.PI * f.value * t[i] + th.value));
        sup.push(e); inf.push(-e);
    }
    d.data = {t: t, x: x, sup: sup, inf: inf};
""")
for c in (sigma, frec, fase):
    c.js_on_change("value", cb)

pb.pagina(__file__, "Exponencial compleja continua", tema=1,
          descripcion="Con s = σ + jω y C = e<sup>jθ</sup>, la parte real de C e<sup>st</sup> "
                      "es una sinusoide de frecuencia f = ω/2π cuya envolvente e<sup>σt</sup> "
                      "crece si σ &gt; 0, decrece si σ &lt; 0 y es constante si σ = 0.",
          controles=[sigma, frec, fase], graficas=[p],
          referencia="Transparencias T1-01, «Exponencial compleja continua» · Apuntes del Tema 1, sección 3")
