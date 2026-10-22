"""T2 · Espectro de una señal muestreada idealmente: réplicas y solapamiento."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import BoxAnnotation, ColumnDataSource, Div
import pds_bokeh as pb

tiempo = ColumnDataSource(dict(t=[], x=[]))
mues = ColumnDataSource(dict(t=[], x=[]))
frec = ColumnDataSource(dict(f=[], X=[], s=[]))
reps = ColumnDataSource(dict(xs=[], ys=[]))

p1 = pb.figura("x(t) = sinc²(Bt) y sus muestras", "t (s)", "", ancho=680, alto=190)
p1.line("t", "x", source=tiempo, color=pb.AZUL, line_width=1.5)
pb.tallos(p1, "t", "x", mues, color=pb.NARANJA)
p2 = pb.figura("Espectro: X(f) (azul), réplicas X(f − k fs) (gris) y su suma fs·Σ (rojo)", "f (Hz)",
               "Ts · Xs(f)", ancho=680, alto=230, x_range=(-12, 12))
banda = BoxAnnotation(left=-2, right=2, fill_color=pb.VERDE, fill_alpha=0.08)
p2.add_layout(banda)
p2.multi_line("xs", "ys", source=reps, color=pb.GRIS_CLARO, line_width=1.5)
p2.line("f", "s", source=frec, color=pb.ROJO, line_width=2.5, legend_label="espectro de la señal muestreada")
p2.line("f", "X", source=frec, color=pb.AZUL, line_width=1.5, line_dash="dashed", legend_label="X(f)")
pb.leyenda(p2, "below")

B = pb.deslizador("B: ancho de banda de x(t) (Hz)", 0.5, 4, 2, 0.1)
fs = pb.deslizador("fs (muestras/s)", 1, 12, 6, 0.1)
info = Div(text="", width=240)

cb = pb.js("""
    const b = B.value, Fs = fs.value;
    const X = f => Math.abs(f) < b ? (1 - Math.abs(f) / b) / b : 0;    // CTFT de sinc²(Bt)
    const f = rango(-12, 12, 2401), xs = [], ys = [];
    for (let k = -8; k <= 8; k++) if (k) { const g = rango(k * Fs - b, k * Fs + b, 41); xs.push(g); ys.push(g.map(v => X(v - k * Fs))); }
    let s = f.map(v => { let a = 0; for (let k = -12; k <= 12; k++) a += X(v - k * Fs); return a; });
    frec.data = {f: f, X: f.map(X), s: s}; reps.data = {xs: xs, ys: ys};
    banda.left = -Fs / 2; banda.right = Fs / 2;
    const t = rango(-3, 3, 1201), n = enteros(Math.ceil(-3 * Fs), Math.floor(3 * Fs));
    tiempo.data = {t: t, x: t.map(u => sinc(b * u) ** 2)};
    mues.data = {t: n.map(k => k / Fs), x: n.map(k => sinc(b * k / Fs) ** 2)};
    info.text = `<p>Nyquist: fs ≥ 2B = ${(2 * b).toFixed(1)} muestras/s</p>` + (Fs < 2 * b
        ? `<p style="color:#C0392B">fs < 2B: las réplicas se solapan en |f| > ${(Fs - b).toFixed(2)} Hz y X(f) no se puede recuperar con un paso bajo.</p>`
        : `<p>Sin solapamiento: un paso bajo ideal de corte entre B y fs − B = ${(Fs - b).toFixed(2)} Hz recupera x(t).</p>`);
""", tiempo=tiempo, mues=mues, frec=frec, reps=reps, banda=banda, B=B, fs=fs, info=info)
pb.conectar(cb, B, fs)

pb.pagina(__file__, "Espectro de una señal muestreada", tema=2,
          descripcion="Muestrear con un tren de impulsos multiplica en el tiempo y convoluciona en "
                      "frecuencia: el espectro de la señal muestreada es la suma de copias de X(f) "
                      "desplazadas k fs. Si fs < 2B las copias se solapan (aliasing).",
          controles=[B, fs, info], graficas=[p1, p2], inicio=cb,
          referencia="Transparencias T2-01, «Espectro de la señal muestreada» · Apuntes del Tema 2, sección 3")
