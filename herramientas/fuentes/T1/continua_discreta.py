"""T1 · Exponencial continua frente a discreta: muestrear cos(2πft)."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

cont = ColumnDataSource(dict(t=[], x=[], a=[]))
mues = ColumnDataSource(dict(t=[], x=[]))

p = pb.figura("x(t) = cos(2πft + θ) y sus muestras x[n] = x(nTs)", "t (s)", "x", ancho=640)
p.line("t", "x", source=cont, color=pb.AZUL, line_width=1.5, legend_label="x(t)")
p.line("t", "a", source=cont, color=pb.ROJO, line_dash="dashed", legend_label="sinusoide de frecuencia principal")
pb.tallos(p, "t", "x", mues, color=pb.NARANJA, legend_label="x[n]")
pb.leyenda(p, "below"); p.y_range.start = -1.3; p.y_range.end = 1.3

f = pb.deslizador("f (Hz)", 0, 30, 3, 0.1)
fs = pb.deslizador("fs (muestras/s)", 2, 40, 10, 0.5)
th = pb.deslizador("θ (rad)", -3.14, 3.14, 0, 0.05)
info = Div(text="", width=240)

cb = pb.js("""
    const F = f.value, Fs = fs.value, T = th.value, t = rango(0, 2, 2001);
    const W = 2 * PI * F / Fs;                       // Ω = ωTs
    const Wp = mod(W + PI, 2 * PI) - PI;            // valor principal en (−π, π]
    const fa = Math.abs(Wp) * Fs / (2 * PI), sg = Wp < 0 ? -1 : 1;
    cont.data = {t: t, x: t.map(u => Math.cos(2 * PI * F * u + T)),
                 a: t.map(u => Math.cos(2 * PI * fa * u + sg * T))};
    const n = enteros(0, Math.floor(2 * Fs));
    mues.data = {t: n.map(k => k / Fs), x: n.map(k => Math.cos(W * k + T))};
    info.text = `<p>Ω = 2πf/fs = ${W.toFixed(3)} rad/muestra</p>` +
                `<p>Valor principal: ${Wp.toFixed(3)} rad/muestra, que corresponde a ${fa.toFixed(2)} Hz.</p>` +
                (F > Fs / 2 ? `<p style="color:#C0392B">f > fs/2: las muestras son las de una sinusoide de ${fa.toFixed(2)} Hz.</p>` : "");
""", cont=cont, mues=mues, f=f, fs=fs, th=th, info=info)
pb.conectar(cb, f, fs, th)

pb.pagina(__file__, "Exponencial continua frente a discreta", tema=1,
          descripcion="Al muestrear cos(2πft) cada Ts = 1/fs se obtiene cos(Ωn) con Ω = 2πf/fs. "
                      "Como Ω y Ω + 2π dan las mismas muestras, frecuencias continuas separadas un "
                      "múltiplo de fs son indistinguibles: es el origen del aliasing del Tema 2.",
          controles=[f, fs, th, info], graficas=[p], inicio=cb,
          referencia="Transparencias T1-01, «frecuencias equivalentes» · Apuntes del Tema 1, sección 3 · Tema 2")
