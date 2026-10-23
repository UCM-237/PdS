"""T1 · Región de convergencia de las transformadas de Laplace y Z."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
import numpy as np
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

An = ColumnDataSource(dict(r0=[], r1=[]))
Fr = ColumnDataSource(dict(left=[], right=[]))
Po = ColumnDataSource(dict(x=[], y=[]))
C = ColumnDataSource(dict(x=[], y=[]))
Xt = ColumnDataSource(dict(t=[], x=[]))
Xn = ColumnDataSource(dict(t=[], x=[]))

p1 = pb.figura("Polos (×) y región de convergencia", "Re", "Im", ancho=280, alto=280, x_range=(-2.5, 2.5), y_range=(-2.5, 2.5))
p1.annulus(x=0, y=0, inner_radius="r0", outer_radius="r1", source=An, fill_color=pb.VERDE, fill_alpha=0.18, line_color=None)
p1.quad(left="left", right="right", top=2.5, bottom=-2.5, source=Fr, fill_color=pb.VERDE, fill_alpha=0.18, line_color=None)
p1.line("x", "y", source=C, color=pb.GRIS, line_width=1.5)
p1.scatter("x", "y", source=Po, marker="x", size=13, line_width=3, color=pb.ROJO)
p2 = pb.figura("Señal correspondiente", "t o n", "", ancho=440, alto=280, x_range=(-10, 10), y_range=(-4, 4))
p2.line("t", "x", source=Xt, color=pb.AZUL, line_width=2)
pb.tallos(p2, "t", "x", Xn, color=pb.AZUL, size=5)

dom = pb.botones(["Transformada Z", "Laplace"])
a = pb.deslizador("Polo p₁ (real)", -1.8, 1.8, 0.5, 0.05)
b = pb.deslizador("Polo p₂ (real)", -1.8, 1.8, -1.4, 0.05)
roc = pb.selector("Región de convergencia", ["Exterior o a la derecha (causal)", "Entre los dos polos (bilateral)", "Interior o a la izquierda (anticausal)"])
info = Div(text="", width=240)

cb = pb.js("""
    const z = dom.active === 0, pa = a.value, pb_ = b.value;
    // Orden por módulo (Z) o por parte real (Laplace)
    const m = v => z ? Math.abs(v) : v, [p1, p2] = m(pa) <= m(pb_) ? [pa, pb_] : [pb_, pa];
    const tipo = ["Exterior", "Entre", "Interior"].findIndex(k => roc.value.startsWith(k));
    // Cada polo da un término causal si la ROC está fuera de él (Z) o a su derecha (Laplace); si no, anticausal
    const causal = [tipo <= 1, tipo === 0];
    const vacia = Math.abs(m(p1) - m(p2)) < 1e-9 && tipo === 1;
    Po.data = {x: [p1, p2], y: [0, 0]};
    const th = rango(0, 2 * PI, 200);
    C.data = z ? {x: th.map(Math.cos), y: th.map(Math.sin)} : {x: [0, 0], y: [-2.5, 2.5]};
    const lim = [[m(p2), 9], [m(p1), m(p2)], [0, m(p1)]][tipo];
    An.data = z && !vacia ? {r0: [lim[0]], r1: [lim[1]]} : {r0: [], r1: []};
    const fr = [[p2, 9], [p1, p2], [-9, p1]][tipo];
    Fr.data = !z && !vacia ? {left: [fr[0]], right: [fr[1]]} : {left: [], right: []};
    const termino = (p, c, t) => z ? (c ? (t >= 0 ? p ** t : 0) : (t <= -1 ? -(p ** t) : 0))
                                   : (c ? (t >= 0 ? Math.exp(p * t) : 0) : (t < 0 ? -Math.exp(p * t) : 0));
    const sig = t => termino(p1, causal[0], t) + termino(p2, causal[1], t);
    if (z) { const n = enteros(-10, 10); Xn.data = {t: n, x: n.map(v => Math.max(-50, Math.min(50, sig(v))))}; Xt.data = {t: [], x: []}; }
    else { const t = rango(-10, 10, 2001); Xt.data = {t: t, x: t.map(v => Math.max(-50, Math.min(50, sig(v))))}; Xn.data = {t: [], x: []}; }
    const contiene = z ? (lim[0] < 1 && 1 < lim[1]) : (fr[0] < 0 && 0 < fr[1]);
    const f = (p, c) => z ? (c ? `${p.toFixed(2)}ⁿ·u[n]` : `−(${p.toFixed(2)})ⁿ·u[−n−1]`) : (c ? `e^(${p.toFixed(2)}t)·u(t)` : `−e^(${p.toFixed(2)}t)·u(−t)`);
    const menos = p => p >= 0 ? `− ${p.toFixed(2)}` : `+ ${(-p).toFixed(2)}`;
    const X = z ? `1/(1 ${menos(p1)}z⁻¹) + 1/(1 ${menos(p2)}z⁻¹)` : `1/(s ${menos(p1)}) + 1/(s ${menos(p2)})`;
    const R = z ? ["|z| > " + m(p2).toFixed(2), m(p1).toFixed(2) + " < |z| < " + m(p2).toFixed(2), "|z| < " + m(p1).toFixed(2)][tipo]
                : ["Re s > " + p2.toFixed(2), p1.toFixed(2) + " < Re s < " + p2.toFixed(2), "Re s < " + p1.toFixed(2)][tipo];
    info.text = `<p>X = ${X}</p>` + (vacia ? "<p style='color:#C0392B'>Los dos polos tienen el mismo " + (z ? "módulo" : "parte real") + ": no hay región entre ellos.</p>" :
        `<p>ROC: ${R}</p><p>x = ${(f(p1, causal[0]) + " + " + f(p2, causal[1])).replace("+ −", "− ")}</p>` +
        `<p>${["Señal causal (a la derecha)", "Señal bilateral", "Señal anticausal (a la izquierda)"][tipo]}.</p>` +
        `<p><b>${contiene ? "Estable" : "Inestable"}</b>: la ROC ${contiene ? "" : "no "}contiene ${z ? "la circunferencia unidad" : "el eje jω"}, ` +
        `así que la ${z ? "DTFT" : "transformada de Fourier"} ${contiene ? "existe" : "no existe"}.</p>`) +
        "<p>La misma expresión de X corresponde a tres señales distintas: sin la ROC, la transformada no está completa.</p>";
""", An=An, Fr=Fr, Po=Po, C=C, Xt=Xt, Xn=Xn, dom=dom, a=a, b=b, roc=roc, info=info)
pb.conectar(cb, dom, a, b, roc)

pb.pagina(__file__, "Región de convergencia", tema=1,
          descripcion="Una transformada de Laplace o Z con dos polos reales puede corresponder a una señal causal, anticausal o "
                      "bilateral: lo decide la región de convergencia (ROC). En Z, la ROC es un anillo limitado por los módulos "
                      "de los polos; en Laplace, una franja vertical limitada por sus partes reales. El sistema es estable si la ROC "
                      "contiene la circunferencia unidad o el eje jω.",
          controles=[dom, a, b, roc, info], graficas=[[p1, p2]], inicio=cb,
          referencia="Transparencias T1-02, transformadas de Laplace y Z · Apuntes del Tema 1, sección 6")
