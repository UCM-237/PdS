"""T4 · Polos y ceros en el plano s y respuesta en frecuencia."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Div, Span
import pds_bokeh as pb

pz = ColumnDataSource(dict(x=[-0.3, -0.3, -1.0], y=[1.0, -1.0, 0.0], t=["polo", "polo", "polo"], par=[1, 1, 2]))
F = ColumnDataSource(dict(w=[], m=[], f=[]))
V = ColumnDataSource(dict(xs=[], ys=[], c=[]))
R = ColumnDataSource(dict(t=[], y=[]))
P = ColumnDataSource(dict(w=[0], m=[0]))

p1 = pb.figura("Plano s: arrastra, añade o borra", "Re s", "Im s", ancho=300, alto=300,
               x_range=(-3, 1), y_range=(-3, 3), tools="wheel_zoom,reset,save")
p1.add_layout(Span(location=0, dimension="height", line_color=pb.GRIS, line_width=1))
p1.add_layout(Span(location=0, dimension="width", line_color=pb.GRIS_CLARO, line_width=1))
p1.multi_line("xs", "ys", source=V, line_color="c", line_width=1, line_dash="dotted")
prueba = ColumnDataSource(dict(x=[0], y=[1]))
p1.scatter("x", "y", source=prueba, marker="diamond", size=10, color=pb.VERDE)
p2 = pb.figura("Módulo |H(jω)| (dB)", "ω (rad/s)", "dB", ancho=380, alto=200, x_range=(0, 3))
p2.line("w", "m", source=F, color=pb.AZUL, line_width=2)
p2.scatter("w", "m", source=P, size=9, color=pb.VERDE)
p3 = pb.figura("Fase ∠H(jω) (rad)", "ω (rad/s)", "rad", ancho=380, alto=150, x_range=(0, 3))
p3.line("w", "f", source=F, color=pb.ROJO, line_width=2)
p4 = pb.figura("Respuesta al escalón", "t (s)", "", ancho=380, alto=150)
p4.line("t", "y", source=R, color=pb.AZUL, line_width=2)

modo = pb.selector("Al hacer clic en el plano", ["Mover", "Añadir polo", "Añadir cero", "Borrar"])
w0 = pb.deslizador("ω₀ (punto de prueba jω₀, rad/s)", 0, 3, 1, 0.01)
info = Div(text="", width=240)

cb = pb.js("""
    const d = pz.data, polos = [], ceros = [];
    for (let i = 0; i < d.x.length; i++) (d.t[i] === "polo" ? polos : ceros).push([d.x[i], d.y[i]]);
    const w = rango(0, 3, 600), k0 = 1;
    let Hs = w.map(v => zpk(ceros, polos, k0, [0, v]));
    // Ganancia: H(0) = 1 si no hay polos ni ceros en el origen; si no, máximo de |H| igual a 1
    const h0 = cabs(zpk(ceros, polos, 1, [0, 1e-9])), k = (h0 > 1e-6 && h0 < 1e6) ? 1 / h0 : 1 / Math.max(...Hs.map(cabs));
    Hs = Hs.map(h => cesc(k, h));
    F.data = {w: w, m: Hs.map(h => db(cabs(h), -80)), f: desenrollar(Hs.map(h => Math.atan2(h[1], h[0])))};
    const s0 = [0, w0.value], h = cesc(k, zpk(ceros, polos, 1, s0));
    P.data = {w: [w0.value], m: [db(cabs(h), -80)]};
    prueba.data = {x: [0], y: [w0.value]};
    V.data = {xs: polos.concat(ceros).map(p => [p[0], 0]), ys: polos.concat(ceros).map(p => [p[1], w0.value]),
              c: polos.map(() => "#C0392B").concat(ceros.map(() => "#2B3A8C"))};
    const estable = polos.every(p => p[0] < 0), propio = ceros.length <= polos.length;
    let txt = "";
    if (propio && polos.length && estable) {
        const t = rango(0, 20, 400), y = continua(polireal(ceros).map(v => k * v), polireal(polos), t, "escalon");
        R.data = {t: t, y: y};
    } else { R.data = {t: [], y: []}; txt = propio ? "<p>Respuesta al escalón: no acotada (inestable).</p>" : "<p>Más ceros que polos: impropio.</p>"; }
    const dz = ceros.map(c => cabs(cres(s0, c))), dp = polos.map(p => cabs(cres(s0, p)));
    info.text = `<p><b>${estable ? "Estable" : "Inestable"}</b>: ${estable ? "todos los polos en Re s < 0" : "hay polos en Re s ≥ 0"}.</p>` +
        `<p>|H(jω₀)| = k·Π|jω₀ − c| / Π|jω₀ − p| = ${cabs(h).toFixed(3)}</p>` +
        `<p>Distancias a los polos: ${dp.map(v => v.toFixed(2)).join(", ") || "—"}<br>a los ceros: ${dz.map(v => v.toFixed(2)).join(", ") || "—"}</p>` + txt;
""", pz=pz, F=F, V=V, R=R, P=P, prueba=prueba, w0=w0, info=info)
pb.plano_pz(p1, pz, modo, callback=cb)
pb.leyenda(p1, "below")
pb.conectar(cb, w0)

pb.pagina(__file__, "Polos y ceros en el plano s", tema=4,
          descripcion="El módulo de H(jω) es el producto de las distancias de jω a los ceros dividido por el de las "
                      "distancias a los polos. Un polo cerca del eje jω produce un pico; un cero sobre el eje, un "
                      "nulo. Arrastra los polos y ceros (los complejos se mueven con su conjugado) o añade otros con un clic.",
          controles=[modo, w0, info], graficas=[[p1, column(p2, p3, p4)]], inicio=cb,
          referencia="Transparencias T4-02, polos, ceros y respuesta en frecuencia · Apuntes del Tema 4, secciones 1 y 2")
