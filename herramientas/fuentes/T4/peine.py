"""T4 · Filtros en peine para eliminar (o extraer) una interferencia periódica."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
import numpy as np
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

FS = 1000
H = ColumnDataSource(dict(f=[], m=[]))
Po = ColumnDataSource(dict(x=[], y=[]))
Ce = ColumnDataSource(dict(x=[], y=[]))
S = ColumnDataSource(dict(t=[], x=[], y=[], r=[]))
E = ColumnDataSource(dict(f=[], x=[], y=[]))

p1 = pb.figura("Módulo |H| (dB)", "f (Hz)", "", ancho=420, alto=200, x_range=(0, FS / 2), y_range=(-50, 5))
p1.line("f", "m", source=H, color=pb.AZUL, line_width=2)
p2 = pb.figura("Polos (×) y ceros (○)", "Re z", "Im z", ancho=200, alto=200, x_range=(-1.25, 1.25), y_range=(-1.25, 1.25))
th = np.linspace(0, 2 * np.pi, 200)
p2.line(np.cos(th), np.sin(th), color=pb.GRIS, line_width=1)
p2.scatter("x", "y", source=Ce, marker="circle", size=8, line_width=2, line_color=pb.AZUL, fill_color=None)
p2.scatter("x", "y", source=Po, marker="x", size=8, line_width=2, color=pb.ROJO)
p3 = pb.figura("Señal con interferencia x[n] y salida y[n]", "t (s)", "", ancho=680, alto=200, x_range=(0, 1.5))
p3.line("t", "x", source=S, color=pb.GRIS_CLARO, line_width=1, legend_label="x[n]")
p3.line("t", "r", source=S, color=pb.VERDE, line_width=1.5, line_dash="dashed", legend_label="referencia")
p3.line("t", "y", source=S, color=pb.AZUL, line_width=1.5, legend_label="y[n]")
pb.leyenda(p3, "below")
p4 = pb.figura("Espectros de x e y (dB, régimen permanente)", "f (Hz)", "", ancho=680, alto=180, x_range=(0, FS / 2), y_range=(-70, 5))
p4.line("f", "x", source=E, color=pb.GRIS, line_width=1.5, legend_label="X")
p4.line("f", "y", source=E, color=pb.AZUL, line_width=1.5, legend_label="Y")
pb.leyenda(p4, "below")

tipo = pb.selector("Filtro", ["Ranuras en peine (IIR)", "Peine FIR: 1 − z^−L", "Resonador en peine"])
f0 = pb.deslizador("Frecuencia de diseño f₀ (Hz)", 40, 70, 50, 1)
a = pb.deslizador("a (polos en radio a^(1/L))", 0.5, 0.995, 0.95, 0.005)
nh = pb.deslizador("Armónicos de la interferencia", 1, 6, 3, 1)
A = pb.deslizador("Amplitud de la interferencia", 0, 2, 1, 0.05)
info = Div(text="", width=240)

cb = pb.js(f"const fs = {FS};" + """
    const L = Math.round(fs / f0.value), av = a.value, Nn = 4000, n = enteros(0, Nn - 1), t = n.map(k => k / fs), res = tipo.value.startsWith("Reson");
    // Señal útil (7 y 23 Hz) más una interferencia de 50 Hz con armónicos de amplitud decreciente
    const util = t.map(v => Math.sin(2 * PI * 7 * v) + 0.5 * Math.sin(2 * PI * 23 * v + 1));
    const zumb = t.map(v => { let s = 0; for (let k = 1; k <= nh.value; k++) s += A.value / k * Math.cos(2 * PI * 50 * k * v + 0.7 * k); return s; });
    const x = util.map((v, i) => v + zumb[i]);
    let b = new Array(L + 1).fill(0), den = new Array(L + 1).fill(0); den[0] = 1;
    if (tipo.value.startsWith("Ranuras")) { b[0] = (1 + av) / 2; b[L] = -(1 + av) / 2; den[L] = -av; }
    else if (tipo.value.startsWith("Peine FIR")) { b[0] = 1; b[L] = -1; den = [1]; }
    else { b = [1 - av]; den[L] = -av; }
    const y = filtrar(b, den, x);
    S.data = {t: t, x: x, y: y, r: res ? zumb : util};
    const f = rango(0, fs / 2, 4001), Hw = f.map(v => { const z = cexp([0, -2 * PI * v / fs]);
        return cdiv(evalpoli(b.slice().reverse(), z), evalpoli(den.slice().reverse(), z)); });
    H.data = {f: f, m: Hw.map(v => db(cabs(v), -60))};
    const raizL = enteros(0, L - 1).map(k => 2 * PI * k / L), rp = av ** (1 / L);
    Ce.data = res ? {x: [0], y: [0]} : {x: raizL.map(Math.cos), y: raizL.map(Math.sin)};
    Po.data = tipo.value.startsWith("Peine FIR") ? {x: [0], y: [0]} : {x: raizL.map(w => rp * Math.cos(w)), y: raizL.map(w => rp * Math.sin(w))};
    // Espectros de las últimas 2048 muestras (pasado el transitorio) con ventana de Hann
    const esp = s => { const seg = s.slice(Nn - 2048), w = ventana("Hann", 2048), [re, im] = fft(seg.map((v, i) => v * w[i]));
        return re.slice(0, 1024).map((v, i) => db(2 * Math.hypot(v, im[i]) / 1024, -80)); };
    E.data = {f: enteros(0, 1023).map(k => k * fs / 2048), x: esp(x), y: esp(y)};
    const fr = fs / L, at = cabs(Hw[400]);
    info.text = `<p>L = round(fs/f₀) = ${L}; las ${res ? "resonancias" : "ranuras"} están en múltiplos de fs/L = ${fr.toFixed(2)} Hz.</p>` +
        `<p>Ganancia a 50 Hz: ${at < 1e-6 ? "0 (un cero cae justo en 50 Hz)" : db(at, -120).toFixed(1) + " dB"}${Math.abs(fr - 50) > 0.01 ? " (fs/L no coincide con la red: la ranura no cae en su sitio)" : ""}.</p>` +
        (tipo.value.startsWith("Ranuras") ? `<p>H(z) = (1 + a)/2 · (1 − z^−L)/(1 − a·z^−L). Ancho de cada ranura ≈ (1 − a)·fs/(πL) = ${((1 - av) * fs / (PI * L)).toFixed(2)} Hz; el transitorio dura unas L/(1 − a) = ${Math.round(L / (1 - av))} muestras.</p>` :
         tipo.value.startsWith("Peine FIR") ? "<p>Sin polos, las ranuras son anchas: el filtro también deforma la señal útil (|H| = 2|sin(ΩL/2)|).</p>" :
         "<p>H(z) = (1 − a)/(1 − a·z^−L) deja pasar solo los múltiplos de fs/L: extrae la interferencia (compárala con la referencia verde).</p>") +
        "<p>Las ranuras en peine también quitan la componente continua (k = 0).</p>";
""", H=H, Po=Po, Ce=Ce, S=S, E=E, tipo=tipo, f0=f0, a=a, nh=nh, A=A, info=info)
pb.conectar(cb, tipo, f0, a, nh, A)

pb.pagina(__file__, "Filtro en peine", tema=4,
          descripcion="Una interferencia periódica, como el zumbido de 50 Hz de la red y sus armónicos, ocupa frecuencias "
                      "múltiplos de f₀. El filtro 1 − z^−L tiene ceros en las L raíces de la unidad, es decir, en múltiplos de "
                      "fs/L. Añadiendo polos muy cerca de cada cero, las ranuras se estrechan y la señal útil apenas cambia. "
                      "Con solo los polos, el filtro hace lo contrario: extrae la parte periódica.",
          controles=[tipo, f0, a, nh, A, info], graficas=[[p1, p2], p3, p4], inicio=cb,
          referencia="Transparencias T4-05, filtros especiales · Apuntes del Tema 4, sección 5")
