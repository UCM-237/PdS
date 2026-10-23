"""T2 · Sobremuestreo y conformado del ruido de cuantificación."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import BoxAnnotation, ColumnDataSource, Div
import pds_bokeh as pb

S = ColumnDataSource(dict(n=[], x=[], y=[]))
E = ColumnDataSource(dict(W=[], y=[], e=[]))
C = ColumnDataSource(dict(R=[], s0=[], s1=[], s2=[]))
M = ColumnDataSource(dict(R=[], s=[]))

p1 = pb.figura("Entrada x[n] y salida cuantificada y[n]", "n", "", ancho=720, alto=170)
p1.line("n", "x", source=S, color=pb.GRIS, line_width=1.5, legend_label="x[n]")
p1.step("n", "y", source=S, color=pb.AZUL, line_width=1.5, mode="center", legend_label="y[n]")
pb.leyenda(p1, "right")
p2 = pb.figura("Espectro de y[n] y del error (dB); en verde, la banda de la señal", "Ω/π", "dB", ancho=440, alto=240,
               x_axis_type="log", x_range=(1e-3, 1), y_range=(-140, 0))
banda = BoxAnnotation(left=1e-3, right=1, fill_color=pb.VERDE, fill_alpha=0.12)
p2.add_layout(banda)
p2.line("W", "y", source=E, color=pb.GRIS_CLARO, line_width=1, legend_label="Y")
p2.line("W", "e", source=E, color=pb.ROJO, line_width=1.5, legend_label="error (suavizado)")
pb.leyenda(p2, "below")
p3 = pb.figura("SQNR en la banda frente a R", "R (factor de sobremuestreo)", "dB", ancho=260, alto=240, x_axis_type="log", x_range=(1, 64))
p3.line("R", "s0", source=C, color=pb.GRIS, line_width=2, legend_label="sin conformar")
p3.line("R", "s1", source=C, color=pb.AZUL, line_width=2, legend_label="1.er orden")
p3.line("R", "s2", source=C, color=pb.NARANJA, line_width=2, legend_label="2.º orden")
p3.scatter("R", "s", source=M, size=11, color=pb.ROJO, legend_label="medida")
pb.leyenda(p3, "top_left")

R = pb.selector("R (factor de sobremuestreo)", ["1", "2", "4", "8", "16", "32", "64"], valor="8")
B = pb.deslizador("B (bits)", 2, 12, 4, 1)
A = pb.deslizador("Amplitud del tono", 0.05, 0.9, 0.5, 0.05)
orden = pb.botones(["Sin conformar", "1.er orden", "2.º orden"])
info = Div(text="", width=240)

cb = pb.js("""
    const N = 8192, r = Number(R.value), b = B.value, D = 2 / 2 ** b, o = orden.active, av = A.value;
    // Tono centrado en una frecuencia de la DFT, al 30 % de la banda de la señal [0, π/R]
    // Un poco de ruido en la entrada (σ = Δ/3) descorrela el error de la señal, como supone el modelo de ruido uniforme
    const k0 = Math.max(1, Math.round(0.3 * N / (2 * r))), w = ruido(N, 9), x = enteros(0, N - 1).map(n => av * Math.sin(2 * PI * k0 * n / N) + D / 3 * w[n]);
    const q = v => Math.max(-(2 ** (b - 1)), Math.min(2 ** (b - 1) - 1, Math.round(v / D))) * D;
    // Realimentación del error: v = x − e[n−1] (1.er orden) o x − 2e[n−1] + e[n−2] (2.º orden); y = Q(v), e = y − v
    const y = new Array(N), ev = [0, 0];
    for (let n = 0; n < N; n++) {
        const v = x[n] - (o === 1 ? ev[0] : o === 2 ? 2 * ev[0] - ev[1] : 0);
        y[n] = q(v); ev[1] = ev[0]; ev[0] = y[n] - v;
    }
    const e = y.map((v, i) => v - x[i]);
    S.data = {n: enteros(0, 199), x: x.slice(0, 200), y: y.slice(0, 200)};
    const [yr, yi] = fft(y), [er, ei] = fft(e), K = N / 2, pot = (re, im) => enteros(0, K - 1).map(k => (re[k] ** 2 + im[k] ** 2) / (N * N));
    const Py = pot(yr, yi), Pe = pot(er, ei);
    // Error suavizado con una media de 17 bins para ver su forma
    const sua = Pe.map((_, k) => { let s = 0, c = 0; for (let j = Math.max(1, k - 8); j <= Math.min(K - 1, k + 8); j++) { s += Pe[j]; c++; } return s / c; });
    E.data = {W: enteros(1, K - 1).map(k => 2 * k / N), y: Py.slice(1).map(v => 10 * Math.log10(Math.max(4 * v, 1e-14))), e: sua.slice(1).map(v => 10 * Math.log10(Math.max(4 * v, 1e-14)))};
    banda.right = 1 / r;
    // Ruido en la banda de la señal (|Ω| < π/R) y SQNR medida
    const kB = Math.floor(N / (2 * r)); let ruidoB = Pe[0]; for (let k = 1; k <= Math.min(kB, K - 1); k++) ruidoB += 2 * Pe[k];
    const Ps = av * av / 2, sq = 10 * Math.log10(Ps / ruidoB), base = 10 * Math.log10(Ps / (D * D / 12));
    const teo = (rr, oo) => base + 10 * Math.log10(rr) + [0, 10 * Math.log10(3 * rr * rr / PI ** 2), 10 * Math.log10(5 * rr ** 4 / PI ** 4)][oo];
    const Rs = rango(0, Math.log10(64), 60).map(v => 10 ** v);
    C.data = {R: Rs, s0: Rs.map(v => teo(v, 0)), s1: Rs.map(v => teo(v, 1)), s2: Rs.map(v => teo(v, 2))};
    M.data = {R: [r], s: [sq]};
    info.text = `<p>Ruido total del cuantificador: Δ²/12, repartido por igual en [0, π] si no se conforma.</p>` +
        `<p>Banda de la señal: Ω < π/R = ${(1 / r).toFixed(3)}π</p>` +
        `<p><b>SQNR en la banda: ${sq.toFixed(1)} dB</b> (teoría ${teo(r, o).toFixed(1)} dB)</p>` +
        `<p>Ganancia frente a R = 1 sin conformar: ${(sq - base).toFixed(1)} dB, como ${((sq - base) / 6.02).toFixed(1)} bits más (${(b + (sq - base) / 6.02).toFixed(1)} bits efectivos).</p>` +
        "<p>La entrada lleva un ruido pequeño (σ = Δ/3) para que el error se parezca al modelo de ruido uniforme; la SQNR mide solo el error de cuantificación.</p>" +
        "<p>Sin conformar, cada vez que R se duplica se ganan 3 dB (medio bit); con conformado de orden L, unos 3(2L + 1) dB.</p>" +
        (o && b <= 3 ? "<p style='color:#C0392B'>Con muy pocos bits, el conformado puede saturar el cuantificador.</p>" : "");
""", S=S, E=E, C=C, M=M, R=R, B=B, A=A, orden=orden, info=info, banda=banda)
pb.conectar(cb, R, B, A, orden)

pb.pagina(__file__, "Sobremuestreo y conformado de ruido", tema=2,
          descripcion="Al muestrear R veces más rápido de lo necesario, la misma potencia de ruido de cuantificación, Δ²/12, se "
                      "reparte en una banda R veces más ancha y en la banda de la señal queda R veces menos. Si además se realimenta "
                      "el error de cuantificación (conversores sigma-delta), el ruido se empuja hacia las frecuencias altas, que un "
                      "filtro digital elimina después.",
          controles=[R, B, A, orden, info], graficas=[p1, [p2, p3]], inicio=cb,
          referencia="Transparencias T2-04, conversores con sobremuestreo · Apuntes del Tema 2, sección 6")
