"""T6 · Realizaciones de una señal aleatoria: promedios de conjunto, estacionariedad y ergodicidad."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div, Span
import pds_bokeh as pb

NN = 200

R = ColumnDataSource(dict(xs=[], ys=[], alfa=[], color=[], ancho=[]))
Mc = ColumnDataSource(dict(n=[], m=[], lo=[], hi=[], mt=[]))
Tm = ColumnDataSource(dict(n=[], a=[]))
Ac = ColumnDataSource(dict(l=[], a=[], b=[], t=[]))

p1 = pb.figura("Realizaciones x[n] (la primera, resaltada)", "n", "", ancho=520, alto=210, x_range=(0, NN))
p1.multi_line("xs", "ys", source=R, color="color", line_alpha="alfa", line_width="ancho")
cortes = [Span(location=v, dimension="height", line_color=pb.VERDE, line_dash="dashed", line_width=1.5) for v in (50, 150)]
for s in cortes:
    p1.add_layout(s)
p2 = pb.figura("Media de conjunto en cada n, ±σ, y media teórica", "n", "", ancho=520, alto=170, x_range=p1.x_range)
p2.varea("n", "lo", "hi", source=Mc, fill_color=pb.AZUL, fill_alpha=0.15)
p2.line("n", "m", source=Mc, color=pb.AZUL, line_width=2, legend_label="media de conjunto")
p2.line("n", "mt", source=Mc, color=pb.ROJO, line_dash="dashed", line_width=1.5, legend_label="teórica")
p2.line("n", "a", source=Tm, color=pb.NARANJA, line_width=2, legend_label="promedio temporal de la primera")
pb.leyenda(p2, "below")
p3 = pb.figura("φ[n₀ + l, n₀] de conjunto en n₀ = 50 y 150", "l", "", ancho=330, alto=230)
p3.line("l", "t", source=Ac, color=pb.GRIS_CLARO, line_width=4, legend_label="teórica (si es ESA)")
p3.line("l", "a", source=Ac, color=pb.VERDE, line_width=1.8, legend_label="n₀ = 50")
p3.line("l", "b", source=Ac, color=pb.NARANJA, line_width=1.8, line_dash="dashed", legend_label="n₀ = 150")
pb.leyenda(p3, "below")

proc = pb.selector("Señal", ["Ruido blanco N(0, 1)", "Paseo aleatorio", "Sinusoide de fase aleatoria", "AR(1)",
                             "Constante aleatoria A ~ U[0, 1]", "Varianza decreciente σ[n] = 0,99ⁿ"], width=250)
Rn = pb.deslizador("Número de realizaciones", 1, 400, 100, 1)
a = pb.deslizador("a del AR(1)", -0.95, 0.95, 0.8, 0.05)
semilla = pb.deslizador("Semilla", 1, 50, 1, 1)
info = Div(text="", width=250)

cb = pb.js("""
    const N = NN, g = generador(semilla.value), K = Rn.value, pr = proc.value, aa = a.value, n = enteros(0, N - 1);
    const reals = [];
    for (let r = 0; r < K; r++) {
        let x;
        if (pr.startsWith("Ruido")) x = n.map(() => gauss(g));
        else if (pr.startsWith("Paseo")) { let s = 0; x = n.map(k => (s = k ? s + gauss(g) : 0)); }
        else if (pr.startsWith("Sinusoide")) { const th = 2 * PI * g(); x = n.map(k => Math.sqrt(2) * Math.cos(0.2 * k + th)); }
        else if (pr.startsWith("AR")) { let s = gauss(g) / Math.sqrt(1 - aa * aa); x = n.map(() => { const v = s; s = aa * s + gauss(g); return v; }); }
        else if (pr.startsWith("Constante")) { const A = g(); x = n.map(() => A); }
        else x = n.map(k => Math.pow(0.99, k) * gauss(g));
        reals.push(x);
    }
    const vis = reals.slice(0, Math.min(K, 30));
    R.data = {xs: vis.map(() => n), ys: vis, alfa: vis.map((_, i) => i ? 0.25 : 1), color: vis.map((_, i) => i ? pb_GRIS : pb_AZUL), ancho: vis.map((_, i) => i ? 1 : 2)};
    // Media y desviación de conjunto en cada instante
    const m = n.map(k => reals.reduce((s, x) => s + x[k], 0) / K);
    const sd = n.map((k, i) => K > 1 ? Math.sqrt(reals.reduce((s, x) => s + (x[k] - m[i]) ** 2, 0) / (K - 1)) : 0);
    const mt = n.map(() => pr.startsWith("Constante") ? 0.5 : 0);
    let acc = 0; const at = n.map((k) => (acc += reals[0][k]) / (k + 1));
    Mc.data = {n: n, m: m, lo: m.map((v, i) => v - sd[i]), hi: m.map((v, i) => v + sd[i]), mt: mt}; Tm.data = {n: n, a: at};
    // Autocorrelación de conjunto en n₀ = 50 y 150, para l = 0..40
    const ls = enteros(0, 40), phi = n0 => ls.map(l => reals.reduce((s, x) => s + x[n0 + l] * x[n0], 0) / K);
    const teo = ls.map(l => pr.startsWith("Ruido") ? (l ? 0 : 1) : pr.startsWith("Sinusoide") ? Math.cos(0.2 * l) :
                            pr.startsWith("AR") ? Math.pow(aa, l) / (1 - aa * aa) : pr.startsWith("Constante") ? 1 / 3 : NaN);
    Ac.data = {l: ls, a: phi(50), b: phi(150), t: teo};
    const tx = {
        "Ruido": ["sí", "sí", "media 0 y φ[l] = δ[l] en todos los instantes"],
        "Paseo": ["no", "no", "la varianza crece con n: Var{x[n]} = n"],
        "Sinusoide": ["sí (en sentido amplio)", "sí", "media 0 y φ[l] = cos(0,2 l), que no se amortigua"],
        "AR": ["sí (empieza en régimen)", "sí", "φ[l] = a^|l|/(1 − a²)"],
        "Constante": ["sí", "no", "cada realización se queda en su valor A: el promedio temporal no tiende a 1/2"],
        "Varianza": ["no", "no", "los valores son independientes, pero la varianza cambia con n"],
    }[Object.keys({"Ruido": 0, "Paseo": 0, "Sinusoide": 0, "AR": 0, "Constante": 0, "Varianza": 0}).find(k => pr.startsWith(k))];
    info.text = `<p>¿Estacionaria? ${tx[0]}</p><p>¿Ergódica? ${tx[1]}</p><p>${tx[2]}</p>` +
        `<p>Media de conjunto en n = 50 y 150: ${m[50].toFixed(3)} y ${m[150].toFixed(3)}</p>` +
        `<p>Desviación de conjunto en n = 50 y 150: ${sd[50].toFixed(3)} y ${sd[150].toFixed(3)}</p>` +
        `<p>Promedio temporal de la primera realización: ${at[N - 1].toFixed(3)}</p>`;
""", R=R, Mc=Mc, Tm=Tm, Ac=Ac, proc=proc, Rn=Rn, a=a, semilla=semilla, info=info, NN=NN,
   pb_GRIS=pb.GRIS, pb_AZUL=pb.AZUL)
pb.conectar(cb, proc, Rn, a, semilla)

pb.pagina(__file__, "Realizaciones, estacionariedad y ergodicidad", tema=6,
          descripcion="Una señal aleatoria es un conjunto de realizaciones. Sus estadísticos son promedios sobre el conjunto "
                      "en cada instante: es estacionaria (en sentido amplio) si la media no depende de n y la autocorrelación "
                      "solo depende de la separación l. Es ergódica si los promedios temporales de una sola realización dan "
                      "los mismos valores.",
          controles=[proc, Rn, a, semilla, info], graficas=[[p1, p3], p2], inicio=cb,
          referencia="Transparencias T6-03, estacionariedad, sinusoide de fase aleatoria y ergodicidad · Apuntes del Tema 6, sección 3")
