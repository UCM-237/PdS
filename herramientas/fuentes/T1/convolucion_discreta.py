"""T1 · Convolución discreta: suma de productos de x[k] y h[n − k]."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div, Span
import pds_bokeh as pb

SECUENCIAS = ["Pulso de 4 muestras", "Pulso de 6 muestras", "Rampa 1, 2, 3, 4", "Exponencial 0,8^n u[n]",
              "δ[n] + δ[n − 3]", "Media móvil de 3 (1/3)", "Diferencia δ[n] − δ[n − 1]"]

sen = ColumnDataSource(dict(k=[], x=[], h=[], p=[]))
sal = ColumnDataSource(dict(n=[], y=[]))
act = ColumnDataSource(dict(n=[], y=[]))

p1 = pb.figura("x[k] y h[n − k]", "k", "", ancho=620, alto=170, x_range=(-8, 20))
pb.tallos(p1, "k", "x", sen, color=pb.AZUL, legend_label="x[k]")
pb.tallos(p1, "k", "h", sen, color=pb.ROJO, legend_label="h[n − k]", marker="square")
p2 = pb.figura("x[k] h[n − k]: su suma es y[n]", "k", "", ancho=620, alto=150, x_range=p1.x_range)
pb.tallos(p2, "k", "p", sen, color=pb.VERDE)
p3 = pb.figura("y[n] = (x * h)[n]", "n", "y[n]", ancho=620, alto=170, x_range=p1.x_range)
pb.tallos(p3, "n", "y", sal, color=pb.GRIS_CLARO, legend_label="y[n] completa")
pb.tallos(p3, "n", "y", act, color=pb.AZUL, legend_label="calculada hasta n")
marca = Span(location=0, dimension="height", line_color=pb.NARANJA, line_dash="dashed")
for q in (p1, p2, p3):
    q.add_layout(marca)
for q in (p1, p3):
    pb.leyenda(q, "right")

sx = pb.selector("Señal x[n]", SECUENCIAS, SECUENCIAS[0])
sh = pb.selector("Respuesta al impulso h[n]", SECUENCIAS, SECUENCIAS[3])
n = pb.deslizador("n (desplazamiento)", -6, 18, 2, 1)
info = Div(text="", width=240)

cb = pb.js("""
    function forma(nombre, m) {
        if (nombre.startsWith("Pulso de 4")) return (m >= 0 && m < 4) ? 1 : 0;
        if (nombre.startsWith("Pulso de 6")) return (m >= 0 && m < 6) ? 1 : 0;
        if (nombre.startsWith("Rampa")) return (m >= 0 && m < 4) ? m + 1 : 0;
        if (nombre.startsWith("Exponencial")) return (m >= 0 && m < 25) ? Math.pow(0.8, m) : 0;
        if (nombre.startsWith("δ[n] +")) return (m === 0 || m === 3) ? 1 : 0;
        if (nombre.startsWith("Media")) return (m >= 0 && m < 3) ? 1 / 3 : 0;
        return m === 0 ? 1 : (m === 1 ? -1 : 0);
    }
    const k = enteros(-8, 20), N = n.value;
    const x = k.map(m => forma(sx.value, m)), h = k.map(m => forma(sh.value, N - m));
    const p = x.map((v, i) => v * h[i]);
    sen.data = {k: k, x: x, h: h, p: p};
    const y = k.map(nn => { let s = 0; for (let i = 0; i < k.length; i++) s += x[i] * forma(sh.value, nn - k[i]); return s; });
    sal.data = {n: k, y: y};
    const j = k.indexOf(N);
    act.data = {n: k.slice(0, j + 1), y: y.slice(0, j + 1)};
    marca.location = N;
    const terminos = p.map((v, i) => [v, i]).filter(a => Math.abs(a[0]) > 1e-12)
        .map(a => `${x[a[1]].toFixed(2)}·${h[a[1]].toFixed(2)}`);
    info.text = `<p>y[${N}] = ${terminos.length ? terminos.join(" + ") : "0"} = <b>${y[j].toFixed(3)}</b></p>`;
""", sen=sen, sal=sal, act=act, marca=marca, sx=sx, sh=sh, n=n, info=info)
pb.conectar(cb, sx, sh, n)

pb.pagina(__file__, "Convolución discreta", tema=1,
          descripcion="y[n] = Σ x[k] h[n − k]. Para cada n se invierte h, se desplaza n muestras, "
                      "se multiplica muestra a muestra por x y se suma. Si x tiene L muestras y h "
                      "tiene P, y tiene L + P − 1.",
          controles=[sx, sh, n, info], graficas=[p1, p2, p3], inicio=cb,
          referencia="Transparencias T1-02, «Convolución discreta: ejemplo» · Apuntes del Tema 1, sección 5")
