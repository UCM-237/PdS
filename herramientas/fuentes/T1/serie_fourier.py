"""T1 · Serie de Fourier: suma parcial, coeficientes y fenómeno de Gibbs."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

SENALES = ["Tren de pulsos", "Cuadrada (simétrica)", "Triangular", "Diente de sierra", "Seno rectificado"]

tiempo = ColumnDataSource(dict(t=[], x=[], s=[]))
coef = ColumnDataSource(dict(k=[], c=[], usado=[]))
usados = ColumnDataSource(dict(k=[], c=[]))

p1 = pb.figura("x(t) y suma parcial con |k| ≤ K", "t (periodos)", "", ancho=620, alto=230)
p1.line("t", "x", source=tiempo, color=pb.GRIS, line_width=1.5, legend_label="x(t)")
p1.line("t", "s", source=tiempo, color=pb.AZUL, line_width=2, legend_label="suma parcial")
pb.leyenda(p1, "right")
p2 = pb.figura("|c_k| (los que entran en la suma, en azul)", "k (armónico; frecuencia k f₀)", "|c_k|", ancho=620, alto=170)
pb.tallos(p2, "k", "c", coef, color=pb.GRIS_CLARO)
pb.tallos(p2, "k", "c", usados, color=pb.AZUL)

sx = pb.selector("Señal periódica", SENALES)
K = pb.deslizador("K (armónicos)", 0, 60, 5, 1)
d = pb.deslizador("Ciclo de trabajo del tren de pulsos", 0.05, 0.95, 0.25, 0.01)
info = Div(text="", width=240)

cb = pb.js("""
    // Un periodo T = 1 muestreado con M puntos; c_k por la DFT (aproximación de la integral).
    const M = 4096, u = rango(0, 1, M + 1).slice(0, M), D = d.value;
    function forma(v) {
        v = mod(v, 1);
        switch (sx.value) {
            case "Tren de pulsos": return (v < D / 2 || v > 1 - D / 2) ? 1 : 0;
            case "Cuadrada (simétrica)": return (v < 0.5) ? 1 : -1;
            case "Triangular": return 1 - 4 * Math.abs(v - 0.5);
            case "Diente de sierra": return 2 * v - 1;
            default: return Math.abs(Math.sin(PI * v));
        }
    }
    const per = u.map(forma), [re, im] = fft(per);
    const Kmax = 60, kk = enteros(-Kmax, Kmax);
    const c = kk.map(k => { const j = mod(k, M); return [re[j] / M, im[j] / M]; });
    coef.data = {k: kk, c: c.map(z => Math.hypot(z[0], z[1]))};
    const Ku = K.value, sel = kk.map((k, i) => [k, i]).filter(a => Math.abs(a[0]) <= Ku);
    usados.data = {k: sel.map(a => a[0]), c: sel.map(a => Math.hypot(c[a[1]][0], c[a[1]][1]))};
    const t = rango(-1, 2, 1501);
    const s = t.map(tt => { let a = 0; for (const [k, i] of sel) a += c[i][0] * Math.cos(2 * PI * k * tt) - c[i][1] * Math.sin(2 * PI * k * tt); return a; });
    tiempo.data = {t: t, x: t.map(forma), s: s};
    // Potencia: Parseval
    const Pt = per.reduce((a, v) => a + v * v, 0) / M;
    const Pk = sel.reduce((a, [k, i]) => a + c[i][0] ** 2 + c[i][1] ** 2, 0);
    const smax = Math.max(...s), xmax = Math.max(...t.map(forma));
    info.text = `<p>Potencia de x(t): ${Pt.toFixed(4)}<br>Potencia con |k| ≤ ${Ku}: ${Pk.toFixed(4)} (${(100 * Pk / Pt).toFixed(1)} %)</p>` +
                `<p>Máximo de la suma parcial: ${smax.toFixed(3)} (x(t) llega a ${xmax.toFixed(3)})</p>`;
""", tiempo=tiempo, coef=coef, usados=usados, sx=sx, K=K, d=d, info=info)
pb.conectar(cb, sx, K, d)

pb.pagina(__file__, "Serie de Fourier", tema=1,
          descripcion="Una señal periódica es una suma de exponenciales complejas a múltiplos de f₀ = 1/T, "
                      "con coeficientes c<sub>k</sub>. Al truncar la suma, la potencia que falta es la de los "
                      "coeficientes omitidos (Parseval). En las discontinuidades la suma parcial se pasa "
                      "de la señal un 9 % del salto por muchos armónicos que se sumen: es el fenómeno de Gibbs.",
          controles=[sx, K, d, info], graficas=[p1, p2], inicio=cb,
          referencia="Transparencias T1-02, «Serie de Fourier de señales continuas periódicas» · Apuntes del Tema 1, sección 6")
