"""T3 · Muestrear la DTFT es periodizar la secuencia."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

LMAX = 16
x = ColumnDataSource(dict(n=list(range(LMAX)), x=[max(0.0, 1 - abs(i - 4) / 5) for i in range(LMAX)]))
per = ColumnDataSource(dict(n=[], x=[]))
dt = ColumnDataSource(dict(W=[], m=[]))
mu = ColumnDataSource(dict(W=[], m=[]))

p1 = pb.figura("x[n] (haz clic o arrastra para cambiarla; solo cuentan las L primeras)", "n", "x[n]",
               ancho=680, alto=170, y_range=(-1.5, 1.5), x_range=(-0.5, LMAX - 0.5), tools="reset,save")
pb.tallos(p1, "n", "x", x, color=pb.AZUL)
p2 = pb.figura("x̃[n] = Σ x[n − rN]: la IDFT de las N muestras de la DTFT", "n", "x̃[n]", ancho=680, alto=190)
pb.tallos(p2, "n", "x", per, color=pb.VERDE)
p3 = pb.figura("|X(e^jΩ)| y sus N muestras en Ωk = 2πk/N", "Ω (rad/muestra)", "", ancho=680, alto=190, x_range=(0, 6.2832))
p3.line("W", "m", source=dt, color=pb.GRIS, line_width=1.5)
pb.tallos(p3, "W", "m", mu, color=pb.ROJO)

L = pb.deslizador("L (soporte de x[n])", 1, LMAX, 9, 1)
N = pb.deslizador("N (muestras de la DTFT)", 1, 24, 12, 1)
info = Div(text="", width=240)

cb = pb.js("""
    const l = L.value, Nn = N.value, xs = x.data.x.slice(0, l);
    const r = new Array(Nn).fill(0); xs.forEach((v, i) => r[i % Nn] += v);
    const n = enteros(-Nn, 3 * Nn - 1);
    per.data = {n: n, x: n.map(k => r[mod(k, Nn)])};
    const M = 4096, [a, b] = dtft(xs, M);
    dt.data = {W: enteros(0, M - 1).map(k => 2 * PI * k / M), m: enteros(0, M - 1).map(k => Math.hypot(a[k], b[k]))};
    const [c, d] = dft(xs, Nn);
    mu.data = {W: enteros(0, Nn - 1).map(k => 2 * PI * k / Nn), m: enteros(0, Nn - 1).map(k => Math.hypot(c[k], d[k]))};
    info.text = Nn >= l ? `<p>N ≥ L: las copias no se solapan y un periodo de x̃[n] es x[n]. Las N muestras de la DTFT bastan para recuperarla.</p>`
                        : `<p style="color:#C0392B">N < L: las copias se solapan (aliasing en el tiempo) y x[n] ya no se puede recuperar.</p>`;
""", x=x, per=per, dt=dt, mu=mu, L=L, N=N, info=info)
pb.editable(p1, x, "n", "x", cb)
pb.conectar(cb, L, N)

pb.pagina(__file__, "Extensión periódica", tema=3,
          descripcion="Tomar N muestras de la DTFT X(e<sup>jΩ</sup>) equivale a sumar copias de x[n] "
                      "desplazadas N: la secuencia que devuelve la IDFT es la extensión periódica x̃[n]. "
                      "Si la secuencia dura más de N muestras, las copias se solapan.",
          controles=[L, N, info], graficas=[p1, p2, p3], inicio=cb,
          referencia="Transparencias T3-01, muestreo en frecuencia · Apuntes del Tema 3, secciones 1 y 2")
