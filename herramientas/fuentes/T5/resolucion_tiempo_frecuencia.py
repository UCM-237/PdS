"""T5 · Compromiso entre resolución en tiempo y en frecuencia de la STFT."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

FS, DUR, F1, TC = 4000, 1.0, 1000, 0.7

E = ColumnDataSource(dict(img=[], x=[], y=[], dw=[], dh=[]))
Cf = ColumnDataSource(dict(f=[], s=[]))
Ct = ColumnDataSource(dict(t=[], s=[]))
Wv = ColumnDataSource(dict(t=[], w=[]))
Wf = ColumnDataSource(dict(f=[], W=[]))
Mf = ColumnDataSource(dict(x=[]))
Mt = ColumnDataSource(dict(x=[]))

p1 = pb.figura("Espectrograma: dos tonos y después dos clics", "t (s)", "f (Hz)", ancho=470, alto=250,
               x_range=(0, DUR), y_range=(600, 1600))
pb.imagen(p1, E, x="x", y="y", dw="dw", dh="dh", paleta="viridis", bajo=-60, alto=0)
p2 = pb.figura("Espectro medio con los dos tonos", "f (Hz)", "dB", ancho=300, alto=250,
               x_range=(850, 1350), y_range=(-50, 3))
p2.line("f", "s", source=Cf, color=pb.AZUL, line_width=1.8)
p2.scatter("x", 0, source=Mf, color=pb.ROJO, marker="inverted_triangle", size=10)
p3 = pb.figura("Energía de cada tramo: ¿se separan los clics?", "t (s)", "dB", ancho=470, alto=200,
               x_range=(TC - 0.08, TC + 0.18), y_range=(-50, 3))
p3.line("t", "s", source=Ct, color=pb.VERDE, line_width=1.8)
p3.scatter("x", 0, source=Mt, color=pb.ROJO, marker="inverted_triangle", size=10)
p4 = pb.figura("Ventana w(t) y su espectro |W(f)|", "t (ms)", "", ancho=300, alto=90,
               tools="reset,save")
p4.line("t", "w", source=Wv, color=pb.NARANJA, line_width=2)
p5 = pb.figura("", "f (Hz)", "dB", ancho=300, alto=90, tools="reset,save", y_range=(-80, 3))
p5.line("f", "W", source=Wf, color=pb.NARANJA, line_width=1.5)

tipo = pb.selector("Ventana", ["Hann", "Hamming", "Blackman", "Rectangular", "Gaussiana (σ = L/6)"])
L = pb.deslizador("L (muestras de la ventana)", 16, 1024, 128, 8)
df = pb.deslizador("Separación de los tonos Δf (Hz)", 5, 200, 40, 1)
dt = pb.deslizador("Separación de los clics Δt (ms)", 1, 100, 20, 1)
info = Div(text="", width=250)

cb = pb.js("""
    const fs = FS, Nx = Math.round(DUR * fs), l = L.value, Rr = Math.max(2, Math.round(l / 8)), N = l <= 512 ? 1024 : 2048;
    const f2 = F1 + df.value, t1 = TC, t2 = TC + dt.value / 1000;
    const x = enteros(0, Nx - 1).map(n => { const t = n / fs; return t < 0.45 ? Math.cos(2 * PI * F1 * t) + Math.cos(2 * PI * f2 * t) : 0; });
    x[Math.round(t1 * fs)] += 30; x[Math.round(t2 * fs)] += 30;
    let w;
    if (tipo.value.startsWith("Gauss")) w = enteros(0, l - 1).map(n => Math.exp(-0.5 * ((n - (l - 1) / 2) / (l / 6)) ** 2));
    else w = ventana(tipo.value, l);
    const st = stft_pot(x, w, Rr, N), M = st.S.length, K = N / 2 + 1;
    const tc = st.ini.map(s => (s + l / 2) / fs);
    // Normalización por separado de las dos zonas, para comparar las formas
    const zona = (a, b) => { let m = 0; st.S.forEach((fila, j) => { if (tc[j] >= a && tc[j] < b) for (const v of fila) m = Math.max(m, v); }); return m; };
    const m1 = zona(0, 0.5), m2 = zona(0.5, DUR);
    const img = enteros(0, K - 1).map(k => st.S.map((fila, j) => 10 * Math.log10(Math.max(fila[k] / (tc[j] < 0.5 ? m1 : m2), 1e-12))));
    E.data = {img: [matriz(img)], x: [tc[0] - Rr / (2 * fs)], y: [-fs / (2 * N)], dw: [M * Rr / fs], dh: [fs / 2 + fs / N]};
    // Media de los espectros de los tramos que caen enteros en la zona de los tonos: así no influye
    // la fase relativa de los dos tonos, que cambia de un tramo a otro (batido)
    const fr = enteros(0, K - 1).map(k => k * fs / N), dentro = enteros(0, M - 1).filter(j => st.ini[j] + l <= 0.45 * fs);
    const sf = fr.map((_, k) => media(dentro.map(j => st.S[j][k]))), mf = maximo(sf), sdb = sf.map(v => 10 * Math.log10(Math.max(v / mf, 1e-12)));
    Cf.data = {f: fr, s: sdb}; Mf.data = {x: [F1, f2]};
    // Corte en el tiempo: energía total de cada tramo
    const en = st.S.map(fila => fila.reduce((a, b) => a + b, 0)), sel = enteros(0, M - 1).filter(j => tc[j] > 0.5);
    const me = maximo(sel.map(j => en[j]));
    Ct.data = {t: sel.map(j => tc[j]), s: sel.map(j => 10 * Math.log10(Math.max(en[j] / me, 1e-12)))}; Mt.data = {x: [t1, t2]};
    // ¿Dos máximos separados por un valle de al menos 3 dB?
    const separa = (xs, ys, a, b) => {
        const ia = xs.reduce((m, v, i) => Math.abs(v - a) < Math.abs(xs[m] - a) ? i : m, 0), ib = xs.reduce((m, v, i) => Math.abs(v - b) < Math.abs(xs[m] - b) ? i : m, 0);
        if (ib - ia < 2) return [false, 0];
        const pa = maximo(ys.slice(Math.max(0, ia - 1), ia + 2)), pbk = maximo(ys.slice(ib - 1, ib + 2)), valle = minimo(ys.slice(ia, ib + 1));
        const prof = Math.min(pa, pbk) - valle; return [prof >= 3, prof];
    };
    const [okf, pf] = separa(fr, sdb, F1, f2), [okt, pt] = separa(Ct.data.t, Ct.data.s, t1, t2);
    // Anchuras rms de |w|² y de |W|²
    const sw = w.reduce((a, v) => a + v * v, 0), nb = w.reduce((a, v, n) => a + n * v * v, 0) / sw;
    const st_ = Math.sqrt(w.reduce((a, v, n) => a + (n - nb) ** 2 * v * v, 0) / sw) / fs;
    const P = 16384, re = new Array(P).fill(0); w.forEach((v, n) => re[n] = v); const [Wr, Wi] = fft(re);
    let s0 = 0, s2 = 0; for (let k = 0; k < P; k++) { const Om = 2 * PI * (k < P / 2 ? k : k - P) / P, a = Wr[k] ** 2 + Wi[k] ** 2; s0 += a; s2 += Om * Om * a; }
    const sw_ = Math.sqrt(s2 / s0) * fs;
    Wv.data = {t: enteros(0, l - 1).map(n => 1000 * (n - (l - 1) / 2) / fs), w: w};
    const Wm = enteros(0, P / 2).map(k => Math.hypot(Wr[k], Wi[k])), W0 = Wm[0];
    const lim = Math.min(P / 2, Math.round(8 * P / l));
    Wf.data = {f: enteros(0, lim).map(k => k * fs / P), W: enteros(0, lim).map(k => db(Wm[k] / W0, -120))};
    p5.x_range.start = 0; p5.x_range.end = lim * fs / P;
    const si = v => v ? "<b style='color:#1E7B4F'>sí</b>" : "<b style='color:#C0392B'>no</b>";
    info.text = `<p>Duración de la ventana: ${(1000 * l / fs).toFixed(1)} ms (se mueve R = ${Rr} muestras)</p>` +
        `<p>¿Se separan los tonos (Δf = ${df.value} Hz)? ${si(okf)}, valle de ${pf.toFixed(1)} dB</p>` +
        `<p>¿Se separan los clics (Δt = ${dt.value} ms)? ${si(okt)}, valle de ${pt.toFixed(1)} dB</p>` +
        `<p>Anchuras rms: σ<sub>t</sub> = ${(1000 * st_).toFixed(2)} ms, σ<sub>ω</sub> = ${sw_.toFixed(1)} rad/s</p>` +
        `<p>σ<sub>t</sub>·σ<sub>ω</sub> = ${(st_ * sw_).toFixed(3)} (como mínimo 1/2)</p>`;
""", E=E, Cf=Cf, Ct=Ct, Wv=Wv, Wf=Wf, Mf=Mf, Mt=Mt, p5=p5, tipo=tipo, L=L, df=df, dt=dt, info=info,
   FS=FS, DUR=DUR, F1=F1, TC=TC)
pb.conectar(cb, tipo, L, df, dt)

pb.pagina(__file__, "Resolución en tiempo y en frecuencia", tema=5,
          descripcion="La misma ventana fija lo bien que la STFT separa dos tonos próximos (hace falta una ventana larga, "
                      "Δf ≳ 2f<sub>s</sub>/L con Hann) y dos sucesos próximos en el tiempo (hace falta una ventana más "
                      "corta que su separación). El principio de incertidumbre, σ<sub>t</sub>σ<sub>ω</sub> ≥ 1/2, impide "
                      "conseguir las dos cosas a la vez.",
          controles=[tipo, L, df, dt, info], graficas=[[p1, p2], [p3, pb.column(p4, p5)]], inicio=cb,
          referencia="Transparencias T5-01, el compromiso tiempo-frecuencia y principio de incertidumbre · Apuntes del Tema 5, sección 1")
