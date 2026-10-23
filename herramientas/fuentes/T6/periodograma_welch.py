"""T6 · Estimación de la DEP: periodograma frente a Bartlett y Welch."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div, Span
import pds_bokeh as pb

NR = 10

E = ColumnDataSource(dict(W=[], e=[], lo=[], hi=[], t=[]))

p1 = pb.figura("Estimación de la DEP (dB): una realización y la franja de 10 realizaciones", "Ω (rad/muestra)", "dB",
               ancho=640, alto=330, x_range=(0, 3.1416), y_range=(-25, 30))
p1.varea("W", "lo", "hi", source=E, fill_color=pb.AZUL, fill_alpha=0.15, legend_label="mín.–máx. de 10 realizaciones")
p1.line("W", "e", source=E, color=pb.AZUL, line_width=1.3, legend_label="una realización")
p1.line("W", "t", source=E, color=pb.ROJO, line_width=2.5, line_dash="dashed", legend_label="DEP del AR(2)")
tono = Span(location=2.2, dimension="height", line_color=pb.NARANJA, line_width=2, line_dash="dotted")
p1.add_layout(tono)
pb.leyenda(p1, "below")

metodo = pb.selector("Método", ["Periodograma", "Bartlett", "Welch"], "Welch")
N = pb.selector("N (muestras de la señal)", ["256", "1024", "4096", "16384"], "4096")
L = pb.selector("L (muestras de cada tramo)", ["32", "64", "128", "256", "512", "1024"], "256")
sol = pb.selector("Solapamiento (Welch)", ["0 %", "50 %", "75 %"], "50 %")
tipo = pb.selector("Ventana (Welch)", ["Hann", "Hamming", "Blackman", "Rectangular"])
A = pb.deslizador("Amplitud del tono A", 0, 1, 0.3, 0.01)
W1 = pb.deslizador("Frecuencia del tono Ω₁", 0.2, 3, 2.2, 0.01)
semilla = pb.deslizador("Realización", 1, 50, 1, 1)
info = Div(text="", width=250)

cb = pb.js("""
    const Nn = parseInt(N.value), met = metodo.value, r = 0.9, th = PI / 3, a1 = -2 * r * Math.cos(th), a2 = r * r;
    let l = met === "Periodograma" ? Nn : Math.min(parseInt(L.value), Nn), Rr = l, w;
    if (met === "Welch") { Rr = Math.max(1, Math.round(l * (1 - parseInt(sol.value) / 100))); w = ventana(tipo.value, l + 1).slice(0, l); }
    else w = new Array(l).fill(1);
    const Nf = Math.max(pot2(l), 1024), ests = [];
    for (let j = 0; j < NR; j++) {
        const g = generador(semilla.value * 100 + j), ph = 2 * PI * g();
        // AR(2) con polos en 0,9e^{±jπ/3} más un tono de fase aleatoria; se descartan 200 muestras de arranque
        const e = enteros(1, Nn + 200).map(() => gauss(g)), x = filtrar([1], [1, a1, a2], e).slice(200).map((v, n) => v + A.value * Math.cos(W1.value * n + ph));
        ests.push(welch(x, null, w, Rr, Nf));
    }
    const W = ests[0].W, K = W.length;
    const teo = W.map(Om => { const z = cexp([0, -Om]), d = csum(csum([1, 0], cesc(a1, z)), cesc(a2, cmul(z, z))); return -10 * Math.log10(d[0] ** 2 + d[1] ** 2); });
    const dB = v => 10 * Math.log10(Math.max(v, 1e-12));
    const lo = enteros(0, K - 1).map(k => dB(minimo(ests.map(s => s.Pxx[k])))), hi = enteros(0, K - 1).map(k => dB(maximo(ests.map(s => s.Pxx[k]))));
    E.data = {W: W, e: ests[0].Pxx.map(dB), lo: lo, hi: hi, t: teo};
    tono.location = W1.value; tono.visible = A.value > 0;
    // Varianza relativa media (lejos del tono y de los extremos): ≈ 1 en el periodograma, ≈ 1/K al promediar K tramos
    let vr = 0, c = 0;
    for (let k = 1; k < K - 1; k++) {
        if (Math.abs(W[k] - W1.value) < 0.3) continue;
        const v = ests.map(s => s.Pxx[k]), m = media(v); vr += varianza(v) / (m * m); c++;
    }
    const ml = tipo.value === "Rectangular" || met !== "Welch" ? 2 : tipo.value === "Blackman" ? 6 : 4;
    info.text = `<p>${ests[0].tramos} tramo(s) de ${l} muestras` + (met === "Welch" ? `, que avanzan ${Rr}` : "") + `</p>` +
        `<p>Lóbulo principal de la ventana: ${(2 * PI * ml / l).toFixed(4)} rad/muestra entre ceros: es la resolución</p>` +
        `<p>Varianza relativa media de la estimación: ${(vr / c).toFixed(3)}` + (met === "Periodograma" ? " (no baja al aumentar N)" : ` (1/K = ${(1 / ests[0].tramos).toFixed(3)})`) + `</p>` +
        `<p>Potencia del tono: A²/2 = ${(A.value ** 2 / 2).toFixed(3)}; potencia del AR(2): ${((1 + a2) / ((1 - a2) * ((1 + a2) ** 2 - a1 * a1))).toFixed(3)}</p>`;
""", E=E, tono=tono, metodo=metodo, N=N, L=L, sol=sol, tipo=tipo, A=A, W1=W1, semilla=semilla, info=info, NR=NR)
pb.conectar(cb, metodo, N, L, sol, tipo, A, W1, semilla)

pb.pagina(__file__, "Periodograma y método de Welch", tema=6,
          descripcion="El periodograma |X(e<sup>jΩ</sup>)|²/N de una sola realización es asintóticamente insesgado, pero su "
                      "varianza no baja con N: con más muestras salen más frecuencias, igual de ruidosas. Bartlett promedia "
                      "los periodogramas de K tramos, y la varianza baja en un factor K a cambio de resolución. Welch, además, "
                      "enventana y solapa los tramos.",
          controles=[metodo, N, L, sol, tipo, A, W1, semilla, info], graficas=[p1], inicio=cb,
          referencia="Transparencias T6-04, periodograma y método de Welch · Apuntes del Tema 6, sección 4")
