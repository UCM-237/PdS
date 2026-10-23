"""T6 · Estimación de la autocorrelación: estimadores sesgado e insesgado."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

X = ColumnDataSource(dict(n=[], x=[]))
A = ColumnDataSource(dict(l=[], s=[], i=[], t=[]))

p1 = pb.figura("Una realización x[n]", "n", "", ancho=620, alto=170)
p1.line("n", "x", source=X, color=pb.AZUL, line_width=1)
p2 = pb.figura("Autocorrelación estimada y teórica", "l", "φ_xx[l]", ancho=620, alto=280)
r_i = p2.line("l", "i", source=A, color=pb.NARANJA, line_width=1.3, legend_label="insesgado: ÷(N − |l|)")
r_s = p2.line("l", "s", source=A, color=pb.AZUL, line_width=1.8, legend_label="sesgado: ÷N")
p2.line("l", "t", source=A, color=pb.ROJO, line_width=2, line_dash="dashed", legend_label="teórica")
pb.leyenda(p2, "below")

proc = pb.selector("Señal", ["Ruido i.i.d. N(5, 1)", "Ruido i.i.d. U[2, 6]", "AR(1)", "Sinusoide de fase aleatoria + ruido",
                             "Ruido blanco N(0, 1)"], width=250)
a = pb.deslizador("a del AR(1)", -0.95, 0.95, 0.9, 0.05)
N = pb.deslizador("N (muestras de la realización)", 32, 4096, 512, 32)
Lm = pb.deslizador("Separación máxima que se dibuja (% de N)", 5, 100, 100, 5)
est = pb.botones(["Los dos", "Sesgado", "Insesgado"])
semilla = pb.deslizador("Realización", 1, 50, 1, 1)
info = Div(text="", width=250)

cb = pb.js("""
    const g = generador(semilla.value), Nn = N.value, pr = proc.value, aa = a.value, n = enteros(0, Nn - 1);
    let x, teo;
    if (pr.includes("N(5")) { x = n.map(() => 5 + gauss(g)); teo = l => l ? 25 : 26; }
    else if (pr.includes("U[2")) { x = n.map(() => 2 + 4 * g()); teo = l => l ? 16 : 52 / 3; }
    else if (pr.startsWith("AR")) { let s = gauss(g) / Math.sqrt(1 - aa * aa); x = n.map(() => { const v = s; s = aa * s + gauss(g); return v; }); teo = l => Math.pow(aa, Math.abs(l)) / (1 - aa * aa); }
    else if (pr.startsWith("Sinusoide")) { const th = 2 * PI * g(); x = n.map(k => Math.sqrt(2) * Math.cos(0.15 * k + th) + 0.5 * gauss(g)); teo = l => Math.cos(0.15 * l) + (l ? 0 : 0.25); }
    else { x = n.map(() => gauss(g)); teo = l => (l ? 0 : 1); }
    X.data = {n: n, x: x};
    const Lmax = Math.max(1, Math.min(Nn - 1, Math.round(Lm.value / 100 * (Nn - 1)))), ls = enteros(-Lmax, Lmax);
    // Σ x[n + |l|] x[n] calculado con la FFT (relleno con ceros para que sea lineal)
    const P = pot2(2 * Nn), re = new Array(P).fill(0); x.forEach((v, i) => re[i] = v);
    const [Xr, Xi] = fft(re), [c] = ifft(Xr.map((v, k) => v * v + Xi[k] * Xi[k]));
    const s = ls.map(l => c[Math.abs(l)] / Nn), i = ls.map(l => c[Math.abs(l)] / (Nn - Math.abs(l)));
    A.data = {l: ls, s: s, i: i, t: ls.map(teo)};
    r_s.visible = est.active !== 2; r_i.visible = est.active !== 1;
    const k0 = Lmax, at = l => [s[k0 + l], i[k0 + l]];
    const lej = Math.min(Lmax, Math.round(0.9 * (Nn - 1)));
    info.text = `<p>φ̂[0] = ${s[k0].toFixed(3)} (teórico ${teo(0).toFixed(3)}): la potencia media</p>` +
        (Lmax >= 5 ? `<p>En l = 5: sesgado ${at(5)[0].toFixed(3)}, insesgado ${at(5)[1].toFixed(3)} (teórico ${teo(5).toFixed(3)})</p>` : "") +
        `<p>En l = ${lej} (solo ${Nn - lej} productos): sesgado ${at(lej)[0].toFixed(3)}, insesgado ${at(lej)[1].toFixed(3)} ` +
        `(teórico ${teo(lej).toFixed(3)})</p>` +
        `<p>Media de la realización: ${media(x).toFixed(3)}; varianza ${varianza(x).toFixed(3)}</p>`;
""", X=X, A=A, r_s=r_s, r_i=r_i, proc=proc, a=a, N=N, Lm=Lm, est=est, semilla=semilla, info=info)
pb.conectar(cb, proc, a, N, Lm, est, semilla)

pb.pagina(__file__, "Estimación de la autocorrelación", tema=6,
          descripcion="Si la señal es ergódica, φ<sub>xx</sub>[l] se estima con una sola realización de N muestras, "
                      "promediando los N − |l| productos x[n + |l|]x[n]. Dividir por N − |l| da el estimador insesgado, que es "
                      "muy ruidoso para |l| cercano a N; dividir por N, el sesgado, que se amortigua hacia los extremos y tiene "
                      "menos varianza.",
          controles=[proc, a, N, Lm, est, semilla, info], graficas=[p1, p2], inicio=cb,
          referencia="Transparencias T6-03, estimar la autocorrelación y AR(1) · Apuntes del Tema 6, sección 3")
