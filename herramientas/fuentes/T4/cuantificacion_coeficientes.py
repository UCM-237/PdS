"""T4 · Cuantificación de coeficientes: forma directa frente a secciones de orden 2."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
import numpy as np
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

P0 = ColumnDataSource(dict(x=[], y=[]))
Pd = ColumnDataSource(dict(x=[], y=[]))
Ps = ColumnDataSource(dict(x=[], y=[]))
F = ColumnDataSource(dict(W=[], o=[], d=[], s=[]))

p1 = pb.figura("Polos: ideales, forma directa cuantizada y secciones", "Re z", "Im z", ancho=300, alto=300,
               x_range=(-0.2, 1.3), y_range=(-0.75, 0.75))
th = np.linspace(0, 2 * np.pi, 400)
p1.line(np.cos(th), np.sin(th), color=pb.GRIS, line_width=1)
p1.scatter("x", "y", source=P0, marker="x", size=12, line_width=2.5, color=pb.GRIS, legend_label="ideales")
p1.scatter("x", "y", source=Pd, marker="circle", size=9, line_width=2, line_color=pb.ROJO, fill_color=None, legend_label="forma directa")
p1.scatter("x", "y", source=Ps, marker="square", size=8, line_width=2, line_color=pb.VERDE, fill_color=None, legend_label="secciones")
pb.leyenda(p1, "below")
p2 = pb.figura("|H(e^jΩ)| (dB)", "Ω (rad/muestra)", "dB", ancho=420, alto=300, x_range=(0, 3.1416), y_range=(-100, 30))
p2.line("W", "o", source=F, color=pb.GRIS, line_width=3, legend_label="sin cuantificar")
p2.line("W", "d", source=F, color=pb.ROJO, line_width=1.5, legend_label="forma directa")
p2.line("W", "s", source=F, color=pb.VERDE, line_width=1.5, line_dash="dashed", legend_label="secciones de orden 2")
pb.leyenda(p2, "below")

N = pb.deslizador("Orden N del Butterworth", 2, 12, 8, 1)
Wc = pb.deslizador("Ωc/π (frecuencia de corte)", 0.02, 0.5, 0.1, 0.01)
B = pb.deslizador("B (bits de cada coeficiente)", 4, 24, 12, 1)
info = Div(text="", width=240)

cb = pb.js("""
    const n = N.value, b = B.value, [ceros, polos, k] = butter_z(n, Wc.value * PI);
    // Cuantificador con paso 2^e/2^(B−1), donde 2^e es la menor potencia de 2 que cubre los coeficientes
    const cuant = c => { const e = Math.ceil(Math.log2(Math.max(...c.map(Math.abs), 1e-12)) + 1e-12), D = 2 ** e / 2 ** (b - 1);
        return [c.map(v => Math.round(v / D) * D), e]; };
    const a = polireal(polos), [aq, ed] = cuant(a), num = polireal(ceros).map(v => k * v);
    const pd = raices(aq);
    // Secciones: cada par conjugado (o polo real) por separado; [1, −2Re p, |p|²] con paso fijo 2/2^(B−1)
    const sup = polos.filter(p => p[1] > 1e-9), real = polos.filter(p => Math.abs(p[1]) <= 1e-9);
    const D2 = 2 / 2 ** (b - 1), q = v => Math.round(v / D2) * D2;
    const secs = sup.map(p => [1, q(-2 * p[0]), q(p[0] * p[0] + p[1] * p[1])]).concat(real.map(p => [1, q(-p[0])]));
    const ps = secs.flatMap(s => raices(s));
    P0.data = {x: polos.map(v => v[0]), y: polos.map(v => v[1])};
    Pd.data = {x: pd.map(v => v[0]), y: pd.map(v => v[1])}; Ps.data = {x: ps.map(v => v[0]), y: ps.map(v => v[1])};
    const W = rango(0.001, PI, 800);
    const H = den => W.map(w => { const zi = cexp([0, -w]), nb = evalpoli(num.slice().reverse(), zi), da = evalpoli(den.slice().reverse(), zi); return db(cabs(cdiv(nb, da)), -200); });
    const Hs = W.map(w => { const zi = cexp([0, -w]); let h = evalpoli(num.slice().reverse(), zi);
        for (const s of secs) h = cdiv(h, evalpoli(s.slice().reverse(), zi)); return db(cabs(h), -200); });
    F.data = {W: W, o: H(a), d: H(aq), s: Hs};
    const rmax = v => Math.max(...v.map(cabs)), est = v => rmax(v) < 1;
    // La vista se amplía si algún polo cuantizado sale lejos
    const R = Math.max(1.3, rmax(pd) + 0.1, rmax(ps) + 0.1), Rv = R === 1.3 ? 0.75 : R;
    p1.x_range.start = R === 1.3 ? -0.2 : -R; p1.x_range.end = R; p1.y_range.start = -Rv; p1.y_range.end = Rv;
    const desp = Math.max(...polos.map(p => Math.min(...pd.map(r => cabs(cres(p, r))))));
    const despS = Math.max(...polos.map(p => Math.min(...ps.map(r => cabs(cres(p, r))))));
    info.text = `<p>Forma directa: ${n + 1} coeficientes a_k hasta |a_k| = ${Math.max(...a.map(Math.abs)).toFixed(1)}; paso ${(2 ** ed / 2 ** (b - 1)).toExponential(1)}.</p>` +
        `<p><b style="color:${est(pd) ? "#1E7B4F" : "#C0392B"}">Forma directa: ${est(pd) ? "estable" : "INESTABLE"}</b> (radio máximo ${rmax(pd).toFixed(4)}); los polos se mueven hasta ${desp.toExponential(1)}.</p>` +
        `<p><b style="color:${est(ps) ? "#1E7B4F" : "#C0392B"}">Secciones de orden 2: ${est(ps) ? "estable" : "INESTABLE"}</b> (radio máximo ${rmax(ps).toFixed(4)}); los polos se mueven hasta ${despS.toExponential(1)}.</p>` +
        "<p>Los polos de un filtro estrecho están muy juntos cerca de z = 1. Las raíces de un polinomio de orden alto con raíces próximas son muy sensibles a sus coeficientes; en una sección de orden 2 cada par depende solo de dos coeficientes.</p>" +
        (est(pd) ? "" : "<p>Con polos fuera, |H(e^jΩ)| ya no describe la salida: el sistema diverge.</p>") +
        "<p>El numerador no se cuantifica, para ver solo el efecto sobre los polos.</p>";
""", P0=P0, Pd=Pd, Ps=Ps, F=F, N=N, Wc=Wc, B=B, info=info, p1=p1)
pb.conectar(cb, N, Wc, B)

pb.pagina(__file__, "Cuantificación de coeficientes", tema=4,
          descripcion="Al implementar un IIR con aritmética de B bits, sus coeficientes se redondean y los polos se desplazan. En "
                      "forma directa, con un polinomio de orden N, un error pequeño en un coeficiente puede mover mucho los polos y "
                      "volver inestable un filtro estrecho. En cascada de secciones de orden 2, cada par de polos solo depende de dos "
                      "coeficientes y el filtro es mucho más robusto.",
          controles=[N, Wc, B, info], graficas=[[p1, p2]], inicio=cb,
          referencia="Transparencias T4-03, estructuras de realización · Apuntes del Tema 4, sección 3")
