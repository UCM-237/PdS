"""T1 · Operaciones sobre la variable independiente: y(t) = x(αt + β)."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div, Span
import pds_bokeh as pb

S = ColumnDataSource(dict(t=[], x=[], v=[], y=[]))
D = ColumnDataSource(dict(n=[], x=[], v=[], y=[]))

p1 = pb.figura("Señal original x", "t", "", ancho=330, alto=200, x_range=(-6, 6), y_range=(-0.3, 1.3))
p1.line("t", "x", source=S, color=pb.GRIS, line_width=2)
pb.tallos(p1, "n", "x", D, color=pb.GRIS)
p2 = pb.figura("Paso 1: desplazar, v = x(t + β)", "t", "", ancho=330, alto=200, x_range=(-6, 6), y_range=(-0.3, 1.3))
p2.line("t", "v", source=S, color=pb.NARANJA, line_width=2)
pb.tallos(p2, "n", "v", D, color=pb.NARANJA)
p3 = pb.figura("Paso 2: escalar e invertir, y(t) = v(αt) = x(αt + β)", "t", "", ancho=720, alto=220,
               x_range=(-6, 6), y_range=(-0.3, 1.3))
p3.line("t", "x", source=S, color=pb.GRIS_CLARO, line_width=1.5, legend_label="x")
p3.line("t", "y", source=S, color=pb.AZUL, line_width=2.5, legend_label="y")
pb.tallos(p3, "n", "y", D, color=pb.AZUL)
pb.leyenda(p3, "right")
for p in (p1, p2, p3):
    p.add_layout(Span(location=0, dimension="height", line_color=pb.GRIS, line_width=1))

senal = pb.selector("Señal x", ["Triángulo asimétrico", "Pulso con escalón", "Exponencial truncada"])
dominio = pb.botones(["Continuo", "Discreto"])
alfa = pb.deslizador("α (escalado; negativo invierte)", -3, 3, 1, 0.1)
beta = pb.deslizador("β (desplazamiento)", -5, 5, 0, 0.1)
info = Div(text="", width=240)

cb = pb.js("""
    const f = u => senal.value.startsWith("Tri") ? (u >= -1 && u < 0 ? u + 1 : (u >= 0 && u <= 3 ? 1 - u / 3 : 0))
                 : senal.value.startsWith("Pulso") ? (u >= -1 && u < 1 ? 1 : (u >= 1 && u < 2 ? 0.5 : 0))
                 : (u >= 0 && u <= 4 ? Math.exp(-0.8 * u) : 0);
    const disc = dominio.active === 1;
    let a = alfa.value, b = beta.value;
    if (Math.abs(a) < 0.05) a = a < 0 ? -0.05 : 0.05;
    if (disc) { a = Math.round(a) || 1; b = Math.round(b); }
    const t = rango(-6, 6, 1201);
    const n = enteros(-6, 6);
    S.data = disc ? {t: [], x: [], v: [], y: []} : {t: t, x: t.map(f), v: t.map(u => f(u + b)), y: t.map(u => f(a * u + b))};
    D.data = disc ? {n: n, x: n.map(f), v: n.map(k => f(k + b)), y: n.map(k => f(a * k + b))} : {n: [], x: [], v: [], y: []};
    const ini = -b / a;
    info.text = `<p>${disc ? "y[n] = x[" + a + "n " + (b < 0 ? "− " + (-b) : "+ " + b) + "]" : "y(t) = x(" + a.toFixed(2) + "t " + (b < 0 ? "− " + (-b).toFixed(2) : "+ " + b.toFixed(2)) + ")"}</p>` +
        `<p>El punto t = 0 de x pasa a t = −β/α = ${ini.toFixed(2)}.</p>` +
        `<p>${Math.abs(a) > 1 ? "|α| > 1: se comprime" + (disc ? " y se pierden muestras (diezmado)" : "") : Math.abs(a) < 1 ? "|α| < 1: se expande" : "|α| = 1: sin cambio de escala"}` +
        `${a < 0 ? "; α < 0: se invierte" : ""}.</p>` +
        `<p>Orden alternativo: primero escalar, x(αt), y después desplazar β/α: x(α(t + β/α)).</p>` +
        (disc ? "<p>En discreto α y β se redondean a enteros.</p>" : "");
""", S=S, D=D, senal=senal, dominio=dominio, alfa=alfa, beta=beta, info=info)
pb.conectar(cb, senal, dominio, alfa, beta)

pb.pagina(__file__, "Operaciones sobre la variable independiente", tema=1,
          descripcion="y(t) = x(αt + β) se obtiene en dos pasos: desplazar x a la izquierda β unidades y después escalar "
                      "el eje por α (comprimir si |α| > 1, expandir si |α| < 1, invertir si α < 0). En discreto, "
                      "comprimir por un entero pierde muestras.",
          controles=[senal, dominio, alfa, beta, info], graficas=[[p1, p2], p3], inicio=cb,
          referencia="Transparencias T1-02, transformaciones de la variable independiente · Apuntes del Tema 1, sección 4")
