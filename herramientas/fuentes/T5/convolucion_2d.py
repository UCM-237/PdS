"""T5 · Convolución bidimensional con núcleos habituales o con un núcleo 3×3 propio."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, CustomJS, Div, NumericInput, Span
import pds_bokeh as pb

LADO, FILA = 256, 192

F0 = ColumnDataSource(dict(img=[]))
G0 = ColumnDataSource(dict(img=[]))
Hk = ColumnDataSource(dict(img=[], x=[], y=[], dw=[], dh=[]))
Ht = ColumnDataSource(dict(x=[], y=[], t=[]))
Pr = ColumnDataSource(dict(n=[], f=[], g=[]))
Foto = ColumnDataSource(dict(f=[]))

p1 = pb.figura_imagen("Imagen f[m, n]", LADO)
pb.imagen(p1, F0, dw=LADO, dh=LADO)
p2 = pb.figura_imagen("Resultado g = h ∗ f", LADO)
mapa = pb.imagen(p2, G0, dw=LADO, dh=LADO)
p2.x_range = p1.x_range
p2.y_range = p1.y_range
for p in (p1, p2):
    p.add_layout(Span(location=FILA, dimension="width", line_color=pb.NARANJA, line_dash="dashed", line_width=1))
p3 = pb.figura("Núcleo h[i, j]", "", "", ancho=170, alto=170, tools="save", match_aspect=True)
mapa_h = pb.imagen(p3, Hk, x="x", y="y", dw="dw", dh="dh", paleta="grises", bajo=-1, alto=1)
p3.text("x", "y", "t", source=Ht, text_align="center", text_baseline="middle", text_font_size="11px", text_color=pb.ROJO)
p3.axis.visible = False
p3.grid.visible = False
p4 = pb.figura(f"Perfil de la fila {FILA} (línea naranja)", "n (columna)", "", ancho=520, alto=170, x_range=(0, LADO))
p4.line("n", "f", source=Pr, color=pb.GRIS_CLARO, line_width=2.5, legend_label="f")
p4.line("n", "g", source=Pr, color=pb.AZUL, line_width=1.5, legend_label="g")
pb.leyenda(p4, "right")

imagen = pb.selector("Imagen", ["Prueba", "Tablero", "Texto", "Foto propia"])
fi = pb.foto()
sr = pb.deslizador("Ruido gaussiano σ", 0, 0.3, 0, 0.01)
nucleo = pb.selector("Núcleo", ["Media K×K", "Gaussiano", "Sobel x", "Sobel y", "Módulo del gradiente (Sobel)",
                                "Laplaciano", "Realce f − k∇²f", "Personalizado 3×3"])
K = pb.deslizador("K (lado de la media)", 3, 15, 5, 2)
sg = pb.deslizador("σ del gaussiano (píxeles)", 0.5, 4, 1.5, 0.1)
kr = pb.deslizador("k del realce", 0, 3, 1, 0.1)
borde = pb.selector("Borde", ["repetir", "reflejar", "ceros"])
celdas = [NumericInput(value=v, mode="float", width=70, height=32) for v in (0, -1, 0, -1, 5, -1, 0, -1, 0)]
rejilla = column(Div(text="Núcleo personalizado (fila 0 arriba):"),
                 *[row(*celdas[3 * i:3 * i + 3]) for i in range(3)])
info = Div(text="", width=250)

cb = pb.js("""
    const N = LADO, g = generador(5);
    let f;
    if (imagen.value === "Foto propia" && Foto.data.f.length) f = Foto.data.f[0].map(r => r.slice());
    else f = imagen_patron(imagen.value === "Foto propia" ? "Prueba" : imagen.value, N);
    if (sr.value > 0) f = f.map(r => r.map(v => v + sr.value * gauss(g)));
    // Núcleo
    let h, nombre = nucleo.value, sep = "";
    const sob = [[1, 0, -1], [2, 0, -2], [1, 0, -1]], lap = [[0, 1, 0], [1, -4, 1], [0, 1, 0]];
    if (nombre.startsWith("Media")) { const k = K.value; h = enteros(1, k).map(() => new Array(k).fill(1 / (k * k))); sep = `sí: (1/${k})·1 por (1/${k})·1`; }
    else if (nombre === "Gaussiano") {
        const r = Math.ceil(3 * sg.value), v = enteros(-r, r).map(i => Math.exp(-i * i / (2 * sg.value ** 2))), s = v.reduce((a, b) => a + b, 0);
        h = v.map(a => v.map(b => a * b / (s * s))); sep = "sí: producto de dos gaussianas 1D";
    }
    else if (nombre === "Sobel x" || nombre.startsWith("Módulo")) { h = sob; sep = "sí: (1, 2, 1)ᵀ por (1, 0, −1)"; }
    else if (nombre === "Sobel y") { h = sob[0].map((_, j) => sob.map(r => r[j])); sep = "sí: (1, 0, −1)ᵀ por (1, 2, 1)"; }
    else if (nombre === "Laplaciano") { h = lap; sep = "no"; }
    else if (nombre.startsWith("Realce")) { h = lap.map((r, i) => r.map((v, j) => (i === 1 && j === 1 ? 1 : 0) - kr.value * v)); sep = "no"; }
    else { h = [0, 1, 2].map(i => [0, 1, 2].map(j => celdas[3 * i + j].value || 0)); sep = "según los valores"; }
    let out = conv2d(f, h, borde.value);
    if (nombre.startsWith("Módulo")) { const gy = conv2d(f, sob[0].map((_, j) => sob.map(r => r[j])), borde.value); out = out.map((r, m) => r.map((v, n) => Math.hypot(v, gy[m][n]))); }
    F0.data = {img: [matriz(f)]}; G0.data = {img: [matriz(out)]};
    // Escala de grises: [0, 1] para los paso bajo; simétrica para los que suman 0
    const suma = h.flat().reduce((a, b) => a + b, 0);
    let lo = 0, hi = 1, omin = Infinity, omax = -Infinity;
    for (const r of out) for (const v of r) { if (v < omin) omin = v; if (v > omax) omax = v; }
    if (nombre.startsWith("Módulo")) { lo = 0; hi = omax; }
    else if (Math.abs(suma) < 1e-9) { const m = Math.max(Math.abs(omin), Math.abs(omax)) || 1; lo = -m; hi = m; }
    mapa.low = lo; mapa.high = hi;
    const k = h.length, hm = Math.max(...h.flat().map(Math.abs)) || 1;
    Hk.data = {img: [matriz(h.slice().reverse())], x: [0], y: [0], dw: [k], dh: [k]};
    mapa_h.low = -hm; mapa_h.high = hm;
    const xs = [], ys = [], ts = [];
    if (k <= 7) for (let i = 0; i < k; i++) for (let j = 0; j < k; j++) { xs.push(j + 0.5); ys.push(k - i - 0.5); ts.push(+h[i][j].toFixed(3) + ""); }
    Ht.data = {x: xs, y: ys, t: ts};
    p3.x_range.start = 0; p3.x_range.end = k; p3.y_range.start = 0; p3.y_range.end = k;
    Pr.data = {n: enteros(0, N - 1), f: f[FILA], g: out[FILA]};
    info.text = `<p>Núcleo de ${k}×${k}; suma de los coeficientes ${suma.toFixed(3)}` +
        (Math.abs(suma - 1) < 1e-9 ? " (conserva el nivel medio)" : Math.abs(suma) < 1e-9 ? " (anula las zonas uniformes)" : "") + `</p>` +
        `<p>¿Separable? ${sep}</p><p>Productos por píxel: ${k * k} directamente` + (sep.startsWith("sí") ? `, ${2 * k} separando filas y columnas` : "") + `</p>` +
        `<p>Valores de g: de ${omin.toFixed(3)} a ${omax.toFixed(3)}</p>`;
