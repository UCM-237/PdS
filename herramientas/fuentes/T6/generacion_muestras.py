"""T6 · Generar muestras: ruleta, inversa de la distribución, Box-Muller, aceptación y rechazo y mezclas."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

Cu = ColumnDataSource(dict(x=[], y=[]))          # curva del método (F_X, f y M·q…)
Cu2 = ColumnDataSource(dict(x=[], y=[]))
Pa = ColumnDataSource(dict(x=[], y=[], color=[]))  # puntos del método
Fl = ColumnDataSource(dict(xs=[], ys=[]))          # flechas u → x
Hi = ColumnDataSource(dict(x=[], top=[], ancho=[]))
Te = ColumnDataSource(dict(x=[], y=[]))
Tp = ColumnDataSource(dict(x=[], y=[]))

p1 = pb.figura("Cómo se genera", "x", "", ancho=380, alto=300)
p1.line("x", "y", source=Cu, color=pb.AZUL, line_width=2)
p1.line("x", "y", source=Cu2, color=pb.NARANJA, line_width=2, line_dash="dashed")
p1.multi_line("xs", "ys", source=Fl, color=pb.ROJO, line_width=1.2, line_dash="dotted")
p1.scatter("x", "y", source=Pa, color="color", size=3, alpha=0.6)
p2 = pb.figura("Histograma normalizado y densidad teórica", "x", "densidad", ancho=380, alto=300)
p2.vbar(x="x", top="top", width="ancho", source=Hi, fill_color=pb.GRIS_CLARO, line_color="white")
p2.line("x", "y", source=Te, color=pb.ROJO, line_width=2)
p2.scatter("x", "y", source=Tp, color=pb.ROJO, size=8)

metodo = pb.selector("Método y distribución", [
    "Ruleta: dado cargado", "Ruleta: binomial B(10, p)", "Inversa: exponencial", "Inversa: Rayleigh",
    "Box-Muller: gaussiana N(0, σ²)", "Rechazo: f(x) = 6x(1 − x)", "Rechazo: f(x) = 30x(1 − x)⁴", "Mezcla de dos gaussianas"], width=250)
par = pb.deslizador("Parámetro", 0.05, 4, 1, 0.05)
N = pb.deslizador("Número de muestras N", 100, 20000, 2000, 100)
semilla = pb.deslizador("Semilla", 1, 50, 1, 1)
info = Div(text="", width=250)

cb = pb.js("""
    const g = generador(semilla.value), Nm = N.value, met = metodo.value, q = par.value;
    let xs = [], cu = {x: [], y: []}, cu2 = {x: [], y: []}, pts = {x: [], y: [], color: []}, fl = {xs: [], ys: []};
    let te = {x: [], y: []}, tp = {x: [], y: []}, mu, s2, extra = "", a = 0, b = 1, discreta = false;
    const muestra_u = () => { const r = []; for (let i = 0; i < 5; i++) r.push(g()); return r; };
    if (met.startsWith("Ruleta")) {
        discreta = true;
        let vals, p;
        if (met.includes("dado")) { vals = [1, 2, 3, 4, 5, 6]; p = [0.1, 0.1, 0.1, 0.1, 0.1, 0.5]; par.title = "Parámetro (no se usa)"; }
        else { const pp = Math.min(0.95, Math.max(0.05, q / 4)); par.title = `p = parámetro/4 = ${pp.toFixed(3)}`;
               vals = enteros(0, 10); const c = k => { let r = 1; for (let i = 1; i <= k; i++) r = r * (11 - i) / i; return r; };
               p = vals.map(k => c(k) * pp ** k * (1 - pp) ** (10 - k)); }
        const F = []; p.reduce((s, v, i) => (F[i] = s + v), 0);
        for (let i = 0; i < Nm; i++) { const u = g(); let k = 0; while (k < vals.length - 1 && u >= F[k]) k++; xs.push(vals[k]); }
        // Escalera de F_X y tres u con su valor
        vals.forEach((v, i) => { cu.x.push(v, v + 1); cu.y.push(F[i], F[i]); });
        for (const u of muestra_u()) { let k = 0; while (k < vals.length - 1 && u >= F[k]) k++; fl.xs.push([vals[0] - 0.5, vals[k], vals[k]]); fl.ys.push([u, u, 0]); pts.x.push(vals[0] - 0.5); pts.y.push(u); pts.color.push(pb_ROJO); }
        mu = vals.reduce((s, v, i) => s + v * p[i], 0); s2 = vals.reduce((s, v, i) => s + (v - mu) ** 2 * p[i], 0);
        tp = {x: vals, y: p}; a = vals[0] - 0.5; b = vals[vals.length - 1] + 0.5;
        extra = "<p>F<sub>X</sub>(x<sub>i−1</sub>) ≤ u &lt; F<sub>X</sub>(x<sub>i</sub>) da x<sub>i</sub>: cada tramo de [0, 1) mide p<sub>X</sub>(x<sub>i</sub>)</p>";
    } else if (met.startsWith("Inversa")) {
        const exp = met.includes("exponencial"), lam = q, sg = q;
        par.title = exp ? "λ" : "σ de la Rayleigh";
        const Finv = u => exp ? -Math.log(1 - u) / lam : sg * Math.sqrt(-2 * Math.log(1 - u));
        const Fd = x => exp ? 1 - Math.exp(-lam * x) : 1 - Math.exp(-x * x / (2 * sg * sg));
        const fd = x => exp ? lam * Math.exp(-lam * x) : x / (sg * sg) * Math.exp(-x * x / (2 * sg * sg));
        for (let i = 0; i < Nm; i++) xs.push(Finv(g()));
        b = exp ? 5 / lam : 4.5 * sg; const xx = rango(0, b, 300); cu = {x: xx, y: xx.map(Fd)};
        for (const u of muestra_u()) { const x = Finv(u); fl.xs.push([0, x, x]); fl.ys.push([u, u, 0]); pts.x.push(0); pts.y.push(u); pts.color.push(pb_ROJO); }
        te = {x: xx, y: xx.map(fd)};
        mu = exp ? 1 / lam : sg * Math.sqrt(PI / 2); s2 = exp ? 1 / lam ** 2 : (4 - PI) / 2 * sg * sg;
        extra = exp ? `<p>x = −ln(1 − u)/λ. P(X > 1) = e<sup>−λ</sup> = ${Math.exp(-lam).toFixed(3)}; con las muestras, ` +
                      `${(xs.filter(v => v > 1).length / Nm).toFixed(3)}</p>` : "<p>x = σ√(−2 ln(1 − u)): es el radio del Box-Muller</p>";
    } else if (met.startsWith("Box")) {
        const sg = q; par.title = "σ";
        for (let i = 0; i < Nm; i += 2) { const r = Math.sqrt(-2 * Math.log(1 - g())), th = 2 * PI * g(); xs.push(sg * r * Math.cos(th)); if (i + 1 < Nm) xs.push(sg * r * Math.sin(th)); }
        // Pares (z₁, z₂) y circunferencias de radio σ y 2σ
        for (let i = 0; i + 1 < Math.min(xs.length, 3000); i += 2) { pts.x.push(xs[i]); pts.y.push(xs[i + 1]); pts.color.push(pb_AZUL); }
        const th = rango(0, 2 * PI, 200); cu = {x: th.map(t => sg * Math.cos(t)), y: th.map(t => sg * Math.sin(t))};
        cu2 = {x: th.map(t => 2 * sg * Math.cos(t)), y: th.map(t => 2 * sg * Math.sin(t))};
        b = 4 * sg; a = -b; const xx = rango(a, b, 300); te = {x: xx, y: xx.map(x => Math.exp(-x * x / (2 * sg * sg)) / (Math.sqrt(2 * PI) * sg))};
        mu = 0; s2 = sg * sg;
        let c = 0; for (let i = 0; i + 1 < xs.length; i += 2) c += xs[i] * xs[i + 1];
        const den = xs.filter(v => Math.abs(v) < sg).length / xs.length;
        extra = `<p>Correlación muestral de z₁ y z₂: ${(c / (xs.length / 2) / (sg * sg)).toFixed(3)} (deben ser independientes)</p>` +
                `<p>Fracción a menos de σ: ${den.toFixed(3)} (teórica 0,683)</p>`;
    } else if (met.startsWith("Rechazo")) {
        const beta = met.includes("6x"), f = beta ? (x => 6 * x * (1 - x)) : (x => 30 * x * (1 - x) ** 4), fmax = beta ? 1.5 : 30 * 0.2 * 0.8 ** 4;
        const M = Math.max(q, 0.3); par.title = `M (como mínimo ${fmax.toFixed(3)} para que M·q ≥ f)`;
        let cand = 0;
        while (xs.length < Nm && cand < 50 * Nm) {
            const x = g(), u = g(); cand++;
            const ok = u * M <= f(x);
            if (ok) xs.push(x);
            if (cand <= 1500) { pts.x.push(x); pts.y.push(u * M); pts.color.push(ok ? pb_VERDE : pb_ROJO); }
        }
        const xx = rango(0, 1, 300); cu = {x: xx, y: xx.map(f)}; cu2 = {x: [0, 1], y: [M, M]}; te = {x: xx, y: xx.map(f)};
        mu = beta ? 0.5 : 2 / 7; s2 = beta ? 0.05 : 2 * 5 / (49 * 8);
        let mal = 0; for (const x of xx) if (M < f(x) - 1e-12) mal++;
        extra = `<p>Candidatos: ${cand}; aceptados ${(100 * xs.length / cand).toFixed(1)} % (teórico 1/M = ${(100 / M).toFixed(1)} %)</p>` +
                (mal ? "<p style='color:#C0392B'>M·q no cubre a f: las muestras no siguen f</p>" : "");
    } else {
        const p1 = Math.min(0.95, Math.max(0.05, q / 4)); par.title = `π₁ = parámetro/4 = ${p1.toFixed(3)}`;
        const comp = [[3, 0.5, p1], [6, 1, 1 - p1]];
        for (let i = 0; i < Nm; i++) { const c = g() < p1 ? comp[0] : comp[1]; xs.push(c[0] + c[1] * gauss(g)); }
        a = 0; b = 10; const xx = rango(a, b, 400), gd = (x, m, s) => Math.exp(-0.5 * ((x - m) / s) ** 2) / (Math.sqrt(2 * PI) * s);
        te = {x: xx, y: xx.map(x => comp.reduce((s, c) => s + c[2] * gd(x, c[0], c[1]), 0))};
        cu = {x: xx, y: xx.map(x => p1 * gd(x, 3, 0.5))}; cu2 = {x: xx, y: xx.map(x => (1 - p1) * gd(x, 6, 1))};
        mu = p1 * 3 + (1 - p1) * 6; s2 = p1 * (0.25 + 9) + (1 - p1) * (1 + 36) - mu * mu;
        extra = "<p>Primero se elige la componente con la ruleta (π₁, 1 − π₁) y después se genera la gaussiana elegida</p>";
    }
    if (!met.startsWith("Ruleta") && !met.startsWith("Box") && !met.startsWith("Mezcla") && !met.startsWith("Inversa")) { a = 0; b = 1; }
    let h;
    if (discreta) { const vals = tp.x; h = {c: vals, d: vals.map(v => xs.filter(z => z === v).length / Nm), ancho: 0.6}; }
    else h = histo(xs, a, b, Math.max(10, Math.min(60, Math.round(Math.sqrt(Nm)))));
    Hi.data = {x: h.c, top: h.d, ancho: h.c.map(() => h.ancho)};
    Cu.data = cu; Cu2.data = cu2; Pa.data = pts; Fl.data = fl; Te.data = te; Tp.data = tp;
    p1.title.text = met.startsWith("Box") ? "Pares (z₁, z₂) y circunferencias de radio σ y 2σ" : met.startsWith("Rechazo") ?
        "Candidatos (x, u·M·q(x)): aceptados en verde" : met.startsWith("Mezcla") ? "Las dos componentes π_k f_k(x)" : "u uniforme → x con F_X(x)";
    p2.title.text = discreta ? "Frecuencias relativas y probabilidades teóricas" : "Histograma normalizado y densidad teórica";
    info.text = `<p>N = ${xs.length} muestras</p><p>Media: ${media(xs).toFixed(4)} (teórica ${mu.toFixed(4)})</p>` +
        `<p>Varianza: ${varianza(xs).toFixed(4)} (teórica ${s2.toFixed(4)})</p>` + extra;
