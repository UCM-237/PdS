"""T1 · Exponencial compleja discreta: periodicidad y frecuencias equivalentes."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

muestras = ColumnDataSource(dict(n=[], x=[]))
curva = ColumnDataSource(dict(t=[], x=[], sup=[], inf=[]))

p = pb.figura("x[n] = r^n · cos(Ωn + θ)", "n", "x[n]", ancho=620)
p.line("t", "sup", source=curva, color=pb.GRIS_CLARO, line_dash="dashed")
p.line("t", "inf", source=curva, color=pb.GRIS_CLARO, line_dash="dashed")
p.line("t", "x", source=curva, color=pb.GRIS_CLARO, legend_label="r^t · cos(Ωt + θ) entre muestras")
pb.tallos(p, "n", "x", muestras, legend_label="x[n]")
pb.leyenda(p, "below")

r = pb.deslizador("r", 0.8, 1.1, 1.0, 0.01)
w = pb.deslizador("Ω (rad/muestra)", 0, 6.28, 0.785, 0.005)
th = pb.deslizador("θ (rad)", -3.14, 3.14, 0, 0.05)
info = Div(text="", width=240)

cb = pb.js("""
    const n = enteros(0, 40), t = rango(0, 40, 801);
    const W = w.value, R = r.value, T = th.value;
    muestras.data = {n: n, x: n.map(k => Math.pow(R, k) * Math.cos(W * k + T))};
    curva.data = {t: t, x: t.map(k => Math.pow(R, k) * Math.cos(W * k + T)),
                  sup: t.map(k => Math.pow(R, k)), inf: t.map(k => -Math.pow(R, k))};
    // Periodicidad: Ω/2π = k/N con N pequeño
    const F = W / (2 * PI);
    let N = 0;
    for (let q = 1; q <= 64; q++) { if (Math.abs(F - Math.round(F * q) / q) < 0.0008) { N = q; break; } }
    const prin = W > PI ? W - 2 * PI : W;
    info.text = `<p>Ω/2π = ${F.toFixed(3)}</p>` +
        (N ? `<p>Periódica con N = ${N} muestras (Ω ≈ 2π·${Math.round(F * N)}/${N}).</p>`
           : `<p>Ω/2π no es un cociente de enteros pequeños: no es periódica en 0 ≤ N ≤ 64.</p>`) +
        `<p>Valor principal: Ω = ${prin.toFixed(3)} rad/muestra. Ω + 2π da la misma secuencia y, con θ = 0, también 2π − Ω.</p>`;
""", muestras=muestras, curva=curva, r=r, w=w, th=th, info=info)
pb.conectar(cb, r, w, th)

pb.pagina(__file__, "Exponencial compleja discreta", tema=1,
          descripcion="Al contrario que en tiempo continuo, cos(Ωn) solo es periódica si Ω/2π es "
                      "racional, y Ω y Ω + 2π dan la misma secuencia: la frecuencia discreta solo "
                      "tiene sentido en un intervalo de 2π. Cuanto más cerca de π, más rápido oscila.",
          controles=[r, w, th, info], graficas=[p], inicio=cb,
          referencia="Transparencias T1-01, «Exponencial compleja discreta» · Apuntes del Tema 1, sección 3")
