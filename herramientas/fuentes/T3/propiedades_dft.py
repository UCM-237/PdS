"""T3 · Propiedades de la DFT con una secuencia editable."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

N0 = 8
x = ColumnDataSource(dict(n=list(range(N0)), x=[1, 0.8, 0.5, 0.2, 0, 0, 0, 0]))
Y = ColumnDataSource(dict(n=[], re=[], im=[]))
F = ColumnDataSource(dict(k=[], mx=[], my=[], fx=[], fy=[]))

p1 = pb.figura("x[n] (haz clic para cambiarla) y y[n] tras la operación", "n", "", ancho=420, alto=230, y_range=(-1.3, 1.3))
pb.tallos(p1, "n", "x", x, color=pb.AZUL, legend_label="x[n]")
p1.scatter("n", "re", source=Y, marker="square", size=11, line_color=pb.NARANJA, fill_color=None, line_width=2, legend_label="Re y[n]")
p1.scatter("n", "im", source=Y, marker="triangle", size=10, line_color=pb.VERDE, fill_color=None, line_width=2, legend_label="Im y[n]")
pb.leyenda(p1, "below")
p2 = pb.figura("Módulo |X[k]| y |Y[k]|", "k", "", ancho=300, alto=200)
pb.tallos(p2, "k", "mx", F, color=pb.AZUL)
p2.scatter("k", "my", source=F, marker="square", size=11, line_color=pb.NARANJA, fill_color=None, line_width=2)
p3 = pb.figura("Fase ∠X[k] y ∠Y[k] (rad)", "k", "", ancho=300, alto=200, y_range=(-3.5, 3.5))
pb.tallos(p3, "k", "fx", F, color=pb.AZUL)
p3.scatter("k", "fy", source=F, marker="square", size=11, line_color=pb.NARANJA, fill_color=None, line_width=2)

op = pb.selector("Operación", ["Desplazamiento circular x[((n − m))_N]", "Inversión circular x[((−n))_N]",
                               "Modulación e^(j2πln/N)·x[n]", "Parte par circular", "Parte impar circular"])
m = pb.deslizador("m o l", 0, N0 - 1, 2, 1)
info = Div(text="", width=240)

cb = pb.js("""
    const xs = x.data.x, N = xs.length, mm = m.value, n = enteros(0, N - 1);
    let yr, yi;
    if (op.value.startsWith("Desplaz")) { yr = n.map(k => xs[mod(k - mm, N)]); yi = n.map(() => 0); }
    else if (op.value.startsWith("Inversión")) { yr = n.map(k => xs[mod(-k, N)]); yi = n.map(() => 0); }
    else if (op.value.startsWith("Modul")) { yr = n.map(k => xs[k] * Math.cos(2 * PI * mm * k / N)); yi = n.map(k => xs[k] * Math.sin(2 * PI * mm * k / N)); }
    else { const s = op.value.includes("par circular") ? 1 : -1; yr = n.map(k => (xs[k] + s * xs[mod(-k, N)]) / 2); yi = n.map(() => 0); }
    Y.data = {n: n, re: yr, im: yi.map(v => Math.abs(v) < 1e-12 ? NaN : v)};
    const [Xr, Xi] = fft(xs), [Yr, Yi] = fft(yr, yi);
    const ang = (r, i) => Math.hypot(r, i) < 1e-9 ? 0 : Math.atan2(i, r);
    F.data = {k: n, mx: n.map(k => Math.hypot(Xr[k], Xi[k])), my: n.map(k => Math.hypot(Yr[k], Yi[k])),
              fx: n.map(k => ang(Xr[k], Xi[k])), fy: n.map(k => ang(Yr[k], Yi[k]))};
    // Lo que predice la propiedad, para comprobarlo
    const pred = n.map(k => {
        if (op.value.startsWith("Desplaz")) return cmul([Xr[k], Xi[k]], cexp([0, -2 * PI * k * mm / N]));
        if (op.value.startsWith("Inversión")) return [Xr[mod(-k, N)], Xi[mod(-k, N)]];
        if (op.value.startsWith("Modul")) return [Xr[mod(k - mm, N)], Xi[mod(k - mm, N)]];
        return op.value.includes("par circular") ? [Xr[k], 0] : [0, Xi[k]]; });
    const err = Math.max(...n.map(k => cabs(cres([Yr[k], Yi[k]], pred[k]))));
    const regla = {"Desplaz": `Y[k] = e^(−j2πkm/N)·X[k]: mismo módulo, la fase cambia −2πkm/N (m = ${mm})`,
        "Inversión": "Y[k] = X[((−k))_N], que para x real es X*[k]: mismo módulo, fase cambiada de signo",
        "Modul": `Y[k] = X[((k − l))_N]: el espectro se desplaza circularmente l = ${mm} posiciones`,
        "Parte par": "Y[k] = Re{X[k]}: la parte par circular de una señal real tiene DFT real",
        "Parte impar": "Y[k] = j·Im{X[k]}: la parte impar circular tiene DFT imaginaria pura"};
    const clave = Object.keys(regla).find(k => op.value.startsWith(k));
    const Ex = xs.reduce((s, v) => s + v * v, 0), EX = n.reduce((s, k) => s + Xr[k] ** 2 + Xi[k] ** 2, 0) / N;
    const simetrica = n.every(k => Math.abs(Xr[k] - Xr[mod(-k, N)]) < 1e-9 && Math.abs(Xi[k] + Xi[mod(-k, N)]) < 1e-9);
    info.text = `<p>${regla[clave]}.</p><p>Diferencia con la predicción: ${err.toExponential(1)}</p>` +
        `<p>Parseval: Σ|x[n]|² = ${Ex.toFixed(3)}; (1/N)·Σ|X[k]|² = ${EX.toFixed(3)}</p>` +
        `<p>x es real, así que X[((−k))_N] = X*[k]: |X| es simétrico y la fase antisimétrica respecto a k = N/2 ${simetrica ? "✓" : ""}.</p>`;
""", x=x, Y=Y, F=F, op=op, m=m, info=info)
pb.editable(p1, x, "n", "x", callback=cb)
pb.conectar(cb, op, m)

pb.pagina(__file__, "Propiedades de la DFT", tema=3,
          descripcion="Edita una secuencia de 8 muestras y aplícale una operación. En la DFT los índices son circulares (módulo N): "
                      "desplazar la secuencia cambia solo la fase, invertirla conjuga la DFT de una señal real y modularla desplaza "
                      "el espectro. La herramienta compara la DFT obtenida con la que predice cada propiedad.",
          controles=[op, m, info], graficas=[[p1, column(p2, p3)]], inicio=cb,
          referencia="Transparencias T3-02, propiedades de la DFT · Apuntes del Tema 3, sección 3")
