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
T0, T1 = -4, 6  # eje común de τ y de t; el desplazamiento recorre el mismo rango

# Arriba: las dos señales y el área de su producto, que es y(t)
p1 = pb.figura("x(τ), h(t − τ) y su producto: el área sombreada es y(t)", "τ", "",
               ancho=None, alto=210, x_range=(T0, T1))
p1.varea("tau", 0, "p", source=senales, fill_color=pb.VERDE, fill_alpha=0.30,
         legend_label="x(τ) h(t − τ)")
p1.line("tau", "x", source=senales, color=pb.AZUL, line_width=2, legend_label="x(τ)")
p1.line("tau", "h", source=senales, color=pb.ROJO, line_width=2, legend_label="h(t − τ)")
# Abajo: la salida completa y lo calculado hasta el instante actual
p2 = pb.figura("y(t) = (x ∗ h)(t)", "t", "y(t)", ancho=None, alto=190, x_range=p1.x_range)
p2.line("t", "y", source=salida, color=pb.GRIS_CLARO, line_width=1.5, legend_label="y(t) completa")
p2.line("t", "y", source=actual, color=pb.AZUL, line_width=2.5, legend_label="calculada hasta t")
punto = ColumnDataSource(dict(t=[], y=[]))
p2.scatter("t", "y", source=punto, color=pb.NARANJA, size=8)
marca = Span(location=0, dimension="height", line_color=pb.NARANJA, line_dash="dashed")
for q in (p1, p2):
    q.add_layout(marca)
    pb.leyenda(q, "top_left")

sx = pb.selector("Señal x(t)", SENALES, SENALES[0])
sh = pb.selector("Respuesta al impulso h(t)", SENALES, SENALES[3])
t = pb.deslizador("Desplazamiento t", T0, T1, 0.5, 0.02)

cb = pb.js("""
    function forma(nombre, u) {
        if (nombre.startsWith("Pulso de anchura 1")) return (u >= 0 && u < 1) ? 1 : 0;
        if (nombre.startsWith("Pulso de anchura 2")) return (u >= 0 && u < 2) ? 1 : 0;
        if (nombre.startsWith("Triángulo")) return (u >= 0 && u < 2) ? 1 - Math.abs(u - 1) : 0;
        if (nombre.startsWith("Exponencial")) return u >= 0 ? Math.exp(-u) : 0;
        if (nombre.startsWith("Escalón")) return u >= 0 ? 1 : 0;
        return (u >= 0 && u < 1) ? u : 0;
    }
    const dt = 0.01, tau = rango(T0, T1, 1001), T = t.value;
    const x = tau.map(u => forma(sx.value, u)), h = tau.map(u => forma(sh.value, T - u));
    senales.data = {tau: tau, x: x, h: h, p: x.map((v, i) => v * h[i])};
    // y(t) completa por integración numérica
    const ts = rango(T0, T1, 501), y = ts.map(tt => {
        let s = 0; for (let i = 0; i < tau.length; i++) s += x[i] * forma(sh.value, tt - tau[i]);
        return s * dt; });
    salida.data = {t: ts, y: y};
    const k = ts.findIndex(v => v > T);
    actual.data = {t: ts.slice(0, k < 0 ? ts.length : k), y: y.slice(0, k < 0 ? ts.length : k)};
    const j = Math.min(Math.max(Math.round((T - T0) / (T1 - T0) * (ts.length - 1)), 0), ts.length - 1);
    punto.data = {t: [T], y: [y[j]]};
    marca.location = T;
""", senales=senales, salida=salida, actual=actual, punto=punto, marca=marca, sx=sx, sh=sh, t=t,
   T0=T0, T1=T1)
pb.conectar(cb, sx, sh, t)

pb.pagina_panel(__file__, "Convolución continua", tema=1,
                descripcion="y(t) = ∫ x(τ) h(t − τ) dτ. Para cada t se invierte h, se desplaza hasta t, "
                            "se multiplica por x y se integra. Mueve t para ver cómo se construye y(t); "
                            "su duración es la suma de las duraciones de x y h.",
                controles=[sx, sh],
                graficas=[pb.grafica(p1, t), p2], inicio=cb,
                referencia="Transparencias T1-02, «Convolución continua: ejemplo» · Apuntes del Tema 1, sección 5")
