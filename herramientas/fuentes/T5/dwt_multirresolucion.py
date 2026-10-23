"""T5 · DWT: análisis multirresolución y banco de filtros."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

NX, JMAX = 512, 6

X = ColumnDataSource(dict(n=[], x=[], y=[]))
Cm = ColumnDataSource(dict(xs=[], ys=[], color=[], alfa=[]))
Et = ColumnDataSource(dict(x=[], y=[], t=[]))
Cf = ColumnDataSource(dict(k=[], c=[], color=[]))
Bd = ColumnDataSource(dict(xs=[], ys=[], color=[]))

p1 = pb.figura("Señal x[n] y reconstrucción con los niveles elegidos", "n", "", ancho=560, alto=170, x_range=(0, NX))
p1.line("n", "x", source=X, color=pb.GRIS_CLARO, line_width=3, legend_label="x[n]")
p1.line("n", "y", source=X, color=pb.ROJO, line_width=1.5, legend_label="reconstrucción")
pb.leyenda(p1, "below")
p2 = pb.figura("Aproximación A_J y detalles D_J … D₁ (cada uno de la longitud de x)", "n", "", ancho=560, alto=330,
               x_range=p1.x_range)
p2.multi_line("xs", "ys", source=Cm, color="color", line_alpha="alfa", line_width=1.3)
p2.text("x", "y", "t", source=Et, text_font_size="12px", text_color=pb.GRIS, text_baseline="middle")
p2.yaxis.visible = False
p3 = pb.figura("Coeficientes: a_J | d_J | … | d₁", "índice", "", ancho=330, alto=200)
p3.segment(x0="k", y0=0, x1="k", y1="c", source=Cf, color="color", line_width=1.2)
p4 = pb.figura("Banda de cada nivel: |DTFT| de una función de la base", "Ω (rad/muestra)", "", ancho=330, alto=200,
               x_range=(0, 3.1416))
p4.multi_line("xs", "ys", source=Bd, color="color", line_width=1.8)

senal = pb.selector("Señal", ["Escalones y oscilación", "Rampa con un salto", "Doppler", "Chirp"])
wav = pb.selector("Wavelet", ["Haar", "db2", "db4"])
J = pb.deslizador("Niveles J", 1, JMAX, 4, 1)
quedan = pb.casillas(["A_J"] + [f"D{j}" for j in range(1, JMAX + 1)], activas=list(range(JMAX + 1)))
info = Div(text="", width=250)

cb = pb.js("""
    const N = NX, n = enteros(0, N - 1), u = generador(2);
    let x;
    if (senal.value.startsWith("Escalones"))
        x = n.map(k => (k < 128 ? 1 : k < 220 ? 3 : k < 300 ? 2 : k < 380 ? 2.5 : 1.5) + (k >= 400 ? 0.8 * Math.sin(2 * PI * k / 6) : 0));
    else if (senal.value.startsWith("Rampa")) x = n.map(k => k / 128 + (k >= 300 ? -2 : 0));
    else if (senal.value === "Doppler") x = n.map(k => { const t = (k + 0.5) / N; return 3 * Math.sqrt(t * (1 - t)) * Math.sin(2 * PI * 1.05 / (t + 0.05)); });
    else x = n.map(k => Math.sin(2 * PI * (0.002 * k + 0.00045 * k * k)));
    const j = J.value, c = dwt_dec(x, wav.value, j), comp = dwt_componentes(c, wav.value);
    // Reconstrucción con las componentes marcadas (casilla 0 = A_J, casilla i = D_i)
    const act = new Set(quedan.active), y = n.map(() => 0);
    if (act.has(0)) comp.A.forEach((v, i) => y[i] += v);
    comp.D.forEach((d, i) => { if (act.has(i + 1)) d.forEach((v, k) => y[k] += v); });
    X.data = {n: n, x: x, y: y};
    // Componentes apiladas: A_J arriba, D_1 abajo
    const lista = [["A" + j, comp.A, 0]].concat(enteros(1, j).reverse().map(i => ["D" + i, comp.D[i - 1], i]));
    const esc = lista.map(e => maximo(e[1].map(Math.abs)) || 1), paso = 2.4;
    const cols = [pb_AZUL, pb_ROJO, pb_VERDE, pb_NARANJA, pb_GRIS, "#7B4FA0", "#2A9DB0"];
    Cm.data = {xs: lista.map(() => n), ys: lista.map((e, i) => e[1].map(v => v / esc[i] - paso * i)),
               color: lista.map(e => cols[e[2]]), alfa: lista.map(e => act.has(e[2]) ? 1 : 0.25)};
    Et.data = {x: lista.map(() => N + 4), y: lista.map((_, i) => -paso * i), t: lista.map(e => e[0])};
    p2.x_range.end = N + 40;
    // Coeficientes concatenados como los devuelve wavedec
    const bloques = [[c.a, 0]].concat(enteros(1, j).reverse().map(i => [c.d[i - 1], i]));
    const kk = [], cc = [], co = []; let pos = 0;
    for (const [v, i] of bloques) { v.forEach(z => { kk.push(pos++); cc.push(z); co.push(cols[i]); }); }
    Cf.data = {k: kk, c: cc, color: co};
    // Banda de cada nivel: una función de la base (un coeficiente a 1 en el centro de su nivel)
    const cero = v => v.map(() => 0), P = 4096, bxs = [], bys = [], bco = [];
    for (const [nombre, i] of [["a", 0]].concat(enteros(1, j).map(i => ["d", i]))) {
        const cc2 = {a: cero(c.a), d: c.d.map(cero)};
        if (nombre === "a") cc2.a[c.a.length >> 1] = 1; else cc2.d[i - 1][c.d[i - 1].length >> 1] = 1;
        const g = dwt_rec(cc2, wav.value), re = new Array(P).fill(0); g.forEach((v, k) => re[k] = v);
        const [Gr, Gi] = fft(re), K = P / 2, m = enteros(0, K).map(k => Math.hypot(Gr[k], Gi[k])), mm = maximo(m);
        bxs.push(enteros(0, K).map(k => PI * k / K)); bys.push(m.map(v => v / mm)); bco.push(cols[i]);
    }
    Bd.data = {xs: bxs, ys: bys, color: bco};
    const Ex = x.reduce((a, v) => a + v * v, 0), Ea = c.a.reduce((a, v) => a + v * v, 0), Ed = c.d.map(d => d.reduce((a, v) => a + v * v, 0));
    let err = 0; y.forEach((v, i) => err = Math.max(err, Math.abs(v - x[i])));
    info.text = `<p>Coeficientes: ${N / 2 ** j} de aproximación y ${N - N / 2 ** j} de detalle, en total ${N}</p>` +
        `<p>Energía: x, ${Ex.toFixed(1)}; a<sub>${j}</sub>, ${(100 * Ea / Ex).toFixed(1)} %; ` +
        Ed.map((e, i) => `d<sub>${i + 1}</sub>, ${(100 * e / Ex).toFixed(2)} %`).join("; ") + `</p>` +
        `<p>Parseval: Σx² − Σ(coeficientes)² = ${(Ex - Ea - Ed.reduce((a, b) => a + b, 0)).toExponential(1)}</p>` +
        `<p>Diferencia máxima entre la reconstrucción y x: ${err.toExponential(1)}</p>`;
""", X=X, Cm=Cm, Et=Et, Cf=Cf, Bd=Bd, p2=p2, senal=senal, wav=wav, J=J, quedan=quedan, info=info, NX=NX,
   pb_AZUL=pb.AZUL, pb_ROJO=pb.ROJO, pb_VERDE=pb.VERDE, pb_NARANJA=pb.NARANJA, pb_GRIS=pb.GRIS)
pb.conectar(cb, senal, wav, J, quedan)

pb.pagina(__file__, "DWT y análisis multirresolución", tema=5,
          descripcion="La DWT divide la señal, nivel a nivel, con un paso bajo h₀ y un paso alto h₁ seguidos de un diezmado "
                      "por 2. Queda una aproximación A_J y unos detalles D_J … D₁ que suman la señal: cada nivel recoge una "
                      "banda de frecuencias de la mitad de anchura que la anterior. Marca qué componentes se conservan para "
                      "reconstruir.",
          controles=[senal, wav, J, Div(text="Componentes que se conservan:"), quedan, info],
          graficas=[p1, p2, [p3, p4]], inicio=cb,
          referencia="Transparencias T5-02, análisis multirresolución, Haar y la DWT como banco de filtros · Apuntes del Tema 5, sección 2")
