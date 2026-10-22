"""T3 · Ventanas y fuga espectral."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

w = ColumnDataSource(dict(n=[], w=[], x=[]))
W = ColumnDataSource(dict(W=[], w=[], x=[]))

p1 = pb.figura("Ventana w[n] y señal enventanada x[n]w[n]", "n", "", ancho=330, alto=220)
p1.line("n", "w", source=w, color=pb.NARANJA, line_width=2, legend_label="w[n]")
pb.tallos(p1, "n", "x", w, color=pb.AZUL, legend_label="x[n]w[n]")
pb.leyenda(p1, "below")
p2 = pb.figura("Espectro de la ventana |W(e^jΩ)|", "Ω (rad/muestra)", "", ancho=330, alto=220, x_range=(0, 3.1416))
p2.line("W", "w", source=W, color=pb.NARANJA, line_width=1.5)
p3 = pb.figura("Espectro de x[n]w[n]: dos tonos de amplitudes 1 y A₂", "Ω (rad/muestra)", "", ancho=720, alto=230,
               x_range=(0, 3.1416))
p3.line("W", "x", source=W, color=pb.AZUL, line_width=1.5)

tipo = pb.selector("Ventana", ["Rectangular", "Hann", "Hamming", "Blackman"])
L = pb.deslizador("L (longitud)", 8, 256, 64, 1)
F2 = pb.deslizador("F₂ − F₁ (ciclos/muestra)", 0.005, 0.2, 0.05, 0.001)
A2 = pb.deslizador("A₂ (dB)", -80, 0, -30, 1)
escala = pb.botones(["dB", "Lineal"])
info = Div(text="", width=240)

cb = pb.js("""
    const l = L.value, v = ventana(tipo.value, l), F1 = 0.2, a2 = Math.pow(10, A2.value / 20), enDB = escala.active === 0;
    const n = enteros(0, l - 1), x = n.map(k => (Math.cos(2 * PI * F1 * k) + a2 * Math.cos(2 * PI * (F1 + F2.value) * k)) * v[k]);
    w.data = {n: n, w: v, x: x};
    const M = 8192, [wr, wi] = dtft(v, M), [xr, xi] = dtft(x, M), K = M / 2 + 1, sw = v.reduce((a, b) => a + b, 0);
    const mw = enteros(0, K - 1).map(k => Math.hypot(wr[k], wi[k]) / sw), mx = enteros(0, K - 1).map(k => 2 * Math.hypot(xr[k], xi[k]) / sw);
    W.data = {W: enteros(0, K - 1).map(k => 2 * PI * k / M), w: mw.map(m => enDB ? db(m, -120) : m), x: mx.map(m => enDB ? db(m, -120) : m)};
    // Lóbulo principal (primer mínimo) y lóbulo secundario más alto
    let i = 1; while (i < K - 1 && !(mw[i] < mw[i - 1] && mw[i] <= mw[i + 1])) i++;
    const lat = Math.max(...mw.slice(i)), ancho = 2 * (2 * PI * i / M);
    info.text = `<p>Lóbulo principal: ${ancho.toFixed(3)} rad/muestra entre ceros (${(ancho * l / (2 * PI)).toFixed(1)}·2π/L)</p>` +
                `<p>Lóbulo secundario más alto: ${db(lat).toFixed(1)} dB</p>` +
                `<p>Separación de los tonos: ${(2 * PI * F2.value).toFixed(3)} rad/muestra</p>`;
""", w=w, W=W, tipo=tipo, L=L, F2=F2, A2=A2, escala=escala, info=info)
pb.conectar(cb, tipo, L, F2, A2, escala)

pb.pagina(__file__, "Ventanas y fuga espectral", tema=3,
          descripcion="Tomar L muestras es multiplicar por una ventana, y el espectro queda convolucionado "
                      "con el de la ventana. El ancho del lóbulo principal fija la resolución (separar dos "
                      "tonos próximos) y los lóbulos secundarios, la fuga (ver un tono débil junto a uno fuerte). "
                      "La rectangular tiene el lóbulo más estrecho y la peor fuga.",
          controles=[tipo, L, F2, A2, escala, info], graficas=[[p1, p2], p3], inicio=cb,
          referencia="Transparencias T3-03, ventanas y resolución · Apuntes del Tema 3, sección 3")
