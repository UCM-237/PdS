"""T6 · Señal aleatoria a través de un sistema LTI: ruido coloreado e identificación de sistemas."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

S = ColumnDataSource(dict(n=[], x=[], y=[]))
D = ColumnDataSource(dict(W=[], yy=[], teo=[], xx=[]))
I = ColumnDataSource(dict(W=[], h=[], cr=[], ing=[], fh=[], fc=[]))
Hn = ColumnDataSource(dict(l=[], h=[], c=[]))

p1 = pb.figura("Entrada blanca x[n] y salida y[n] (primeras 200 muestras)", "n", "", ancho=520, alto=170, x_range=(0, 200))
p1.line("n", "x", source=S, color=pb.GRIS_CLARO, line_width=1, legend_label="x")
p1.line("n", "y", source=S, color=pb.AZUL, line_width=1.5, legend_label="y")
pb.leyenda(p1, "right")
p2 = pb.figura("DEP de la salida: Welch y σ²|H|² + ruido de medida", "Ω (rad/muestra)", "dB", ancho=520, alto=230,
               x_range=(0, 3.1416))
p2.line("W", "xx", source=D, color=pb.GRIS_CLARO, line_width=1.5, legend_label="Φ̂_xx (entrada)")
p2.line("W", "teo", source=D, color=pb.ROJO, line_width=2.5, legend_label="teórica")
p2.line("W", "yy", source=D, color=pb.AZUL, line_width=1.5, legend_label="Φ̂_yy (Welch)")
pb.leyenda(p2, "right")
p3 = pb.figura("Identificación: |H| verdadera y estimada", "Ω (rad/muestra)", "dB", ancho=520, alto=230, x_range=p2.x_range)
p3.line("W", "h", source=I, color=pb.ROJO, line_width=2.5, legend_label="|H| verdadera")
p3.line("W", "cr", source=I, color=pb.VERDE, line_width=1.6, legend_label="|Φ̂_yx/Φ̂_xx|")
p3.line("W", "ing", source=I, color=pb.NARANJA, line_width=1.4, line_dash="dashed", legend_label="√(Φ̂_yy/Φ̂_xx)")
pb.leyenda(p3, "right")
p4 = pb.figura("Fase de H: verdadera y estimada", "Ω (rad/muestra)", "rad", ancho=300, alto=200, x_range=p2.x_range)
p4.line("W", "fh", source=I, color=pb.ROJO, line_width=2.5)
p4.line("W", "fc", source=I, color=pb.VERDE, line_width=1.4)
p5 = pb.figura("h[l] y φ̂_yx[l]/σ²", "l", "", ancho=300, alto=200)
pb.tallos(p5, "l", "h", Hn, color=pb.ROJO, size=7)
p5.scatter("l", "c", source=Hn, color=pb.VERDE, size=5, marker="square")

sis = pb.selector("Sistema", ["H(z) de los apuntes: (0,2 + 0,3z⁻¹)/(1 − 1,2z⁻¹ + 0,72z⁻²)", "Butterworth paso bajo de orden 4",
                              "AR(1): 1/(1 − a z⁻¹)", "Media móvil de L muestras", "Resonador"], width=250)
par = pb.deslizador("Parámetro del sistema", 0.05, 0.95, 0.5, 0.01)
sx = pb.deslizador("σ de la entrada", 0.2, 2, 1, 0.05)
sv = pb.deslizador("σ del ruido de medida v", 0, 1, 0.3, 0.01)
N = pb.deslizador("N (muestras)", 1024, 32768, 16384, 1024)
Lw = pb.selector("Longitud de los tramos de Welch", ["64", "128", "256", "512", "1024"], "256")
info = Div(text="", width=250)

cb = pb.js("""
    const g = generador(3), Nn = N.value, q = par.value, s = sis.value;
    let b, a, txt = "";
    if (s.startsWith("H(z)")) { b = [0.2, 0.3]; a = [1, -1.2, 0.72]; par.title = "Parámetro (no se usa)"; }
    else if (s.startsWith("Butter")) { const [z, p, k] = butter_z(4, q * PI); [b, a] = ba(z, p, k); par.title = `Ω_c/π = ${q.toFixed(2)}`; }
    else if (s.startsWith("AR")) { const aa = 2 * q - 1; b = [1]; a = [1, -aa]; par.title = `a = 2·parámetro − 1 = ${aa.toFixed(2)}`; }
    else if (s.startsWith("Media")) { const L = Math.max(2, Math.round(q * 20)); b = new Array(L).fill(1 / L); a = [1]; par.title = `L = ${L}`; }
    else { const r = 0.95, W0 = q * PI; b = [1 - r]; a = [1, -2 * r * Math.cos(W0), r * r]; par.title = `Ω₀/π = ${q.toFixed(2)} (r = 0,95)`; }
    const x = enteros(1, Nn).map(() => sx.value * gauss(g)), y0 = filtrar(b, a, x), y = y0.map(v => v + sv.value * gauss(g));
    S.data = {n: enteros(0, 199), x: x.slice(0, 200), y: y.slice(0, 200)};
    const L = parseInt(Lw.value), w = ventana("Hann", L + 1).slice(0, L), est = welch(x, y, w, L / 2, Math.max(L, 512));
    const H = est.W.map(W => { const z = cexp([0, -W]); return cdiv(evalpoli(b.slice().reverse(), z), evalpoli(a.slice().reverse(), z)); });
    // evalpoli con los coeficientes en orden creciente de z⁻¹ evalúa B(z⁻¹) en z⁻¹ = e^{−jΩ}
    const s2 = sx.value ** 2, H2 = H.map(h => h[0] * h[0] + h[1] * h[1]);
    D.data = {W: est.W, yy: est.Pyy.map(v => 10 * Math.log10(v)), teo: H2.map(v => 10 * Math.log10(s2 * v + sv.value ** 2)), xx: est.Pxx.map(v => 10 * Math.log10(v))};
    const Hc = est.Pyx[0].map((v, k) => [v / est.Pxx[k], est.Pyx[1][k] / est.Pxx[k]]);
    I.data = {W: est.W, h: H2.map(v => 10 * Math.log10(v)), cr: Hc.map(h => 20 * Math.log10(cabs(h))),
              ing: est.Pyy.map((v, k) => 10 * Math.log10(v / est.Pxx[k])),
              fh: desenrollar(H.map(h => Math.atan2(h[1], h[0]))), fc: desenrollar(Hc.map(h => Math.atan2(h[1], h[0])))};
    // Respuesta al impulso y correlación cruzada salida-entrada (estimador sesgado)
    const ls = enteros(0, 30), imp = filtrar(b, a, ls.map(l => (l ? 0 : 1)));
    const cyx = ls.map(l => { let t = 0; for (let n = 0; n + l < Nn; n++) t += y[n + l] * x[n]; return t / Nn / s2; });
    Hn.data = {l: ls, h: imp, c: cyx};
    const hl = filtrar(b, a, enteros(0, 2047).map(l => (l ? 0 : 1))), Py = s2 * hl.reduce((t, v) => t + v * v, 0);
    let py = 0; for (const v of y0) py += v * v; py /= Nn;
    info.text = `<p>Potencia de la salida (sin el ruido de medida): ${py.toFixed(4)}; teórica σ²Σh²[k] = ${Py.toFixed(4)}</p>` +
        `<p>Media de la salida: ${media(y0).toFixed(4)} (μ<sub>y</sub> = H(e<sup>j0</sup>)μ<sub>x</sub> = 0)</p>` +
        `<p>Welch: ${est.tramos} tramos de ${L} muestras con 50 % de solapamiento</p>` +
        `<p>El cociente cruzado no se ve afectado por v; √(Φ̂_yy/Φ̂_xx) sube donde |H| es pequeño, porque suma Φ_vv/Φ_xx = ${(sv.value ** 2 / s2).toFixed(3)}</p>`;
""", S=S, D=D, I=I, Hn=Hn, sis=sis, par=par, sx=sx, sv=sv, N=N, Lw=Lw, info=info)
pb.conectar(cb, sis, par, sx, sv, N, Lw)

pb.pagina(__file__, "Ruido a través de un sistema LTI", tema=6,
          descripcion="Si una señal ESA atraviesa un sistema LTI, Φ<sub>yy</sub> = |H|²Φ<sub>xx</sub> y "
                      "Φ<sub>yx</sub> = HΦ<sub>xx</sub>. Con ruido blanco a la entrada, la salida es ruido coloreado con la "
                      "forma de |H|². Midiendo entrada y salida se identifica H: el cociente Φ<sub>yx</sub>/Φ<sub>xx</sub> da "
                      "el módulo y la fase y no le afecta el ruido de medida.",
          controles=[sis, par, sx, sv, N, Lw, info], graficas=[[p1, p5], [p2, p4], p3], inicio=cb,
          referencia="Transparencias T6-04, sistema LTI, ruido coloreado e identificación de sistemas · Apuntes del Tema 6, sección 4")
