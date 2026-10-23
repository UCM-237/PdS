"""T6 · Gaussiana bivariante: elipses, marginales, condicionadas e incorrelación frente a independencia."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div, Span
import pds_bokeh as pb

M = ColumnDataSource(dict(x=[], y=[], color=[]))
El = ColumnDataSource(dict(xs=[], ys=[]))
Ej = ColumnDataSource(dict(xs=[], ys=[]))
H1 = ColumnDataSource(dict(x=[], top=[], ancho=[]))
T1 = ColumnDataSource(dict(x=[], y=[]))
H2 = ColumnDataSource(dict(x=[], top=[], ancho=[]))
T2 = ColumnDataSource(dict(x=[], y=[]))
Hc = ColumnDataSource(dict(x=[], top=[], ancho=[]))
Tc = ColumnDataSource(dict(x=[], y=[]))

p1 = pb.figura("Muestras, elipses de igual densidad (1σ y 2σ) y sus ejes", "x₁", "x₂", ancho=360, alto=360,
               match_aspect=True, x_range=(-5, 5), y_range=(-5, 5))
p1.scatter("x", "y", source=M, color="color", size=3, alpha=0.5)
p1.multi_line("xs", "ys", source=El, color=pb.ROJO, line_width=2)
p1.multi_line("xs", "ys", source=Ej, color=pb.NARANJA, line_width=2, line_dash="dashed")
banda = [Span(location=0, dimension="height", line_color=pb.VERDE, line_width=1.5, line_dash="dotted") for _ in range(2)]
for s in banda:
    p1.add_layout(s)
p2 = pb.figura("Marginal de X₁", "x₁", "densidad", ancho=300, alto=160, x_range=p1.x_range)
p2.vbar(x="x", top="top", width="ancho", source=H1, fill_color=pb.GRIS_CLARO, line_color="white")
p2.line("x", "y", source=T1, color=pb.ROJO, line_width=2)
p3 = pb.figura("Marginal de X₂", "x₂", "densidad", ancho=300, alto=160, x_range=p1.y_range)
p3.vbar(x="x", top="top", width="ancho", source=H2, fill_color=pb.GRIS_CLARO, line_color="white")
p3.line("x", "y", source=T2, color=pb.ROJO, line_width=2)
p4 = pb.figura("Condicionada f(x₂ | x₁ ≈ c): banda verde", "x₂", "densidad", ancho=300, alto=160,
               x_range=p1.y_range)
p4.vbar(x="x", top="top", width="ancho", source=Hc, fill_color=pb.VERDE, fill_alpha=0.4, line_color="white")
p4.line("x", "y", source=Tc, color=pb.ROJO, line_width=2)

ejemplo = pb.selector("Ejemplo", ["Gaussiana bivariante", "Incorreladas pero dependientes: X₂ = X₁² − 4/3, X₁ ~ U[−2, 2]",
                                  "Incorreladas pero dependientes: puntos en un anillo"], width=250)
s1 = pb.deslizador("σ₁", 0.2, 2, 1.4, 0.05)
s2 = pb.deslizador("σ₂", 0.2, 2, 1, 0.05)
rho = pb.deslizador("ρ (coeficiente de correlación)", -0.99, 0.99, 0.85, 0.01)
c = pb.deslizador("Condición x₁ = c", -3, 3, 1, 0.05)
N = pb.deslizador("Número de muestras N", 200, 20000, 4000, 200)
info = Div(text="", width=250)

cb = pb.js("""
    const g = generador(9), Nm = N.value, a = s1.value, b = s2.value, r = rho.value, cc = c.value, ej = ejemplo.value;
    let x = [], y = [];
    const gaussiana = ej.startsWith("Gaussiana");
    if (gaussiana) {
        // x = L z con L el factor de Cholesky de Σ = [[a², rab], [rab, b²]]
        const l11 = a, l21 = r * b, l22 = b * Math.sqrt(1 - r * r);
        for (let i = 0; i < Nm; i++) { const z1 = gauss(g), z2 = gauss(g); x.push(l11 * z1); y.push(l21 * z1 + l22 * z2); }
    } else if (ej.includes("X₁²")) {
        for (let i = 0; i < Nm; i++) { const u = 2 * g() - 1; x.push(2 * u); y.push(4 * (u * u - 1 / 3)); }
    } else {
        for (let i = 0; i < Nm; i++) { const th = 2 * PI * g(), rr = 2 + 0.25 * gauss(g); x.push(rr * Math.cos(th)); y.push(rr * Math.sin(th)); }
    }
    const ancho = 0.15 * (gaussiana ? a : 1), dentro = x.map(v => Math.abs(v - cc) < ancho);
    M.data = {x: x.slice(0, 5000), y: y.slice(0, 5000), color: dentro.slice(0, 5000).map(d => d ? pb_VERDE : pb_AZUL)};
    banda[0].location = cc - ancho; banda[1].location = cc + ancho;
    const xx = rango(-5, 5, 300), gd = (t, s) => Math.exp(-0.5 * (t / s) ** 2) / (Math.sqrt(2 * PI) * s);
    const h1 = histo(x, -5, 5, 50), h2 = histo(y, -5, 5, 50);
    H1.data = {x: h1.c, top: h1.d, ancho: h1.c.map(() => h1.ancho)}; H2.data = {x: h2.c, top: h2.d, ancho: h2.c.map(() => h2.ancho)};
    const yc = y.filter((_, i) => dentro[i]), hc = histo(yc, -5, 5, 40);
    // Densidad de la condicionada normalizada con las muestras de la banda
    Hc.data = {x: hc.c, top: hc.d, ancho: hc.c.map(() => hc.ancho)};
    const mx = media(x), my = media(y), vx = varianza(x), vy = varianza(y);
    let cxy = 0; for (let i = 0; i < Nm; i++) cxy += (x[i] - mx) * (y[i] - my); cxy /= Nm - 1;
    const re = cxy / Math.sqrt(vx * vy);
    if (gaussiana) {
        T1.data = {x: xx, y: xx.map(t => gd(t, a))}; T2.data = {x: xx, y: xx.map(t => gd(t, b))};
        const mc = r * b / a * cc, sc = b * Math.sqrt(1 - r * r);
        Tc.data = {x: xx, y: xx.map(t => gd(t - mc, sc))};
        // Elipses xᵀΣ⁻¹x = k² con los autovectores de Σ
        const S11 = a * a, S22 = b * b, S12 = r * a * b, tr = S11 + S22, det = S11 * S22 - S12 * S12;
        const l1 = tr / 2 + Math.sqrt(tr * tr / 4 - det), l2 = tr / 2 - Math.sqrt(tr * tr / 4 - det);
        const ang = Math.abs(S12) < 1e-12 ? (S11 >= S22 ? 0 : PI / 2) : Math.atan2(l1 - S11, S12);
        const th = rango(0, 2 * PI, 200), el = k => [th.map(t => k * (Math.sqrt(l1) * Math.cos(t) * Math.cos(ang) - Math.sqrt(l2) * Math.sin(t) * Math.sin(ang))),
                                                     th.map(t => k * (Math.sqrt(l1) * Math.cos(t) * Math.sin(ang) + Math.sqrt(l2) * Math.sin(t) * Math.cos(ang)))];
        const e1 = el(1), e2 = el(2);
        El.data = {xs: [e1[0], e2[0]], ys: [e1[1], e2[1]]};
        Ej.data = {xs: [[-2 * Math.sqrt(l1) * Math.cos(ang), 2 * Math.sqrt(l1) * Math.cos(ang)], [-2 * Math.sqrt(l2) * -Math.sin(ang), 2 * Math.sqrt(l2) * -Math.sin(ang)]],
                   ys: [[-2 * Math.sqrt(l1) * Math.sin(ang), 2 * Math.sqrt(l1) * Math.sin(ang)], [-2 * Math.sqrt(l2) * Math.cos(ang), 2 * Math.sqrt(l2) * Math.cos(ang)]]};
        info.text = `<p>Σ = [${S11.toFixed(2)}, ${S12.toFixed(2)}; ${S12.toFixed(2)}, ${S22.toFixed(2)}]</p>` +
            `<p>Autovalores (varianzas a lo largo de los ejes): ${l1.toFixed(3)} y ${l2.toFixed(3)}; eje mayor a ${(180 * ang / PI).toFixed(1)}°</p>` +
            `<p>Cholesky: L = [${a.toFixed(2)}, 0; ${(r * b).toFixed(2)}, ${(b * Math.sqrt(1 - r * r)).toFixed(2)}]</p>` +
            `<p>Condicionada: media ρσ₂c/σ₁ = ${mc.toFixed(3)}, desviación σ₂√(1 − ρ²) = ${sc.toFixed(3)}</p>` +
            `<p>Con las muestras: ρ̂ = ${re.toFixed(3)}; media de la banda ${yc.length ? media(yc).toFixed(3) : "—"} (${yc.length} muestras)</p>`;
    } else {
        T1.data = {x: [], y: []}; T2.data = {x: [], y: []}; Tc.data = {x: [], y: []}; El.data = {xs: [], ys: []}; Ej.data = {xs: [], ys: []};
        info.text = `<p>Covarianza muestral: ${cxy.toFixed(4)}; ρ̂ = ${re.toFixed(3)}: incorreladas</p>` +
            `<p>Pero la condicionada no es la marginal: dentro de la banda, X₂ toma solo unos valores, que dependen de c. ` +
            `Las variables son dependientes.</p><p>Media de X₂ en la banda: ${yc.length ? media(yc).toFixed(3) : "—"}; ` +
            `desviación típica ${yc.length > 1 ? Math.sqrt(varianza(yc)).toFixed(3) : "—"} (sin condicionar, ${Math.sqrt(vy).toFixed(3)})</p>`;
    }
""", M=M, El=El, Ej=Ej, H1=H1, T1=T1, H2=H2, T2=T2, Hc=Hc, Tc=Tc, banda=banda, ejemplo=ejemplo, s1=s1, s2=s2,
   rho=rho, c=c, N=N, info=info, pb_VERDE=pb.VERDE, pb_AZUL=pb.AZUL)
pb.conectar(cb, ejemplo, s1, s2, rho, c, N)

pb.pagina(__file__, "Gaussiana bivariante", tema=6,
          descripcion="Una gaussiana de dos variables queda fijada por sus medias y su matriz de covarianza Σ. Sus curvas de "
                      "nivel son elipses con los ejes en los autovectores de Σ. Las marginales y las condicionadas también son "
                      "gaussianas, y si ρ = 0 las variables son independientes. En otras distribuciones, incorreladas no "
                      "significa independientes.",
          controles=[ejemplo, s1, s2, rho, c, N, info], graficas=[[p1, pb.column(p2, p3, p4)]], inicio=cb,
          referencia="Transparencias T6-02, marginales y condicionadas, incorreladas frente a independientes y gaussiana multivariable · Apuntes del Tema 6, sección 2")
