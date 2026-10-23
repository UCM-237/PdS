"""T3 · Convolución por bloques: solapamiento-suma y solapamiento-almacenamiento."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

X = ColumnDataSource(dict(n=[], x=[]))
Bq = ColumnDataSource(dict(x0=[], x1=[], y=[], color=[]))
Hh = ColumnDataSource(dict(n=[], h=[]))
Pl = ColumnDataSource(dict(xs=[], ys=[], color=[], alfa=[], trazo=[]))
Pp = ColumnDataSource(dict(n=[], v=[], color=[], alfa=[]))
Y = ColumnDataSource(dict(n=[], y=[], d=[]))

p1 = pb.figura("Entrada x[n] y bloques en que se divide", "n", "", ancho=560, alto=170)
pb.tallos(p1, "n", "x", X, color=pb.AZUL, size=4)
p1.segment(x0="x0", x1="x1", y0="y", y1="y", source=Bq, color="color", line_width=5)
p2 = pb.figura("Respuesta al impulso h[n]", "n", "", ancho=170, alto=170)
pb.tallos(p2, "n", "h", Hh, color=pb.VERDE, size=4)
p3 = pb.figura("Salidas parciales de cada bloque", "n", "", ancho=760, alto=190)
p3.multi_line("xs", "ys", source=Pl, color="color", line_alpha="alfa", line_dash="trazo", line_width=2)
p3.scatter("n", "v", source=Pp, color="color", alpha="alfa", size=5)
p4 = pb.figura("Salida y[n] por bloques (puntos) y convolución directa (línea)", "n", "", ancho=760, alto=170)
p4.line("n", "d", source=Y, color=pb.GRIS_CLARO, line_width=3)
pb.tallos(p4, "n", "y", Y, color=pb.ROJO, size=4)
for p in (p1, p3, p4):
    p.x_range = p1.x_range

metodo = pb.selector("Método", ["Solapamiento-suma", "Solapamiento-almacenamiento"])
Lb = pb.deslizador("L (muestras nuevas por bloque)", 4, 40, 16, 1)
P = pb.deslizador("P (longitud de h[n])", 2, 16, 6, 1)
tipo = pb.selector("Respuesta al impulso", ["Media móvil", "Exponencial decreciente", "Diferenciador suavizado"])
info = Div(text="", width=300)

cb = pb.js("""
    const Nx = 80, l = Lb.value, p = P.value, N = l + p - 1, r = ruido(Nx, 3), n = enteros(0, Nx - 1);
    const x = n.map(k => Math.sin(2 * PI * k / 29) + 0.5 * Math.sin(2 * PI * k / 7) + 0.2 * r[k]);
    const h = enteros(0, p - 1).map(k => tipo.value === "Media móvil" ? 1 / p
                   : tipo.value.startsWith("Exp") ? 0.3 * 0.75 ** k : (k < p / 2 ? 1 : -1) * 2 / p);
    const d = conv(x, h), Ny = d.length, B = Math.ceil(Nx / l), oa = metodo.value === "Solapamiento-suma";
    // Convolución circular de N puntos (lo que haría la FFT de N puntos)
    const circ = (a, b) => enteros(0, N - 1).map(k => { let s = 0; for (let j = 0; j < N; j++) s += (a[j] || 0) * (b[mod(k - j, N)] || 0); return s; });
    const cols = [pb_AZUL, pb_NARANJA, pb_VERDE, pb_ROJO];
    const y = new Array(Ny).fill(0), bq = {x0: [], x1: [], y: [], color: []}, pl = {xs: [], ys: [], color: [], alfa: [], trazo: []}, pp = {n: [], v: [], color: [], alfa: []};
    const tramo = (ns, vs, c, a, t) => { pl.xs.push(ns); pl.ys.push(vs); pl.color.push(c); pl.alfa.push(a); pl.trazo.push(t);
                                         ns.forEach((v, i) => { pp.n.push(v); pp.v.push(vs[i]); pp.color.push(c); pp.alfa.push(a); }); };
    const ymin = Math.min(...x) - 0.25;
    // En solapamiento-almacenamiento hace falta un bloque más para llegar al final de la convolución lineal
    const Bt = oa ? B : Math.ceil(Ny / l);
    for (let b = 0; b < Bt; b++) {
        const c = cols[b % 4];
        if (oa) {
            // Bloque de L muestras, completado con ceros hasta N; su salida (N muestras) se suma desplazada b·L
            const xb = x.slice(b * l, (b + 1) * l), yb = circ(xb, h), ini = b * l;
            yb.forEach((v, i) => { if (ini + i < Ny) y[ini + i] += v; });
            bq.x0.push(ini); bq.x1.push(Math.min(ini + l, Nx) - 1); bq.y.push(ymin - 0.2 * (b % 2)); bq.color.push(c);
            tramo(yb.map((_, i) => ini + i), yb, c, 0.9, "solid");
        } else {
            // Bloque de N muestras que solapa P − 1 con el anterior; de su convolución circular se descartan las P − 1 primeras
            const ini = b * l - (p - 1), xb = enteros(ini, ini + N - 1).map(k => k >= 0 && k < Nx ? x[k] : 0), yb = circ(xb, h);
            for (let i = p - 1; i < N; i++) if (ini + i < Ny) y[ini + i] = yb[i];
            bq.x0.push(Math.max(ini, 0)); bq.x1.push(Math.min(ini + N, Nx) - 1); bq.y.push(ymin - 0.2 * (b % 2)); bq.color.push(c);
            if (p > 1) tramo(enteros(ini, ini + p - 2), yb.slice(0, p - 1), c, 0.3, "dashed");
            tramo(enteros(ini + p - 1, ini + N - 1), yb.slice(p - 1), c, 0.9, "solid");
        }
    }
    X.data = {n: n, x: x}; Bq.data = bq; Hh.data = {n: enteros(0, p - 1), h: h}; Pl.data = pl; Pp.data = pp;
    Y.data = {n: enteros(0, Ny - 1), y: y, d: d};
    const err = Math.max(...y.map((v, i) => Math.abs(v - d[i])));
    // Coste en productos complejos con FFT de tamaño potencia de 2 ≥ N
    const Nf = 2 ** Math.ceil(Math.log2(N)), lg = Math.log2(Nf), cfft = Bt * (Nf * lg + Nf) + Nf / 2 * lg;
    info.text = `<p>N = L + P − 1 = ${N} (FFT de ${Nf} puntos); ${Bt} bloques</p>` +
        (oa ? "<p>Cada bloque se completa con P − 1 ceros; las colas de salidas vecinas se solapan P − 1 muestras y se suman.</p>"
            : "<p>Cada bloque repite las P − 1 últimas muestras del anterior; en trazo discontinuo, las muestras con aliasing temporal que se descartan.</p>") +
        `<p>Diferencia máxima con la convolución directa: ${err.toExponential(1)}</p>` +
        `<p>Coste directo: ${Nx}·${p} = ${Nx * p} productos reales.</p>` +
        `<p>Coste con FFT: unos ${Math.round(cfft)} productos complejos (${(cfft / Nx).toFixed(1)} por muestra). Compensa cuando P es grande.</p>`;
""", X=X, Bq=Bq, Hh=Hh, Pl=Pl, Pp=Pp, Y=Y, metodo=metodo, Lb=Lb, P=P, tipo=tipo, info=info,
   pb_AZUL=pb.AZUL, pb_NARANJA=pb.NARANJA, pb_VERDE=pb.VERDE, pb_ROJO=pb.ROJO)
pb.conectar(cb, metodo, Lb, P, tipo)

pb.pagina(__file__, "Convolución por bloques", tema=3,
          descripcion="Para filtrar una señal larga con la FFT se trocea en bloques. En solapamiento-suma, cada bloque de L "
                      "muestras se convoluciona con h[n] y las salidas, de L + P − 1 muestras, se suman donde se solapan. En "
                      "solapamiento-almacenamiento, los bloques de entrada se solapan P − 1 muestras y de cada convolución "
                      "circular se descartan las P − 1 primeras, que tienen aliasing temporal. Los dos dan la convolución lineal exacta.",
          controles=[metodo, tipo, Lb, P, info], graficas=[[p1, p2], p3, p4], inicio=cb,
          referencia="Transparencias T3-04, FFT y convolución rápida · Apuntes del Tema 3, sección 5")
