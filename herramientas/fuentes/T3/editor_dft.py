"""T3 · Editor de la DFT: cambia la secuencia y mira su DFT."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, CustomJS, Div
import pds_bokeh as pb

N = 16
x = ColumnDataSource(dict(n=list(range(N)), x=[1.0] + [0.0] * (N - 1)))
X = ColumnDataSource(dict(k=[], a=[], b=[]))

p1 = pb.figura("x[n] · haz clic o arrastra para cambiar las muestras", "n", "x[n]", ancho=680, alto=200,
               y_range=(-2, 2), tools="reset,save")
pb.tallos(p1, "n", "x", x, color=pb.AZUL)
p2 = pb.figura("", "k", "", ancho=330, alto=200, tools="reset,save")
p3 = pb.figura("", "k", "", ancho=330, alto=200, tools="reset,save")
pb.tallos(p2, "k", "a", X, color=pb.ROJO)
pb.tallos(p3, "k", "b", X, color=pb.VERDE)

vista = pb.botones(["Módulo y fase", "Re e Im"])
inicial = pb.selector("Secuencia de partida", ["Impulso δ[n]", "Impulso desplazado δ[n − 3]", "Pulso de 4",
                                              "Coseno, k = 2", "Seno, k = 2", "Constante", "Alterna (−1)ⁿ"])
info = Div(text="", width=240)

calc = pb.js("""
    const xs = x.data.x, n = xs.length, [re, im] = dft(xs, n), k = enteros(0, n - 1);
    const lim = v => Math.abs(v) < 1e-9 ? 0 : v;
    if (vista.active === 0) {
        X.data = {k: k, a: re.map((r, i) => Math.hypot(r, im[i])), b: re.map((r, i) => Math.hypot(r, im[i]) < 1e-9 ? 0 : Math.atan2(im[i], r))};
        p2.title.text = "|X[k]|"; p3.title.text = "∠X[k] (rad)";
    } else {
        X.data = {k: k, a: re.map(lim), b: im.map(lim)};
        p2.title.text = "Re X[k]"; p3.title.text = "Im X[k]";
    }
    const E = xs.reduce((s, v) => s + v * v, 0), EX = re.reduce((s, r, i) => s + r * r + im[i] * im[i], 0) / n;
    info.text = `<p>X[0] = Σ x[n] = ${re[0].toFixed(3)}</p><p>Parseval: Σ|x[n]|² = ${E.toFixed(3)} = (1/N) Σ|X[k]|² = ${EX.toFixed(3)}</p>` +
        "<p>Si x[n] es real, X[N − k] = X*[k]: el módulo es simétrico y la fase, antisimétrica.</p>";
""", x=x, X=X, vista=vista, p2=p2, p3=p3, info=info)
pb.editable(p1, x, "n", "x", calc)
partida = CustomJS(args=dict(x=x, s=inicial, calc=calc, N=N), code="""
    const n = [...Array(N).keys()], v = s.value;
    const f = {"Impulso δ[n]": i => +(i === 0), "Impulso desplazado δ[n − 3]": i => +(i === 3), "Pulso de 4": i => +(i < 4),
               "Coseno, k = 2": i => Math.cos(2 * Math.PI * 2 * i / N), "Seno, k = 2": i => Math.sin(2 * Math.PI * 2 * i / N),
               "Constante": i => 1, "Alterna (−1)ⁿ": i => (i % 2 ? -1 : 1)}[v];
    x.data = {n: n, x: n.map(f)}; calc.execute(cb_obj);
""")
inicial.js_on_change("value", partida)
pb.conectar(calc, vista)

pb.pagina(__file__, "Editor de la DFT", tema=3,
          descripcion="Cambia las muestras de x[n] (N = 16) con el ratón y observa su DFT. Prueba a "
                      "desplazar un impulso (cambia solo la fase), a hacer la secuencia par o impar, o a "
                      "poner una sinusoide que no complete un número entero de periodos.",
          controles=[inicial, vista, info], graficas=[p1, [p2, p3]], inicio=calc,
          referencia="Transparencias T3-02, propiedades de la DFT · Apuntes del Tema 3, secciones 2 y 3")
