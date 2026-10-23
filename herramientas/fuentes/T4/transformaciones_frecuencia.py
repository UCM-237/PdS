"""T4 · Transformaciones en frecuencia de un prototipo paso bajo."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
import numpy as np
from bokeh.models import ColumnDataSource, Div, Span
import pds_bokeh as pb

# Diseño en ceros, polos y ganancia, como lp2lp_zpk, lp2hp_zpk, lp2bp_zpk, lp2bs_zpk y bilinear_zpk de SciPy
DISENO = """
function prototipo(cheby, N, rp) {
    if (!cheby) return [[], polos_butter(N, 1), 1];
    const e = Math.sqrt(10 ** (rp / 10) - 1), mu = Math.asinh(1 / e) / N, p = [];
    for (let k = 1; k <= N; k++) { const t = (2 * k - 1) * PI / (2 * N); p.push([-Math.sinh(mu) * Math.sin(t), Math.cosh(mu) * Math.cos(t)]); }
    let g = [1, 0]; p.forEach(v => g = cmul(g, cesc(-1, v)));
    return [[], p, g[0] / (N % 2 ? 1 : Math.sqrt(1 + e * e))];
}
function transformar(z, p, k, tipo, w1, w2) {
    const g = p.length - z.length, wo = Math.sqrt(w1 * w2), bw = w2 - w1, prod = v => v.reduce((a, b) => cmul(a, cesc(-1, b)), [1, 0]);
    if (tipo === "Paso bajo") return [z.map(v => cesc(w1, v)), p.map(v => cesc(w1, v)), k * w1 ** g];
    if (tipo === "Paso alto") {
        const kk = k * cdiv(prod(z), prod(p))[0];
        return [z.map(v => cdiv([w1, 0], v)).concat(new Array(g).fill(0).map(() => [0, 0])), p.map(v => cdiv([w1, 0], v)), kk];
    }
    const par = v => { const r = csqrt(cres(cmul(v, v), [wo * wo, 0])); return [csum(v, r), cres(v, r)]; };
    if (tipo === "Paso banda") {
        const zz = z.map(v => cesc(bw / 2, v)).flatMap(par).concat(new Array(g).fill(0).map(() => [0, 0]));
        return [zz, p.map(v => cesc(bw / 2, v)).flatMap(par), k * bw ** g];
    }
    const kk = k * cdiv(prod(z), prod(p))[0], ceros = [];
    for (let i = 0; i < g; i++) ceros.push([0, wo], [0, -wo]);
    return [z.map(v => cdiv([bw / 2, 0], v)).flatMap(par).concat(ceros), p.map(v => cdiv([bw / 2, 0], v)).flatMap(par), kk];
}
// Bilineal con 2/T = 2: z = (2 + s)/(2 − s); los ceros en el infinito van a z = −1
function bilineal(z, p, k) {
    const f = v => cdiv(csum([2, 0], v), cres([2, 0], v)), pr = v => v.reduce((a, b) => cmul(a, cres([2, 0], b)), [1, 0]);
    return [z.map(f).concat(new Array(p.length - z.length).fill(0).map(() => [-1, 0])), p.map(f), k * cdiv(pr(z), pr(p))[0]];
}
"""

Hp = ColumnDataSource(dict(w=[], m=[]))
H = ColumnDataSource(dict(w=[], m=[]))
Po = ColumnDataSource(dict(x=[], y=[]))
Ce = ColumnDataSource(dict(x=[], y=[]))
Ci = ColumnDataSource(dict(x=[], y=[]))
Mk = ColumnDataSource(dict(x=[], y0=[], y1=[]))

p1 = pb.figura("Prototipo paso bajo |H_p(jω)| (ωc = 1)", "ω (rad/s)", "", ancho=300, alto=200, x_range=(0, 3))
p1.line("w", "m", source=Hp, color=pb.GRIS, line_width=2)
p1.add_layout(Span(location=1, dimension="height", line_color=pb.GRIS_CLARO, line_dash="dashed"))
p2 = pb.figura("Polos (×) y ceros (○)", "Re", "Im", ancho=230, alto=230, x_range=(-4, 2), y_range=(-3, 3))
p2.line("x", "y", source=Ci, color=pb.GRIS, line_width=1)
p2.add_layout(Span(location=0, dimension="height", line_color=pb.GRIS_CLARO))
p2.add_layout(Span(location=0, dimension="width", line_color=pb.GRIS_CLARO))
p2.scatter("x", "y", source=Po, marker="x", size=12, line_width=2.5, color=pb.ROJO)
p2.scatter("x", "y", source=Ce, marker="circle", size=11, line_width=2, line_color=pb.AZUL, fill_color=None)
p3 = pb.figura("Filtro transformado |H|", "ω (rad/s)", "", ancho=480, alto=230, x_range=(0, 3.1416))
p3.segment(x0="x", x1="x", y0="y0", y1="y1", source=Mk, color=pb.NARANJA, line_dash="dashed", line_width=1.5)
p3.line("w", "m", source=H, color=pb.AZUL, line_width=2)

proto = pb.selector("Prototipo", ["Butterworth", "Chebyshev I"])
N = pb.deslizador("Orden N del prototipo", 1, 8, 3, 1)
rp = pb.deslizador("Rizado en la banda de paso (dB, Chebyshev)", 0.1, 3, 1, 0.1)
tipo = pb.selector("Transformación", ["Paso bajo", "Paso alto", "Paso banda", "Banda eliminada"], valor="Paso banda")
w1 = pb.deslizador("Frecuencia de corte 1 (ω₁ o Ω₁)", 0.1, 3, 0.8, 0.05)
w2 = pb.deslizador("Frecuencia de corte 2 (ω₂ o Ω₂)", 0.1, 3, 1.6, 0.05)
dom = pb.botones(["Continuo", "Discreto (bilineal)"])
escala = pb.botones(["Lineal", "dB"])
info = Div(text="", width=240)

cb = pb.js(DISENO + """
    const ch = proto.value !== "Butterworth", d = dom.active === 1, n = N.value, t = tipo.value;
    let a = Math.min(w1.value, w2.value), b = Math.max(w1.value, w2.value); if (b - a < 0.05) b = a + 0.05;
    const banda = t === "Paso banda" || t === "Banda eliminada";
    // En discreto se predistorsionan las frecuencias de corte: ω = 2·tan(Ω/2)
    const pw = v => d ? 2 * Math.tan(Math.min(v, 3.1) / 2) : v;
    const [zp, pp, kp] = prototipo(ch, n, rp.value);
    let [z, p, k] = transformar(zp, pp, kp, t, pw(a), banda ? pw(b) : pw(a));
    if (d) [z, p, k] = bilineal(z, p, k);
    const lim = v => Math.max(-60, v), esc = v => escala.active ? lim(20 * Math.log10(Math.max(v, 1e-12))) : v;
    const W = rango(0.0005, 3, 600);
    Hp.data = {w: W, m: W.map(w => esc(cabs(zpk(zp, pp, kp, [0, w]))))};
    const Wt = rango(0.0005, d ? PI : 3.1416, 900);
    H.data = {w: Wt, m: Wt.map(w => esc(cabs(zpk(z, p, k, d ? cexp([0, w]) : [0, w]))))};
    const lo = escala.active ? -60 : 0, hi = escala.active ? 3 : 1.15;
    Mk.data = banda ? {x: [a, b], y0: [lo, lo], y1: [hi, hi]} : {x: [a], y0: [lo], y1: [hi]};
    Po.data = {x: p.map(v => v[0]), y: p.map(v => v[1])}; Ce.data = {x: z.map(v => v[0]), y: z.map(v => v[1])};
    const th = rango(0, 2 * PI, 200); Ci.data = d ? {x: th.map(Math.cos), y: th.map(Math.sin)} : {x: [], y: []};
    p2.title.text = d ? "Polos (×) y ceros (○) en el plano z" : "Polos (×) y ceros (○) en el plano s";
    p2.below[0].axis_label = d ? "Re z" : "Re s"; p2.left[0].axis_label = d ? "Im z" : "Im s";
    const R = d ? 1.4 : Math.max(1.2, ...p.concat(z).map(cabs)) * 1.15;
    p2.x_range.start = d ? -R : -R * 1.4; p2.x_range.end = d ? R : R * 0.6; p2.y_range.start = -R; p2.y_range.end = R;
    p3.below[0].axis_label = d ? "Ω (rad/muestra)" : "ω (rad/s)";
    p3.title.text = (d ? "Filtro digital |H(e^jΩ)|" : "Filtro analógico |H(jω)|") + (escala.active ? " (dB)" : "");
    const s = ["s/ω₁", "ω₁/s", "(s² + ω₀²)/(B·s)", "B·s/(s² + ω₀²)"][["Paso bajo", "Paso alto", "Paso banda", "Banda eliminada"].indexOf(t)];
    info.text = `<p>Sustitución en el prototipo: s → ${s}</p>` +
        (banda ? `<p>ω₀ = √(ω₁ω₂) = ${Math.sqrt(pw(a) * pw(b)).toFixed(3)} rad/s, B = ω₂ − ω₁ = ${(pw(b) - pw(a)).toFixed(3)} rad/s</p>` : "") +
        (d ? `<p>Predistorsión: ω = 2·tan(Ω/2): ${banda ? `Ω₁ = ${a.toFixed(2)} → ω₁ = ${pw(a).toFixed(3)}; Ω₂ = ${b.toFixed(2)} → ω₂ = ${pw(b).toFixed(3)}` : `Ω₁ = ${a.toFixed(2)} → ω₁ = ${pw(a).toFixed(3)}`}</p>` +
             "<p>Después, bilineal: s = 2(z − 1)/(z + 1).</p>" : "") +
        `<p>Orden del filtro: ${p.length} (${banda ? "el doble que" : "igual que"} el prototipo)</p>`;
""", Hp=Hp, H=H, Po=Po, Ce=Ce, Ci=Ci, Mk=Mk, proto=proto, N=N, rp=rp, tipo=tipo, w1=w1, w2=w2,
   dom=dom, escala=escala, info=info, p2=p2, p3=p3)
pb.conectar(cb, proto, N, rp, tipo, w1, w2, dom, escala)

pb.pagina(__file__, "Transformaciones en frecuencia", tema=4,
          descripcion="Un filtro paso alto, paso banda o de banda eliminada se obtiene a partir de un prototipo paso bajo "
                      "normalizado (ωc = 1) cambiando la variable s. Cada transformación lleva la banda de paso del prototipo "
                      "a la nueva banda; las de paso banda y banda eliminada duplican el orden. En discreto, las frecuencias "
                      "de corte se predistorsionan y luego se aplica la transformación bilineal.",
          controles=[proto, N, rp, tipo, w1, w2, dom, escala, info], graficas=[[p1, p2], p3], inicio=cb,
          referencia="Transparencias T4-02, transformaciones en frecuencia · Apuntes del Tema 4, secciones 2 y 3")
