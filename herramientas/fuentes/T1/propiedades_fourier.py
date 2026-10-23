"""T1 · Propiedades de la transformada de Fourier: tiempo y frecuencia a la vez."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div
import pds_bokeh as pb

T = ColumnDataSource(dict(t=[], x=[], y=[]))
F = ColumnDataSource(dict(f=[], X=[], Y=[], pX=[], pY=[]))

p1 = pb.figura("Tiempo: x(t) y y(t)", "t (s)", "", ancho=720, alto=200, x_range=(-6, 6))
p1.line("t", "x", source=T, color=pb.GRIS_CLARO, line_width=2, legend_label="x(t)")
p1.line("t", "y", source=T, color=pb.AZUL, line_width=2, legend_label="y(t)")
pb.leyenda(p1, "right")
p2 = pb.figura("Módulo |X(f)| y |Y(f)|", "f (Hz)", "", ancho=330, alto=200, x_range=(-4, 4))
p2.line("f", "X", source=F, color=pb.GRIS_CLARO, line_width=2)
p2.line("f", "Y", source=F, color=pb.AZUL, line_width=2)
p3 = pb.figura("Fase ∠X(f) y ∠Y(f) (rad)", "f (Hz)", "", ancho=330, alto=200, x_range=(-4, 4), y_range=(-3.4, 3.4))
p3.line("f", "pX", source=F, color=pb.GRIS_CLARO, line_width=2)
p3.line("f", "pY", source=F, color=pb.ROJO, line_width=2)

senal = pb.selector("Señal x(t)", ["Pulso rectangular (ancho 1)", "Pulso triangular (ancho 2)", "Gaussiana", "Exponencial e^(−t)u(t)"])
op = pb.selector("Operación", ["Ninguna", "Desplazamiento x(t − t₀)", "Escalado x(at)", "Modulación x(t)·cos(2πf₀t)",
                               "Derivada dx/dt", "Convolución x(t) ∗ x(t)"], "Desplazamiento x(t − t₀)")
t0 = pb.deslizador("t₀ (s)", -3, 3, 1, 0.05)
a = pb.deslizador("a (escalado)", 0.25, 4, 2, 0.05)
f0 = pb.deslizador("f₀ (Hz)", 0, 3, 1.5, 0.05)
info = Div(text="", width=240)

cb = pb.js("""
    const N = 4096, dt = 0.02, tmin = -N / 2 * dt, t = enteros(0, N - 1).map(n => tmin + n * dt);
    const base = u => senal.value.startsWith("Pulso r") ? (Math.abs(u) <= 0.5 ? 1 : 0)
                    : senal.value.startsWith("Pulso t") ? Math.max(0, 1 - Math.abs(u))
                    : senal.value.startsWith("Gauss") ? Math.exp(-PI * u * u) : (u >= 0 ? Math.exp(-u) : 0);
    const x = t.map(base);
    let y, formula;
    if (op.value.startsWith("Desp")) { y = t.map(u => base(u - t0.value)); formula = "Y(f) = e^{−j2πf t₀} X(f): mismo módulo, fase lineal de pendiente −2πt₀"; }
    else if (op.value.startsWith("Esc")) { y = t.map(u => base(a.value * u)); formula = "Y(f) = X(f/a)/|a|: comprimir en el tiempo ensancha el espectro"; }
    else if (op.value.startsWith("Mod")) { y = t.map((u, i) => x[i] * Math.cos(2 * PI * f0.value * u)); formula = "Y(f) = ½X(f − f₀) + ½X(f + f₀): el espectro se traslada a ±f₀"; }
    else if (op.value.startsWith("Der")) { y = x.map((v, i) => i ? (v - x[i - 1]) / dt : 0); formula = "Y(f) = j2πf X(f): realza las frecuencias altas y anula la continua"; }
    else if (op.value.startsWith("Conv")) { const [r, im] = fft(x), Y2 = ifft(r.map((v, k) => (v * v - im[k] * im[k]) * dt), r.map((v, k) => 2 * v * im[k] * dt));
        y = enteros(0, N - 1).map(n => Y2[0][mod(n - N / 2, N)]); formula = "Y(f) = X(f)²: la convolución en el tiempo es un producto en frecuencia"; }
    else { y = x.slice(); formula = "Y(f) = X(f)"; }
    const tf = (s) => { const [r, im] = fft(s); return enteros(0, N - 1).map(k => { const kk = mod(k + N / 2, N) - N / 2, f = kk / (N * dt);
                         return [f, cmul([r[mod(kk, N)] * dt, im[mod(kk, N)] * dt], cexp([0, -2 * PI * f * tmin]))]; }); };
    const FX = tf(x), FY = tf(y), sel = FX.map((v, i) => Math.abs(v[0]) <= 4.2 ? i : -1).filter(i => i >= 0).sort((i, j) => FX[i][0] - FX[j][0]);
    const mx = Math.max(...sel.map(i => cabs(FX[i][1]))), my = Math.max(...sel.map(i => cabs(FY[i][1])));
    const fase = (c, m) => { if (cabs(c) <= 0.01 * m) return NaN; if (Math.abs(c[1]) < 1e-6 * m) return c[0] >= 0 ? 0 : PI; const p = Math.atan2(c[1], c[0]); return p < -PI + 1e-3 ? PI : p; };
    F.data = {f: sel.map(i => FX[i][0]), X: sel.map(i => cabs(FX[i][1])), Y: sel.map(i => cabs(FY[i][1])),
              pX: sel.map(i => fase(FX[i][1], mx)), pY: sel.map(i => fase(FY[i][1], my))};
    const vis = t.map((u, i) => Math.abs(u) <= 6.2 ? i : -1).filter(i => i >= 0);
    T.data = {t: vis.map(i => t[i]), x: vis.map(i => x[i]), y: vis.map(i => y[i])};
    info.text = `<p>${formula}</p><p>Energía: ∫|y|²dt = ${(y.reduce((s, v) => s + v * v, 0) * dt).toFixed(3)} (en x: ${(x.reduce((s, v) => s + v * v, 0) * dt).toFixed(3)}). Por Parseval coincide con ∫|Y|²df.</p>`;
""", T=T, F=F, senal=senal, op=op, t0=t0, a=a, f0=f0, info=info)
pb.conectar(cb, senal, op, t0, a, f0)

pb.pagina(__file__, "Propiedades de la transformada de Fourier", tema=1,
          descripcion="Cada operación en el tiempo tiene su pareja en frecuencia: desplazar añade una fase lineal sin "
                      "tocar el módulo, comprimir ensancha el espectro, modular lo traslada, derivar lo multiplica por "
                      "j2πf y convolucionar lo multiplica. La transformada se calcula con la FFT de la señal muestreada finamente.",
          controles=[senal, op, t0, a, f0, info], graficas=[p1, [p2, p3]], inicio=cb,
          referencia="Transparencias T1-02, propiedades de la transformada de Fourier · Apuntes del Tema 1, sección 6")
