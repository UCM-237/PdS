"""T6 · Distribuciones de probabilidad: densidad, función de distribución y muestras."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

Hi = ColumnDataSource(dict(x=[], top=[], ancho=[]))
Pd = ColumnDataSource(dict(x=[], y=[]))
Pp = ColumnDataSource(dict(x=[], y=[]))
Fe = ColumnDataSource(dict(x=[], y=[]))
Ft = ColumnDataSource(dict(x=[], y=[]))

p1 = pb.figura("Densidad f(x) (o probabilidades) e histograma normalizado", "x", "", ancho=420, alto=270)
p1.vbar(x="x", top="top", width="ancho", source=Hi, fill_color=pb.GRIS_CLARO, line_color="white", legend_label="histograma")
p1.line("x", "y", source=Pd, color=pb.ROJO, line_width=2.2, legend_label="teórica")
p1.scatter("x", "y", source=Pp, color=pb.ROJO, size=7, legend_label="teórica")
pb.leyenda(p1, "below")
p2 = pb.figura("Función de distribución F(x) y distribución empírica", "x", "F(x)", ancho=420, alto=270,
               x_range=p1.x_range, y_range=(-0.02, 1.02))
p2.step("x", "y", source=Fe, color=pb.AZUL, line_width=1.6, mode="after", legend_label="empírica F_N(x)")
p2.line("x", "y", source=Ft, color=pb.ROJO, line_width=2, line_dash="dashed", legend_label="teórica F(x)")
pb.leyenda(p2, "below")

dist = pb.selector("Distribución", ["Uniforme U[a, b]", "Normal N(μ, σ²)", "Exponencial", "Rayleigh", "Laplace",
                                   "Binomial B(n, p)", "Poisson"], "Normal N(μ, σ²)")
a = pb.deslizador("Media μ", -3, 10, 0, 0.1)
b = pb.deslizador("Desviación típica σ", 0.1, 5, 1, 0.1)
N = pb.selector("N (muestras)", ["10", "100", "1000", "10000", "100000"], "1000")
nb = pb.deslizador("Intervalos del histograma", 5, 100, 30, 1)
semilla = pb.deslizador("Realización", 1, 50, 1, 1)
info = Div(text="", width=250)

cb = pb.js("""
    const d = dist.value, g = generador(semilla.value), Nn = parseInt(N.value), p = a.value, q = b.value;
    const erf = x => { const s = Math.sign(x), t = 1 / (1 + 0.3275911 * Math.abs(x));
        return s * (1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x)); };
    const lgam = k => { let s = 0; for (let i = 2; i <= k; i++) s += Math.log(i); return s; };
    let gen, pdf, cdf, mu, v, lo, hi, disc = false, pmf, nom;
    if (d.startsWith("Uniforme")) { const lo_ = Math.min(p, p + q), hi_ = p + q; nom = `U[${lo_.toFixed(1)}, ${hi_.toFixed(1)}]`;
        gen = () => lo_ + q * g(); pdf = x => (x >= lo_ && x <= hi_ ? 1 / q : 0); cdf = x => Math.min(1, Math.max(0, (x - lo_) / q));
        mu = lo_ + q / 2; v = q * q / 12; lo = lo_ - 0.2 * q; hi = hi_ + 0.2 * q; }
    else if (d.startsWith("Normal")) { nom = `N(${p.toFixed(1)}, ${q.toFixed(1)}²)`; gen = () => p + q * gauss(g);
        pdf = x => Math.exp(-0.5 * ((x - p) / q) ** 2) / (q * Math.sqrt(2 * PI)); cdf = x => 0.5 * (1 + erf((x - p) / (q * Math.SQRT2)));
        mu = p; v = q * q; lo = p - 4 * q; hi = p + 4 * q; }
    else if (d.startsWith("Exp")) { const l = q; nom = `exponencial de λ = ${l.toFixed(1)}`; gen = () => -Math.log(1 - g()) / l;
        pdf = x => (x < 0 ? 0 : l * Math.exp(-l * x)); cdf = x => (x < 0 ? 0 : 1 - Math.exp(-l * x)); mu = 1 / l; v = 1 / (l * l); lo = -0.5 / l; hi = 6 / l; }
    else if (d.startsWith("Rayleigh")) { const s = q; nom = `Rayleigh de σ = ${s.toFixed(1)}`; gen = () => s * Math.sqrt(-2 * Math.log(1 - g()));
        pdf = x => (x < 0 ? 0 : x / (s * s) * Math.exp(-x * x / (2 * s * s))); cdf = x => (x < 0 ? 0 : 1 - Math.exp(-x * x / (2 * s * s)));
        mu = s * Math.sqrt(PI / 2); v = (2 - PI / 2) * s * s; lo = -0.5 * s; hi = 4.5 * s; }
    else if (d.startsWith("Laplace")) { const s = q; nom = `Laplace de media ${p.toFixed(1)} y escala ${s.toFixed(1)}`;
        gen = () => { const u = g() - 0.5; return p - s * Math.sign(u) * Math.log(1 - 2 * Math.abs(u)); };
        pdf = x => Math.exp(-Math.abs(x - p) / s) / (2 * s); cdf = x => (x < p ? 0.5 * Math.exp((x - p) / s) : 1 - 0.5 * Math.exp(-(x - p) / s));
        mu = p; v = 2 * s * s; lo = p - 6 * s; hi = p + 6 * s; }
    else if (d.startsWith("Binomial")) { disc = true; const n = Math.max(1, Math.round(q)), pr = Math.min(1, Math.max(0, p)); nom = `B(${n}, ${pr.toFixed(2)})`;
        gen = () => { let k = 0; for (let i = 0; i < n; i++) if (g() < pr) k++; return k; };
        pmf = k => (k < 0 || k > n ? 0 : Math.exp(lgam(n) - lgam(k) - lgam(n - k) + (k ? k * Math.log(pr) : 0) + (n - k ? (n - k) * Math.log(1 - pr) : 0)));
        mu = n * pr; v = n * pr * (1 - pr); lo = -1; hi = n + 1; }
    else { disc = true; const l = q; nom = `Poisson de λ = ${l.toFixed(1)}`;
        gen = () => { const L = Math.exp(-l); let k = 0, t = g(); while (t > L) { k++; t *= g(); } return k; };
        pmf = k => (k < 0 ? 0 : Math.exp(-l + k * Math.log(l) - lgam(k))); mu = l; v = l; lo = -1; hi = Math.ceil(l + 5 * Math.sqrt(l) + 2); }
    const x = enteros(1, Nn).map(gen), xs = x.slice().sort((u, w) => u - w);
    if (disc) {
        const ks = enteros(Math.max(0, Math.floor(lo)), Math.ceil(hi)), cnt = new Map();
        for (const k of x) cnt.set(k, (cnt.get(k) || 0) + 1);
        Hi.data = {x: ks, top: ks.map(k => (cnt.get(k) || 0) / Nn), ancho: ks.map(() => 0.7)};
        Pd.data = {x: [], y: []}; Pp.data = {x: ks, y: ks.map(pmf)};
        let s = 0; const kk = enteros(Math.floor(lo), Math.ceil(hi)); const F = kk.map(k => (s += pmf(k)));
        Ft.data = {x: kk.flatMap(k => [k, k + 1]), y: F.flatMap(f => [f, f])};
    } else {
        const h = histo(x, lo, hi, nb.value), xx = rango(lo, hi, 400);
        Hi.data = {x: h.c, top: h.d, ancho: h.c.map(() => h.ancho)};
        Pd.data = {x: xx, y: xx.map(pdf)}; Pp.data = {x: [], y: []}; Ft.data = {x: xx, y: xx.map(cdf)};
    }
    Fe.data = {x: [lo].concat(xs, [hi]), y: [0].concat(xs.map((_, i) => (i + 1) / Nn), [1])};
    p1.x_range.start = lo; p1.x_range.end = hi;
    // Distancia de Kolmogórov-Smirnov: máxima diferencia entre F_N y F (sólo continuas)
    let ks = NaN;
    if (!disc) { ks = 0; xs.forEach((u, i) => { const F = cdf(u); ks = Math.max(ks, Math.abs(F - i / Nn), Math.abs(F - (i + 1) / Nn)); }); }
    const m = media(x), s2 = varianza(x);
    info.text = `<p>${nom}</p><p>Media: teórica ${mu.toFixed(3)}, muestral ${m.toFixed(3)}</p>` +
        `<p>Varianza: teórica ${v.toFixed(3)}, muestral ${s2.toFixed(3)}</p>` +
        `<p>El error de la media muestral es del orden de σ/√N = ${Math.sqrt(v / Nn).toFixed(3)}</p>` +
        (disc ? "" : `<p>Máxima distancia entre F<sub>N</sub> y F: ${ks.toFixed(3)} (del orden de 1/√N = ${(1 / Math.sqrt(Nn)).toFixed(3)})</p>`);
