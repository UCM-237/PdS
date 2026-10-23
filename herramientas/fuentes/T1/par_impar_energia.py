"""T1 · Parte par e impar de una señal; señales de energía y de potencia."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

S = ColumnDataSource(dict(t=[], x=[], xr=[], p=[], i=[]))
D = ColumnDataSource(dict(t=[], x=[], xr=[], p=[], i=[]))
EP = ColumnDataSource(dict(T=[], E=[], P=[]))

def tres(titulo, col, color, extra=None):
    p = pb.figura(titulo, "t o n", "", ancho=340 if extra is None else 720, alto=170, x_range=(-8, 8))
    if extra:
        p.line("t", extra, source=S, color=pb.GRIS_CLARO, line_width=2, line_dash="dashed", legend_label="x(−t)")
    p.line("t", col, source=S, color=color, line_width=2, **({"legend_label": "x(t)"} if extra else {}))
    pb.tallos(p, "t", col, D, color=color, size=5)
    if extra:
        pb.leyenda(p, "right")
    return p

p1 = tres("Señal x y su reflejada x(−t)", "x", pb.AZUL, extra="xr")
p2 = tres("Parte par x_p = [x(t) + x(−t)]/2", "p", pb.VERDE)
p3 = tres("Parte impar x_i = [x(t) − x(−t)]/2", "i", pb.ROJO)
p4 = pb.figura("Energía en [−T, T]", "T", "E(T)", ancho=340, alto=170, x_axis_type="log")
p4.line("T", "E", source=EP, color=pb.AZUL, line_width=2)
p5 = pb.figura("Potencia media en [−T, T]", "T", "E(T)/2T", ancho=340, alto=170, x_axis_type="log")
p5.line("T", "P", source=EP, color=pb.NARANJA, line_width=2)

senal = pb.selector("Señal", ["Pulso rectangular", "Exponencial causal e^(−at)u(t)", "Escalón u(t)",
                              "Sinusoide cos(t + φ)", "Rampa t·u(t)", "Exponencial bilateral impar"])
a = pb.deslizador("a (decaimiento)", 0.1, 2, 0.5, 0.05)
fi = pb.deslizador("φ (rad, sinusoide)", -3.14, 3.14, 0, 0.01)
t0 = pb.deslizador("Desplazamiento t₀: x(t − t₀)", -4, 4, 0, 0.5)
dom = pb.botones(["Continuo", "Discreto"])
info = Div(text="", width=240)

cb = pb.js("""
    const av = a.value, s = senal.value, sh = t0.value;
    const f = t => { t -= sh;
        if (s.startsWith("Pulso")) return t >= 0.5 && t < 2.5 ? 1 : 0;
        if (s.startsWith("Exponencial causal")) return t >= 0 ? Math.exp(-av * t) : 0;
        if (s.startsWith("Escalón")) return t >= 0 ? 1 : 0;
        if (s.startsWith("Sinusoide")) return Math.cos(t + fi.value);
        if (s.startsWith("Rampa")) return t >= 0 ? t : 0;
        return Math.sign(t) * Math.exp(-av * Math.abs(t)); };
    const disc = dom.active === 1, t = disc ? enteros(-8, 8) : rango(-8, 8, 1601);
    const fila = t => { const x = t.map(f), xr = t.map(v => f(-v));
        return {t: t, x: x, xr: xr, p: x.map((v, i) => (v + xr[i]) / 2), i: x.map((v, i) => (v - xr[i]) / 2)}; };
    const vacio = {t: [], x: [], xr: [], p: [], i: []};
    S.data = disc ? vacio : fila(t); D.data = disc ? fila(t) : vacio;
    // E(T) = ∫ de −T a T de |x|² (o la suma de n = −T a T) y P(T) = E(T)/2T (o E/(2T + 1)), para T de 1 a 1000
    const Ts = rango(0, 3, 61).map(v => 10 ** v), E = [], P = [];
    for (const T of Ts) {
        let e = 0;
        if (disc) { for (let n = -Math.floor(T); n <= Math.floor(T); n++) e += f(n) ** 2; P.push(e / (2 * Math.floor(T) + 1)); }
        else { const M = Math.ceil(T * 200), h = 2 * T / M; for (let k = 0; k < M; k++) e += f(-T + (k + 0.5) * h) ** 2 * h; P.push(e / (2 * T)); }
        E.push(e);
    }
    EP.data = {T: Ts, E: E, P: P};
    // Comprobación de E_x = E_p + E_i en la ventana mostrada (el producto cruzado par·impar integra cero)
    const sum = (v, w) => v.reduce((q, y) => q + y * y, 0) * w, d = disc ? fila(t) : S.data, w = disc ? 1 : 0.01;
    const Ex = sum(d.x, w), Ep = sum(d.p, w), Ei = sum(d.i, w);
    const clase = {"Pulso": "de energía: E = 2", "Exponencial causal": `de energía: E = 1/(2a) = ${(1 / (2 * av)).toFixed(3)}`,
        "Escalón": "de potencia: P = 1/2", "Sinusoide": "de potencia: P = 1/2", "Rampa": "ni de energía ni de potencia: E y P crecen sin límite",
        "Exponencial bilateral": `de energía: E = 1/a = ${(1 / av).toFixed(3)}`};
    const clave = Object.keys(clase).find(k => s.startsWith(k));
    info.text = `<p>En la ventana de la gráfica: E_x = ${Ex.toFixed(3)}, E_p + E_i = ${(Ep + Ei).toFixed(3)}.</p>` +
        `<p>Señal ${clase[clave]}${disc ? " (en continuo; en discreto, las sumas dan valores parecidos)" : ""}.</p>` +
        `<p>Con T = 1000: E = ${E[E.length - 1].toFixed(3)}, P = ${P[P.length - 1].toExponential(2)}.</p>` +
        "<p>Una señal de energía tiene E finita y P → 0; una de potencia, P finita y no nula y E → ∞.</p>";
""", S=S, D=D, EP=EP, senal=senal, a=a, fi=fi, t0=t0, dom=dom, info=info)
pb.conectar(cb, senal, a, fi, t0, dom)

pb.pagina(__file__, "Par, impar, energía y potencia", tema=1,
          descripcion="Toda señal es la suma de una parte par, x_p(t) = [x(t) + x(−t)]/2, y una impar, x_i(t) = [x(t) − x(−t)]/2. "
                      "Las gráficas de abajo acumulan la energía y la potencia media en una ventana [−T, T] cada vez más ancha: "
                      "si la energía se estabiliza, la señal es de energía; si lo hace la potencia, es de potencia.",
          controles=[senal, a, fi, t0, dom, info], graficas=[p1, [p2, p3], [p4, p5]], inicio=cb,
          referencia="Transparencias T1-01, clasificación de señales · Apuntes del Tema 1, sección 2")
