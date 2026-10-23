"""T5 · Marcación por tonos (DTMF): espectro de una tecla, detección y espectrograma de un número."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.layouts import column, row
from bokeh.models import Button, ColumnDataSource, CustomJS, Div, TextInput
import pds_bokeh as pb

FS = 8000
FILAS = [697, 770, 852, 941]
COLS = [1209, 1336, 1477]
TECLAS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "0", "#"]

Tk = ColumnDataSource(dict(t=["5"]))
X = ColumnDataSource(dict(t=[], x=[]))
Sp = ColumnDataSource(dict(f=[], s=[]))
Mk = ColumnDataSource(dict(f=[], y=[], color=[]))
Gz = ColumnDataSource(dict(f=[], g=[], color=[]))
E = ColumnDataSource(dict(img=[], x=[], y=[], dw=[], dh=[]))
Et = ColumnDataSource(dict(x=[], y=[], t=[]))

p1 = pb.figura("Señal de la tecla (primeros 30 ms)", "t (ms)", "", ancho=330, alto=170, x_range=(0, 30))
p1.line("t", "x", source=X, color=pb.AZUL, line_width=1.2)
p2 = pb.figura("Espectro del tramo analizado (L muestras, Hann)", "f (Hz)", "dB", ancho=420, alto=230,
               x_range=(500, 1700), y_range=(-60, 3))
p2.line("f", "s", source=Sp, color=pb.AZUL, line_width=1.6)
p2.scatter("f", "y", source=Mk, color="color", marker="inverted_triangle", size=11)
p3 = pb.figura("Algoritmo de Goertzel: las 7 frecuencias", "f (Hz)", "|X| relativo", ancho=330, alto=230,
               x_range=(600, 1550))
p3.vbar(x="f", top="g", width=25, source=Gz, fill_color="color", line_color=None)
p4 = pb.figura("Espectrograma del número marcado", "t (s)", "f (Hz)", ancho=760, alto=230, y_range=(500, 1700))
pb.imagen(p4, E, x="x", y="y", dw="dw", dh="dh", paleta="viridis", bajo=-50, alto=0)
p4.text("x", "y", "t", source=Et, text_color="white", text_font_size="14px", text_align="center", text_font_style="bold")

dur = pb.deslizador("Duración de cada tono (ms)", 20, 200, 80, 5)
sr = pb.deslizador("Desviación típica del ruido", 0, 2, 0.5, 0.05)
L = pb.selector("L (muestras analizadas)", ["64", "128", "256", "512"], "256")
numero = TextInput(title="Número que se marca", value="2025", width=240)
oir = pb.boton("Oír la tecla")
oir_n = pb.boton("Oír el número")
info = Div(text="", width=250)

cb = pb.js("""
    const fs = FS, tecla = Tk.data.t[0], Ld = parseInt(L.value), g = generador(4);
    const fila = k => Math.floor("123456789*0#".indexOf(k) / 3), col = k => "123456789*0#".indexOf(k) % 3;
    const tono = (k, n0, M) => enteros(0, M - 1).map(n => { const t = (n0 + n) / fs; return Math.sin(2 * PI * FILAS[fila(k)] * t) + Math.sin(2 * PI * COLS[col(k)] * t); });
    const M = Math.round(dur.value / 1000 * fs), x = tono(tecla, 0, M).map(v => v + sr.value * gauss(g));
    X.data = {t: enteros(0, Math.min(M, 240) - 1).map(n => 1000 * n / fs), x: x.slice(0, 240)};
    // Espectro de las primeras L muestras (o de todas si el tono es más corto)
    const l = Math.min(Ld, M), w = ventana("Hann", l), P = 4096, re = new Array(P).fill(0);
    for (let n = 0; n < l; n++) re[n] = x[n] * w[n];
    const [a, b] = fft(re), K = P / 2 + 1, m = enteros(0, K - 1).map(k => Math.hypot(a[k], b[k])), mm = maximo(m);
    Sp.data = {f: enteros(0, K - 1).map(k => k * fs / P), s: m.map(v => db(v / mm, -100))};
    // Goertzel: |X(e^{jΩ})| en cada frecuencia del estándar con las mismas l muestras
    const goe = f => { const c = 2 * Math.cos(2 * PI * f / fs); let s1 = 0, s2 = 0; for (let n = 0; n < l; n++) { const s0 = x[n] * w[n] + c * s1 - s2; s2 = s1; s1 = s0; } return Math.sqrt(s1 * s1 + s2 * s2 - c * s1 * s2); };
    const gf = FILAS.map(goe), gc = COLS.map(goe), gm = Math.max(...gf, ...gc);
    const iF = gf.indexOf(Math.max(...gf)), iC = gc.indexOf(Math.max(...gc)), det = "123456789*0#"[3 * iF + iC];
    Gz.data = {f: FILAS.concat(COLS), g: gf.concat(gc).map(v => v / gm), color: FILAS.map((_, i) => i === iF ? pb_ROJO : pb_GRIS_CLARO).concat(COLS.map((_, i) => i === iC ? pb_ROJO : pb_GRIS_CLARO))};
    Mk.data = {f: [FILAS[fila(tecla)], COLS[col(tecla)]], y: [2, 2], color: [pb_ROJO, pb_ROJO]};
    // Número completo: tonos de la duración elegida separados por 50 ms de silencio
    const dig = numero.value.split("").filter(c => "123456789*0#".includes(c)).slice(0, 12), hueco = Math.round(0.05 * fs);
    let sx = []; const pos = [];
    dig.forEach(k => { pos.push((sx.length + M / 2) / fs); sx = sx.concat(tono(k, sx.length, M), new Array(hueco).fill(0)); });
    sx = sx.map(v => v + sr.value * gauss(g));
    window.__pds_dtmf = {tecla: x, numero: sx};
    if (sx.length > 256) {
        const st = stft_pot(sx, ventana("Hann", Ld), Math.max(8, Ld / 4), Math.max(512, Ld)), Nf = Math.max(512, Ld), Kk = Nf / 2 + 1;
        let mx = 0; for (const f of st.S) for (const v of f) mx = Math.max(mx, v);
        const img = enteros(0, Kk - 1).map(k => st.S.map(f => 10 * Math.log10(Math.max(f[k] / mx, 1e-12))));
        const R = Math.max(8, Ld / 4);
        E.data = {img: [matriz(img)], x: [(Ld / 2 - R / 2) / fs], y: [-fs / (2 * Nf)], dw: [st.S.length * R / fs], dh: [fs / 2 + fs / Nf]};
        Et.data = {x: pos, y: pos.map(() => 1600), t: dig};
        p4.x_range.start = 0; p4.x_range.end = sx.length / fs;
    }
    info.text = `<p>Tecla ${tecla}: ${FILAS[fila(tecla)]} + ${COLS[col(tecla)]} Hz</p>` +
        `<p>Detectada: <b style="color:${det === tecla ? "#1E7B4F" : "#C0392B"}">${det}</b></p>` +
        `<p>Se analizan ${l} muestras (${(1000 * l / fs).toFixed(0)} ms). Para separar 697 y 770 Hz con Hann hacen falta unas ` +
        `2f<sub>s</sub>/73 ≈ 220 muestras</p><p>Resolución 2f<sub>s</sub>/L = ${(2 * fs / l).toFixed(0)} Hz</p>`;
