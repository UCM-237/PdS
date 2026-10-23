"""T3 · FFT de 8 puntos por diezmado en el tiempo: el grafo de mariposas."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div, LabelSet
import pds_bokeh as pb

G = ColumnDataSource(dict(x0=[], y0=[], x1=[], y1=[], color=[], ancho=[]))
Nd = ColumnDataSource(dict(x=[], y=[], txt=[], color=[]))
Tw = ColumnDataSource(dict(x=[], y=[], txt=[]))
Et = ColumnDataSource(dict(x=[], y=[], txt=[]))
C = ColumnDataSource(dict(N=[], dft=[], fft=[]))

p1 = pb.figura("Grafo de mariposas (N = 8): valores en cada etapa", "", "", ancho=760, alto=380,
               x_range=(-0.9, 3.9), y_range=(-0.8, 8.0), tools="save")
p1.xaxis.visible = False; p1.yaxis.visible = False; p1.grid.visible = False
p1.segment(x0="x0", y0="y0", x1="x1", y1="y1", source=G, color="color", line_width="ancho", alpha=0.8)
p1.scatter("x", "y", source=Nd, size=7, color="color")
p1.add_layout(LabelSet(x="x", y="y", text="txt", source=Nd, x_offset=4, y_offset=4, text_font_size="11px", text_color=pb.GRIS))
p1.add_layout(LabelSet(x="x", y="y", text="txt", source=Tw, text_font_size="11px", text_color=pb.ROJO))
p1.add_layout(LabelSet(x="x", y="y", text="txt", source=Et, text_font_size="12px", text_color=pb.AZUL, text_align="center"))
p2 = pb.figura("Productos complejos: DFT directa (N²) y FFT ((N/2)·log₂N)", "N", "", ancho=330, alto=240,
               x_axis_type="log", y_axis_type="log")
p2.line("N", "dft", source=C, color=pb.GRIS, line_width=2, legend_label="DFT")
p2.line("N", "fft", source=C, color=pb.AZUL, line_width=2, legend_label="FFT")
p2.scatter("N", "dft", source=C, color=pb.GRIS, size=5); p2.scatter("N", "fft", source=C, color=pb.AZUL, size=5)
pb.leyenda(p2, "top_left")

senal = pb.selector("Entrada x[n]", ["Impulso δ[n]", "Impulso δ[n − 1]", "Constante", "Coseno cos(2πn/8)", "Rampa n", "Aleatoria"])
etapa = pb.deslizador("Etapa resaltada", 0, 3, 1, 1)
info = Div(text="", width=240)

cb = pb.js("""
    const N = 8, r = ruido(N, 4), n = enteros(0, N - 1);
    const x = n.map(k => ({"Impulso δ[n]": k === 0 ? 1 : 0, "Impulso δ[n − 1]": k === 1 ? 1 : 0, "Constante": 1,
        "Coseno cos(2πn/8)": Math.cos(2 * PI * k / 8), "Rampa n": k}[senal.value] ?? Math.round(r[k] * 100) / 100));
    const inv = k => parseInt(k.toString(2).padStart(3, "0").split("").reverse().join(""), 2);
    // Etapa 0: entrada en orden de bits invertido; cada etapa s combina pares separados 2^(s−1)
    let v = n.map(k => [x[inv(k)], 0]);
    const etapas = [v], g = {x0: [], y0: [], x1: [], y1: [], color: [], ancho: []}, tw = {x: [], y: [], txt: []};
    const fila = i => 7 - i, sup = ["⁰", "¹", "²", "³"];
    for (let s = 1; s <= 3; s++) {
        const h = 2 ** (s - 1), w = v.map(c => c.slice()), res = etapa.value === s;
        for (let ini = 0; ini < N; ini += 2 * h) for (let j = 0; j < h; j++) {
            const a = ini + j, b = a + h, e = N / (2 * h) * j, W = cexp([0, -2 * PI * e / N]), t = cmul(W, v[b]);
            w[a] = csum(v[a], t); w[b] = cres(v[a], t);
            for (const [i0, i1] of [[a, a], [a, b], [b, a], [b, b]]) {
                g.x0.push(s - 1); g.y0.push(fila(i0)); g.x1.push(s); g.y1.push(fila(i1));
                g.color.push(res ? pb_ROJO : pb_GRIS); g.ancho.push(res ? 2 : 1);
            }
            tw.x.push(s - 1 + 0.06); tw.y.push(fila(b) - 0.38); tw.txt.push("W₈" + sup[e]);
        }
        v = w; etapas.push(v);
    }
    const fmt = c => { const re = Math.abs(c[0]) < 5e-3 ? 0 : c[0], im = Math.abs(c[1]) < 5e-3 ? 0 : c[1];
        return im === 0 ? re.toFixed(2) : re === 0 ? `${im.toFixed(2)}j` : `${re.toFixed(2)}${im < 0 ? "−" : "+"}${Math.abs(im).toFixed(2)}j`; };
    const nd = {x: [], y: [], txt: [], color: []};
    etapas.forEach((e, s) => e.forEach((c, i) => { nd.x.push(s); nd.y.push(fila(i));
        nd.txt.push(s === 0 ? `x[${inv(i)}] = ${fmt(c)}` : s === 3 ? `X[${i}] = ${fmt(c)}` : fmt(c));
        nd.color.push(s === etapa.value || s === etapa.value - 1 ? pb_ROJO : pb_AZUL); }));
    G.data = g; Nd.data = nd; Tw.data = tw;
    Et.data = {x: [0, 1, 2, 3], y: [7.6, 7.6, 7.6, 7.6], txt: ["entrada (bits invertidos)", "etapa 1: DFT de 2", "etapa 2: DFT de 4", "etapa 3: DFT de 8"]};
    const Ns = enteros(1, 10).map(k => 2 ** k);
    C.data = {N: Ns, dft: Ns.map(v => v * v), fft: Ns.map(v => v / 2 * Math.log2(v))};
    const [dr, di] = dft(x, N), err = Math.max(...n.map(k => cabs(cres(v[k], [dr[k], di[k]]))));
    info.text = `<p>Cada mariposa calcula a + W·b y a − W·b con un solo producto complejo.</p>` +
        `<p>N = 8: 3 etapas de 4 mariposas, 12 productos (muchos triviales, W₈⁰ = 1 y W₈² = −j), frente a 64 de la DFT directa.</p>` +
        `<p>Diferencia con la DFT directa: ${err.toExponential(1)}</p>` +
        "<p>Con N = 1024: 5120 productos frente a 1 048 576, unas 200 veces menos.</p>";
""", G=G, Nd=Nd, Tw=Tw, Et=Et, C=C, senal=senal, etapa=etapa, info=info, pb_ROJO=pb.ROJO, pb_GRIS=pb.GRIS_CLARO, pb_AZUL=pb.AZUL)
pb.conectar(cb, senal, etapa)

pb.pagina(__file__, "FFT: el grafo de mariposas", tema=3,
          descripcion="La FFT por diezmado en el tiempo divide la DFT de N puntos en dos de N/2 (muestras pares e impares) y repite "
                      "hasta llegar a DFT de 2 puntos. Con N = 8 son tres etapas de mariposas; la entrada se ordena con los bits del "
                      "índice invertidos. El número de productos pasa de N² a (N/2)·log₂N.",
          controles=[senal, etapa, info], graficas=[p1, p2], inicio=cb,
          referencia="Transparencias T3-04, la FFT · Apuntes del Tema 3, sección 5")
