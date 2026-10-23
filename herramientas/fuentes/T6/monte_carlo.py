"""T6 · Método de Monte Carlo: estimar una esperanza con la media de N muestras."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

NR = 5

Pt = ColumnDataSource(dict(x=[], y=[], color=[]))
Gf = ColumnDataSource(dict(x=[], y=[]))
Es = ColumnDataSource(dict(n=[], e=[], lo=[], hi=[], v=[]))
Er = ColumnDataSource(dict(xs=[], ys=[]))
Ref = ColumnDataSource(dict(n=[], s=[]))

p1 = pb.figura("Muestras (las 2000 primeras)", "x", "", ancho=300, alto=300)
p1.line("x", "y", source=Gf, color=pb.AZUL, line_width=2)
p1.scatter("x", "y", source=Pt, color="color", size=3, alpha=0.6)
p2 = pb.figura("Estimación con las n primeras muestras y franja ±2σ̂/√n", "n", "", ancho=460, alto=300,
               x_axis_type="log", x_range=(10, 1e5))
p2.varea("n", "lo", "hi", source=Es, fill_color=pb.AZUL, fill_alpha=0.15)
p2.line("n", "e", source=Es, color=pb.AZUL, line_width=1.6, legend_label="estimación")
p2.line("n", "v", source=Es, color=pb.ROJO, line_width=2, line_dash="dashed", legend_label="valor exacto")
pb.leyenda(p2, "below")
p3 = pb.figura(f"|error| de {NR} realizaciones frente a σ/√n", "n", "|error|", ancho=380, alto=300,
               x_axis_type="log", y_axis_type="log", x_range=(10, 1e5))
p3.multi_line("xs", "ys", source=Er, color=pb.GRIS, line_width=1, alpha=0.8)
p3.line("n", "s", source=Ref, color=pb.ROJO, line_width=2.5, legend_label="σ/√n")
pb.leyenda(p3, "below")

prob = pb.selector("Qué se estima", ["π (puntos en un cuarto de círculo)", "E{cos X} con X ~ N(0, 1)",
                                     "∫₀¹ e^(−x²) dx con X ~ U[0, 1]", "P(X > 3) con X ~ N(0, 1)",
                                     "P(X > 3) por muestreo de importancia"])
N = pb.selector("N (muestras)", ["1000", "10000", "100000"], "10000")
semilla = pb.deslizador("Realización", 1, 50, 1, 1)
info = Div(text="", width=250)

cb = pb.js("""
    const Nn = parseInt(N.value), pr = prob.value, Phi3 = 0.0013498980316301;
    // Cada problema da una muestra (x, y) para dibujar y el valor h que se promedia
    let muestra, verdad, sigma, graf = {x: [], y: []};
    if (pr.startsWith("π")) { verdad = PI; sigma = 4 * Math.sqrt(PI / 4 * (1 - PI / 4));
        muestra = g => { const x = g(), y = g(); return [x, y, x * x + y * y <= 1 ? 4 : 0]; };
        const t = rango(0, PI / 2, 100); graf = {x: t.map(Math.cos), y: t.map(Math.sin)}; }
    else if (pr.startsWith("E{cos")) { verdad = Math.exp(-0.5); sigma = Math.sqrt(0.5 * (1 + Math.exp(-2)) - Math.exp(-1));
        muestra = g => { const x = gauss(g); return [x, Math.cos(x), Math.cos(x)]; };
        const t = rango(-4, 4, 200); graf = {x: t, y: t.map(Math.cos)}; }
    else if (pr.startsWith("∫")) { verdad = 0.746824132812427; sigma = Math.sqrt(0.5981440066613 - verdad * verdad);
        muestra = g => { const x = g(); return [x, Math.exp(-x * x), Math.exp(-x * x)]; };
        const t = rango(0, 1, 100); graf = {x: t, y: t.map(v => Math.exp(-v * v))}; }
    else if (pr.endsWith("importancia")) { verdad = Phi3;
        // Y ~ N(3, 1); se promedia 1{Y > 3}·φ(Y)/φ(Y − 3) = 1{Y > 3}·e^{4,5 − 3Y}
        sigma = Math.sqrt(6.1721779047e-6);
        muestra = g => { const y = 3 + gauss(g); return [y, 0, y > 3 ? Math.exp(4.5 - 3 * y) : 0]; }; }
    else { verdad = Phi3; sigma = Math.sqrt(Phi3 * (1 - Phi3));
        muestra = g => { const x = gauss(g); return [x, 0, x > 3 ? 1 : 0]; }; }
    if (pr.startsWith("P(")) { const t = rango(-4, 7, 300); graf = {x: t, y: t.map(v => Math.exp(-v * v / 2) / Math.sqrt(2 * PI))}; }
    const marcas = enteros(0, 299).map(i => Math.round(Math.pow(10, 1 + Math.log10(Nn / 10) * i / 299))).filter((v, i, a) => !i || v !== a[i - 1]);
    const err = [];
    let est = null;
    for (let r = 0; r < NR; r++) {
        const g = generador(1000 * semilla.value + r);
        let s = 0, s2 = 0, j = 0; const e = [], lo = [], hi = [], pts = [];
        for (let n = 1; n <= Nn; n++) {
            const [x, y, h] = muestra(g); s += h; s2 += h * h;
            if (r === 0 && n <= 2000) pts.push([x, pr.startsWith("P(") ? 0.02 * g() : y, h]);
            if (n === marcas[j]) { const m = s / n, sd = Math.sqrt(Math.max(s2 / n - m * m, 0)); e.push(m); lo.push(m - 2 * sd / Math.sqrt(n)); hi.push(m + 2 * sd / Math.sqrt(n)); j++; }
        }
        err.push(e.map(v => Math.max(Math.abs(v - verdad), 1e-12)));
        if (r === 0) { est = {e, lo, hi, s, s2, pts}; }
    }
    const col = est.pts.map(p => (!pr.startsWith("E") && !pr.startsWith("∫") && p[2] ? pb_ROJO : pb_AZUL));
    Pt.data = {x: est.pts.map(p => p[0]), y: est.pts.map(p => p[1]), color: col};
    Gf.data = graf;
    Es.data = {n: marcas, e: est.e, lo: est.lo, hi: est.hi, v: marcas.map(() => verdad)};
    const mN = est.s / Nn;
    Er.data = {xs: err.map(() => marcas), ys: err};
    Ref.data = {n: marcas, s: marcas.map(n => sigma / Math.sqrt(n))};
    p2.x_range.end = Nn; p3.x_range.end = Nn;
    const ea = Math.abs(mN - verdad);
    info.text = `<p>Valor exacto: ${verdad.toPrecision(6)}</p><p>Estimación con N = ${Nn}: ${mN.toPrecision(6)}</p>` +
        `<p>Error: ${ea.toExponential(2)}; error típico σ/√N = ${(sigma / Math.sqrt(Nn)).toExponential(2)}</p>` +
        `<p>Error relativo típico: ${(100 * sigma / Math.sqrt(Nn) / verdad).toFixed(2)} %</p>` +
        (pr.startsWith("P(X > 3) con") ? `<p>Solo una muestra de cada ${Math.round(1 / Phi3)} cae en la cola: hacen falta muchas para acertar</p>` : "") +
        (pr.endsWith("importancia") ? `<p>Se muestrea donde está la cola y se corrige con el peso φ(y)/φ(y − 3). La varianza baja unas ${Math.round(Phi3 * (1 - Phi3) / (sigma * sigma))} veces</p>` : "");
""", Pt=Pt, Gf=Gf, Es=Es, Er=Er, Ref=Ref, p2=p2, p3=p3, prob=prob, N=N, semilla=semilla, info=info, NR=NR,
   pb_ROJO=pb.ROJO, pb_AZUL=pb.AZUL)
pb.conectar(cb, prob, N, semilla)

pb.pagina(__file__, "Método de Monte Carlo", tema=6,
          descripcion="Para calcular E{h(X)} basta con generar N muestras de X y promediar h. La media es insesgada y su "
                      "desviación típica es σ/√N: para ganar una cifra decimal hay que multiplicar N por 100. Cuando el "
                      "suceso es raro, el muestreo de importancia genera muestras donde importa y las pondera.",
          controles=[prob, N, semilla, info], graficas=[[p1, p2], [p3]], inicio=cb,
          referencia="Transparencias T6-01, generación de muestras y Monte Carlo · Apuntes del Tema 6, sección 1")
