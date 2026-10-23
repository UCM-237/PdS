"""T4 · Diseño de filtros FIR por el método de la ventana (fijas y Kaiser)."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import BoxAnnotation, ColumnDataSource, Div
import pds_bokeh as pb

h = ColumnDataSource(dict(n=[], h=[], hd=[], w=[]))
H = ColumnDataSource(dict(W=[], m=[]))

p1 = pb.figura("Respuesta al impulso h[n] = h_d[n − L]·w[n − L]", "n", "", ancho=330, alto=240)
p1.line("n", "hd", source=h, color=pb.GRIS_CLARO, line_width=1.5, line_dash="dashed", legend_label="ideal h_d")
p1.line("n", "w", source=h, color=pb.NARANJA, line_width=1.5, legend_label="ventana (escalada)")
pb.tallos(p1, "n", "h", h, color=pb.AZUL, legend_label="h[n]")
pb.leyenda(p1, "below")
p2 = pb.figura("Módulo |H(e^jΩ)|", "Ω (rad/muestra)", "", ancho=420, alto=240, x_range=(0, 3.1416))
paso = BoxAnnotation(fill_color=pb.VERDE, fill_alpha=0.10, line_color=None)
banda = BoxAnnotation(fill_color=pb.ROJO, fill_alpha=0.10, line_color=None)
p2.add_layout(paso); p2.add_layout(banda)
p2.line("W", "m", source=H, color=pb.AZUL, line_width=2)

tipo = pb.selector("Tipo", ["Paso bajo", "Paso alto"])
diseno = pb.selector("Diseño", ["Ventana fija", "Kaiser a partir de α_s y ΔΩ"])
vent = pb.selector("Ventana (diseño con ventana fija)", ["Rectangular", "Hann", "Hamming", "Blackman", "Kaiser"], "Hann")
Wc = pb.deslizador("Ωc / π (centro de la transición)", 0.05, 0.95, 0.4, 0.01)
L = pb.deslizador("L (N = 2L + 1 coeficientes)", 1, 60, 16, 1)
beta = pb.deslizador("β (Kaiser)", 0, 12, 5, 0.1)
As = pb.deslizador("α_s (dB, Kaiser)", 20, 100, 40, 1)
dW = pb.deslizador("ΔΩ / π (transición, Kaiser)", 0.02, 0.5, 0.2, 0.01)
escala = pb.botones(["dB", "Lineal"])
info = Div(text="", width=240)

cb = pb.js("""
    function I0(x) { let s = 1, t = 1; for (let k = 1; k < 40; k++) { t *= (x / (2 * k)) ** 2; s += t; } return s; }
    const wc = Wc.value * PI, alto = tipo.value === "Paso alto", kaiser = diseno.value.startsWith("Kaiser");
    let l = L.value, b = beta.value, nombre = vent.value;
    if (kaiser) {
        const a = As.value, dw = dW.value * PI;
        b = a > 50 ? 0.1102 * (a - 8.7) : a >= 21 ? 0.5842 * (a - 21) ** 0.4 + 0.07886 * (a - 21) : 0;
        l = Math.max(1, Math.ceil((a - 8) / (2.285 * dw) / 2)); nombre = "Kaiser";
    }
    const m = enteros(-l, l), N = 2 * l + 1;
    const w = m.map(k => {
        const c = 2 * PI * k / N;
        if (nombre === "Hann") return 0.5 + 0.5 * Math.cos(c);
        if (nombre === "Hamming") return 0.54 + 0.46 * Math.cos(c);
        if (nombre === "Blackman") return 0.42 + 0.5 * Math.cos(c) + 0.08 * Math.cos(2 * c);
        if (nombre === "Kaiser") return I0(b * Math.sqrt(Math.max(0, 1 - (k / l) ** 2))) / I0(b);
        return 1;
    });
    const hd = m.map(k => (alto ? (k === 0 ? 1 : 0) : 0) + (alto ? -1 : 1) * wc / PI * sinc(wc * k / PI));
    const hh = hd.map((v, i) => v * w[i]), top = Math.max(...hd.map(Math.abs));
    h.data = {n: enteros(0, N - 1), h: hh, hd: hd, w: w.map(v => v * top)};
    const M = 4096, [re, im] = dtft(hh, M), K = M / 2 + 1, mag = enteros(0, K - 1).map(k => Math.hypot(re[k], im[k]));
    const W = enteros(0, K - 1).map(k => 2 * PI * k / M), enDB = escala.active === 0;
    H.data = {W: W, m: mag.map(v => enDB ? db(v, -120) : v)};
    p2.title.text = enDB ? "Módulo |H(e^jΩ)| (dB)" : "Módulo |H(e^jΩ)|";
    // Bandas de la especificación (Kaiser) o de la transición teórica de la tabla (fijas)
    const tabla = {Rectangular: 0.92, Hann: 3.11, Hamming: 3.32, Blackman: 5.56};
    const dw = kaiser ? dW.value * PI : (tabla[nombre] ? tabla[nombre] * PI / l : (b * 0.17 + 0.92) * PI / l);
    const bp = alto ? [wc + dw / 2, PI] : [0, wc - dw / 2], bs = alto ? [0, wc - dw / 2] : [wc + dw / 2, PI];
    paso.left = bp[0]; paso.right = bp[1]; banda.left = bs[0]; banda.right = bs[1];
    // Atenuación conseguida en la banda de supresión y rizado en la de paso
    let peor = 0, rp = 0;
    for (let k = 0; k < K; k++) {
        if (W[k] >= bs[0] && W[k] <= bs[1]) peor = Math.max(peor, mag[k]);
        if (W[k] >= bp[0] && W[k] <= bp[1]) rp = Math.max(rp, Math.abs(mag[k] - 1));
    }
    info.text = `<p>${nombre}${nombre === "Kaiser" ? ", β = " + b.toFixed(2) : ""}; L = ${l}, N = ${N} coeficientes, retardo ${l} muestras</p>` +
                `<p>Transición ${kaiser ? "pedida" : "según la tabla"}: ΔΩ ≈ ${(dw / PI).toFixed(3)}π</p>` +
                `<p>Atenuación en la banda sombreada en rojo: ${(-db(peor)).toFixed(1)} dB${kaiser ? " (pedida " + As.value + " dB)" : ""}</p>` +
                `<p>Rizado en la banda de paso: δ = ${rp.toFixed(4)}</p>`;

""", h=h, H=H, tipo=tipo, diseno=diseno, vent=vent, Wc=Wc, L=L, beta=beta, As=As, dW=dW,
    escala=escala, info=info, p2=p2, paso=paso, banda=banda)
pb.conectar(cb, tipo, diseno, vent, Wc, L, beta, As, dW, escala)

pb.pagina(__file__, "Diseño FIR por ventanas", tema=4,
          descripcion="Se trunca la respuesta ideal h_d[n] a |n| ≤ L con una ventana y se retrasa L muestras. "
                      "La ventana fija el rizado (los lóbulos secundarios) y L, la anchura de la transición: "
                      "alargar la rectangular no quita el rizado de Gibbs. Con Kaiser, β y L salen de las fórmulas "
                      "empíricas a partir de la atenuación α_s y la transición ΔΩ pedidas.",
          controles=[tipo, diseno, vent, Wc, L, beta, As, dW, escala, info], graficas=[[p1, p2]], inicio=cb,
          referencia="Transparencias T4-04, ventanas fijas y ventana de Kaiser · Apuntes del Tema 4, sección 4")
