"""T5 · Eliminación de ruido y compresión con umbral sobre la DWT."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

NX = 1024

X = ColumnDataSource(dict(n=[], s=[], x=[], y=[], m=[]))
Cf = ColumnDataSource(dict(k=[], c=[], color=[]))
Um = ColumnDataSource(dict(x=[], y=[]))
Rg = ColumnDataSource(dict(d=[], h=[]))

p1 = pb.figura("Señal con ruido, señal limpia y resultado", "n", "", ancho=620, alto=240, x_range=(0, NX))
p1.line("n", "x", source=X, color=pb.GRIS_CLARO, line_width=1, legend_label="con ruido")
r_m = p1.line("n", "m", source=X, color=pb.VERDE, line_width=1.3, legend_label="media móvil de 9")
p1.line("n", "s", source=X, color=pb.ROJO, line_width=1, line_dash="dashed", legend_label="sin ruido")
p1.line("n", "y", source=X, color=pb.AZUL, line_width=1.8, legend_label="umbral sobre la DWT")
pb.leyenda(p1, "below")
p2 = pb.figura("Coeficientes a_J | d_J | … | d₁ y umbral ±u", "índice", "", ancho=420, alto=220, x_range=(0, NX))
p2.segment(x0="k", y0=0, x1="k", y1="c", source=Cf, color="color", line_width=1)
p2.multi_line("x", "y", source=Um, color=pb.ROJO, line_dash="dashed", line_width=1.5)
p3 = pb.figura("Regla del umbral", "d", "d̂", ancho=180, alto=180, x_range=(-3, 3), y_range=(-3, 3))
p3.line("d", "d", source=Rg, color=pb.GRIS_CLARO, line_dash="dotted")
p3.line("d", "h", source=Rg, color=pb.AZUL, line_width=2)

senal = pb.selector("Señal", ["Bloques", "Escalones", "Doppler", "HeaviSine"])
modo = pb.botones(["Eliminar ruido", "Comprimir"])
wav = pb.selector("Wavelet", ["Haar", "db2", "db4"])
J = pb.deslizador("Niveles J", 1, 7, 5, 1)
sigma = pb.deslizador("Desviación típica del ruido σ", 0, 1.5, 0.5, 0.05)
semilla = pb.deslizador("Realización del ruido", 1, 20, 1, 1)
regla = pb.botones(["Umbral duro", "Umbral suave"])
fac = pb.deslizador("u / u_universal", 0, 3, 1, 0.05)
pct = pb.deslizador("Coeficientes que se guardan (%) al comprimir", 0.5, 50, 5, 0.5)
mm = pb.casillas(["Comparar con una media móvil de 9 muestras"], activas=[0])
info = Div(text="", width=250)

cb = pb.js("""
    const N = NX, n = enteros(0, N - 1), t = n.map(k => k / N), g = generador(semilla.value);
    let s;
    if (senal.value === "Bloques") {
        const tj = [0.1, 0.13, 0.15, 0.23, 0.25, 0.4, 0.44, 0.65, 0.76, 0.78, 0.81], hj = [4, -5, 3, -4, 5, -4.2, 2.1, 4.3, -3.1, 2.1, -4.2];
        s = t.map(v => tj.reduce((a, tk, i) => a + hj[i] * (v >= tk ? 1 : 0), 0) / 2);
    } else if (senal.value === "Escalones") s = n.map(k => (k < 256 ? 1 : k < 440 ? 3 : k < 600 ? 2 : k < 760 ? 2.5 : 1.5));
    else if (senal.value === "Doppler") s = t.map(v => 4 * Math.sqrt(v * (1 - v)) * Math.sin(2 * PI * 1.05 / (v + 0.05)));
    else s = t.map(v => (4 * Math.sin(4 * PI * v) - Math.sign(v - 0.3) - Math.sign(0.72 - v)) / 2);
    const x = s.map(v => v + sigma.value * gauss(g)), j = J.value, c = dwt_dec(x, wav.value, j), duro = regla.active === 0;
    // σ̂ con la mediana de |d₁| y umbral universal u = σ̂√(2 ln N)
    const ad1 = c.d[0].map(Math.abs).sort((a, b) => a - b), sig = ad1[ad1.length >> 1] / 0.6745, uu = sig * Math.sqrt(2 * Math.log(N));
    let u, comprimir = modo.active === 1, cuenta = 0;
    const todos = c.a.concat(...c.d).map(Math.abs).sort((a, b) => b - a);
    if (comprimir) u = todos[Math.max(0, Math.round(pct.value / 100 * N) - 1)];
    else u = fac.value * uu;
    const umbral = d => { const a = Math.abs(d); if (a <= u) return 0; cuenta++; return duro || comprimir ? d : Math.sign(d) * (a - u); };
    // Al eliminar ruido solo se tocan los detalles; al comprimir, todos los coeficientes
    const ch = {a: comprimir ? c.a.map(umbral) : c.a.slice(), d: c.d.map(d => d.map(umbral))};
    if (!comprimir) cuenta += c.a.length;
    const y = dwt_rec(ch, wav.value);
    const m = n.map(k => { let a = 0, q = 0; for (let i = -4; i <= 4; i++) if (k + i >= 0 && k + i < N) { a += x[k + i]; q++; } return a / q; });
    X.data = {n: n, s: s, x: x, y: y, m: m}; r_m.visible = mm.active.length > 0;
    const cols = [pb_AZUL, pb_ROJO, pb_VERDE, pb_NARANJA, pb_GRIS, "#7B4FA0", "#2A9DB0", pb_AZUL];
    const bloques = [[c.a, 0]].concat(enteros(1, j).reverse().map(i => [c.d[i - 1], i]));
    const kk = [], cc = [], co = []; let pos = 0;
    for (const [v, i] of bloques) v.forEach(z => { kk.push(pos++); cc.push(z); co.push(cols[i]); });
    Cf.data = {k: kk, c: cc, color: co};
    const desde = comprimir ? 0 : c.a.length;
    Um.data = {x: [[desde, N], [desde, N]], y: [[u, u], [-u, -u]]};
    const dd = rango(-3, 3, 241), uv = Math.min(u, 2.5);
    Rg.data = {d: dd, h: dd.map(v => Math.abs(v) <= uv ? 0 : duro || comprimir ? v : Math.sign(v) * (Math.abs(v) - uv))};
    const ecm = z => z.reduce((a, v, i) => a + (v - s[i]) ** 2, 0) / N, Ps = s.reduce((a, v) => a + v * v, 0) / N;
    const snr = e => e > 0 ? 10 * Math.log10(Ps / e) : Infinity;
    const e0 = ecm(x), e1 = ecm(y), e2 = ecm(m);
    info.text = `<p>σ̂ = mediana|d₁|/0,6745 = ${sig.toFixed(3)}; u<sub>universal</sub> = σ̂√(2 ln N) = ${uu.toFixed(3)}</p>` +
        `<p>Umbral aplicado: u = ${u.toFixed(3)}</p>` +
        `<p>Coeficientes no nulos: ${cuenta} de ${N} (${(100 * cuenta / N).toFixed(1)} %)</p>` +
        `<p>ECM con ruido: ${e0.toFixed(4)} (SNR ${snr(e0).toFixed(1)} dB)</p>` +
        `<p>ECM tras el umbral: ${e1.toFixed(4)} (SNR ${snr(e1).toFixed(1)} dB)</p>` +
        `<p>ECM con la media móvil: ${e2.toFixed(4)} (SNR ${snr(e2).toFixed(1)} dB)</p>`;
