"""T2 · Cambio de la frecuencia de muestreo: expansor, filtro y compresor."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

ETAPAS = [("x", "Entrada x[n]"), ("e", "Tras el expansor ↑L"), ("w", "Tras el filtro paso bajo"), ("y", "Salida y[m] tras el compresor ↓M")]
ESPECTRO = dict(x="|X(e^jΩ)|", e="|X_e(e^jΩ)|", w="|W(e^jΩ)|", y="|Y(e^jΩ)|")
T = {k: ColumnDataSource(dict(t=[], v=[])) for k, _ in ETAPAS}
F = {k: ColumnDataSource(dict(W=[], m=[])) for k, _ in ETAPAS}
banda = ColumnDataSource(dict(W=[], m=[]))
COLOR = dict(x=pb.AZUL, e=pb.GRIS, w=pb.VERDE, y=pb.ROJO)

filas = []
for k, titulo in ETAPAS:
    pt = pb.figura(titulo, "tiempo (en periodos de muestreo de x)", "", ancho=420, alto=120, x_range=(-12, 12))
    pb.tallos(pt, "t", "v", T[k], color=COLOR[k], size=4)
    pf = pb.figura(ESPECTRO[k], "Ω (rad/muestra)", "",
                   ancho=300, alto=120, x_range=(-3.1416, 3.1416))
    if k == "w":
        pf.line("W", "m", source=banda, color=pb.GRIS_CLARO, line_width=2, line_dash="dashed")
    pf.line("W", "m", source=F[k], color=COLOR[k], line_width=2)
    filas.append([pt, pf])

senal = pb.selector("Señal", ["Espectro triangular", "Dos tonos"])
Wb = pb.deslizador("Ω_b/π (frecuencia máxima de x)", 0.05, 1, 0.5, 0.05)
L = pb.deslizador("L (factor de interpolación)", 1, 6, 2, 1)
M = pb.deslizador("M (factor de diezmado)", 1, 6, 3, 1)
filtro = pb.botones(["Con filtro", "Sin filtro"])
info = Div(text="", width=240)

cb = pb.js("""
    const l = L.value, m = M.value, wb = Wb.value * PI, K = 100, n = enteros(-K, K), tri = senal.value.startsWith("Espectro");
    // Entrada: sinc² (espectro triangular de altura 1 y ancho Ω_b) o dos tonos de Ω_b/2 y Ω_b con ventana de Hann
    const hann = n.map(k => 0.5 + 0.5 * Math.cos(PI * k / (K + 1)));
    const x = tri ? n.map(k => wb / (2 * PI) * sinc(wb * k / (2 * PI)) ** 2)
                  : n.map((k, i) => hann[i] * (Math.cos(wb / 2 * k) + 0.5 * Math.cos(wb * k)));
    const c = tri ? 1 : hann.reduce((s, v) => s + v, 0) / 2;
    // Expansor: L − 1 ceros entre muestras
    const e = new Array(x.length * l).fill(0); x.forEach((v, i) => e[i * l] = v);
    // Filtro paso bajo FIR (ventana de Hamming), corte π/max(L, M) y ganancia L; se compensa su retardo
    const R = Math.max(l, m), P = 8 * R, Wc = PI / R;
    const h = enteros(-P, P).map(k => l * Wc / PI * sinc(Wc * k / PI) * (0.54 + 0.46 * Math.cos(PI * k / (P + 1))));
    const con = filtro.active === 0 && R > 1;
    const w = con ? conv(e, h).slice(P, P + e.length) : e;
    // Compresor: se queda con una de cada M muestras (las de índice múltiplo de M respecto a n = 0)
    const i0 = K * l, y = [], ty = [];
    for (let i = i0 % m; i < w.length; i += m) { y.push(w[i]); ty.push((i - i0) / l); }
    const te = e.map((_, i) => (i - i0) / l);
    T.x.data = {t: n, v: x}; T.e.data = {t: te, v: e}; T.w.data = {t: te, v: w}; T.y.data = {t: ty, v: y};
    const espectro = s => { const Nf = 4096, [a, b] = dtft(s, Nf), W = [], v = [];
        for (let k = -Nf / 2; k < Nf / 2; k++) { const j = mod(k, Nf); W.push(2 * PI * k / Nf); v.push(Math.hypot(a[j], b[j]) / c); }
        return {W: W, m: v}; };
    F.x.data = espectro(x); F.e.data = espectro(e); F.w.data = espectro(w); F.y.data = espectro(y);
    banda.data = con ? {W: [-PI, -Wc, -Wc, Wc, Wc, PI], m: [0, 0, l, l, 0, 0]} : {W: [], m: []};
    // Diagnóstico de lo que ocurre con la banda de la señal
    const bandaE = wb / l, avisos = [];
    if (!con && l > 1) avisos.push(`Sin filtro quedan las ${l - 1} imágenes que crea el expansor.`);
    if (!con && m > 1 && bandaE * m > PI + 1e-9) avisos.push(`Hay aliasing: la banda Ω_b/L = ${(bandaE / PI).toFixed(2)}π supera π/M = ${(1 / m).toFixed(2)}π antes del compresor.`);
    if (con && m > l && wb > PI * l / m + 1e-9) avisos.push(`El filtro corta la parte de x por encima de πL/M = ${(l / m).toFixed(2)}π: se pierde, pero no se solapa.`);
    info.text = `<p>Frecuencia de muestreo de salida: fs·L/M = fs·${(l / m).toFixed(3)}</p>` +
        `<p>Tras ↑L, el espectro se comprime: X(e^jΩL), con imágenes cada 2π/L.</p>` +
        `<p>Tras ↓M, se ensancha M veces y se repite cada 2π: (1/M)·Σ W(e^j(Ω−2πk)/M).</p>` +
        `<p>Filtro: corte π/max(L, M) = ${(Wc / PI).toFixed(3)}π, ganancia L = ${l}, ${2 * P + 1} coeficientes.</p>` +
        (avisos.length ? avisos.map(a => `<p style="color:#C0392B">${a}</p>`).join("") : "<p style='color:#27AE60'>Ni imágenes ni aliasing.</p>");
""", T=T, F=F, banda=banda, senal=senal, Wb=Wb, L=L, M=M, filtro=filtro, info=info)
pb.conectar(cb, senal, Wb, L, M, filtro)

pb.pagina(__file__, "Diezmado e interpolación", tema=2,
          descripcion="Para cambiar la frecuencia de muestreo de una secuencia por un factor L/M, se intercalan L − 1 ceros "
                      "entre muestras (expansor), se filtra con un paso bajo de corte π/max(L, M) y ganancia L, y se toma "
                      "una de cada M muestras (compresor). El expansor crea imágenes del espectro y el compresor puede "
                      "producir aliasing; el filtro evita las dos cosas. Quita el filtro para ver qué ocurre sin él.",
          controles=[senal, Wb, L, M, filtro, info], graficas=filas, inicio=cb,
          referencia="Transparencias T2-04, muestreo de señales discretas · Apuntes del Tema 2, sección 6")
