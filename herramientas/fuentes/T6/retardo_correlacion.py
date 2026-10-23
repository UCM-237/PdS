"""T6 · Estimar un retardo con la correlación cruzada (radar, sonar, GPS)."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div, Span
import pds_bokeh as pb

NY = 1024

X = ColumnDataSource(dict(n=[], x=[]))
Y = ColumnDataSource(dict(n=[], y=[], e=[]))
R = ColumnDataSource(dict(l=[], r=[]))
A = ColumnDataSource(dict(l=[], r=[]))

p1 = pb.figura("Pulso emitido x[n]", "n", "", ancho=300, alto=170)
p1.line("n", "x", source=X, color=pb.AZUL, line_width=1.4)
p2 = pb.figura("Señal recibida y[n] = α·x[n − D] + v[n]", "n", "", ancho=560, alto=170, x_range=(0, NY))
p2.line("n", "y", source=Y, color=pb.GRIS, line_width=1)
p2.line("n", "e", source=Y, color=pb.AZUL, line_width=1.6, legend_label="α·x[n − D] (sin ruido)")
pb.leyenda(p2, "below")
p3 = pb.figura("Correlación cruzada r_yx[l] / ‖x‖²", "l (retardo de prueba)", "", ancho=560, alto=240,
               x_range=p2.x_range)
p3.line("l", "r", source=R, color=pb.AZUL, line_width=1.4)
real = Span(location=300, dimension="height", line_color=pb.VERDE, line_width=2, line_dash="dashed")
est = Span(location=300, dimension="height", line_color=pb.ROJO, line_width=2, line_dash="dotted")
p3.add_layout(real)
p3.add_layout(est)
p4 = pb.figura("Autocorrelación r_xx[l] / ‖x‖²", "l", "", ancho=300, alto=240, y_range=(-1.05, 1.05))
p4.line("l", "r", source=A, color=pb.AZUL, line_width=1.6)

senal = pb.selector("Pulso emitido", ["Ruido blanco", "Chirp", "Pulso sinc", "Pulso rectangular", "Sinusoide"])
Lx = pb.selector("Longitud del pulso L", ["16", "32", "64", "128", "256"], "128")
D = pb.deslizador("Retardo verdadero D", 0, 760, 300, 1)
alfa = pb.deslizador("Atenuación α", 0.02, 1, 0.5, 0.01)
sr = pb.deslizador("Desviación típica del ruido σ", 0, 3, 1, 0.05)
semilla = pb.deslizador("Realización", 1, 50, 1, 1)
info = Div(text="", width=250)

cb = pb.js("""
    const L = parseInt(Lx.value), s = senal.value, g = generador(semilla.value), gx = generador(7);
    const n = enteros(0, L - 1);
    let x;
    if (s === "Ruido blanco") x = n.map(() => gauss(gx));
    else if (s === "Chirp") x = n.map(k => Math.cos(PI * (0.05 * k + 0.45 * k * k / (2 * L))));
    else if (s === "Pulso sinc") x = n.map(k => sinc((k - (L - 1) / 2) / 4));
    else if (s === "Pulso rectangular") x = n.map(() => 1);
    else x = n.map(k => Math.cos(0.3 * PI * k));
    const Ex = x.reduce((a, v) => a + v * v, 0), d = Math.min(D.value, NY - L);
    const e = new Array(NY).fill(0); for (let k = 0; k < L; k++) e[d + k] = alfa.value * x[k];
    const y = e.map(v => v + sr.value * gauss(g));
    X.data = {n: n, x: x}; Y.data = {n: enteros(0, NY - 1), y: y, e: e};
    // r_yx[l] = Σ y[n]·x[n − l], con la FFT: Y(k)·X*(k)
    const P = pot2(NY + L), yr = y.concat(new Array(P - NY).fill(0)), xr = x.concat(new Array(P - L).fill(0));
    const [ya, yb] = fft(yr), [xa, xb] = fft(xr);
    const [ra] = ifft(ya.map((v, k) => v * xa[k] + yb[k] * xb[k]), ya.map((v, k) => yb[k] * xa[k] - v * xb[k]));
    const ls = enteros(0, NY - L), r = ls.map(l => ra[l] / Ex);
    R.data = {l: ls, r: r};
    let im = 0; r.forEach((v, i) => { if (v > r[im]) im = i; });
    real.location = d; est.location = ls[im];
    const rxx = enteros(-L + 1, L - 1).map(l => { let a = 0; for (let k = Math.max(0, l); k < Math.min(L, L + l); k++) a += x[k] * x[k - l]; return a / Ex; });
    A.data = {l: enteros(-L + 1, L - 1), r: rxx};
    // Anchura del pico principal de r_xx a media altura
    let w = 0; while (w < L - 1 && rxx[L - 1 + w + 1] > 0.5) w++;
    // Pico secundario: el mayor valor de r_xx más allá del primer cero
    let z = 1; while (z < L - 1 && rxx[L - 1 + z] > 0) z++;
    const sec = z < L - 1 ? maximo(rxx.slice(L - 1 + z)) : 0;
    const snr = 10 * Math.log10(alfa.value ** 2 * Ex / Math.max(sr.value ** 2, 1e-12));
    const ok = Math.abs(ls[im] - d) <= Math.max(1, w);
    info.text = `<p>Retardo estimado: <b style="color:${ok ? "#1E7B4F" : "#C0392B"}">${ls[im]}</b> (verdadero ${d})</p><p>Sin ruido, el máximo de r<sub>yx</sub>/‖x‖² vale α = ${alfa.value.toFixed(2)}; el ruido de la correlación tiene σ/‖x‖ = ${(sr.value / Math.sqrt(Ex)).toFixed(3)}</p>` +
        `<p>Relación señal-ruido a la salida del correlador: α²‖x‖²/σ² = ${sr.value > 0 ? snr.toFixed(1) + " dB" : "∞"}. Crece con la energía del pulso, no con su amplitud</p>` +
        `<p>SNR por muestra de y: ${sr.value > 0 ? (10 * Math.log10(alfa.value ** 2 * Ex / L / sr.value ** 2)).toFixed(1) + " dB" : "∞"}</p>` +
        `<p>Pico de r<sub>xx</sub> a media altura: ±${w} muestras; pico secundario ${sec.toFixed(2)}. Un pulso de banda ancha da un pico estrecho y sin rivales, y un retardo preciso; si el secundario se acerca a 1, el ruido puede hacer que gane</p>`;
""", X=X, Y=Y, R=R, A=A, real=real, est=est, senal=senal, Lx=Lx, D=D, alfa=alfa, sr=sr, semilla=semilla, info=info, NY=NY)
pb.conectar(cb, senal, Lx, D, alfa, sr, semilla)

pb.pagina(__file__, "Estimación de un retardo por correlación", tema=6,
          descripcion="Un radar emite un pulso x[n] y recibe un eco atenuado, retrasado y con ruido. La correlación cruzada "
                      "r<sub>yx</sub>[l] compara el eco con el pulso desplazado l muestras; su máximo da el retardo. Funciona "
                      "aunque el eco no se vea a simple vista, si el pulso tiene energía suficiente. La forma del pico es la "
                      "autocorrelación del pulso: estrecha para el ruido o el chirp, ancha o ambigua para el rectángulo o la "
                      "sinusoide.",
          controles=[senal, Lx, D, alfa, sr, semilla, info], graficas=[[p1, p2], [p4, p3]], inicio=cb,
          referencia="Transparencias T6-03, correlación cruzada y estimación de retardos · Apuntes del Tema 6, sección 3")
