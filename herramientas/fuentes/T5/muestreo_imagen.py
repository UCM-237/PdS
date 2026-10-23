"""T5 · Muestreo y cuantificación de imágenes: muaré, prefiltro y contornos falsos."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

LADO = 256

F0 = ColumnDataSource(dict(img=[]))
S1 = ColumnDataSource(dict(img=[]))
Q1 = ColumnDataSource(dict(img=[]))
Pr = ColumnDataSource(dict(n=[], f=[]))
Ps = ColumnDataSource(dict(n=[], s=[]))
Foto = ColumnDataSource(dict(f=[]))

p1 = pb.figura_imagen("Original (256×256)", LADO, ancho=240)
pb.imagen(p1, F0, dw=LADO, dh=LADO)
p2 = pb.figura_imagen("Submuestreada", LADO, ancho=240)
pb.imagen(p2, S1, dw=LADO, dh=LADO)
p3 = pb.figura_imagen("Cuantificada con b bits", LADO, ancho=240)
pb.imagen(p3, Q1, dw=LADO, dh=LADO)
for p in (p2, p3):
    p.x_range = p1.x_range
    p.y_range = p1.y_range
p4 = pb.figura("Fila central: original y muestras que se conservan", "n (columna)", "", ancho=740, alto=170, x_range=(0, LADO))
p4.line("n", "f", source=Pr, color=pb.GRIS_CLARO, line_width=2)
pb.tallos(p4, "n", "s", Ps, color=pb.ROJO, size=4)

imagen = pb.selector("Imagen", ["Anillos", "Rayas", "Prueba", "Texto", "Tablero", "Foto propia"])
fi = pb.foto()
M = pb.deslizador("Submuestreo M", 1, 8, 3, 1)
pre = pb.selector("Prefiltro antes de submuestrear", ["Ninguno", "Media M×M", "Gaussiano (σ = M/2)"])
bits = pb.deslizador("Bits por píxel b", 1, 8, 3, 1)
info = Div(text="", width=250)

cb = pb.js("""
    const N = LADO, m = M.value;
    let f;
    if (imagen.value === "Foto propia" && Foto.data.f.length) f = Foto.data.f[0];
    else f = imagen_patron(imagen.value === "Foto propia" ? "Prueba" : imagen.value, N);
    // Prefiltro paso bajo para quitar lo que no cabe en la nueva frecuencia de muestreo
    let g = f;
    if (m > 1 && pre.value.startsWith("Media")) { const h = enteros(1, 2 * Math.floor(m / 2) + 1).map((_, i, a) => a.map(() => 1 / (a.length ** 2))); g = conv2d(f, h, "reflejar"); }
    else if (m > 1 && pre.value.startsWith("Gauss")) {
        const s = m / 2, r = Math.ceil(3 * s), v = enteros(-r, r).map(i => Math.exp(-i * i / (2 * s * s))), t = v.reduce((a, b) => a + b, 0);
        g = conv2d(f, v.map(a => v.map(b => a * b / (t * t))), "reflejar");
    }
    // Se toma una muestra de cada M y se repite en un bloque de M×M para verla al mismo tamaño
    const sub = f.map((fila, i) => fila.map((_, j) => g[i - (i % m)][j - (j % m)]));
    const L = 2 ** bits.value, cuant = f.map(fila => fila.map(v => Math.round(Math.min(1, Math.max(0, v)) * (L - 1)) / (L - 1)));
    F0.data = {img: [matriz(f)]}; S1.data = {img: [matriz(sub)]}; Q1.data = {img: [matriz(cuant)]};
    const c = N >> 1, cols = enteros(0, N - 1).filter(j => j % m === 0);
    Pr.data = {n: enteros(0, N - 1), f: f[c]}; Ps.data = {n: cols, s: cols.map(j => g[c - (c % m)][j])};
    const fmax = imagen.value === "Anillos" ? 0.5 : imagen.value === "Rayas" ? 0.42 : NaN;
    const kb = (N * N * 8 / 8 / 1024).toFixed(0), kbs = ((N / m) ** 2 / 1024).toFixed(1), kbq = (N * N * bits.value / 8 / 1024).toFixed(1);
    info.text = `<p>Tras submuestrear, la frecuencia espacial máxima que se representa sin aliasing es 1/(2M) = ${(1 / (2 * m)).toFixed(3)} ciclos/píxel</p>` +
        (isNaN(fmax) ? "" : `<p>Esta imagen llega a ${fmax} ciclos/píxel: con M ≥ 2 aparece muaré si no se prefiltra</p>`) +
        `<p>Niveles de gris: 2<sup>${bits.value}</sup> = ${L}. Con pocos niveles, los degradados se convierten en escalones (contornos falsos)</p>` +
        `<p>Tamaño sin comprimir: ${kb} kB a 8 bits; ${kbs} kB submuestreada; ${kbq} kB con ${bits.value} bits</p>`;
""", F0=F0, S1=S1, Q1=Q1, Pr=Pr, Ps=Ps, Foto=Foto, imagen=imagen, M=M, pre=pre, bits=bits, info=info, LADO=LADO)
pb.conectar(cb, imagen, M, pre, bits)
fi.js_on_change("value", pb.js("""
    foto_cargar(fi, LADO, img => { Foto.data = {f: [img]}; if (imagen.value === "Foto propia") cb.execute(); else imagen.value = "Foto propia"; });
""", fi=fi, Foto=Foto, imagen=imagen, cb=cb, LADO=LADO))

pb.pagina(__file__, "Muestreo y cuantificación de imágenes", tema=5,
          descripcion="Muestrear una imagen sigue las mismas reglas que muestrear en el tiempo: un detalle con periodo menor "
                      "que dos píxeles produce aliasing, el efecto muaré. Un paso bajo antes de submuestrear lo evita a cambio "
                      "de emborronar. Cuantificar con b bits deja 2<sup>b</sup> niveles, y con pocos aparecen contornos falsos.",
          controles=[imagen, fi, M, pre, bits, info], graficas=[[p1, p2, p3], p4], inicio=cb,
          referencia="Transparencias T5-03, muestreo, cuantificación y almacenamiento · Apuntes del Tema 5, sección 3")
