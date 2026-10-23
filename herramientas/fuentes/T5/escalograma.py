"""T5 · Escalograma (CWT) frente a espectrograma."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
import math
from bokeh.models import ColumnDataSource, CustomJSTickFormatter, Div, FixedTicker
import pds_bokeh as pb

FS, DUR, NE, FMIN, FMAX = 1000, 1.0, 72, 4, 400

X = ColumnDataSource(dict(t=[], x=[]))
Es = ColumnDataSource(dict(img=[], x=[], y=[], dw=[], dh=[]))
Ec = ColumnDataSource(dict(img=[], x=[], y=[], dw=[], dh=[]))
Wv = ColumnDataSource(dict(xs=[], ys=[], color=[]))

p1 = pb.figura("Señal x(t)", "t (s)", "", ancho=520, alto=140, x_range=(0, DUR))
p1.line("t", "x", source=X, color=pb.AZUL, line_width=1)
marcas = [5, 10, 20, 50, 100, 200, 400]
p2 = pb.figura("Espectrograma (STFT con ventana de Hann de L muestras)", "t (s)", "f (Hz)", ancho=520, alto=220,
               x_range=p1.x_range, y_range=(math.log10(FMIN), math.log10(FMAX)))
pb.imagen(p2, Es, x="x", y="y", dw="dw", dh="dh", paleta="viridis", bajo=-40, alto=0)
p3 = pb.figura("Escalograma |W(a, b)|² (frecuencia equivalente de cada escala)", "b (s)", "f (Hz)", ancho=520, alto=220,
               x_range=p1.x_range, y_range=p2.y_range)
pb.imagen(p3, Ec, x="x", y="y", dw="dw", dh="dh", paleta="viridis", bajo=-40, alto=0)
for p in (p2, p3):
    p.yaxis.ticker = FixedTicker(ticks=[math.log10(v) for v in marcas])
    p.yaxis.formatter = CustomJSTickFormatter(code="return Math.round(Math.pow(10, tick)).toString();")
p4 = pb.figura("Wavelet escalada a 10, 40 y 160 Hz (parte real)", "t (s)", "", ancho=300, alto=220)
p4.multi_line("xs", "ys", source=Wv, color="color", line_width=1.5)

senal = pb.selector("Señal", ["Tonos de 20 y 120 Hz y un clic", "Chirp de 5 a 300 Hz", "Tono de 50 Hz con un transitorio de 200 Hz",
                              "Dos clics a 10 ms"])
wav = pb.selector("Wavelet", ["Morlet", "Sombrero mexicano"])
L = pb.selector("L de la STFT (muestras)", ["32", "64", "128", "256", "512"], "128")
info = Div(text="", width=250)

cb = pb.js("""
    const fs = FS, Nx = Math.round(DUR * fs), t = enteros(0, Nx - 1).map(n => n / fs), s = senal.value;
    let x;
    if (s.startsWith("Tonos")) { x = t.map(v => (v < 0.5 ? Math.cos(2 * PI * 20 * v) : 0) + (v >= 0.5 ? Math.cos(2 * PI * 120 * v) : 0)); x[Math.round(0.3 * fs)] += 10; }
    else if (s.startsWith("Chirp")) x = t.map(v => Math.cos(2 * PI * (5 * v + 295 / 2 * v * v)));
    else if (s.startsWith("Tono")) x = t.map(v => Math.cos(2 * PI * 50 * v) + 2 * Math.exp(-(((v - 0.6) / 0.01) ** 2)) * Math.cos(2 * PI * 200 * v));
    else { x = t.map(() => 0); x[500] = 1; x[510] = 1; }
    X.data = {t: t, x: x};
    // Espectrograma con el eje de frecuencias logarítmico: se remuestrea en las mismas filas que el escalograma
    const lf = rango(Math.log10(FMIN), Math.log10(FMAX), NE), fr = lf.map(v => Math.pow(10, v));
    const l = parseInt(L.value), R = 4, Nf = Math.max(1024, l), st = stft_pot(x, ventana("Hann", l), R, Nf);
    let ms = 0; for (const f of st.S) for (const v of f) ms = Math.max(ms, v);
    const img = fr.map(f => { const k = Math.round(f * Nf / fs); return st.S.map(c => 10 * Math.log10(Math.max(c[k] / ms, 1e-12))); });
    const dlf = lf[1] - lf[0];
    Es.data = {img: [matriz(img)], x: [(l / 2 - R / 2) / fs], y: [lf[0] - dlf / 2], dw: [st.S.length * R / fs], dh: [NE * dlf]};
    // Escalograma: escala a = frecuencia de la wavelet / f
    const esc = fr.map(f => wavelet_frec(wav.value, 1) / f), W = cwt_pot(x, 1 / fs, esc, wav.value);
    let mw = 0; for (const f of W) for (const v of f) mw = Math.max(mw, v);
    Ec.data = {img: [matriz(W.map(f => f.map(v => 10 * Math.log10(Math.max(v / mw, 1e-12)))))], x: [-0.5 / fs], y: [lf[0] - dlf / 2], dw: [DUR], dh: [NE * dlf]};
    const cols = [pb_AZUL, pb_VERDE, pb_ROJO];
    Wv.data = {xs: [10, 40, 160].map(f => { const a = wavelet_frec(wav.value, 1) / f; return rango(-4 * a, 4 * a, 300); }),
               ys: [10, 40, 160].map(f => { const a = wavelet_frec(wav.value, 1) / f; return rango(-4 * a, 4 * a, 300).map(v => wavelet(wav.value, v / a)[0]); }),
               color: cols};
    const sa = f => wavelet_frec(wav.value, 1) / f;
    info.text = `<p>STFT: ventana de ${(1000 * l / fs).toFixed(0)} ms en todas las frecuencias; separa tonos a unos ${(2 * fs / l).toFixed(0)} Hz</p>` +
        `<p>Wavelet: duración proporcional a la escala a. A 10 Hz, a = ${(1000 * sa(10)).toFixed(1)} ms; a 160 Hz, a = ${(1000 * sa(160)).toFixed(2)} ms</p>` +
        (wav.value === "Morlet" ? `<p>Morlet: σ<sub>t</sub> = a y σ<sub>ω</sub> = 1/a. La resolución relativa en frecuencia, Δf/f, es la misma en todas las escalas</p>` :
         `<p>El sombrero mexicano es real y oscila poco: localiza muy bien en el tiempo y peor en frecuencia</p>`);
""", X=X, Es=Es, Ec=Ec, Wv=Wv, senal=senal, wav=wav, L=L, info=info, FS=FS, DUR=DUR, NE=NE, FMIN=FMIN, FMAX=FMAX,
   pb_AZUL=pb.AZUL, pb_VERDE=pb.VERDE, pb_ROJO=pb.ROJO)
pb.conectar(cb, senal, wav, L)

pb.pagina(__file__, "Escalograma frente a espectrograma", tema=5,
          descripcion="La STFT analiza todas las frecuencias con la misma ventana. La transformada wavelet continua "
                      "correla la señal con versiones escaladas de una wavelet: larga para las frecuencias bajas, corta para "
                      "las altas. En el escalograma, los clics se estrechan al subir la frecuencia y los tonos graves se "
                      "resuelven mejor que los agudos. El eje de frecuencias es logarítmico en las dos gráficas.",
          controles=[senal, wav, L, info], graficas=[[p1], [p2, p4], [p3]], inicio=cb,
          referencia="Transparencias T5-02, escala y desplazamiento y escalograma frente a espectrograma · Apuntes del Tema 5, sección 2")
