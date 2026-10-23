"""T4 · Filtro de media móvil."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

s = ColumnDataSource(dict(n=[], x=[], y=[], limpia=[]))
H = ColumnDataSource(dict(W=[], m=[], f=[]))

p1 = pb.figura("Señal con ruido x[n] y salida del filtro y[n]", "n", "", ancho=720, alto=240)
p1.line("n", "x", source=s, color=pb.GRIS_CLARO, line_width=1, legend_label="x[n]")
p1.line("n", "limpia", source=s, color=pb.VERDE, line_width=1.5, line_dash="dashed", legend_label="señal sin ruido")
p1.line("n", "y", source=s, color=pb.AZUL, line_width=2, legend_label="y[n]")
pb.leyenda(p1, "below")
p2 = pb.figura("Módulo |H(e^jΩ)|", "Ω (rad/muestra)", "", ancho=330, alto=220, x_range=(0, 3.1416))
p2.line("W", "m", source=H, color=pb.AZUL, line_width=2)
p3 = pb.figura("Fase ∠H(e^jΩ) (rad)", "Ω (rad/muestra)", "", ancho=330, alto=220, x_range=(0, 3.1416))
p3.line("W", "f", source=H, color=pb.ROJO, line_width=2)

L = pb.deslizador("L (muestras promediadas)", 1, 60, 8, 1)
A = pb.deslizador("Desviación del ruido", 0, 1, 0.3, 0.01)
tipo = pb.selector("Señal", ["Seno lento", "Escalones", "Seno lento + tono rápido"])
escala = pb.botones(["Lineal", "dB"])
info = Div(text="", width=240)

cb = pb.js("""
    const l = L.value, N = 300, n = enteros(0, N - 1), r = ruido(N, 7);
    const limpia = n.map(k => tipo.value === "Escalones" ? (Math.floor(k / 75) % 2 ? 1 : -0.5)
                              : Math.sin(2 * PI * k / 150) + (tipo.value.endsWith("rápido") ? 0.5 * Math.cos(0.8 * PI * k) : 0));
    const x = limpia.map((v, k) => v + A.value * r[k]);
    const b = new Array(l).fill(1 / l), y = filtrar(b, [1], x);
    s.data = {n: n, x: x, y: y, limpia: limpia};
    const W = rango(0, PI, 600), Hc = W.map(w => evalpoli(b, cexp([0, w])));
    // H(e^jΩ) = Σ b_k e^{-jΩk}: evalpoli en e^{jΩ} da Σ b_k e^{jΩ(l-1-k)}, se corrige con e^{-jΩ(l-1)}
    const Hr = Hc.map((h, i) => cmul(h, cexp([0, -W[i] * (l - 1)])));
    const m = Hr.map(cabs);
    H.data = {W: W, m: escala.active ? m.map(v => db(v, -60)) : m, f: Hr.map(h => Math.atan2(h[1], h[0]))};
    p2.title.text = escala.active ? "Módulo |H(e^jΩ)| (dB)" : "Módulo |H(e^jΩ)|";
    info.text = `<p>h[n] = 1/${l} para n = 0, …, ${l - 1}</p><p>Primer cero de |H|: Ω = 2π/L = ${(2 * PI / l).toFixed(3)} rad/muestra</p>` +
                `<p>Retardo: (L − 1)/2 = ${((l - 1) / 2).toFixed(1)} muestras</p>` +
                `<p>Varianza del ruido a la salida: σ²/L (se divide por ${l})</p>`;
""", s=s, H=H, L=L, A=A, tipo=tipo, escala=escala, info=info, p2=p2)
pb.conectar(cb, L, A, tipo, escala)

pb.pagina(__file__, "Filtro de media móvil", tema=4,
          descripcion="La media de las L últimas muestras es el FIR más sencillo: h[n] = 1/L. Reduce el ruido "
                      "(su varianza se divide por L) a cambio de suavizar los cambios bruscos y retrasar la señal "
                      "(L − 1)/2 muestras. Es un paso bajo con ceros en múltiplos de 2π/L y fase lineal.",
          controles=[tipo, L, A, escala, info], graficas=[p1, [p2, p3]], inicio=cb,
          referencia="Transparencias T4-01, filtros discretos · Apuntes del Tema 4, sección 1")