""", F0=F0, G0=G0, Hk=Hk, Ht=Ht, Pr=Pr, Foto=Foto, mapa=mapa, mapa_h=mapa_h, p3=p3, imagen=imagen, sr=sr,
   nucleo=nucleo, K=K, sg=sg, kr=kr, borde=borde, celdas=celdas, info=info, LADO=LADO, FILA=FILA)
pb.conectar(cb, imagen, sr, nucleo, K, sg, kr, borde)
for c in celdas:
    c.js_on_change("value", cb)
fi.js_on_change("value", pb.js("""
    foto_cargar(fi, LADO, img => { Foto.data = {f: [img]}; if (imagen.value === "Foto propia") cb.execute(); else imagen.value = "Foto propia"; });
""", fi=fi, Foto=Foto, imagen=imagen, cb=cb, LADO=LADO))

pb.pagina(__file__, "Convolución bidimensional", tema=5,
          descripcion="Cada píxel de g = h ∗ f es una combinación lineal de sus vecinos, con los pesos del núcleo h girado "
                      "180°. Los núcleos que suman 1 (media, gaussiano) suavizan; los que suman 0 (Sobel, laplaciano) "
                      "responden a los cambios y marcan los bordes. Puedes cargar una foto propia: se procesa en el "
                      "navegador y no se envía a ningún sitio.",
          controles=[imagen, fi, sr, nucleo, K, sg, kr, borde, rejilla, info],
          graficas=[[p1, p2, p3], p4], inicio=cb,
          referencia="Transparencias T5-03, convolución bidimensional, núcleos habituales y Sobel · Apuntes del Tema 5, sección 3")
