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
punto = ColumnDataSource(dict(n=[], y=[]))
K0, K1 = -8, 20  # eje común de k y de n; el desplazamiento recorre el mismo rango

# Arriba: las dos secuencias y su producto (barras verdes), cuya suma es y[n]
p1 = pb.figura("x[k], h[n − k] y su producto: la suma de las barras verdes es y[n]", "k", "",
               ancho=None, alto=210, x_range=(K0, K1))
p1.vbar(x="k", top="p", width=0.7, source=sen, fill_color=pb.VERDE, fill_alpha=0.30,
        line_color=None, legend_label="x[k] h[n − k]")
pb.tallos(p1, "k", "x", sen, color=pb.AZUL, legend_label="x[k]")
pb.tallos(p1, "k", "h", sen, color=pb.ROJO, legend_label="h[n − k]", marker="square", size=5)
# Abajo: la salida completa y lo calculado hasta la muestra actual
p2 = pb.figura("y[n] = (x ∗ h)[n]", "n", "y[n]", ancho=None, alto=190, x_range=p1.x_range)
pb.tallos(p2, "n", "y", sal, color=pb.GRIS_CLARO, legend_label="y[n] completa")
pb.tallos(p2, "n", "y", act, color=pb.AZUL, legend_label="calculada hasta n")
p2.scatter("n", "y", source=punto, color=pb.NARANJA, size=9)
marca = Span(location=0, dimension="height", line_color=pb.NARANJA, line_dash="dashed")
for q in (p1, p2):
    q.add_layout(marca)
    pb.leyenda(q, "top_right")

sx = pb.selector("Señal x[n]", SECUENCIAS, SECUENCIAS[0])
sh = pb.selector("Respuesta al impulso h[n]", SECUENCIAS, SECUENCIAS[3])
n = pb.deslizador("Desplazamiento n", K0, K1, 2, 1)
info = pb.info()

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
    const k = enteros(K0, K1), N = n.value;
    const x = k.map(m => forma(sx.value, m)), h = k.map(m => forma(sh.value, N - m));
    const p = x.map((v, i) => v * h[i]);
    sen.data = {k: k, x: x, h: h, p: p};
    const y = k.map(nn => { let s = 0; for (let i = 0; i < k.length; i++) s += x[i] * forma(sh.value, nn - k[i]); return s; });
    sal.data = {n: k, y: y};
    const j = k.indexOf(N);
    act.data = {n: k.slice(0, j + 1), y: y.slice(0, j + 1)};
    punto.data = {n: [N], y: [y[j]]};
    marca.location = N;
    const terminos = p.map((v, i) => [v, i]).filter(a => Math.abs(a[0]) > 1e-12)
        .map(a => `${x[a[1]].toFixed(2)}·${h[a[1]].toFixed(2)}`);
    info.text = `<p>y[${N}] = ${terminos.length ? terminos.join(" + ") : "0"} = <b>${y[j].toFixed(3)}</b></p>`;
""", sen=sen, sal=sal, act=act, marca=marca, sx=sx, sh=sh, n=n, info=info,
   punto=punto, K0=K0, K1=K1)
pb.conectar(cb, sx, sh, n)

pb.pagina_panel(__file__, "Convolución discreta", tema=1,
                descripcion=r"$y[n] = \sum_k x[k]\,h[n-k]$. Para cada $n$ se invierte $h$, se desplaza "
                            r"$n$ muestras, se multiplica muestra a muestra por $x$ y se suma. Si $x$ tiene "
                            r"$L$ muestras y $h$ tiene $P$, $y$ tiene $L + P - 1$.",
                controles=[sx, sh],
                graficas=[pb.grafica(p1, n, info), p2], inicio=cb,
                referencia="Transparencias T1-02, «Convolución discreta: ejemplo» · Apuntes del Tema 1, sección 5")
