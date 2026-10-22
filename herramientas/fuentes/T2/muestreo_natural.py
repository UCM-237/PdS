"""T2 · Muestreo no ideal: natural y de techo plano."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

tiempo = ColumnDataSource(dict(t=[], x=[], m=[]))
frec = ColumnDataSource(dict(f=[], s=[], env=[]))

p1 = pb.figura("x(t) y señal muestreada con pulsos de anchura τ", "t (s)", "", ancho=680, alto=200)
p1.line("t", "x", source=tiempo, color=pb.GRIS_CLARO, line_width=1.5, legend_label="x(t)")
p1.line("t", "m", source=tiempo, color=pb.AZUL, line_width=1.5, legend_label="muestreada")
pb.leyenda(p1, "right")
p2 = pb.figura("Módulo del espectro de la señal muestreada (×Ts)", "f (Hz)", "", ancho=680, alto=220, x_range=(-25, 25))
p2.line("f", "env", source=frec, color=pb.NARANJA, line_dash="dashed", legend_label="peso de las réplicas")
p2.line("f", "s", source=frec, color=pb.ROJO, line_width=2, legend_label="espectro")
pb.leyenda(p2, "right")

tipo = pb.botones(["Natural", "Techo plano"])
fs = pb.deslizador("fs (muestras/s)", 2, 12, 6, 0.1)
d = pb.deslizador("τ/Ts (ciclo de trabajo)", 0.05, 1, 0.3, 0.01)
info = Div(text="", width=240)

cb = pb.js("""
    const b = 2, Fs = fs.value, Ts = 1 / Fs, D = d.value, tau = D * Ts, plano = tipo.active === 1;
    const X = f => Math.abs(f) < b ? (1 - Math.abs(f) / b) / b : 0;
    const x = u => sinc(b * u) ** 2;
    const t = rango(-2, 2, 4001);
    const m = t.map(u => { const k = Math.round(u / Ts), r = u - k * Ts;     // pulso centrado en kTs
        return Math.abs(r) <= tau / 2 ? (plano ? x(k * Ts) : x(u)) : 0; });
    tiempo.data = {t: t, x: t.map(x), m: m};
    const f = rango(-25, 25, 2501);
    // Natural: Σ d sinc(k d) X(f − k fs).  Techo plano: d sinc(f τ) Σ X(f − k fs).
    const s = f.map(v => { let a = 0; for (let k = -20; k <= 20; k++) a += (plano ? 1 : sinc(k * D)) * X(v - k * Fs);
                           return Math.abs(D * (plano ? sinc(v * tau) : 1) * a); });
    const env = f.map(v => plano ? D * Math.abs(sinc(v * tau)) / b : D * Math.abs(sinc(v / Fs * D)) / b);
    frec.data = {f: f, s: s, env: env};
    info.text = plano
        ? `<p>Techo plano: todas las réplicas quedan multiplicadas por sinc(fτ). Distorsiona incluso la banda base (en f = B = 2 Hz, ${(sinc(2 * tau) * 100).toFixed(1)} %): hay que compensarla.</p>`
        : `<p>Natural: cada réplica k se escala por d·sinc(kd), pero conserva su forma; la banda base no se distorsiona.</p>`;
""", tiempo=tiempo, frec=frec, tipo=tipo, fs=fs, d=d, info=info)
pb.conectar(cb, tipo, fs, d)

pb.pagina(__file__, "Muestreo natural y de techo plano", tema=2,
          descripcion="Un muestreador real toma pulsos de anchura τ, no impulsos. En el muestreo natural "
                      "el pulso sigue a la señal; en el de techo plano mantiene el valor de la muestra. "
                      "x(t) = sinc²(2t), de ancho de banda B = 2 Hz.",
          controles=[tipo, fs, d, info], graficas=[p1, p2], inicio=cb,
          referencia="Transparencias T2-01, «Muestreo no ideal» · Apuntes del Tema 2, sección 3")