""", Tk=Tk, X=X, Sp=Sp, Mk=Mk, Gz=Gz, E=E, Et=Et, p4=p4, dur=dur, sr=sr, L=L, numero=numero, info=info, FS=FS,
   FILAS=FILAS, COLS=COLS, pb_ROJO=pb.ROJO, pb_GRIS_CLARO=pb.GRIS_CLARO)
pb.conectar(cb, dur, sr, L, numero)

teclado = []
for t in TECLAS:
    b = Button(label=t, width=74, height=40)
    b.js_on_event("button_click", CustomJS(args=dict(Tk=Tk, cb=cb, t=t), code="Tk.data = {t: [t]}; cb.execute();"))
    teclado.append(b)
oir.js_on_event("button_click", pb.js("if (window.__pds_dtmf) sonar(window.__pds_dtmf.tecla, FS);", FS=FS))
oir_n.js_on_event("button_click", pb.js("if (window.__pds_dtmf) sonar(window.__pds_dtmf.numero, FS);", FS=FS))
panel = column(Div(text="Pulsa una tecla:"), *[row(*teclado[3 * i:3 * i + 3]) for i in range(4)])

pb.pagina(__file__, "Marcación por tonos (DTMF)", tema=5,
          descripcion="Cada tecla del teléfono suma una sinusoide de fila (697, 770, 852 o 941 Hz) y una de columna (1209, "
                      "1336 o 1477 Hz). El receptor busca la más fuerte de cada grupo. Con pocas muestras el lóbulo principal es "
                      "ancho y las frecuencias de fila próximas se confunden; con ruido, hace falta más duración. Puedes oír "
                      "la tecla y el número.",
          controles=[panel, oir, numero, oir_n, dur, sr, L, info], graficas=[[p1, p3], p2, p4], inicio=cb,
          referencia="Transparencias T5-01, ejemplo DTMF y reconocer una tecla · Apuntes del Tema 5, sección 1")
