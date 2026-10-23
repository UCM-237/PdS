"""T4 · Sistemas de fase mínima y paso todo."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
import numpy as np
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

Z = ColumnDataSource(dict(x=[], y=[], color=[]))
Za = ColumnDataSource(dict(x=[], y=[]))
F = ColumnDataSource(dict(W=[], m=[], f=[], fm=[], fa=[], g=[], gm=[], ga=[]))
Hn = ColumnDataSource(dict(n=[], h=[], hm=[], e=[], em=[]))

p1 = pb.figura("Ceros de H(z)", "Re z", "Im z", ancho=230, alto=230, x_range=(-2.2, 2.2), y_range=(-2.2, 2.2))
th = np.linspace(0, 2 * np.pi, 200)
p1.line(np.cos(th), np.sin(th), color=pb.GRIS, line_width=1)
p1.scatter("x", "y", source=Za, marker="circle", size=10, line_color=pb.GRIS_CLARO, line_dash="dashed", fill_color=None)
p1.scatter("x", "y", source=Z, marker="circle", size=12, line_width=2.5, line_color="color", fill_color=None)
p2 = pb.figura("Módulo |H(e^jΩ)| (igual en todos los casos)", "Ω (rad/muestra)", "", ancho=330, alto=230, x_range=(0, 3.1416))
p2.line("W", "m", source=F, color=pb.AZUL, line_width=2)
p3 = pb.figura("Fase desenrollada (rad)", "Ω (rad/muestra)", "", ancho=330, alto=200, x_range=(0, 3.1416))
p3.line("W", "fm", source=F, color=pb.GRIS, line_width=2, line_dash="dashed", legend_label="fase mínima")
p3.line("W", "fa", source=F, color=pb.NARANJA, line_width=2, legend_label="paso todo")
p3.line("W", "f", source=F, color=pb.AZUL, line_width=2, legend_label="H")
pb.leyenda(p3, "below")
p4 = pb.figura("Retardo de grupo (muestras)", "Ω (rad/muestra)", "", ancho=330, alto=200, x_range=(0, 3.1416))
p4.line("W", "gm", source=F, color=pb.GRIS, line_width=2, line_dash="dashed", legend_label="fase mínima")
p4.line("W", "ga", source=F, color=pb.NARANJA, line_width=2, legend_label="paso todo")
p4.line("W", "g", source=F, color=pb.AZUL, line_width=2, legend_label="H")
pb.leyenda(p4, "below")
p5 = pb.figura("Respuesta al impulso h[n]", "n", "", ancho=330, alto=200)
p5.scatter("n", "hm", source=Hn, marker="square", size=9, line_color=pb.GRIS, fill_color=None, legend_label="fase mínima")
pb.tallos(p5, "n", "h", Hn, color=pb.AZUL, legend_label="H")
pb.leyenda(p5, "below")
p6 = pb.figura("Energía acumulada Σ h²[k], k ≤ n (normalizada)", "n", "", ancho=330, alto=200, y_range=(0, 1.05))
p6.step("n", "em", source=Hn, color=pb.GRIS, line_width=2, line_dash="dashed", mode="after", legend_label="fase mínima")
p6.step("n", "e", source=Hn, color=pb.AZUL, line_width=2, mode="after", legend_label="H")
pb.leyenda(p6, "below")

r1 = pb.deslizador("Par 1: radio r₁", 0.2, 0.95, 0.8, 0.05)
t1 = pb.deslizador("Par 1: ángulo θ₁ (rad)", 0.1, 3.0, 0.8, 0.05)
r2 = pb.deslizador("Par 2: radio r₂", 0.2, 0.95, 0.6, 0.05)
t2 = pb.deslizador("Par 2: ángulo θ₂ (rad)", 0.1, 3.0, 2.2, 0.05)
c = pb.deslizador("Cero real c", -0.9, 0.9, 0.5, 0.05)
refl = pb.casillas(["Reflejar el par 1 fuera del círculo", "Reflejar el par 2 fuera del círculo", "Reflejar el cero real"], [0])
info = Div(text="", width=240)

cb = pb.js("""
    const cr = Math.abs(c.value) < 0.05 ? 0.05 : c.value;
    const ceros = [cexp([Math.log(r1.value), t1.value]), cexp([Math.log(r1.value), -t1.value]),
                   cexp([Math.log(r2.value), t2.value]), cexp([Math.log(r2.value), -t2.value]), [cr, 0]];
    const grupo = [0, 0, 1, 1, 2], fuera = ceros.map((_, i) => refl.active.includes(grupo[i]));
    // Factor de cada cero en z⁻¹: dentro, 1 − z₀z⁻¹; reflejado en 1/z₀*, |z₀| − (z₀/|z₀|)z⁻¹, con el mismo módulo
    const factor = (z0, f) => f ? [[cabs(z0), 0], cesc(-1 / cabs(z0), z0)] : [[1, 0], cesc(-1, z0)];
    const pmul = (a, b) => { const y = new Array(a.length + b.length - 1).fill(0).map(() => [0, 0]);
        a.forEach((u, i) => b.forEach((v, j) => y[i + j] = csum(y[i + j], cmul(u, v)))); return y; };
    const coef = fs => ceros.reduce((acc, z0, i) => pmul(acc, factor(z0, fs[i])), [[1, 0]]).map(v => v[0]);
    const h = coef(fuera), hm = coef(ceros.map(() => false));
    const W = rango(0, PI, 801), resp = b => W.map(w => b.reduce((s, v, n) => csum(s, cesc(v, cexp([0, -w * n]))), [0, 0]));
    const H = resp(h), Hm = resp(hm);
    const fase = R => desenrollar(R.map(v => Math.atan2(v[1], v[0]))), f = fase(H), fm = fase(Hm), fa = f.map((v, i) => v - fm[i]);
    const dW = W[1] - W[0], retardo = g => g.map((v, i) => -(g[Math.min(i + 1, g.length - 1)] - g[Math.max(i - 1, 0)]) / (dW * (i > 0 && i < g.length - 1 ? 2 : 1)));
    F.data = {W: W, m: H.map(cabs), f: f, fm: fm, fa: fa, g: retardo(f), gm: retardo(fm), ga: retardo(fa)};
    const acum = b => { let s = 0; const t = b.reduce((a, v) => a + v * v, 0); return b.map(v => (s += v * v) / t); };
    Hn.data = {n: enteros(0, h.length - 1), h: h, hm: hm, e: acum(h), em: acum(hm)};
    const pos = ceros.map((z0, i) => fuera[i] ? cesc(1 / (cabs(z0) ** 2), z0) : z0);
    const alt = ceros.map((z0, i) => fuera[i] ? z0 : cesc(1 / (cabs(z0) ** 2), z0));
    Z.data = {x: pos.map(v => v[0]), y: pos.map(v => v[1]), color: fuera.map(v => v ? pb_ROJO : pb_AZUL)};
    Za.data = {x: alt.map(v => v[0]), y: alt.map(v => v[1])};
    const nf = fuera.filter(v => v).length;
    const clase = nf === 0 ? "de fase mínima" : nf === 5 ? "de fase máxima" : "de fase mixta";
    info.text = `<p><b>H(z) es ${clase}</b>: ${nf} de 5 ceros fuera del círculo unidad.</p>` +
        "<p>Reflejar un cero z₀ en 1/z₀* (y escalar por |z₀|) no cambia |H|, pero añade fase y retardo.</p>" +
        "<p>H(z) = H_min(z)·H_ap(z): H_min tiene todos los ceros dentro; H_ap es un paso todo con |H_ap| = 1 y retardo de grupo positivo.</p>" +
        `<p>Retraso de la energía: la mitad de la energía de h[n] llega en n = ${Hn.data.e.findIndex(v => v >= 0.5)}; en la de fase mínima, en n = ${Hn.data.em.findIndex(v => v >= 0.5)}.</p>`;
""", Z=Z, Za=Za, F=F, Hn=Hn, r1=r1, t1=t1, r2=r2, t2=t2, c=c, refl=refl, info=info, pb_ROJO=pb.ROJO, pb_AZUL=pb.AZUL)
pb.conectar(cb, r1, t1, r2, t2, c, refl)

pb.pagina(__file__, "Fase mínima y paso todo", tema=4,
          descripcion="Un FIR con cinco ceros: dos pares complejos conjugados y uno real. Cada cero se puede reflejar fuera del "
                      "círculo unidad, a 1/z₀*, sin que cambie |H(e^jΩ)|. De todos los sistemas con el mismo módulo, el de fase "
                      "mínima (todos los ceros dentro) tiene el menor retardo de grupo y concentra antes la energía de h[n]. "
                      "Cualquier otro es el de fase mínima en cascada con un paso todo.",
          controles=[r1, t1, r2, t2, c, refl, info], graficas=[[p1, p2], [p3, p4], [p5, p6]], inicio=cb,
          referencia="Transparencias T4-05, filtros especiales · Apuntes del Tema 4, sección 5")
