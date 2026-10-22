"""T2 · Aliasing de sinusoides: en el tiempo y en el espectro."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import BoxAnnotation, ColumnDataSource, Div
import pds_bokeh as pb

cont = ColumnDataSource(dict(t=[], x=[], r=[]))
mues = ColumnDataSource(dict(t=[], x=[]))
esp = ColumnDataSource(dict(f=[], a=[], c=[]))
rep = ColumnDataSource(dict(f=[], a=[]))

p1 = pb.figura("x(t), muestras y reconstrucción ideal con banda [−fs/2, fs/2]", "t (s)", "", ancho=680, alto=210)
p1.line("t", "x", source=cont, color=pb.GRIS, line_width=1.5, legend_label="x(t)")
p1.line("t", "r", source=cont, color=pb.ROJO, line_width=2, line_dash="dashed", legend_label="reconstruida")
pb.tallos(p1, "t", "x", mues, color=pb.NARANJA, legend_label="x(nTs)")
pb.leyenda(p1, "right")
p2 = pb.figura("Espectro de x(t) (azul) y de la señal muestreada (réplicas cada fs, gris)", "f (Hz)", "amplitud",
               ancho=680, alto=190, x_range=(-30, 30))
banda = BoxAnnotation(left=-5, right=5, fill_color=pb.VERDE, fill_alpha=0.08)
p2.add_layout(banda)
p2.segment(x0="f", y0=0, x1="f", y1="a", source=rep, color=pb.GRIS_CLARO, line_width=2)
p2.segment(x0="f", y0=0, x1="f", y1="a", source=esp, color="c", line_width=3)

fs = pb.deslizador("fs (muestras/s)", 2, 30, 10, 0.5)
f1 = pb.deslizador("f₁ (Hz)", 0, 25, 1, 0.1)
f2 = pb.deslizador("f₂ (Hz)", 0, 25, 3, 0.1)
f3 = pb.deslizador("f₃ (Hz)", 0, 25, 7, 0.1)
info = Div(text="", width=240)

cb = pb.js("""
    const Fs = fs.value, F = [f1.value, f2.value, f3.value], A = [1, 0.6, 0.4];
    const col = ["#2B3A8C", "#1E7B4F", "#D9822B"];
    function alias(f) { return Math.abs(mod(f + Fs / 2, Fs) - Fs / 2); }
    const t = rango(0, 2, 2001), n = enteros(0, Math.floor(2 * Fs));
    const x = u => F.reduce((s, f, i) => s + A[i] * Math.cos(2 * PI * f * u), 0);
    cont.data = {t: t, x: t.map(x), r: t.map(u => F.reduce((s, f, i) => s + A[i] * Math.cos(2 * PI * alias(f) * u), 0))};
    mues.data = {t: n.map(k => k / Fs), x: n.map(k => x(k / Fs))};
    const ef = [], ea = [], ec = [], rf = [], ra = [];
    F.forEach((f, i) => { for (const s of [-1, 1]) { ef.push(s * f); ea.push(A[i] / 2); ec.push(col[i]);
        for (let k = -4; k <= 4; k++) if (k) { rf.push(s * f + k * Fs); ra.push(A[i] / 2); } } });
    esp.data = {f: ef, a: ea, c: ec}; rep.data = {f: rf, a: ra};
    banda.left = -Fs / 2; banda.right = Fs / 2;
    info.text = "<p>Banda de Nyquist: |f| < fs/2 = " + (Fs / 2).toFixed(2) + " Hz</p>" +
        F.map((f, i) => `<p style="color:${col[i]}">f${i + 1} = ${f.toFixed(1)} Hz → ` +
            (f > Fs / 2 ? `alias en ${alias(f).toFixed(2)} Hz` : "sin aliasing") + "</p>").join("");
""", cont=cont, mues=mues, esp=esp, rep=rep, banda=banda, fs=fs, f1=f1, f2=f2, f3=f3, info=info)
pb.conectar(cb, fs, f1, f2, f3)

pb.pagina(__file__, "Aliasing", tema=2,
          descripcion="Al muestrear, el espectro se repite cada fs. Una sinusoide de frecuencia mayor que "
                      "fs/2 tiene una réplica dentro de la banda [−fs/2, fs/2] y, al reconstruir, aparece "
                      "en su frecuencia alias |f − k fs|. Las tres sinusoides tienen amplitudes 1; 0,6 y 0,4.",
          controles=[fs, f1, f2, f3, info], graficas=[p1, p2], inicio=cb,
          referencia="Transparencias T2-01, «Aliasing en sinusoides» · Apuntes del Tema 2, sección 2")