""", Hi=Hi, Pd=Pd, Pp=Pp, Fe=Fe, Ft=Ft, p1=p1, dist=dist, a=a, b=b, N=N, nb=nb, semilla=semilla, info=info)
pb.conectar(cb, dist, a, b, N, nb, semilla)
# Títulos y valores de los parámetros según la distribución
dist.js_on_change("value", pb.js("""
    // [título, inicio, fin, paso, valor] de cada parámetro
    const t = {"Uniforme U[a, b]": [["Extremo a", -3, 10, 0.1, 0], ["Anchura b − a", 0.1, 10, 0.1, 1]],
               "Normal N(μ, σ²)": [["Media μ", -3, 10, 0.1, 0], ["Desviación típica σ", 0.1, 5, 0.1, 1]],
               "Exponencial": [null, ["λ", 0.1, 5, 0.1, 1]], "Rayleigh": [null, ["σ", 0.1, 5, 0.1, 1]],
               "Laplace": [["Media", -3, 10, 0.1, 0], ["Escala s", 0.1, 5, 0.1, 1]],
               "Binomial B(n, p)": [["p", 0, 1, 0.01, 0.3], ["n", 1, 60, 1, 10]], "Poisson": [null, ["λ", 0.1, 30, 0.1, 3]]}[dist.value];
    const pon = (s, c) => { s.visible = c !== null; if (!c) return; s.title = c[0]; s.start = c[1]; s.end = c[2]; s.step = c[3]; s.value = c[4]; };
    pon(a, t[0]); pon(b, t[1]);
""", dist=dist, a=a, b=b))

pb.pagina(__file__, "Distribuciones de probabilidad", tema=6,
          descripcion="Una variable aleatoria queda descrita por su función de distribución F(x) = P(X ≤ x), o por su "
                      "densidad f(x) = F′(x). Con N muestras, el histograma normalizado se acerca a f y la distribución "
                      "empírica a F; las diferencias bajan como 1/√N.",
          controles=[dist, a, b, N, nb, semilla, info], graficas=[[p1, p2]], inicio=cb,
          referencia="Transparencias T6-01, variables aleatorias y distribuciones · Apuntes del Tema 6, sección 1")
