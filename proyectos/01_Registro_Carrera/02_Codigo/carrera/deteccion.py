"""Deteccion de eventos y clasificacion (Hito 4).

Tres niveles:
1. Muestra a muestra: estado parado / andando / corriendo (umbrales + duracion
   minima).
2. Tramos: cambios de ritmo dentro de la carrera. Se comparan dos metodos:
   a) derivada + umbral MAD (punto de partida, ``entrenamiento/main.py``);
   b) segmentacion binaria por minimos cuadrados con penalizacion.
3. Sesion: clasificacion del tipo de entrenamiento con reglas sencillas.
"""
import numpy as np

PARADO, ANDANDO, CORRIENDO = 0, 1, 2
NOMBRE_ESTADO = {PARADO: "parado", ANDANDO: "andando", CORRIENDO: "corriendo"}


# ---------------------------------------------------------------------------
# 1) Estados
# ---------------------------------------------------------------------------
def tramos(etiquetas):
    """Agrupa una secuencia de etiquetas en tramos (etiqueta, i_ini, i_fin)."""
    e = np.asarray(etiquetas)
    cortes = np.flatnonzero(np.diff(e)) + 1
    ini = np.r_[0, cortes]
    fin = np.r_[cortes - 1, len(e) - 1]
    return [(int(e[a]), int(a), int(b)) for a, b in zip(ini, fin)]


def clasificar_estados(v_kmh, fs=1.0, v_parado=2.0, v_correr=7.0, dur_min_s=20):
    """Estado por muestra a partir de la velocidad filtrada.

    - < 2 km/h: parado (deriva del GPS en reposo)
    - 2-7 km/h: andando (un paseo rapido ronda 6 km/h)
    - > 7 km/h: corriendo (trote muy suave ~ 8 km/h)

    Los tramos mas cortos que ``dur_min_s`` se absorben en el tramo vecino mas
    largo para evitar el parpadeo de la etiqueta cerca de los umbrales.
    """
    v = np.asarray(v_kmh, float)
    e = np.where(v < v_parado, PARADO, np.where(v < v_correr, ANDANDO, CORRIENDO))
    n_min = int(dur_min_s * fs)
    cambiado = True
    while cambiado:
        cambiado = False
        tr = tramos(e)
        if len(tr) < 2:
            break
        # el tramo corto mas breve primero
        k = min(range(len(tr)), key=lambda i: tr[i][2] - tr[i][1])
        lab, a, b = tr[k]
        if b - a + 1 < n_min:
            vecinos = [tr[j] for j in (k - 1, k + 1) if 0 <= j < len(tr)]
            nuevo = max(vecinos, key=lambda x: x[2] - x[1])[0]
            e[a:b + 1] = nuevo
            cambiado = True
    return e


# ---------------------------------------------------------------------------
# 2a) Cambios de ritmo por derivada + MAD
# ---------------------------------------------------------------------------
def cambios_derivada(t, v, factor=5.0, separacion_s=30.0):
    """Metodo del codigo de partida, corregido.

    Se marca cambio cuando |dv/dt| supera ``factor`` * MAD(dv/dt). En el
    codigo original cada muestra por encima del umbral era un cambio distinto
    (decenas de cambios para una sola transicion); aqui las detecciones mas
    proximas que ``separacion_s`` se agrupan y se toma el maximo de |dv/dt|.
    """
    t, v = np.asarray(t, float), np.asarray(v, float)
    dv = np.gradient(v, t)
    mad = np.median(np.abs(dv - np.median(dv)))
    umbral = factor * 1.4826 * mad
    idx = np.flatnonzero(np.abs(dv) > umbral)
    cambios, grupo = [], []
    for i in idx:
        if grupo and t[i] - t[grupo[-1]] > separacion_s:
            cambios.append(grupo[np.argmax(np.abs(dv[grupo]))])
            grupo = []
        grupo.append(i)
    if grupo:
        cambios.append(grupo[np.argmax(np.abs(dv[grupo]))])
    return np.array(cambios, dtype=int), dv, umbral


# ---------------------------------------------------------------------------
# 2b) Segmentacion binaria (cambios en la media)
# ---------------------------------------------------------------------------
def _coste(cs, cs2, a, b):
    """Suma de cuadrados respecto a la media de x[a:b] en O(1)."""
    n = b - a
    s = cs[b] - cs[a]
    return (cs2[b] - cs2[a]) - s * s / n


def segmentacion_binaria(x, fs=1.0, min_seg_s=45.0, penalizacion=None, sigma=None):
    """Detecta cambios de media de ``x`` por segmentacion binaria.

    Modelo: x es constante a trozos + ruido. Se busca recursivamente el corte
    que mas reduce la suma de cuadrados y se acepta si la reduccion supera la
    penalizacion beta = 2*sigma^2*log(n) (tipo BIC). ``sigma`` se estima de
    forma robusta a partir de las diferencias de primer orden de la senal
    original (MAD/sqrt(2)), que apenas se ven afectadas por los escalones.
    """
    x = np.asarray(x, float)
    n = len(x)
    if sigma is None:
        sigma = 1.4826 * np.median(np.abs(np.diff(x) - np.median(np.diff(x)))) / np.sqrt(2)
    if penalizacion is None:
        penalizacion = 2 * sigma ** 2 * np.log(n)
    m = int(min_seg_s * fs)
    cs = np.r_[0.0, np.cumsum(x)]
    cs2 = np.r_[0.0, np.cumsum(x * x)]

    cortes = []
    pila = [(0, n)]
    while pila:
        a, b = pila.pop()
        if b - a < 2 * m:
            continue
        ks = np.arange(a + m, b - m + 1)
        n1, n2 = ks - a, b - ks
        s1, s2 = cs[ks] - cs[a], cs[b] - cs[ks]
        q1, q2 = cs2[ks] - cs2[a], cs2[b] - cs2[ks]
        c = (q1 - s1 ** 2 / n1) + (q2 - s2 ** 2 / n2)
        j = int(np.argmin(c))
        ganancia = _coste(cs, cs2, a, b) - c[j]
        if ganancia > penalizacion:
            k = int(ks[j])
            cortes.append(k)
            pila += [(a, k), (k, b)]
    return np.array(sorted(cortes), dtype=int)


