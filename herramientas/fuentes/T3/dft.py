"""T3 · DFT de una suma de sinusoides: fuga y relleno con ceros."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

sec = ColumnDataSource(dict(n=[], x=[]))
cero = ColumnDataSource(dict(n=[], x=[]))
dt = ColumnDataSource(dict(W=[], m=[]))
X = ColumnDataSource(dict(W=[], m=[]))

p1 = pb.figura("x[n]: L muestras de la señal y N − L ceros", "n", "x[n]", ancho=680, alto=180)
pb.tallos(p1, "n", "x", sec, color=pb.AZUL)
pb.tallos(p1, "n", "x", cero, color=pb.GRIS_CLARO)
p2 = pb.figura("|X[k]| en Ωk = 2πk/N y |X(e^jΩ)| de las L muestras", "Ω (rad/muestra)", "|X|", ancho=680, alto=230,
               x_range=(0, 3.1416))
p2.line("W", "m", source=dt, color=pb.GRIS_CLARO, line_width=1.5, legend_label="DTFT")
pb.tallos(p2, "W", "m", X, color=pb.ROJO, legend_label="DFT")
pb.leyenda(p2, "below")

L = pb.deslizador("L (muestras de señal)", 8, 128, 32, 1)
N = pb.deslizador("N (puntos de la DFT, log₂)", 3, 9, 6, 1)
F1 = pb.deslizador("F₁ (ciclos/muestra)", 0, 0.5, 0.125, 0.001)
F2 = pb.deslizador("F₂ (ciclos/muestra)", 0, 0.5, 0.2, 0.001)
A2 = pb.deslizador("Amplitud de la segunda", 0, 1, 0.5, 0.05)
info = Div(text="", width=240)

cb = pb.js("""
    const l = L.value, Nd = Math.max(Math.pow(2, N.value), l), Nfft = Math.pow(2, Math.ceil(Math.log2(Nd)));
    const x = enteros(0, l - 1).map(n => Math.cos(2 * PI * F1.value * n) + A2.value * Math.cos(2 * PI * F2.value * n));
    sec.data = {n: enteros(0, l - 1), x: x};
    cero.data = {n: enteros(l, Nfft - 1), x: new Array(Nfft - l).fill(0)};
    const [dr, di] = dtft(x, 4096), half = 2049;
    dt.data = {W: enteros(0, half - 1).map(k => 2 * PI * k / 4096), m: enteros(0, half - 1).map(k => Math.hypot(dr[k], di[k]))};
    const xp = x.concat(new Array(Nfft - l).fill(0)), [re, im] = fft(xp), K = Nfft / 2 + 1;
    X.data = {W: enteros(0, K - 1).map(k => 2 * PI * k / Nfft), m: enteros(0, K - 1).map(k => Math.hypot(re[k], im[k]))};
    const k1 = F1.value * l;
    info.text = `<p>N = ${Nfft} (la DFT necesita N ≥ L)</p>` +
        `<p>Separación entre muestras de la DFT: 2π/N = ${(2 * PI / Nfft).toFixed(4)} rad/muestra</p>` +
        `<p>Resolución de las L muestras: unos 2π/L = ${(2 * PI / l).toFixed(4)} rad/muestra; |F₁ − F₂|·L = ${(Math.abs(F1.value - F2.value) * l).toFixed(2)}</p>` +
        (Math.abs(k1 - Math.round(k1)) < 1e-6 && Nfft === l ? "<p>F₁·L es entero y N = L: el tono cae en una frecuencia de la DFT y no hay fuga.</p>" : "");
""", sec=sec, cero=cero, dt=dt, X=X, L=L, N=N, F1=F1, F2=F2, A2=A2, info=info)
pb.conectar(cb, L, N, F1, F2, A2)

pb.pagina(__file__, "DFT, fuga y relleno con ceros", tema=3,
          descripcion="La DFT de N puntos muestrea la DTFT de las L muestras en Ωk = 2πk/N. Rellenar con "
                      "ceros (N > L) muestrea más densamente la misma DTFT, pero no separa dos tonos más "
                      "próximos que unos 2π/L: para eso hace falta más señal. Si un tono no cae en una "
                      "Ωk, su energía se reparte entre varias (fuga).",
          controles=[L, N, F1, F2, A2, info], graficas=[p1, p2], inicio=cb,
          referencia="Transparencias T3-01 y T3-03 · Apuntes del Tema 3, secciones 1 y 3")
