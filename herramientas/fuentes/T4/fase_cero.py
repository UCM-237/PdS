"""T4 · Filtrado de fase cero (hacia delante y hacia atrás)."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

s = ColumnDataSource(dict(n=[], x=[], limpia=[], y1=[], y2=[]))
H = ColumnDataSource(dict(W=[], m1=[], m2=[], f1=[]))

p1 = pb.figura("Entrada y salidas", "n", "", ancho=720, alto=250)
p1.line("n", "x", source=s, color=pb.GRIS_CLARO, line_width=1, legend_label="x[n]")
p1.line("n", "limpia", source=s, color=pb.GRIS, line_width=1.5, line_dash="dotted", legend_label="señal sin ruido")
p1.line("n", "y1", source=s, color=pb.ROJO, line_width=2, legend_label="filtro causal (una pasada)")
p1.line("n", "y2", source=s, color=pb.AZUL, line_width=2, legend_label="fase cero (ida y vuelta)")
pb.leyenda(p1, "below")
p2 = pb.figura("Módulo", "Ω (rad/muestra)", "", ancho=330, alto=210, x_range=(0, 3.1416))
p2.line("W", "m1", source=H, color=pb.ROJO, line_width=2, legend_label="|H|")
p2.line("W", "m2", source=H, color=pb.AZUL, line_width=2, legend_label="|H|² (ida y vuelta)")
pb.leyenda(p2, "below")
p3 = pb.figura("Fase (rad)", "Ω (rad/muestra)", "", ancho=330, alto=210, x_range=(0, 3.1416))
p3.line("W", "f1", source=H, color=pb.ROJO, line_width=2, legend_label="∠H (causal)")
p3.line(x=[0, 3.1416], y=[0, 0], color=pb.AZUL, line_width=2, legend_label="fase cero")
pb.leyenda(p3, "below")

senal = pb.selector("Señal", ["Pulsos con ruido", "Escalones con ruido", "ECG simulado con ruido"])
N = pb.deslizador("Orden del Butterworth", 1, 10, 4, 1)
Wc = pb.deslizador("Ωc / π (corte)", 0.02, 0.5, 0.08, 0.01)
A = pb.deslizador("Desviación del ruido", 0, 0.5, 0.15, 0.01)
info = Div(text="", width=240)

cb = pb.js("""
    const L = 400, n = enteros(0, L - 1), r = ruido(L, 3);
    let limpia;
    if (senal.value.startsWith("Pulsos")) limpia = n.map(k => Math.exp(-(((k - 120) / 10) ** 2)) + 0.7 * Math.exp(-(((k - 260) / 6) ** 2)));
    else if (senal.value.startsWith("Escalones")) limpia = n.map(k => k > 100 && k < 250 ? 1 : (k >= 250 && k < 320 ? 0.4 : 0));
    else limpia = n.map(k => { const t = k % 100; return Math.exp(-(((t - 40) / 2.5) ** 2)) - 0.15 * Math.exp(-(((t - 36) / 2) ** 2))
                                                + 0.25 * Math.exp(-(((t - 70) / 7) ** 2)); });
    const x = limpia.map((v, k) => v + A.value * r[k]);
    const [z, p, k] = butter_z(N.value, Wc.value * PI), [b, a] = ba(z, p, k);
    const y1 = filtrar(b, a, x), y2 = filtrar(b, a, filtrar(b, a, x).reverse()).reverse();
    s.data = {n: n, x: x, limpia: limpia, y1: y1, y2: y2};
    const W = rango(0, PI, 500), Hc = W.map(w => zpk(z, p, k, cexp([0, w])));
    H.data = {W: W, m1: Hc.map(cabs), m2: Hc.map(h => cabs(h) ** 2), f1: desenrollar(Hc.map(h => Math.atan2(h[1], h[0])))};
    // Retardo de grupo en continua del filtro causal
    const d = 1e-3, g = -(Math.atan2(...zpk(z, p, k, cexp([0, d])).slice().reverse()) - 0) / d;
    info.text = `<p>Una pasada: retardo de unas ${g.toFixed(1)} muestras a bajas frecuencias y distorsión de fase cerca del corte.</p>` +
                `<p>Ida y vuelta: H(e^jΩ)·H*(e^jΩ) = |H|², fase nula y atenuación doble (en Ωc, −6 dB en lugar de −3 dB).</p>` +
                `<p>No es causal: necesita la señal completa (procesado fuera de línea).</p>`;
""", s=s, H=H, senal=senal, N=N, Wc=Wc, A=A, info=info)
pb.conectar(cb, senal, N, Wc, A)

pb.pagina(__file__, "Filtrado de fase cero", tema=4,
          descripcion="Si la señal está grabada, se puede filtrar hacia delante, invertir en el tiempo, filtrar otra vez "
                      "e invertir de nuevo (filtfilt). El resultado tiene respuesta |H|² y fase nula: no hay retardo ni "
                      "distorsión de fase, a cambio de no ser causal.",
          controles=[senal, N, Wc, A, info], graficas=[p1, [p2, p3]], inicio=cb,
          referencia="Transparencias T4-05, filtros especiales · Apuntes del Tema 4, sección 5")
