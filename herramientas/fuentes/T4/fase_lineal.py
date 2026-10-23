"""T4 · Fase lineal, retardo de grupo y distorsión de fase."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

s = ColumnDataSource(dict(n=[], x=[], y=[], xr=[]))
H = ColumnDataSource(dict(W=[], m=[], f=[], g=[]))

p1 = pb.figura("Entrada x[n] y salida y[n]", "n", "", ancho=720, alto=230)
p1.line("n", "x", source=s, color=pb.GRIS_CLARO, line_width=1.5, legend_label="x[n]")
p1.line("n", "xr", source=s, color=pb.VERDE, line_width=1.5, line_dash="dashed", legend_label="x[n − τ] (sólo retraso)")
p1.line("n", "y", source=s, color=pb.AZUL, line_width=2, legend_label="y[n]")
pb.leyenda(p1, "below")
p2 = pb.figura("Módulo |H(e^jΩ)|", "Ω (rad/muestra)", "", ancho=220, alto=200, x_range=(0, 3.1416))
p2.line("W", "m", source=H, color=pb.AZUL, line_width=2)
p3 = pb.figura("Fase desenrollada φ(Ω) (rad)", "Ω (rad/muestra)", "", ancho=220, alto=200, x_range=(0, 3.1416))
p3.line("W", "f", source=H, color=pb.ROJO, line_width=2)
p4 = pb.figura("Retardo de grupo τ(Ω) = −dφ/dΩ", "Ω (rad/muestra)", "muestras", ancho=220, alto=200,
               x_range=(0, 3.1416))
p4.line("W", "g", source=H, color=pb.VERDE, line_width=2)

filtro = pb.selector("Filtro", ["Ideal: φ = −αΩ − β", "FIR de fase lineal (Hamming)", "IIR Butterworth"])
senal = pb.selector("Entrada", ["Tres tonos", "Pulso rectangular", "Pulso modulado (envolvente)"])
Wc = pb.deslizador("Ωc / π (corte)", 0.1, 0.9, 0.3, 0.01)
alfa = pb.deslizador("α (retardo, muestras; ideal)", 0, 40, 15, 0.5)
beta = pb.deslizador("β / π (fase constante; ideal)", -1, 1, 0, 0.05)
N = pb.deslizador("Orden (FIR: N − 1 ≤ 60; IIR: N ≤ 12)", 1, 60, 30, 1)
info = Div(text="", width=240)

cb = pb.js("""
    const M = 512, wc = Wc.value * PI, Wk = enteros(0, M - 1).map(k => 2 * PI * k / M);
    // Respuesta en frecuencia en las M frecuencias de la FFT (simetría hermítica)
    let Hf;
    if (filtro.value.startsWith("Ideal")) {
        Hf = Wk.map(w => { const v = w > PI ? w - 2 * PI : w, a = Math.abs(v) <= wc ? 1 : 0;
                           return cesc(a, cexp([0, -alfa.value * v - Math.sign(v) * beta.value * PI])); });
    } else if (filtro.value.startsWith("FIR")) {
        const L = N.value, h = enteros(0, L).map(n => wc / PI * sinc(wc * (n - L / 2) / PI) * (0.54 - 0.46 * Math.cos(2 * PI * n / L)));
        Hf = Wk.map(w => evalpoli(h.slice().reverse(), cexp([0, -w])));
    } else {
        const [z, p, k] = butter_z(Math.min(N.value, 12), wc);
        Hf = Wk.map(w => zpk(z, p, k, cexp([0, w])));
    }
    // Entrada periódica de periodo M
    const n = enteros(0, M - 1);
    let x;
    if (senal.value === "Tres tonos") x = n.map(k => Math.cos(2 * PI * 8 * k / M) + Math.cos(2 * PI * 20 * k / M + 1) + 0.8 * Math.cos(2 * PI * 32 * k / M + 2));
    else if (senal.value.startsWith("Pulso rect")) x = n.map(k => (k >= 40 && k < 72) ? 1 : 0);
    else x = n.map(k => Math.exp(-(((k - 80) / 18) ** 2)) * Math.cos(0.5 * wc * (k - 80)));
    const [xr, xi] = fft(x), Yr = [], Yi = [];
    for (let k = 0; k < M; k++) { const y = cmul([xr[k], xi[k]], Hf[k]); Yr.push(y[0]); Yi.push(-y[1]); }
    const y = fft(Yr, Yi)[0].map(v => v / M);
    // Fase y retardo de grupo en la banda de paso
    const K = M / 2 + 1, W = Wk.slice(0, K), mag = Hf.slice(0, K).map(cabs);
    const f = desenrollar(Hf.slice(0, K).map(h => Math.atan2(h[1], h[0])));
    const g = W.map((w, i) => { const j = Math.min(Math.max(i, 1), K - 2); return mag[i] > 0.05 ? -(f[j + 1] - f[j - 1]) / (W[j + 1] - W[j - 1]) : NaN; });
    H.data = {W: W, m: mag, f: f.map((v, i) => mag[i] > 0.05 ? v : NaN), g: g};
    // Retraso de referencia: el retardo de grupo en Ω ≈ 0 (o el de la frecuencia de la envolvente)
    const i0 = senal.value.startsWith("Pulso mod") ? Math.round(0.5 * wc / (2 * PI) * M) : 2;
    const tau = isNaN(g[i0]) ? 0 : g[i0], t = Math.round(tau);
    s.data = {n: n.slice(0, 260), x: x.slice(0, 260), y: y.slice(0, 260), xr: n.slice(0, 260).map(k => x[mod(k - t, M)])};
    const gs = g.filter(v => !isNaN(v)), dg = gs.length ? Math.max(...gs) - Math.min(...gs) : 0;
    info.text = `<p>Retardo de grupo en la banda de paso: de ${Math.min(...gs).toFixed(1)} a ${Math.max(...gs).toFixed(1)} muestras</p>` +
                `<p>${dg < 0.5 && Math.abs(beta.value) < 1e-9 || !filtro.value.startsWith("Ideal") && dg < 0.5 ? "Fase lineal: todas las componentes se retrasan lo mismo y la forma se conserva." : dg < 0.5 ? "Fase lineal generalizada (β ≠ 0): la envolvente se retrasa α muestras, pero la portadora se desfasa y la forma cambia." : "Fase no lineal: cada componente se retrasa distinto y la forma de la señal cambia."}</p>`;
""", s=s, H=H, filtro=filtro, senal=senal, Wc=Wc, alfa=alfa, beta=beta, N=N, info=info)
pb.conectar(cb, filtro, senal, Wc, alfa, beta, N)

pb.pagina(__file__, "Fase lineal y retardo de grupo", tema=4,
          descripcion="Con fase lineal φ(Ω) = −αΩ todas las componentes de la banda de paso se retrasan α muestras "
                      "y la salida es la entrada retrasada. Un término constante β desfasa la portadora pero mantiene "
                      "el retardo de la envolvente; una fase no lineal (IIR) retrasa cada frecuencia de forma distinta "
                      "y deforma los pulsos.",
          controles=[filtro, senal, Wc, alfa, beta, N, info], graficas=[p1, [p2, p3, p4]], inicio=cb,
          referencia="Transparencias T4-04, simetría y fase lineal · Apuntes del Tema 4, secciones 1 y 4")
