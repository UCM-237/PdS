"""T5 · DFT bidimensional y filtrado en el dominio de la frecuencia."""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
from bokeh.models import ColumnDataSource, Div, Range1d
import pds_bokeh as pb

LADO = 256
H = LADO // 2

F0 = ColumnDataSource(dict(img=[]))
Fm = ColumnDataSource(dict(img=[]))
Hm = ColumnDataSource(dict(img=[]))
G0 = ColumnDataSource(dict(img=[]))
Foto = ColumnDataSource(dict(f=[]))


def espectro(titulo):
    p = pb.figura(titulo, "l (frecuencia horizontal)", "k (frecuencia vertical)", ancho=240, alto=240,
                  x_range=Range1d(-H, H), y_range=Range1d(H, -H), tools="pan,wheel_zoom,reset,save")
    p.grid.visible = False
    return p


p1 = pb.figura_imagen("Imagen f[m, n]", LADO, ancho=240)
pb.imagen(p1, F0, dw=LADO, dh=LADO)
p2 = espectro("log(1 + |F[k, l]|), centrada")
mapa_F = pb.imagen(p2, Fm, x=-H, y=-H, dw=LADO, dh=LADO, paleta="magma", bajo=0, alto=8)
p3 = espectro("Filtro H[k, l], centrado")
pb.imagen(p3, Hm, x=-H, y=-H, dw=LADO, dh=LADO, paleta="grises", bajo=0, alto=1)
p3.x_range = p2.x_range
p3.y_range = p2.y_range
p4 = pb.figura_imagen("Resultado g = IDFT{H·F}", LADO, ancho=240)
mapa_g = pb.imagen(p4, G0, dw=LADO, dh=LADO)
p4.x_range = p1.x_range
p4.y_range = p1.y_range

imagen = pb.selector("Imagen", ["Prueba", "Prueba con ruido periódico", "Coseno", "Cuadrado", "Anillos", "Texto", "Foto propia"])
fi = pb.foto()
k0 = pb.deslizador("k₀ (ciclos a lo largo de las filas)", -64, 64, 0, 1)
l0 = pb.deslizador("l₀ (ciclos a lo largo de las columnas)", -64, 64, 24, 1)
filtro = pb.selector("Filtro", ["Ninguno", "Paso bajo ideal", "Paso bajo gaussiano", "Paso bajo Butterworth",
                                "Paso alto ideal", "Paso alto gaussiano", "Paso alto Butterworth", "Muescas en ±(k₀, l₀)"])
D0 = pb.deslizador("D₀ (frecuencia de corte)", 2, 128, 20, 1)
orden = pb.deslizador("Orden del Butterworth", 1, 8, 2, 1)
rm = pb.deslizador("Radio de las muescas", 1, 12, 4, 0.5)
fase = pb.casillas(["Reconstruir solo con la fase (|F| = 1)"])
info = Div(text="", width=250)

