"""T5 · STFT y espectrograma, con la reconstrucción por solapamiento y suma."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div, Span
import pds_bokeh as pb

FS, DUR = 4000, 1.5

X = ColumnDataSource(dict(t=[], x=[]))
Wt = ColumnDataSource(dict(t=[], w=[]))
E = ColumnDataSource(dict(img=[], x=[], y=[], dw=[], dh=[]))
T = ColumnDataSource(dict(f=[], s=[]))
Rc = ColumnDataSource(dict(t=[], y=[], cola=[]))

p1 = pb.figura("Señal x(t) y ventana del tramo elegido", "t (s)", "", ancho=560, alto=150, x_range=(0, DUR))
p1.line("t", "x", source=X, color=pb.AZUL, line_width=1)
p1.varea("t", 0, "w", source=Wt, fill_color=pb.NARANJA, fill_alpha=0.35)
p2 = pb.figura("Espectrograma |X[m, k]|² (dB respecto al máximo)", "t (s)", "f (Hz)", ancho=560, alto=260,
               x_range=p1.x_range, y_range=(0, FS / 2))
mapa = pb.imagen(p2, E, x="x", y="y", dw="dw", dh="dh", paleta="viridis", bajo=-60, alto=0, barra=True)
marca = Span(location=0, dimension="height", line_color="white", line_dash="dashed", line_width=1.5)
p2.add_layout(marca)
p3 = pb.figura("Espectro del tramo elegido", "f (Hz)", "dB", ancho=300, alto=260, x_range=(0, FS / 2), y_range=(-80, 3))
p3.line("f", "s", source=T, color=pb.NARANJA, line_width=1.5)
p4 = pb.figura("Reconstrucción por solapamiento y suma", "t (s)", "", ancho=560, alto=150, x_range=p1.x_range)
p4.line("t", "y", source=Rc, color=pb.ROJO, line_width=1, legend_label="y[n]/C (ISTFT)")
p4.line("t", "cola", source=Rc, color=pb.GRIS, line_width=2, line_dash="dashed", legend_label="Σ w[n − mR] / C")
pb.leyenda(p4, "below")

senal = pb.selector("Señal", ["Chirp, tono y clic", "Dos tonos sucesivos", "Voz sintética"])
tipo = pb.selector("Ventana (periódica)", ["Hann", "Hamming", "Blackman", "Rectangular"])
L = pb.selector("L (muestras de la ventana)", ["32", "64", "128", "256", "512"], "128")
sol = pb.selector("Solapamiento L − R", ["0 %", "25 %", "50 %", "75 %"], "75 %")
Nf = pb.selector("N (puntos de la DFT)", ["L", "2L", "4L"])
tm = pb.deslizador("Instante del tramo t (s)", 0, DUR, 0.5, 0.005)
info = Div(text="", width=250)

cb = pb.js("""
    const fs = FS, Nx = Math.round(DUR * fs), t = enteros(0, Nx - 1).map(n => n / fs);
    let x;
    if (senal.value.startsWith("Chirp")) {
        // Chirp de 100 a 1500 Hz, tono de 1200 Hz entre 0,4 y 0,8 s y clic en 1,1 s
        x = t.map(v => Math.cos(2 * PI * (100 * v + 1400 / (2 * DUR) * v * v)) + (v >= 0.4 && v < 0.8 ? 0.7 * Math.cos(2 * PI * 1200 * v) : 0));
        x[Math.round(1.1 * fs)] += 8;
    } else if (senal.value.startsWith("Dos")) {
        x = t.map(v => v < DUR / 2 ? Math.cos(2 * PI * 500 * v) : Math.cos(2 * PI * 1200 * v));
    } else {
        // Tren de pulsos glotales (de 110 a 150 Hz) a través de dos resonadores en cascada, cuyos
        // formantes van de los de /a/ (700 y 1100 Hz) a los de /i/ (300 y 1800 Hz)
        x = new Array(Nx).fill(0); let fase = 0;
        const s1 = [0, 0], s2 = [0, 0];
        const reson = (s, F, B, u) => { const r = Math.exp(-PI * B / fs), c = 2 * r * Math.cos(2 * PI * F / fs), y = u + c * s[0] - r * r * s[1];
                                        s[1] = s[0]; s[0] = y; return y; };
        for (let n = 0; n < Nx; n++) {
            fase += (110 + 40 * n / Nx) / fs; let e = 0; if (fase >= 1) { fase -= 1; e = 1; }
            x[n] = reson(s2, 1100 + 700 * n / Nx, 120, reson(s1, 700 - 400 * n / Nx, 90, e));
        }
    }
    const l = parseInt(L.value), Rr = Math.max(1, Math.round(l * (1 - parseInt(sol.value) / 100)));
    const N = l * (Nf.value === "L" ? 1 : Nf.value === "2L" ? 2 : 4);
    const w = ventana(tipo.value, l + 1).slice(0, l);
    const st = stft_pot(x, w, Rr, N), M = st.S.length;
    let mx = 0; for (const fila of st.S) for (const v of fila) mx = Math.max(mx, v);
    const K = N / 2 + 1, img = enteros(0, K - 1).map(k => st.S.map(fila => 10 * Math.log10(Math.max(fila[k] / mx, 1e-12))));
    E.data = {img: [matriz(img)], x: [(st.ini[0] + l / 2 - Rr / 2) / fs], y: [-fs / (2 * N)], dw: [M * Rr / fs], dh: [fs / 2 + fs / N]};
    X.data = {t: t, x: x};
    // Tramo más próximo al instante elegido (centrado en t_m = (mR + L/2)/fs)
    const m = Math.min(M - 1, Math.max(0, Math.round((tm.value * fs - l / 2) / Rr))), ini = st.ini[m];
    const amp = x.map(Math.abs).sort((a, b) => a - b)[Math.floor(0.99 * Nx)];
    Wt.data = {t: enteros(0, l - 1).map(r => (ini + r) / fs), w: w.map(v => v * amp)};
    marca.location = (ini + l / 2) / fs;
    T.data = {f: enteros(0, K - 1).map(k => k * fs / N), s: st.S[m].map(v => 10 * Math.log10(Math.max(v / mx, 1e-12)))};
    // ISTFT: IDFT de cada tramo (sin modificar) y suma desplazada; C es la suma de las ventanas en régimen
    const y = new Array(Nx).fill(0), cola = new Array(Nx).fill(0);
    for (let j = 0; j < M; j++) {
        const s = st.ini[j], re = new Array(N).fill(0); for (let r = 0; r < l; r++) re[r] = x[s + r] * w[r];
        const [a, b] = fft(re), [yr] = ifft(a, b);
        for (let r = 0; r < l; r++) { y[s + r] += yr[r]; cola[s + r] += w[r]; }
    }
    const mid = cola.slice(l, Nx - 2 * l), C = media(mid), riz = (maximo(mid) - minimo(mid)) / C;
    let err = 0; for (let n = l; n < Nx - 2 * l; n++) err = Math.max(err, Math.abs(y[n] / C - x[n]));
    Rc.data = {t: t, y: y.map(v => v / C), cola: cola.map(v => v / C)};
    info.text = `<p>R = ${Rr} muestras (${(1000 * Rr / fs).toFixed(1)} ms); ${M} tramos de ${(1000 * l / fs).toFixed(0)} ms</p>` +
        `<p>Resolución en frecuencia: f<sub>s</sub>/N = ${(fs / N).toFixed(1)} Hz entre muestras; lóbulo principal de ` +
        `${(fs / l * (tipo.value === "Rectangular" ? 2 : tipo.value === "Blackman" ? 6 : 4)).toFixed(0)} Hz entre ceros</p>` +
        `<p>Tramo elegido: m = ${m}, centrado en ${((ini + l / 2) / fs).toFixed(3)} s</p>` +
        `<p>Suma de las ventanas: C = ${C.toFixed(3)}, rizado ${(100 * riz).toFixed(1)} % ` +
        (riz < 1e-6 ? "(cumple COLA)" : "(no cumple COLA)") + `</p><p>Error de la reconstrucción y/C − x: ${err.toExponential(1)}</p>`;
""", X=X, Wt=Wt, E=E, T=T, Rc=Rc, marca=marca, senal=senal, tipo=tipo, L=L, sol=sol, Nf=Nf, tm=tm, info=info,
   FS=FS, DUR=DUR)
pb.conectar(cb, senal, tipo, L, sol, Nf, tm)

pb.pagina(__file__, "STFT y espectrograma", tema=5,
          descripcion="La STFT calcula la DFT de tramos sucesivos de la señal, enventanados con w[n] de L muestras que "
                      "avanzan R muestras. El espectrograma, |X[m, k]|² en dB, muestra cómo cambia el espectro con el tiempo. "
                      "Si las ventanas desplazadas suman una constante (condición COLA), la señal se recupera sumando las "
                      "IDFT de los tramos (solapamiento y suma).",
          controles=[senal, tipo, L, sol, Nf, tm, info], graficas=[p1, [p2, p3], p4], inicio=cb,
          referencia="Transparencias T5-01, parámetros, espectrograma y solapamiento y suma · Apuntes del Tema 5, sección 1")
