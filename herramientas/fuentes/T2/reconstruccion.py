"""T2 · Reconstrucción a partir de las muestras: ideal, ZOH y FOH."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

METODOS = ["Ideal (interpolación con sinc)", "ZOH (retenedor de orden cero)", "FOH no causal (interpolación lineal)",
           "FOH predictivo (causal)"]

datos = ColumnDataSource(dict(t=[], x=[], r=[], e=[]))
mues = ColumnDataSource(dict(t=[], x=[]))

p1 = pb.figura("x(t) = sin(2πt) + 0,5 sin(2π·3t) + 0,25 sin(2π·6t) y su reconstrucción", "t (s)", "", ancho=680, alto=230)
p1.line("t", "x", source=datos, color=pb.GRIS, line_width=1.5, legend_label="x(t)")
p1.line("t", "r", source=datos, color=pb.ROJO, line_width=2, legend_label="reconstruida")
pb.tallos(p1, "t", "x", mues, color=pb.AZUL, legend_label="muestras")
pb.leyenda(p1, "below")
p2 = pb.figura("Error de reconstrucción", "t (s)", "x(t) − x̂(t)", ancho=680, alto=150, x_range=p1.x_range)
p2.line("t", "e", source=datos, color=pb.NARANJA, line_width=1.5)

met = pb.selector("Método", METODOS)
fs = pb.deslizador("fs (muestras/s)", 4, 60, 20, 0.5)
info = Div(text="", width=240)

cb = pb.js("""
    const Fs = fs.value, Ts = 1 / Fs, m = met.value;
    const x = u => Math.sin(2 * PI * u) + 0.5 * Math.sin(6 * PI * u) + 0.25 * Math.sin(12 * PI * u);
    const n = enteros(-Math.ceil(3 * Fs), Math.ceil(5 * Fs)), xn = n.map(k => x(k * Ts));
    const i0 = n.indexOf(0);
    const t = rango(0, 2, 2001);
    const r = t.map(u => {
        const k = Math.floor(u / Ts + 1e-9), j = i0 + k, a = u / Ts - k;
        if (m.startsWith("Ideal")) { let s = 0; for (let q = 0; q < n.length; q++) s += xn[q] * sinc(u / Ts - n[q]); return s; }
        if (m.startsWith("ZOH")) return xn[j];
        if (m.startsWith("FOH no")) return xn[j] + a * (xn[j + 1] - xn[j]);
        return xn[j] + a * (xn[j] - xn[j - 1]);   // prolonga la recta de las dos últimas muestras
    });
    const xs = t.map(x), e = xs.map((v, i) => v - r[i]);
    datos.data = {t: t, x: xs, r: r, e: e};
    const sel = n.map((k, q) => [k * Ts, xn[q]]).filter(a => a[0] >= 0 && a[0] <= 2);
    mues.data = {t: sel.map(a => a[0]), x: sel.map(a => a[1])};
    const rms = Math.sqrt(e.reduce((s, v) => s + v * v, 0) / e.length), mx = Math.max(...e.map(Math.abs));
    info.text = `<p>fs = ${Fs} muestras/s; la componente más alta es de 6 Hz, así que Nyquist pide fs > 12.</p>` +
                `<p>Error eficaz: ${rms.toFixed(4)}<br>Error máximo: ${mx.toFixed(4)}</p>` +
                (m.startsWith("ZOH") ? "<p>El ZOH retrasa la señal media muestra (Ts/2) y deja escalones.</p>" : "") +
                (m.startsWith("Ideal") && Fs <= 12 ? '<p style="color:#C0392B">Con fs ≤ 12 hay aliasing: ni la reconstrucción ideal recupera x(t).</p>' : "");
""", datos=datos, mues=mues, met=met, fs=fs, info=info)
pb.conectar(cb, met, fs)

pb.pagina(__file__, "Reconstrucción", tema=2,
          descripcion="La reconstrucción ideal suma un sinc por muestra y recupera x(t) exactamente si se "
                      "cumple Nyquist, pero no es realizable. Los retenedores unen las muestras con "
                      "escalones (ZOH) o rectas (FOH): son causales o casi, a cambio de un error que "
                      "disminuye al aumentar fs.",
          controles=[met, fs, info], graficas=[p1, p2], inicio=cb,
          referencia="Transparencias T2-02, «Retenedores sobre una misma señal» · Apuntes del Tema 2, sección 4")