""", Cu=Cu, Cu2=Cu2, Pa=Pa, Fl=Fl, Hi=Hi, Te=Te, Tp=Tp, p1=p1, p2=p2, metodo=metodo, par=par, N=N, semilla=semilla,
   info=info, pb_ROJO=pb.ROJO, pb_VERDE=pb.VERDE, pb_AZUL=pb.AZUL)
pb.conectar(cb, metodo, par, N, semilla)
# Valor de partida del parámetro para cada método
metodo.js_on_change("value", pb.js("""
    const v = {"Ruleta: binomial B(10, p)": 1.2, "Inversa: exponencial": 2, "Rechazo: f(x) = 6x(1 − x)": 1.5,
               "Rechazo: f(x) = 30x(1 − x)⁴": 2.5, "Mezcla de dos gaussianas": 1.6}[metodo.value];
    par.value = v === undefined ? 1 : v;
""", metodo=metodo, par=par))

pb.pagina(__file__, "Generación de muestras aleatorias", tema=6,
          descripcion="Todos los métodos parten de números uniformes en [0, 1). La ruleta reparte [0, 1) en tramos de longitud "
                      "p<sub>X</sub>(x<sub>i</sub>); la inversa toma x = F<sub>X</sub><sup>−1</sup>(u); Box-Muller convierte dos "
                      "uniformes en dos gaussianas independientes; aceptación y rechazo se queda con los candidatos que caen "
                      "bajo f; una mezcla elige primero la componente.",
          controles=[metodo, par, N, semilla, info], graficas=[[p1, p2]], inicio=cb,
          referencia="Transparencias T6-01, generar muestras con el ordenador · Apuntes del Tema 6, sección 1")
