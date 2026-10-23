"""T6 · Teorema del límite central: la suma normalizada de n variables independientes."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

D1 = ColumnDataSource(dict(x=[], y=[]))
D1p = ColumnDataSource(dict(x=[], y=[]))
Hi = ColumnDataSource(dict(x=[], top=[], ancho=[]))
Ex = ColumnDataSource(dict(x=[], y=[]))
Exp_ = ColumnDataSource(dict(x=[], y=[]))
Ga = ColumnDataSource(dict(x=[], y=[]))

p1 = pb.figura("Densidad (o probabilidades) de cada X_i", "x", "", ancho=300, alto=260)
p1.line("x", "y", source=D1, color=pb.AZUL, line_width=2)
p1.segment(x0="x", y0=0, x1="x", y1="y", source=D1p, color=pb.AZUL, line_width=3)
p2 = pb.figura("Suma normalizada Z_n: histograma, densidad exacta y N(0, 1)", "z", "densidad", ancho=460, alto=260,
               x_range=(-4, 4))
p2.vbar(x="x", top="top", width="ancho", source=Hi, fill_color=pb.GRIS_CLARO, line_color="white")
p2.line("x", "y", source=Ga, color=pb.ROJO, line_width=2, legend_label="N(0, 1)")
p2.line("x", "y", source=Ex, color=pb.AZUL, line_width=1.8, line_dash="dashed", legend_label="exacta")
p2.scatter("x", "y", source=Exp_, color=pb.AZUL, size=5, legend_label="exacta")
pb.leyenda(p2, "below")

dist = pb.selector("Distribución de cada X_i", ["Uniforme U[0, 1]", "Exponencial (λ = 1)", "Bernoulli (p = 0,2)",
                                               "Dado (1 a 6)", "Cauchy (sin media ni varianza)"])
n = pb.deslizador("n (variables que se suman)", 1, 50, 1, 1)
N = pb.deslizador("Número de sumas simuladas", 1000, 50000, 10000, 1000)
info = Div(text="", width=250)

cb = pb.js("""
    const g = generador(11), d = dist.value, k = n.value, Ns = N.value;
    let gen, mu, sg, discreta = false, vals = [], p = [];
    if (d.startsWith("Uniforme")) { gen = () => g(); mu = 0.5; sg = Math.sqrt(1 / 12); D1.data = {x: [-0.5, 0, 0, 1, 1, 1.5], y: [0, 0, 1, 1, 0, 0]}; D1p.data = {x: [], y: []}; }
    else if (d.startsWith("Exp")) { gen = () => -Math.log(1 - g()); mu = 1; sg = 1; const xx = rango(0, 6, 200); D1.data = {x: xx, y: xx.map(v => Math.exp(-v))}; D1p.data = {x: [], y: []}; }
    else if (d.startsWith("Bern")) { discreta = true; vals = [0, 1]; p = [0.8, 0.2]; }
    else if (d.startsWith("Dado")) { discreta = true; vals = [1, 2, 3, 4, 5, 6]; p = new Array(6).fill(1 / 6); }
    else { gen = () => Math.tan(PI * (g() - 0.5)); mu = 0; sg = 1; const xx = rango(-8, 8, 300); D1.data = {x: xx, y: xx.map(v => 1 / (PI * (1 + v * v)))}; D1p.data = {x: [], y: []}; }
    if (discreta) {
        mu = vals.reduce((s, v, i) => s + v * p[i], 0); sg = Math.sqrt(vals.reduce((s, v, i) => s + (v - mu) ** 2 * p[i], 0));
        gen = () => { const u = g(); let a = 0, i = 0; while (i < vals.length - 1 && u >= (a += p[i])) i++; return vals[i]; };
        D1.data = {x: [], y: []}; D1p.data = {x: vals, y: p};
    }
    const cauchy = d.startsWith("Cauchy");
    // Z_n = (S_n − nμ)/(√n σ); para Cauchy, que no tiene varianza, se muestra la media S_n/n
    const z = [];
    for (let i = 0; i < Ns; i++) { let s = 0; for (let j = 0; j < k; j++) s += gen(); z.push(cauchy ? s / k : (s - k * mu) / (Math.sqrt(k) * sg)); }
    const zz = rango(-4, 4, 400);
    Ga.data = {x: zz, y: zz.map(v => Math.exp(-v * v / 2) / Math.sqrt(2 * PI))};
    Ex.data = {x: [], y: []}; Exp_.data = {x: [], y: []};
    if (discreta) {
        // Probabilidades exactas de la suma (convolución de las de cada variable), en la red de Z_n
        let q = [1]; const v0 = vals[0], paso = vals[1] - vals[0], pp = p;
        for (let j = 0; j < k; j++) { const r = new Array(q.length + pp.length - 1).fill(0); q.forEach((a, i) => pp.forEach((b, l) => r[i + l] += a * b)); q = r; }
        const delta = paso / (Math.sqrt(k) * sg), zs = q.map((_, i) => (k * v0 + i * paso - k * mu) / (Math.sqrt(k) * sg));
        const sel = zs.map((v, i) => i).filter(i => Math.abs(zs[i]) <= 4.2);
        Exp_.data = {x: sel.map(i => zs[i]), y: sel.map(i => q[i] / delta)};
        const cnt = new Map(); for (const v of z) { const i = Math.round((v - zs[0]) / delta); cnt.set(i, (cnt.get(i) || 0) + 1); }
        Hi.data = {x: sel.map(i => zs[i]), top: sel.map(i => (cnt.get(i) || 0) / (Ns * delta)), ancho: sel.map(() => 0.9 * Math.min(delta, 0.5))};
    } else {
        const h = histo(z, -4, 4, 64); Hi.data = {x: h.c, top: h.d, ancho: h.c.map(() => h.ancho)};
        if (d.startsWith("Uniforme")) {
            // Densidad de la suma de k uniformes por convolución numérica, cambiada de escala
            const dx = 0.01, base = new Array(100).fill(1); let q = base.slice();
            for (let j = 1; j < k; j++) { const r = new Array(q.length + 99).fill(0); for (let i = 0; i < q.length; i++) { const a = q[i] * dx; for (let l = 0; l < 100; l++) r[i + l] += a; } q = r; }
            const sc = Math.sqrt(k) * sg, xs = q.map((_, i) => ((i + 0.5 * k) * dx - k * mu) / sc);
            const sel = xs.map((v, i) => i).filter(i => Math.abs(xs[i]) <= 4 && i % 4 === 0);
            Ex.data = {x: sel.map(i => xs[i]), y: sel.map(i => q[i] * sc)};
        } else if (d.startsWith("Exp")) {
            // La suma de k exponenciales es una gamma: f(s) = s^(k−1) e^(−s)/(k − 1)!
            let lf = 0; for (let j = 2; j < k; j++) lf += Math.log(j);
            Ex.data = {x: zz, y: zz.map(v => { const s = k + Math.sqrt(k) * v; return s <= 0 ? 0 : Math.sqrt(k) * Math.exp((k - 1) * Math.log(s) - s - lf); })};
        } else Ex.data = {x: zz, y: zz.map(v => 1 / (PI * (1 + v * v)))};
    }
    const m = media(z), v = varianza(z), sk = z.reduce((a, t) => a + ((t - m) / Math.sqrt(v)) ** 3, 0) / Ns;
    const dentro = z.filter(t => Math.abs(t) <= 1).length / Ns, colas = z.filter(t => Math.abs(t) > 3).length / Ns;
    info.text = (cauchy ? "<p>Cauchy no tiene varianza: se representa la media S<sub>n</sub>/n, que es Cauchy para todo n y no se concentra.</p>"
                        : `<p>μ = ${mu.toFixed(3)}, σ = ${sg.toFixed(3)}; Z<sub>n</sub> = (S<sub>n</sub> − nμ)/(√n σ)</p>`) +
        `<p>Media de las muestras: ${m.toFixed(3)}; varianza ${v.toFixed(3)}</p>` +
        `<p>Asimetría: ${sk.toFixed(3)} (0 en la gaussiana)</p>` +
        `<p>P(|Z| ≤ 1): ${dentro.toFixed(3)} (0,683 en la gaussiana); P(|Z| &gt; 3): ${colas.toFixed(4)} (0,0027)</p>`;
""", D1=D1, D1p=D1p, Hi=Hi, Ex=Ex, Exp_=Exp_, Ga=Ga, dist=dist, n=n, N=N, info=info)
pb.conectar(cb, dist, n, N)

pb.pagina(__file__, "Teorema del límite central", tema=6,
          descripcion="La densidad de una suma de variables independientes es la convolución de sus densidades. Al sumar "
                      "muchas y normalizar, Z<sub>n</sub> = (S<sub>n</sub> − nμ)/(√n σ), el resultado se acerca a una "
                      "gaussiana N(0, 1), sea cual sea la distribución de partida, siempre que tenga varianza finita.",
          controles=[dist, n, N, info], graficas=[[p1, p2]], inicio=cb,
          referencia="Transparencias T6-02, suma de variables independientes · Apuntes del Tema 6, sección 2")