""", X=X, Cf=Cf, Um=Um, Rg=Rg, r_m=r_m, senal=senal, modo=modo, wav=wav, J=J, sigma=sigma, semilla=semilla,
   regla=regla, fac=fac, pct=pct, mm=mm, info=info, NX=NX,
   pb_AZUL=pb.AZUL, pb_ROJO=pb.ROJO, pb_VERDE=pb.VERDE, pb_NARANJA=pb.NARANJA, pb_GRIS=pb.GRIS)
pb.conectar(cb, senal, modo, wav, J, sigma, semilla, regla, fac, pct, mm)

pb.pagina(__file__, "Eliminación de ruido y compresión con wavelets", tema=5,
          descripcion="Una señal con pocas discontinuidades concentra su energía en pocos coeficientes grandes de la DWT, "
                      "mientras que el ruido blanco la reparte por igual entre todos. Anular los detalles menores que un "
                      "umbral u y reconstruir quita gran parte del ruido sin suavizar los saltos. Guardar solo los coeficientes "
                      "mayores comprime la señal.",
          controles=[senal, modo, wav, J, sigma, semilla, regla, fac, pct, mm, info],
          graficas=[p1, [p2, p3]], inicio=cb,
          referencia="Transparencias T5-02, eliminación de ruido y compresión · Apuntes del Tema 5, sección 2")
