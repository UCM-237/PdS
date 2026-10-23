"""T2 · Cuantificación uniforme y relación señal a ruido de cuantificación."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div, Span
import pds_bokeh as pb

S = ColumnDataSource(dict(n=[], x=[], q=[], e=[]))
Hs = ColumnDataSource(dict(c=[], h=[], w=[]))
C = ColumnDataSource(dict(x=[], q=[]))

p1 = pb.figura("Señal x[n] y señal cuantificada x_q[n]", "n", "", ancho=480, alto=220)
p1.line("n", "x", source=S, color=pb.GRIS, line_width=1.5, legend_label="x[n]")
p1.step("n", "q", source=S, color=pb.AZUL, line_width=2, mode="center", legend_label="x_q[n]")
pb.leyenda(p1, "below")
p2 = pb.figura("Característica del cuantificador", "x", "x_q", ancho=220, alto=220, x_range=(-1.6, 1.6), y_range=(-1.6, 1.6))
p2.line("x", "q", source=C, color=pb.AZUL, line_width=2)
p2.line(x=[-1.6, 1.6], y=[-1.6, 1.6], color=pb.GRIS_CLARO, line_dash="dashed")
p3 = pb.figura("Error e[n] = x_q[n] − x[n]", "n", "", ancho=480, alto=180)
p3.line("n", "e", source=S, color=pb.ROJO, line_width=1.2)
lim1 = Span(location=0, dimension="width", line_color=pb.GRIS, line_dash="dashed")
lim2 = Span(location=0, dimension="width", line_color=pb.GRIS, line_dash="dashed")
p3.add_layout(lim1); p3.add_layout(lim2)
p4 = pb.figura("Histograma del error", "e/Δ", "", ancho=220, alto=180, x_range=(-1.1, 1.1))
p4.vbar(x="c", top="h", width="w", source=Hs, color=pb.ROJO, alpha=0.6)

senal = pb.selector("Señal", ["Sinusoide", "Suma de tonos", "Rampa lenta", "Ruido gaussiano"])
B = pb.deslizador("B (bits)", 1, 12, 4, 1)
A = pb.deslizador("Amplitud (fondo de escala = 1)", 0.02, 1.5, 0.95, 0.01)
modo = pb.botones(["Redondeo", "Truncamiento"])
info = Div(text="", width=240)

cb = pb.js("""
    const L = 2000, n = enteros(0, L - 1), r = ruido(L, 11), b = B.value, D = 2 / 2 ** b, red = modo.active === 0;
    let x;
    if (senal.value === "Sinusoide") x = n.map(k => A.value * Math.sin(2 * PI * k * 0.0123 + 0.3));
    else if (senal.value.startsWith("Suma")) x = n.map(k => A.value * (0.6 * Math.sin(2 * PI * k * 0.0071) + 0.4 * Math.sin(2 * PI * k * 0.0533 + 1)));
    else if (senal.value.startsWith("Rampa")) x = n.map(k => A.value * (2 * k / (L - 1) - 1));
    else x = r.map(v => A.value * v / 3);
    // Cuantificador de B bits en [−1, 1): niveles k·Δ (redondeo) o truncando hacia −∞, con saturación
    const qz = v => { const k = red ? Math.round(v / D) : Math.floor(v / D); return Math.max(-(2 ** (b - 1)), Math.min(2 ** (b - 1) - 1, k)) * D; };
    const q = x.map(qz), e = q.map((v, i) => v - x[i]);
    const vis = 300;
    S.data = {n: n.slice(0, vis), x: x.slice(0, vis), q: q.slice(0, vis), e: e.slice(0, vis)};
    const cx = rango(-1.6, 1.6, 2001); C.data = {x: cx, q: cx.map(qz)};
    lim1.location = red ? D / 2 : 0; lim2.location = red ? -D / 2 : -D;
    // Histograma del error sin contar las muestras saturadas
    const ok = e.filter((v, i) => Math.abs(x[i]) < 1 - D), nb = 20, c = [], h = new Array(nb).fill(0);
    for (let i = 0; i < nb; i++) c.push(-1 + (i + 0.5) * 2 / nb);
    ok.forEach(v => { const i = Math.floor((v / D + 1) / 2 * nb); if (i >= 0 && i < nb) h[i]++; });
    Hs.data = {c: c, h: h.map(v => v / Math.max(1, ok.length) * nb / 2), w: c.map(() => 2 / nb * 0.9)};
    const Px = x.reduce((s, v) => s + v * v, 0) / L, Pe = e.reduce((s, v) => s + v * v, 0) / L, me = e.reduce((s, v) => s + v, 0) / L;
    const sat = x.filter(v => v >= (red ? 1 - D / 2 : 1) || v < (red ? -1 - D / 2 : -1)).length;
    info.text = `<p>Δ = 2/2^B = ${D.toPrecision(3)}; ${2 ** b} niveles</p>` +
        `<p>Error: media ${me.toExponential(2)}, varianza ${(Pe - me * me).toExponential(2)} (Δ²/12 = ${(D * D / 12).toExponential(2)})</p>` +
        `<p><b>SQNR medida: ${(10 * Math.log10(Px / Pe)).toFixed(1)} dB</b></p>` +
        `<p>Modelo: 10·log₁₀(P_x/(Δ²/12)) = ${(10 * Math.log10(Px / (D * D / 12))).toFixed(1)} dB; sinusoide a fondo de escala: 6,02B + 1,76 = ${(6.02 * b + 1.76).toFixed(1)} dB</p>` +
        (sat ? `<p style="color:#C0392B">${sat} muestras saturadas: la señal sale del rango del cuantificador y el error supera Δ/2.</p>` : "") +
        (red ? "" : "<p>El truncamiento tiene error medio −Δ/2: un sesgo que el redondeo no tiene.</p>");
""", S=S, Hs=Hs, C=C, lim1=lim1, lim2=lim2, senal=senal, B=B, A=A, modo=modo, info=info)
pb.conectar(cb, senal, B, A, modo)

pb.pagina(__file__, "Cuantificación y SQNR", tema=2,
          descripcion="Un cuantificador uniforme de B bits en [−1, 1) tiene paso Δ = 2/2^B. Con redondeo, el error está "
                      "entre −Δ/2 y Δ/2 y, si la señal varía lo suficiente, se comporta como un ruido uniforme de varianza "
                      "Δ²/12: cada bit más mejora la SQNR en unos 6 dB. Con señales pequeñas o lentas el modelo falla, y "
                      "por encima del fondo de escala la señal se satura.",
          controles=[senal, B, A, modo, info], graficas=[[p1, p2], [p3, p4]], inicio=cb,
          referencia="Transparencias T2-03, cuantificación y ruido de cuantificación · Apuntes del Tema 2, sección 5")
