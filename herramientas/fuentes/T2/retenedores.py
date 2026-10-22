"""T2 · Respuesta al impulso y en frecuencia de los retenedores."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

h = ColumnDataSource(dict(t=[], ideal=[], zoh=[], foh=[], pred=[]))
H = ColumnDataSource(dict(f=[], ideal=[], zoh=[], foh=[], pred=[]))

p1 = pb.figura("Respuesta al impulso h(t)/Ts", "t / Ts", "", ancho=380, alto=230, x_range=(-4, 4))
p2 = pb.figura("|H(f)| / Ts", "f / fs", "", ancho=380, alto=230, x_range=(0, 3))
for col, c, nombre in (("ideal", pb.GRIS, "ideal"), ("zoh", pb.AZUL, "ZOH"),
                       ("foh", pb.VERDE, "FOH no causal"), ("pred", pb.NARANJA, "FOH predictivo")):
    p1.line("t", col, source=h, color=c, line_width=2, legend_label=nombre)
    p2.line("f", col, source=H, color=c, line_width=2, legend_label=nombre)
pb.leyenda(p1, "below"); pb.leyenda(p2, "below")

escala = pb.botones(["Lineal", "dB"])
info = Div(text="<p>Las réplicas de la señal muestreada están en f = fs, 2fs…: un buen retenedor "
                "tiene |H| grande en [0, fs/2] y pequeño a partir de ahí.</p>"
                "<p>ZOH: |H| = Ts|sinc(f/fs)|, vale 0,64 (−3,9 dB) en fs/2 y retrasa Ts/2.</p>"
                "<p>FOH no causal: Ts sinc²(f/fs), atenúa más las réplicas.</p>"
                "<p>FOH predictivo: |1 + j2πf Ts| sinc²(f/fs); es causal pero realza las altas frecuencias.</p>",
           width=240)

cb = pb.js("""
    const t = rango(-4, 4, 1601), f = rango(0, 3, 1201), dB = escala.active === 1;
    const g = v => dB ? db(v, -60) : v;
    h.data = {t: t, ideal: t.map(u => sinc(u)), zoh: t.map(u => (u >= 0 && u < 1) ? 1 : 0),
              foh: t.map(u => Math.abs(u) < 1 ? 1 - Math.abs(u) : 0),
              pred: t.map(u => (u >= 0 && u < 1) ? 1 + u : ((u >= 1 && u < 2) ? 1 - u : 0))};
    H.data = {f: f, ideal: f.map(v => g(v < 0.5 ? 1 : (v === 0.5 ? 0.5 : 0))), zoh: f.map(v => g(Math.abs(sinc(v)))),
              foh: f.map(v => g(sinc(v) ** 2)), pred: f.map(v => g(Math.hypot(1, 2 * PI * v) * sinc(v) ** 2))};
""", h=h, H=H, escala=escala)
pb.conectar(cb, escala)

pb.pagina(__file__, "Retenedores", tema=2,
          descripcion="Un retenedor es un filtro de reconstrucción realizable. Su respuesta en frecuencia "
                      "dice cuánto deforma la banda base y cuánto deja pasar de las réplicas.",
          controles=[escala, info], graficas=[[p1, p2]], inicio=cb,
          referencia="Transparencias T2-02, «Comparación de los retenedores» · Apuntes del Tema 2, sección 4")
