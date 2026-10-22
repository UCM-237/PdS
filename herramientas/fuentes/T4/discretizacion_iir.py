"""T4 · Diseño de filtros IIR por discretización de un prototipo analógico."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
import numpy as np
from bokeh.models import ColumnDataSource, Div, Span
import pds_bokeh as pb

S = ColumnDataSource(dict(x=[], y=[]))
Zp = ColumnDataSource(dict(x=[], y=[]))
Zc = ColumnDataSource(dict(x=[], y=[]))
F = ColumnDataSource(dict(w=[], a=[], d=[]))
Ra = ColumnDataSource(dict(t=[], y=[]))
Rd = ColumnDataSource(dict(t=[], y=[]))

p1 = pb.figura("Polos del prototipo en el plano s", "Re s", "Im s", ancho=200, alto=210,
               x_range=(-6, 1), y_range=(-6, 6))
p1.add_layout(Span(location=0, dimension="height", line_color=pb.GRIS, line_width=1))
p1.scatter("x", "y", source=S, marker="x", size=12, line_width=2.5, color=pb.ROJO)
p2 = pb.figura("Polos y ceros de H(z)", "Re z", "Im z", ancho=200, alto=210, x_range=(-2, 2), y_range=(-2, 2))
th = np.linspace(0, 2 * np.pi, 200)
p2.line(np.cos(th), np.sin(th), color=pb.GRIS, line_width=1)
p2.scatter("x", "y", source=Zp, marker="x", size=12, line_width=2.5, color=pb.ROJO)
p2.scatter("x", "y", source=Zc, marker="circle", size=11, line_width=2, line_color=pb.AZUL, fill_color=None)
p3 = pb.figura("Módulo: analógico |H(jω)| y digital |H(e^jωT)|", "ω (rad/s), hasta ωs/2 = π/T", "",
               ancho=300, alto=210)
p3.line("w", "a", source=F, color=pb.GRIS, line_width=2, line_dash="dashed", legend_label="analógico")
p3.line("w", "d", source=F, color=pb.AZUL, line_width=2, legend_label="digital")
pb.leyenda(p3, "below")
p4 = pb.figura("Respuesta temporal", "t (s)", "", ancho=720, alto=200)
p4.line("t", "y", source=Ra, color=pb.GRIS, line_width=2, line_dash="dashed", legend_label="analógico")
pb.tallos(p4, "t", "y", Rd, color=pb.AZUL, legend_label="digital, en t = nT")
pb.leyenda(p4, "right")

metodo = pb.selector("Método", ["Invarianza al impulso", "Transformación bilineal", "Bilineal con predistorsión",
                                "Correspondencia de polos y ceros", "Euler hacia atrás", "Euler hacia delante"])
N = pb.deslizador("Orden N del Butterworth", 1, 6, 2, 1)
wc = pb.deslizador("ωc (rad/s)", 0.2, 5, 1, 0.05)
T = pb.deslizador("Periodo de muestreo T (s)", 0.05, 2, 0.5, 0.01)
resp = pb.botones(["Escalón", "Impulso (h[n]/T)"])
escala = pb.botones(["Lineal", "dB"])
info = Div(text="", width=240)

cb = pb.js("""
    const n = N.value, Ts = T.value, wcv = wc.value, m = metodo.value, ws2 = PI / Ts;
    const ps = polos_butter(n, wcv), ks = wcv ** n;
    S.data = {x: ps.map(p => p[0]), y: ps.map(p => p[1])};
    let b, a, pz, cz = [], aviso = "";
    if (m.startsWith("Invarianza")) {
        pz = ps.map(p => cexp(cesc(Ts, p)));
        const bc = new Array(n).fill(0).map(() => [0, 0]);
        ps.forEach((p, i) => {
            let r = [ks, 0]; ps.forEach((q, j) => { if (j !== i) r = cdiv(r, cres(p, q)); });
            const c = poli(pz.filter((_, j) => j !== i));
            c.forEach((v, j) => { bc[j] = csum(bc[j], cesc(Ts, cmul(r, v))); });
        });
        b = bc.map(v => v[0]); a = polireal(pz);
        // H(z) = z·b(z)/a(z) con b de grado N − 1: un cero en el origen y las raíces de b
        cz = [[0, 0]].concat(raices(b));
    } else {
        let p = ps, wcp = wcv;
        if (m === "Bilineal con predistorsión") {
            if (wcv * Ts / 2 >= PI / 2 * 0.98) aviso = "<p>ωc ≥ ωs/2: no se puede predistorsionar.</p>";
            wcp = 2 / Ts * Math.tan(Math.min(wcv * Ts / 2, PI / 2 * 0.98)); p = polos_butter(n, wcp);
            S.data = {x: p.map(v => v[0]), y: p.map(v => v[1])};
        }
        if (m.includes("ilineal")) { pz = p.map(v => cdiv(csum([1, 0], cesc(Ts / 2, v)), cres([1, 0], cesc(Ts / 2, v)))); cz = pz.map(() => [-1, 0]); }
        else if (m.startsWith("Correspondencia")) { pz = p.map(v => cexp(cesc(Ts, v))); cz = pz.map(() => [-1, 0]); }
        else if (m === "Euler hacia atrás") { pz = p.map(v => cdiv([1, 0], cres([1, 0], cesc(Ts, v)))); cz = pz.map(() => [0, 0]); }
        else { pz = p.map(v => csum([1, 0], cesc(Ts, v))); cz = []; }
        const k = 1 / zpk(cz, pz, 1, [1, 0])[0];
        [b, a] = ba(cz, pz, k);
    }
    Zp.data = {x: pz.map(v => v[0]), y: pz.map(v => v[1])};
    Zc.data = {x: cz.map(v => v[0]), y: cz.map(v => v[1])};
    // Respuesta en frecuencia hasta ωs/2
    const w = rango(0, ws2, 400), enDB = escala.active === 1;
    const Hd = w.map(v => { const z1 = cexp([0, -v * Ts]); return cdiv(evalpoli(b.slice().reverse(), z1), evalpoli(a.slice().reverse(), z1)); });
    const Ha = w.map(v => 1 / Math.sqrt(1 + (v / wcv) ** (2 * n)));
    const f = x => enDB ? db(x, -80) : x;
    F.data = {w: w, a: Ha.map(f), d: Hd.map(h => f(cabs(h)))};
    // Respuesta temporal: analógica en una rejilla fina y digital en t = nT
    const imp = resp.active === 1, tf = Math.max(12 / wcv, 10 * Ts), M = Math.min(400, Math.ceil(tf / Ts) + 1);
    const ta = rango(0, (M - 1) * Ts, 500), ya = continua([ks], polireal(ps), ta, imp ? "impulso" : "escalon");
    const x = new Array(M).fill(imp ? 0 : 1); if (imp) x[0] = 1;
    const yd = filtrar(b, a, x).map(v => imp ? v / Ts : v);
    Ra.data = {t: ta, y: ya}; Rd.data = {t: enteros(0, M - 1).map(i => i * Ts), y: yd};
    p4.title.text = imp ? "Respuesta al impulso: h(t) y h[n]/T" : "Respuesta al escalón";
    const estable = pz.every(v => cabs(v) < 1), g0 = cabs(cdiv(evalpoli(b.slice().reverse(), [1, 0]), evalpoli(a.slice().reverse(), [1, 0])));
    const gp = cabs(cdiv(evalpoli(b.slice().reverse(), [-1, 0]), evalpoli(a.slice().reverse(), [-1, 0])));
    info.text = `<p>ωs/2 = π/T = ${ws2.toFixed(2)} rad/s; ωc·T = ${(wcv * Ts).toFixed(2)} rad/muestra</p>` +
        `<p><b>${estable ? "Estable" : "Inestable"}</b>: ${estable ? "polos dentro de |z| = 1" : "hay polos en |z| ≥ 1"}</p>` +
        `<p>Ganancia en continua: ${g0.toFixed(3)}; en Ω = π: ${gp.toExponential(2)}</p>` + aviso +
        (m.startsWith("Invarianza") ? "<p>z = e^{sT}: los polos se transforman exactamente, pero |H(jω)| se repite cada ωs y se solapa (aliasing).</p>"
         : m.includes("ilineal") ? "<p>s = (2/T)(z − 1)/(z + 1): sin aliasing, pero comprime el eje ω (Ω = 2 arctan(ωT/2))" + (m.endsWith("predistorsión") ? "; la predistorsión hace coincidir ωc." : ".") + "</p>"
         : m.startsWith("Euler hacia d") ? "<p>z = 1 + sT: un polo estable puede quedar fuera de la circunferencia si T es grande.</p>"
         : m.startsWith("Euler") ? "<p>z = 1/(1 − sT): siempre estable, pero deforma la respuesta si T no es pequeño.</p>"
         : "<p>Polos en e^{pT} y ceros del infinito en z = −1; ganancia ajustada en continua.</p>");
""", S=S, Zp=Zp, Zc=Zc, F=F, Ra=Ra, Rd=Rd, metodo=metodo, N=N, wc=wc, T=T, resp=resp, escala=escala,
    info=info, p4=p4)
pb.conectar(cb, metodo, N, wc, T, resp, escala)

pb.pagina(__file__, "Discretización de filtros IIR", tema=4,
          descripcion="Un filtro IIR se obtiene transformando un prototipo analógico (aquí, un Butterworth de orden N). "
                      "La invarianza al impulso conserva h(t) en los instantes de muestreo pero sufre aliasing; la "
                      "bilineal no tiene aliasing pero deforma el eje de frecuencias, y se corrige predistorsionando ωc. "
                      "Al reducir T todos los métodos se parecen al analógico.",
          controles=[metodo, N, wc, T, resp, escala, info], graficas=[[p1, p2, p3], p4], inicio=cb,
          referencia="Transparencias T4-03, filtros IIR · Apuntes del Tema 4, sección 3")
