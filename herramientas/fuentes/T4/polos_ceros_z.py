"""T4 · Polos y ceros en el plano z y respuesta en frecuencia."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
import numpy as np
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Div, Span
import pds_bokeh as pb

pz = ColumnDataSource(dict(x=[0.6, 0.6, -1.0], y=[0.6, -0.6, 0.0], t=["polo", "polo", "cero"], par=[1, 1, 2]))
F = ColumnDataSource(dict(W=[], m=[], f=[]))
V = ColumnDataSource(dict(xs=[], ys=[], c=[]))
R = ColumnDataSource(dict(n=[], h=[]))
P = ColumnDataSource(dict(W=[0], m=[0]))
prueba = ColumnDataSource(dict(x=[1], y=[0]))

p1 = pb.figura("Plano z: arrastra, añade o borra", "Re z", "Im z", ancho=300, alto=300,
               x_range=(-1.6, 1.6), y_range=(-1.6, 1.6), tools="wheel_zoom,reset,save")
th = np.linspace(0, 2 * np.pi, 200)
p1.line(np.cos(th), np.sin(th), color=pb.GRIS, line_width=1)
p1.add_layout(Span(location=0, dimension="height", line_color=pb.GRIS_CLARO, line_width=1))
p1.add_layout(Span(location=0, dimension="width", line_color=pb.GRIS_CLARO, line_width=1))
p1.multi_line("xs", "ys", source=V, line_color="c", line_width=1, line_dash="dotted")
p1.scatter("x", "y", source=prueba, marker="diamond", size=10, color=pb.VERDE)
p2 = pb.figura("Módulo |H(e^jΩ)| (dB)", "Ω (rad/muestra)", "dB", ancho=380, alto=200, x_range=(0, 3.1416))
p2.line("W", "m", source=F, color=pb.AZUL, line_width=2)
p2.scatter("W", "m", source=P, size=9, color=pb.VERDE)
p3 = pb.figura("Fase ∠H(e^jΩ) (rad)", "Ω (rad/muestra)", "rad", ancho=380, alto=150, x_range=(0, 3.1416))
p3.line("W", "f", source=F, color=pb.ROJO, line_width=2)
p4 = pb.figura("Respuesta al impulso h[n]", "n", "", ancho=380, alto=150)
pb.tallos(p4, "n", "h", R)

# Ejemplos: (polos, ceros) con un elemento por punto del semiplano superior o del eje real
def _pares(polos, ceros):
    x, y, t, par = [], [], [], []
    for tipo, lista in (("polo", polos), ("cero", ceros)):
        for z in lista:
            grupo = [z, np.conj(z)] if abs(np.imag(z)) > 1e-9 else [z]
            n = len(set(par)) + 1
            for v in grupo:
                x.append(round(float(np.real(v)), 4)); y.append(round(float(np.imag(v)), 4)); t.append(tipo); par.append(n)
    return dict(x=x, y=y, t=t, par=par)
e = np.exp(1j)
EJEMPLOS = {
    "Paso bajo de un polo": _pares([0.8], []),
    "Paso alto de un polo": _pares([-0.8], []),
    "Resonador (polos cerca de la circunferencia)": _pares([0.95 * e], []),
    "Muesca (ceros sobre la circunferencia)": _pares([0.9 * e], [e]),
    "Paso todo de primer orden": _pares([0.7], [1 / 0.7]),
    "Media móvil de 5 muestras (FIR)": _pares([], [np.exp(2j * np.pi / 5), np.exp(4j * np.pi / 5)]),
    "Inestable (polos fuera)": _pares([1.1 * np.exp(0.6j)], [-1]),
}
ejemplo = pb.selector("Cargar un ejemplo", ["—"] + list(EJEMPLOS))
modo = pb.selector("Al hacer clic en el plano", ["Mover", "Añadir polo", "Añadir cero", "Borrar"])
W0 = pb.deslizador("Ω₀ (punto de prueba e^jΩ₀)", 0, 3.14, 1, 0.01)
info = Div(text="", width=240)

cb = pb.js("""
    const d = pz.data, polos = [], ceros = [];
    for (let i = 0; i < d.x.length; i++) (d.t[i] === "polo" ? polos : ceros).push([d.x[i], d.y[i]]);
    // Si hay más ceros que polos, se añaden polos en el origen (un retraso) para que sea causal
    const extra = Math.max(0, ceros.length - polos.length), pc = polos.concat(new Array(extra).fill(0).map(() => [0, 0]));
    const W = rango(0, PI, 600);
    let Hz = W.map(w => zpk(ceros, pc, 1, cexp([0, w])));
    const k = 1 / Math.max(...Hz.map(cabs));
    Hz = Hz.map(h => cesc(k, h));
    F.data = {W: W, m: Hz.map(h => db(cabs(h), -80)), f: desenrollar(Hz.map(h => Math.atan2(h[1], h[0])))};
    const z0 = cexp([0, W0.value]), h0 = cesc(k, zpk(ceros, pc, 1, z0));
    P.data = {W: [W0.value], m: [db(cabs(h0), -80)]};
    prueba.data = {x: [z0[0]], y: [z0[1]]};
    V.data = {xs: polos.concat(ceros).map(p => [p[0], z0[0]]), ys: polos.concat(ceros).map(p => [p[1], z0[1]]),
              c: polos.map(() => "#C0392B").concat(ceros.map(() => "#2B3A8C"))};
    const [b, a] = ba(ceros, pc, k), x = new Array(40).fill(0); x[0] = 1;
    R.data = {n: enteros(0, 39), h: filtrar(b, a, x)};
    const estable = polos.every(p => cabs(p) < 1), fir = polos.every(p => cabs(p) < 1e-9);
    info.text = `<p><b>${estable ? "Estable" : "Inestable"}</b>: ${estable ? "todos los polos dentro de la circunferencia unidad" : "hay polos en |z| ≥ 1"}.</p>` +
        `<p>${fir ? "Sin polos fuera del origen: FIR (h[n] de duración finita)." : "Con polos fuera del origen: IIR."}</p>` +
        `<p>|H(e^jΩ₀)| = ${cabs(h0).toFixed(3)}; distancias a los polos: ${polos.map(p => cabs(cres(z0, p)).toFixed(2)).join(", ") || "—"}; ` +
        `a los ceros: ${ceros.map(c => cabs(cres(z0, c)).toFixed(2)).join(", ") || "—"}</p>` +
        (extra ? `<p>Se añaden ${extra} polos en z = 0 para que el sistema sea causal.</p>` : "");
""", pz=pz, F=F, V=V, R=R, P=P, prueba=prueba, W0=W0, info=info)
pb.plano_pz(p1, pz, modo, callback=cb, real_tol=0.02)
pb.leyenda(p1, "below")
pb.conectar(cb, W0)
ejemplo.js_on_change("value", pb.js("""
    if (ejemplo.value in E) { pz.data = Object.assign({}, E[ejemplo.value]); cb.execute(); }
""", ejemplo=ejemplo, E=EJEMPLOS, pz=pz, cb=cb))

pb.pagina(__file__, "Polos y ceros en el plano z", tema=4,
          descripcion="La respuesta en frecuencia se lee sobre la circunferencia unidad: |H(e^jΩ)| es el cociente "
                      "entre el producto de distancias de e^jΩ a los ceros y el de distancias a los polos. Un polo "
                      "cerca de la circunferencia da un pico estrecho y una h[n] que tarda en extinguirse; fuera de ella, "
                      "el sistema es inestable. Carga un ejemplo para empezar.",
          controles=[ejemplo, modo, W0, info], graficas=[[p1, column(p2, p3, p4)]], inicio=cb,
          referencia="Transparencias T4-01, polos, ceros y respuesta en frecuencia · Apuntes del Tema 4")
