"""T1 · Convolución continua: invertir, desplazar, multiplicar e integrar."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Span
import pds_bokeh as pb

SENALES = ["Pulso de anchura 1", "Pulso de anchura 2", "Triángulo", "Exponencial e^(−t)u(t)",
           "Escalón u(t)", "Rampa en [0, 1]"]

senales = ColumnDataSource(dict(tau=[], x=[], h=[], p=[]))
salida = ColumnDataSource(dict(t=[], y=[]))
actual = ColumnDataSource(dict(t=[], y=[]))

p1 = pb.figura("x(τ) y h(t − τ)", "τ", "", ancho=620, alto=170, x_range=(-4, 6))
p1.line("tau", "x", source=senales, color=pb.AZUL, line_width=2, legend_label="x(τ)")
p1.line("tau", "h", source=senales, color=pb.ROJO, line_width=2, legend_label="h(t − τ)")
p2 = pb.figura("x(τ) h(t − τ): su área es y(t)", "τ", "", ancho=620, alto=150, x_range=p1.x_range)
p2.varea("tau", 0, "p", source=senales, fill_color=pb.VERDE, fill_alpha=0.35)
p2.line("tau", "p", source=senales, color=pb.VERDE, line_width=1.5)
p3 = pb.figura("y(t) = (x * h)(t)", "t", "y(t)", ancho=620, alto=170, x_range=p1.x_range)
p3.line("t", "y", source=salida, color=pb.GRIS_CLARO, line_width=1.5, legend_label="y(t) completa")
p3.line("t", "y", source=actual, color=pb.AZUL, line_width=2.5, legend_label="calculada hasta t")
marca = Span(location=0, dimension="height", line_color=pb.NARANJA, line_dash="dashed")
for q in (p1, p2, p3):
    q.add_layout(marca)
for q in (p1, p3):
    pb.leyenda(q, "right")

sx = pb.selector("Señal x(t)", SENALES, SENALES[0])
sh = pb.selector("Respuesta al impulso h(t)", SENALES, SENALES[3])
t = pb.deslizador("t (desplazamiento)", -3, 5, -1, 0.02)

cb = pb.js("""
    function forma(nombre, u) {
        if (nombre.startsWith("Pulso de anchura 1")) return (u >= 0 && u < 1) ? 1 : 0;
        if (nombre.startsWith("Pulso de anchura 2")) return (u >= 0 && u < 2) ? 1 : 0;
        if (nombre.startsWith("Triángulo")) return (u >= 0 && u < 2) ? 1 - Math.abs(u - 1) : 0;
        if (nombre.startsWith("Exponencial")) return u >= 0 ? Math.exp(-u) : 0;
        if (nombre.startsWith("Escalón")) return u >= 0 ? 1 : 0;
        return (u >= 0 && u < 1) ? u : 0;
    }
    const dt = 0.01, tau = rango(-4, 6, 1001), T = t.value;
    const x = tau.map(u => forma(sx.value, u)), h = tau.map(u => forma(sh.value, T - u));
    senales.data = {tau: tau, x: x, h: h, p: x.map((v, i) => v * h[i])};
    // y(t) completa por integración numérica
    const ts = rango(-4, 6, 501), y = ts.map(tt => {
        let s = 0; for (let i = 0; i < tau.length; i++) s += x[i] * forma(sh.value, tt - tau[i]);
        return s * dt; });
    salida.data = {t: ts, y: y};
    const k = ts.findIndex(v => v > T);
    actual.data = {t: ts.slice(0, k < 0 ? ts.length : k), y: y.slice(0, k < 0 ? ts.length : k)};
    marca.location = T;
""", senales=senales, salida=salida, actual=actual, marca=marca, sx=sx, sh=sh, t=t)
pb.conectar(cb, sx, sh, t)

pb.pagina(__file__, "Convolución continua", tema=1,
          descripcion="y(t) = ∫ x(τ) h(t − τ) dτ. Para cada t se invierte h, se desplaza hasta t, "
                      "se multiplica por x y se integra. Mueve t para ver cómo se construye y(t); "
                      "su duración es la suma de las duraciones de x y h.",
          controles=[sx, sh, t], graficas=[p1, p2, p3], inicio=cb,
          referencia="Transparencias T1-02, «Convolución continua: ejemplo» · Apuntes del Tema 1, sección 5")
