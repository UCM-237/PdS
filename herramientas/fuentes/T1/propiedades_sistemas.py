"""T1 · Propiedades de los sistemas: linealidad, invarianza, causalidad y estabilidad."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div, Span
import pds_bokeh as pb

E = ColumnDataSource(dict(n=[], a=[], b=[]))
Sa = ColumnDataSource(dict(n=[], a=[], b=[]))

p1 = pb.figura("Entradas", "n", "", ancho=680, alto=200, x_range=(-20.5, 20.5))
pb.tallos(p1, "n", "a", E, color=pb.AZUL, legend_label="entrada A")
p1.scatter("n", "b", source=E, marker="square", size=9, line_color=pb.NARANJA, fill_color=None, line_width=2, legend_label="entrada B")
pb.leyenda(p1, "right")
p2 = pb.figura("Salidas que se comparan", "n", "", ancho=680, alto=220, x_range=p1.x_range)
pb.tallos(p2, "n", "a", Sa, color=pb.AZUL, legend_label="salida A")
p2.scatter("n", "b", source=Sa, marker="square", size=9, line_color=pb.NARANJA, fill_color=None, line_width=2, legend_label="salida B")
pb.leyenda(p2, "right")
marca = Span(location=0, dimension="height", line_color=pb.GRIS, line_dash="dashed")
p1.add_layout(marca); p2.add_layout(Span(location=0, dimension="height", line_color=pb.GRIS, line_dash="dashed"))

SISTEMAS = ["y[n] = ½(x[n] + x[n−1])", "y[n] = 2x[n] + 1", "y[n] = x²[n]", "y[n] = n·x[n]", "y[n] = x[n+1] − x[n]",
            "y[n] = x[−n]", "y[n] = Σ x[k], k ≤ n (acumulador)", "y[n] = x[2n]", "y[n] = x[n]·cos(πn/4)"]
sistema = pb.selector("Sistema", SISTEMAS)
prueba = pb.selector("Propiedad que se comprueba", ["Linealidad", "Invarianza en el tiempo", "Causalidad", "Estabilidad (BIBO)"])
x1 = pb.selector("Señal x₁", ["Pulso", "Rampa corta", "Seno", "Aleatoria"])
x2 = pb.selector("Señal x₂", ["Seno", "Pulso", "Rampa corta", "Aleatoria"])
al = pb.deslizador("α (linealidad)", -2, 2, 1.5, 0.5)
be = pb.deslizador("β (linealidad)", -2, 2, -1, 0.5)
n0 = pb.deslizador("n₀ (retardo o instante de corte)", -8, 8, 3, 1)
info = Div(text="", width=240)

cb = pb.js("""
    const r = ruido(81, 5), sen = (nom) => n => {
        if (nom === "Pulso") return n >= -3 && n <= 3 ? 1 : 0;
        if (nom === "Rampa corta") return n >= 0 && n <= 6 ? n / 6 : 0;
        if (nom === "Seno") return Math.abs(n) <= 15 ? Math.sin(PI * n / 6) : 0;
        return Math.abs(n) <= 40 ? 0.5 * r[n + 40] : 0; };
    const S = {
        0: x => n => 0.5 * (x(n) + x(n - 1)), 1: x => n => 2 * x(n) + 1, 2: x => n => x(n) ** 2, 3: x => n => n * x(n),
        4: x => n => x(n + 1) - x(n), 5: x => n => x(-n), 6: x => n => { let s = 0; for (let k = -60; k <= n; k++) s += x(k); return s; },
        7: x => n => x(2 * n), 8: x => n => x(n) * Math.cos(PI * n / 4)}[SIS.indexOf(sistema.value)];
    // Propiedades teóricas [lineal, invariante, causal, estable]
    const T = [[1, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [1, 0, 1, 0], [1, 1, 0, 1], [1, 0, 0, 1], [1, 1, 1, 0], [1, 0, 0, 1], [1, 0, 1, 1]][SIS.indexOf(sistema.value)];
    const n = enteros(-20, 20), f1 = sen(x1.value), f2 = sen(x2.value), a = al.value, b = be.value, d = n0.value;
    let A, B, ya, yb, texto, nombres;
    if (prueba.value === "Linealidad") {
        const comb = k => a * f1(k) + b * f2(k);
        A = n.map(comb); B = n.map(() => NaN);
        ya = n.map(S(comb)); const s1 = S(f1), s2 = S(f2); yb = n.map(k => a * s1(k) + b * s2(k));
        nombres = ["T{αx₁ + βx₂}", "αT{x₁} + βT{x₂}", "αx₁ + βx₂", ""]; texto = "Lineal si las dos salidas coinciden para cualquier α, β, x₁ y x₂.";
    } else if (prueba.value.startsWith("Invarianza")) {
        const xd = k => f1(k - d), s1 = S(f1);
        A = n.map(xd); B = n.map(f1);
        ya = n.map(S(xd)); yb = n.map(k => s1(k - d));
        nombres = ["T{x₁[n − n₀]}", "y₁[n − n₀]", "x₁[n − n₀]", "x₁[n]"]; texto = "Invariante si retrasar la entrada solo retrasa la salida.";
    } else if (prueba.value === "Causalidad") {
        // Dos entradas iguales hasta n₀ y distintas después: en un sistema causal, las salidas coinciden hasta n₀
        const xc = k => k <= d ? f1(k) : f1(k) + f2(k);
        A = n.map(f1); B = n.map(xc); ya = n.map(S(f1)); yb = n.map(S(xc));
        nombres = ["T{x₁}", "T{x₁ cambiada después de n₀}", "x₁", "x₁ cambiada después de n₀"]; texto = "Causal si las salidas coinciden hasta n₀: la salida no puede depender de valores futuros.";
    } else {
        const u = k => (k >= -15 ? 1 : 0);
        A = n.map(u); B = n.map(() => NaN); ya = n.map(S(u)); yb = n.map(() => NaN);
        nombres = ["T{u[n + 15]}", "", "u[n + 15]", ""]; texto = "Estable (BIBO) si toda entrada acotada da una salida acotada; aquí la entrada es un escalón, |x| ≤ 1.";
    }
    E.data = {n: n, a: A, b: B}; Sa.data = {n: n, a: ya, b: yb};
    marca.location = prueba.value === "Causalidad" ? d + 0.5 : -1000;
    ley.items[0].label = {value: nombres[0]}; ley.items[1].label = {value: nombres[1] || " "};
    leyE.items[0].label = {value: nombres[2]}; leyE.items[1].label = {value: nombres[3] || " "};
    const tramo = prueba.value === "Causalidad" ? n.map((k, i) => k <= d ? i : -1).filter(i => i >= 0) : n.map((_, i) => i);
    const dif = prueba.value.startsWith("Estab") ? NaN : Math.max(...tramo.map(i => Math.abs(ya[i] - yb[i])));
    const idx = ["Linealidad", "Invarianza en el tiempo", "Causalidad", "Estabilidad (BIBO)"].indexOf(prueba.value);
    const sino = v => v ? "sí" : "no";
    info.text = `<p>${texto}</p>` +
        (prueba.value.startsWith("Estab") ? `<p>max |y[n]| en la ventana: ${Math.max(...ya.map(Math.abs)).toFixed(2)}</p>`
            : `<p>Diferencia máxima entre las salidas${prueba.value === "Causalidad" ? " hasta n₀" : ""}: <b>${dif.toExponential(1)}</b></p>`) +
        `<p>Para este sistema: lineal ${sino(T[0])}, invariante ${sino(T[1])}, causal ${sino(T[2])}, estable ${sino(T[3])}.</p>` +
        "<p>Una sola prueba que falla basta para negar una propiedad; que una prueba pase no la demuestra: cambia las señales y n₀.</p>";
""", E=E, Sa=Sa, sistema=sistema, prueba=prueba, x1=x1, x2=x2, al=al, be=be, n0=n0, info=info, marca=marca, ley=p2.legend[0], leyE=p1.legend[0], SIS=SISTEMAS)
pb.conectar(cb, sistema, prueba, x1, x2, al, be, n0)

pb.pagina(__file__, "Propiedades de los sistemas", tema=1,
          descripcion="Elige un sistema y la propiedad que quieres comprobar. La herramienta le aplica las entradas que pide la "
                      "definición y compara las dos salidas: si no coinciden, el sistema no tiene la propiedad. Para la estabilidad, "
                      "se mira si un escalón (entrada acotada) da una salida acotada.",
          controles=[sistema, prueba, x1, x2, al, be, n0, info], graficas=[p1, p2], inicio=cb,
          referencia="Transparencias T1-03, propiedades de los sistemas · Apuntes del Tema 1, sección 7")
