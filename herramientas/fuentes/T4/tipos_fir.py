"""T4 · Los cuatro tipos de FIR de fase lineal y sus ceros."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
import numpy as np
from bokeh.models import ColumnDataSource, Div, Span
import pds_bokeh as pb

C = ColumnDataSource(dict(n=list(range(5)), c=[-0.05, 0.0, 0.2, 0.45, 0.6]))
Hn = ColumnDataSource(dict(n=[], h=[]))
Z = ColumnDataSource(dict(x=[], y=[], color=[]))
F = ColumnDataSource(dict(W=[], m=[], A=[]))

p0 = pb.figura("Mitad editable: c[0] … c[4] (haz clic)", "n", "", ancho=250, alto=200, x_range=(-0.5, 4.5), y_range=(-1, 1))
pb.tallos(p0, "n", "c", C, color=pb.NARANJA)
p1 = pb.figura("h[n] completa", "n", "", ancho=330, alto=200, y_range=(-1, 1))
pb.tallos(p1, "n", "h", Hn, color=pb.AZUL)
centro = Span(location=4, dimension="height", line_color=pb.GRIS, line_dash="dashed")
p1.add_layout(centro)
p2 = pb.figura("Ceros de H(z)", "Re z", "Im z", ancho=250, alto=250, x_range=(-3, 3), y_range=(-3, 3))
th = np.linspace(0, 2 * np.pi, 200)
p2.line(np.cos(th), np.sin(th), color=pb.GRIS, line_width=1)
p2.scatter("x", "y", source=Z, marker="circle", size=11, line_width=2, line_color="color", fill_color=None)
p3 = pb.figura("|H(e^jΩ)| y amplitud real A(Ω)", "Ω (rad/muestra)", "", ancho=340, alto=250, x_range=(0, 3.1416))
p3.add_layout(Span(location=0, dimension="width", line_color=pb.GRIS_CLARO))
p3.line("W", "A", source=F, color=pb.VERDE, line_width=2, line_dash="dashed", legend_label="A(Ω)")
p3.line("W", "m", source=F, color=pb.AZUL, line_width=2, legend_label="|H|")
pb.leyenda(p3, "below")

tipo = pb.selector("Tipo", ["I: simétrica, longitud impar", "II: simétrica, longitud par",
                            "III: antisimétrica, longitud impar", "IV: antisimétrica, longitud par"])
info = Div(text="", width=240)

cb = pb.js("""
    const c = C.data.c, t = ["I", "II", "III", "IV"].indexOf(tipo.value.split(":")[0]);
    let h;
    if (t === 0) h = c.concat(c.slice(0, 4).reverse());
    else if (t === 1) h = c.concat(c.slice().reverse());
    else if (t === 2) h = c.slice(0, 4).concat([0], c.slice(0, 4).reverse().map(v => -v));
    else h = c.concat(c.slice().reverse().map(v => -v));
    const M = h.length, D = (M - 1) / 2, anti = t >= 2;
    Hn.data = {n: enteros(0, M - 1), h: h}; centro.location = D;
    // Ceros: raíces de h[0]z^(M−1) + … + h[M−1]
    const r = raices(h);
    const forzado = z => (Math.abs(z[1]) < 1e-4 && (((t === 1 || t === 2) && Math.abs(z[0] + 1) < 1e-3) || ((t >= 2) && Math.abs(z[0] - 1) < 1e-3)));
    Z.data = {x: r.map(v => v[0]), y: r.map(v => v[1]), color: r.map(v => forzado(v) ? pb_ROJO : pb_AZUL)};
    // A(Ω) = H(e^jΩ)·e^(jΩD), multiplicada por −j si es antisimétrica, es real
    const W = rango(0, PI, 600), Hw = W.map(w => h.reduce((s, v, n) => csum(s, cesc(v, cexp([0, -w * n]))), [0, 0]));
    const A = Hw.map((v, i) => { const a = cmul(v, cexp([0, W[i] * D])); return anti ? a[1] : a[0]; });
    F.data = {W: W, m: Hw.map(cabs), A: A};
    const H0 = Math.abs(A[0]), Hpi = Math.abs(A[A.length - 1]);
    const desc = [["simétrica", "nada fuerza ceros", "cualquier tipo de filtro"],
                  ["simétrica", "un cero forzado en z = −1 (H(e^jπ) = 0)", "paso bajo o paso banda; no sirve para paso alto ni banda eliminada"],
                  ["antisimétrica", "ceros forzados en z = 1 y z = −1", "solo paso banda, derivadores o transformadores de Hilbert"],
                  ["antisimétrica", "un cero forzado en z = 1 (H(1) = 0)", "paso alto, paso banda, derivadores o Hilbert; no sirve para paso bajo"]][t];
    info.text = `<p>Longitud M = ${M}, ${desc[0]}; retardo de grupo constante D = (M − 1)/2 = ${D} muestras.</p>` +
        `<p>${desc[1][0].toUpperCase() + desc[1].slice(1)}; los ceros forzados se dibujan en rojo.</p>` +
        `<p>Adecuado para: ${desc[2]}.</p>` +
        `<p>|H(1)| = ${H0.toFixed(3)}, |H(−1)| = ${Hpi.toFixed(3)}</p>` +
        "<p>Los demás ceros aparecen en cuartetos z₀, z₀*, 1/z₀ y 1/z₀* (o en parejas, si están en el eje real o en la circunferencia).</p>";
""", C=C, Hn=Hn, Z=Z, F=F, tipo=tipo, info=info, centro=centro, pb_ROJO=pb.ROJO, pb_AZUL=pb.AZUL)
pb.editable(p0, C, "n", "c", callback=cb)
pb.conectar(cb, tipo)

pb.pagina(__file__, "Tipos de FIR de fase lineal", tema=4,
          descripcion="Un FIR tiene fase lineal si sus coeficientes son simétricos o antisimétricos respecto al centro. Según la "
                      "simetría y la paridad de la longitud hay cuatro tipos, y los de tipo II, III y IV tienen ceros forzados en "
                      "z = 1 o z = −1, que limitan qué filtros pueden ser. Edita la mitad de los coeficientes y cambia de tipo.",
          controles=[tipo, info], graficas=[[p0, p1], [p2, p3]], inicio=cb,
          referencia="Transparencias T4-04, filtros FIR de fase lineal · Apuntes del Tema 4, sección 4")
