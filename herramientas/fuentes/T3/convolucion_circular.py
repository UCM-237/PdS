"""T3 · Convolución circular frente a lineal."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

SEC = ["Pulso de 4", "Pulso de 6", "Rampa 1…5", "Exponencial 0,7ⁿ (8 muestras)", "1, −1", "1, 2, 1"]

a = ColumnDataSource(dict(k=[], x=[], h=[]))
res = ColumnDataSource(dict(n=[], c=[], l=[]))
act = ColumnDataSource(dict(n=[], c=[]))

p1 = pb.figura("x[k] y h[((n − k))_N] en 0 ≤ k < N", "k", "", ancho=680, alto=200)
pb.tallos(p1, "k", "x", a, color=pb.AZUL, legend_label="x[k]")
pb.tallos(p1, "k", "h", a, color=pb.ROJO, legend_label="h[((n − k))_N]", marker="square")
pb.leyenda(p1, "right")
p2 = pb.figura("Convolución circular de N puntos (azul) y lineal (gris)", "n", "", ancho=680, alto=220)
pb.tallos(p2, "n", "l", res, color=pb.GRIS_CLARO, legend_label="lineal x * h")
pb.tallos(p2, "n", "c", res, color=pb.AZUL, legend_label="circular x ⊛ h")
p2.scatter("n", "c", source=act, size=12, color=pb.NARANJA, legend_label="n actual")
pb.leyenda(p2, "right")

sx = pb.selector("x[n]", SEC, SEC[2])
sh = pb.selector("h[n]", SEC, SEC[0])
N = pb.deslizador("N (puntos)", 4, 20, 6, 1)
n = pb.deslizador("n", 0, 19, 0, 1)
info = Div(text="", width=240)

cb = pb.js("""
    function sec(s) {
        if (s === "Pulso de 4") return [1, 1, 1, 1];
        if (s === "Pulso de 6") return [1, 1, 1, 1, 1, 1];
        if (s.startsWith("Rampa")) return [1, 2, 3, 4, 5];
        if (s.startsWith("Exponencial")) return enteros(0, 7).map(k => Math.pow(0.7, k));
        if (s === "1, −1") return [1, -1];
        return [1, 2, 1];
    }
    const x0 = sec(sx.value), h0 = sec(sh.value), Nn = N.value, nn = Math.min(n.value, Nn - 1);
    // Si N es menor que una secuencia, se pliega (equivale a tomar la DFT de N puntos)
    const fold = s => { const r = new Array(Nn).fill(0); s.forEach((v, i) => r[i % Nn] += v); return r; };
    const x = fold(x0), h = fold(h0), k = enteros(0, Nn - 1);
    a.data = {k: k, x: x, h: k.map(i => h[mod(nn - i, Nn)])};
    const lin = new Array(x0.length + h0.length - 1).fill(0);
    x0.forEach((u, i) => h0.forEach((v, j) => lin[i + j] += u * v));
    const M = Math.max(Nn, lin.length), c = k.map(m => k.reduce((s, i) => s + x[i] * h[mod(m - i, Nn)], 0));
    res.data = {n: enteros(0, M - 1), c: enteros(0, M - 1).map(m => m < Nn ? c[m] : NaN), l: enteros(0, M - 1).map(m => m < lin.length ? lin[m] : 0)};
    act.data = {n: [nn], c: [c[nn]]};
    const need = x0.length + h0.length - 1;
    info.text = `<p>L = ${x0.length}, P = ${h0.length}: la lineal tiene L + P − 1 = ${need} muestras.</p>` +
        (Nn >= need ? `<p>N ≥ L + P − 1: la circular coincide con la lineal.</p>`
                    : `<p style="color:#C0392B">N < L + P − 1: las últimas ${need - Nn} muestras de la lineal se suman a las primeras (aliasing temporal).</p>`) +
        `<p>Es lo que se obtiene con IDFT{X[k]H[k]} de N puntos.</p>`;
""", a=a, res=res, act=act, sx=sx, sh=sh, N=N, n=n, info=info)
pb.conectar(cb, sx, sh, N, n)

pb.pagina(__file__, "Convolución circular", tema=3,
          descripcion="Multiplicar dos DFT de N puntos equivale a una convolución circular: h se invierte "
                      "y se desplaza módulo N, de modo que lo que sale por la derecha entra por la "
                      "izquierda. Para obtener la convolución lineal hay que rellenar con ceros hasta "
                      "N ≥ L + P − 1.",
          controles=[sx, sh, N, n, info], graficas=[p1, p2], inicio=cb,
          referencia="Transparencias T3-02, convolución circular · Apuntes del Tema 3, sección 2")