cb = pb.js("""
    const N = LADO, m0 = k0.value, n0 = l0.value, onda = (m, n) => Math.cos(2 * PI * (m0 * m + n0 * n) / N);
    let f;
    if (imagen.value === "Foto propia" && Foto.data.f.length) f = Foto.data.f[0].map(r => r.slice());
    else if (imagen.value === "Coseno") f = enteros(0, N - 1).map(m => enteros(0, N - 1).map(n => 0.5 + 0.5 * onda(m, n)));
    else if (imagen.value === "Cuadrado") f = enteros(0, N - 1).map(m => enteros(0, N - 1).map(n => Math.abs(m - N / 2) < 16 && Math.abs(n - N / 2) < 16 ? 1 : 0));
    else if (imagen.value.startsWith("Prueba con")) f = imagen_prueba(N).map((r, m) => r.map((v, n) => v + 0.2 * onda(m, n)));
    else f = imagen_patron(imagen.value === "Foto propia" ? "Prueba" : imagen.value, N);
    const [Fr, Fi] = fft2d(f);
    const w = i => (i < N / 2 ? i : i - N);
    // Filtro sobre los índices sin centrar, con las frecuencias negativas en su sitio
    const tipo = filtro.value, d0 = D0.value, nb = orden.value;
    const Hf = enteros(0, N - 1).map(k => enteros(0, N - 1).map(l => {
        const D = Math.hypot(w(k), w(l));
        let pbj = 1;
        if (tipo.endsWith("ideal")) pbj = D <= d0 ? 1 : 0;
        else if (tipo.endsWith("gaussiano")) pbj = Math.exp(-D * D / (2 * d0 * d0));
        else if (tipo.endsWith("Butterworth")) pbj = 1 / (1 + Math.pow(D / d0, 2 * nb));
        else if (tipo.startsWith("Muescas")) {
            const d1 = Math.hypot(w(k) - m0, w(l) - n0), d2 = Math.hypot(w(k) + m0, w(l) + n0), r2 = 2 * rm.value ** 2;
            return (1 - Math.exp(-d1 * d1 / r2)) * (1 - Math.exp(-d2 * d2 / r2));
        }
        return tipo.startsWith("Paso alto") ? 1 - pbj : pbj;
    }));
    let Gr = Fr.map((r, k) => r.map((v, l) => v * Hf[k][l])), Gi = Fi.map((r, k) => r.map((v, l) => v * Hf[k][l]));
    if (fase.active.length) {
        Gr = Gr.map((r, k) => r.map((v, l) => { const a = Math.hypot(v, Gi[k][l]); return a > 1e-12 ? v / a : 0; }));
        Gi = Gi.map((r, k) => r.map((v, l) => { const a = Math.hypot(Fr[k][l] * Hf[k][l], v); return a > 1e-12 ? v / a : 0; }));
    }
    const [g] = ifft2d(Gr, Gi);
    const lg = centrar2d(Fr.map((r, k) => r.map((v, l) => Math.log(1 + Math.hypot(v, Fi[k][l])))));
    F0.data = {img: [matriz(f)]}; Fm.data = {img: [matriz(lg)]}; Hm.data = {img: [matriz(centrar2d(Hf))]}; G0.data = {img: [matriz(g)]};
    let lmax = 0; for (const r of lg) for (const v of r) lmax = Math.max(lmax, v); mapa_F.high = lmax;
    let gmin = Infinity, gmax = -Infinity; for (const r of g) for (const v of r) { gmin = Math.min(gmin, v); gmax = Math.max(gmax, v); }
    if (fase.active.length || tipo.startsWith("Paso alto")) { mapa_g.low = gmin; mapa_g.high = gmax; } else { mapa_g.low = 0; mapa_g.high = 1; }
    let E = 0, Eg = 0; for (let k = 0; k < N; k++) for (let l = 0; l < N; l++) { const a = Fr[k][l] ** 2 + Fi[k][l] ** 2; E += a; Eg += a * Hf[k][l] ** 2; }
    const per = Math.hypot(m0, n0) > 0 ? (N / Math.hypot(m0, n0)).toFixed(1) + " píxeles" : "—";
    info.text = `<p>Nivel medio: F[0, 0]/(MN) = ${(Fr[0][0] / (N * N)).toFixed(3)}</p>` +
        `<p>Onda de (k₀, l₀) = (${m0}, ${n0}): periodo ${per}, picos de la DFT en ±(${m0}, ${n0})</p>` +
        `<p>Energía que conserva el filtro: ${(100 * Eg / E).toFixed(1)} %</p>` +
        (tipo.startsWith("Paso bajo gaussiano") ? `<p>Equivale a un gaussiano espacial de σ = N/(2πD₀) = ${(N / (2 * PI * d0)).toFixed(2)} píxeles</p>` : "") +
        `<p>Valores de g: de ${gmin.toFixed(3)} a ${gmax.toFixed(3)}</p>`;
""", F0=F0, Fm=Fm, Hm=Hm, G0=G0, Foto=Foto, mapa_F=mapa_F, mapa_g=mapa_g, imagen=imagen, k0=k0, l0=l0, filtro=filtro,
   D0=D0, orden=orden, rm=rm, fase=fase, info=info, LADO=LADO)
pb.conectar(cb, imagen, k0, l0, filtro, D0, orden, rm, fase)
fi.js_on_change("value", pb.js("""
    foto_cargar(fi, LADO, img => { Foto.data = {f: [img]}; if (imagen.value === "Foto propia") cb.execute(); else imagen.value = "Foto propia"; });
""", fi=fi, Foto=Foto, imagen=imagen, cb=cb, LADO=LADO))

pb.pagina(__file__, "DFT 2D y filtrado en frecuencia", tema=5,
          descripcion="La DFT 2D descompone la imagen en ondas planas: un coseno da dos puntos simétricos, en la dirección "
                      "perpendicular a sus franjas y tanto más lejos del centro cuanto más finas son. Multiplicar por H[k, l] y "
                      "volver con la IDFT filtra la imagen: el paso bajo ideal deja anillos alrededor de los bordes; el gaussiano, "
                      "no. Unas muescas quitan un ruido periódico.",
          controles=[imagen, fi, k0, l0, filtro, D0, orden, rm, fase, info],
          graficas=[[p1, p2], [p3, p4]], inicio=cb,
          referencia="Transparencias T5-03, DFT 2D y filtros en el dominio de la frecuencia · Apuntes del Tema 5, sección 3")