def medias_por_tramo(x, cortes):
    """Senal constante a trozos con la media de cada tramo."""
    x = np.asarray(x, float)
    y = np.empty_like(x)
    lim = np.r_[0, cortes, len(x)]
    for a, b in zip(lim[:-1], lim[1:]):
        y[a:b] = x[a:b].mean()
    return y


def fusionar_tramos(x, cortes, delta_min=1.0):
    """Elimina cortes entre tramos cuya media difiere menos de ``delta_min``
    (km/h): diferencias estadisticamente significativas pero sin interes
    deportivo (p. ej. un falso llano)."""
    cortes = list(cortes)
    cambiado = True
    while cambiado and cortes:
        cambiado = False
        lim = [0] + cortes + [len(x)]
        medias = [np.mean(x[a:b]) for a, b in zip(lim[:-1], lim[1:])]
        saltos = np.abs(np.diff(medias))
        j = int(np.argmin(saltos))
        if saltos[j] < delta_min:
            cortes.pop(j)
            cambiado = True
    return np.array(cortes, dtype=int)


def detectar_cambios_ritmo(v, fs=1.0, min_seg_s=45.0, delta_min=1.0, sigma=None):
    """Segmentacion binaria + fusion de tramos poco distintos."""
    c = segmentacion_binaria(v, fs, min_seg_s, sigma=sigma)
    return fusionar_tramos(np.asarray(v, float), c, delta_min)


# ---------------------------------------------------------------------------
# Validacion de detectores de eventos
# ---------------------------------------------------------------------------
def evaluar_detecciones(detectados, reales, tolerancia):
    """Precision, sensibilidad y F1 emparejando cada evento real con el
    detectado mas cercano a menos de ``tolerancia`` (misma unidad)."""
    detectados = list(np.sort(detectados))
    tp, errores = 0, []
    for r in reales:
        if not detectados:
            break
        j = int(np.argmin([abs(d - r) for d in detectados]))
        if abs(detectados[j] - r) <= tolerancia:
            errores.append(detectados[j] - r)
            detectados.pop(j)
            tp += 1
    fp = len(detectados)
    fn = len(reales) - tp
    p = tp / (tp + fp) if tp + fp else 0.0
    s = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * p * s / (p + s) if p + s else 0.0
    return {"TP": tp, "FP": fp, "FN": fn, "precision": p, "sensibilidad": s, "F1": f1,
            "error_medio_s": float(np.mean(np.abs(errores))) if errores else np.nan}


# ---------------------------------------------------------------------------
# 3) Clasificacion de la sesion
# ---------------------------------------------------------------------------
def contar_repeticiones(v, cortes, delta=2.0, v_correr=7.0):
    """Numero de bloques 'rapidos' separados por tramos lentos (patron de
    series).

    Cada tramo de la segmentacion se etiqueta como rapido si su media supera
    en ``delta``/2 la mediana de la velocidad en carrera. Los tramos rapidos
    consecutivos se agrupan en un solo bloque (asi da igual que la
    segmentacion parta una repeticion en dos) y solo se cuentan los bloques
    con un tramo no rapido a cada lado (el arranque o el final no cuentan).
    """
    v = np.asarray(v, float)
    lim = np.r_[0, cortes, len(v)]
    m = np.array([np.mean(v[a:b]) for a, b in zip(lim[:-1], lim[1:])])
    ref = np.median(v[v > v_correr])
    rapido = m >= ref + delta / 2
    bloques = [(e, a, b) for e, a, b in tramos(rapido.astype(int)) if e == 1]
    return sum(1 for _, a, b in bloques if a > 0 and b < len(m) - 1)


def clasificar_sesion(r, v_referencia, n_repeticiones):
    """Reglas sencillas, en orden de prioridad.

    r              resumen de la sesion (``caracteristicas.resumen``)
    v_referencia   velocidad de carrera 'habitual' del atleta (mediana de sus
                   sesiones), para que las reglas sean relativas al corredor.
    """
    intensa = r["t_Z4_pct"] + r["t_Z5_pct"]
    if n_repeticiones >= 3:
        return "Series", f"{n_repeticiones} repeticiones rapido/lento"
    if r["distancia_km"] >= 12 or r["tiempo_carrera_min"] >= 75:
        return "Tirada larga", f"{r['distancia_km']:.1f} km"
    if r["v_carrera_kmh"] >= 1.05 * v_referencia and intensa >= 40:
        return "Tempo", (f"v = {r['v_carrera_kmh']:.1f} km/h (> 105 % ref.), "
                         f"{intensa:.0f} % en Z4-Z5")
    return "Rodaje", f"v = {r['v_carrera_kmh']:.1f} km/h, {intensa:.0f} % en Z4-Z5"
