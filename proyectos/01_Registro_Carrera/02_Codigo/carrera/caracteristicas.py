"""Extraccion de caracteristicas (Hito 3).

Todas las funciones reciben la senal ya preprocesada y remuestreada a fs
uniforme (salida de ``preprocesado.preprocesar``).
"""
import numpy as np
import pandas as pd

FC_MAXIMA = 190  # ppm. Supuesto: 220 - edad (30 anos). No hay prueba de esfuerzo.
# Zonas de FC en % de FC maxima (modelo clasico de 5 zonas)
ZONAS_FC = {"Z1": (0.50, 0.60), "Z2": (0.60, 0.70), "Z3": (0.70, 0.80),
            "Z4": (0.80, 0.90), "Z5": (0.90, 1.01)}
V_MOVIMIENTO = 2.0  # km/h: por debajo se considera parado


def ritmo_min_km(v_kmh):
    """Velocidad (km/h) -> ritmo (min/km)."""
    v = np.asarray(v_kmh, float)
    with np.errstate(divide="ignore"):
        return np.where(v > 0, 60.0 / v, np.nan)


def formato_ritmo(r):
    """5.4 -> '5:24'."""
    if not np.isfinite(r):
        return "-"
    m, s = divmod(round(r * 60), 60)
    return f"{m}:{s:02d}"


def desnivel(alt, umbral=1.0):
    """Desnivel positivo y negativo acumulado con histeresis de ``umbral`` m.

    Sumar todas las diferencias positivas de la altitud sobrestima mucho el
    desnivel porque el ruido de 0.1-0.2 m tambien suma. Con la histeresis solo
    se cuenta un cambio cuando la altitud se ha movido mas de ``umbral`` desde
    el ultimo punto de referencia."""
    sube = baja = 0.0
    ref = alt[0]
    for a in alt[1:]:
        if a - ref >= umbral:
            sube += a - ref
            ref = a
        elif ref - a >= umbral:
            baja += ref - a
            ref = a
    return sube, baja


def pendiente(dist_m, alt, paso_m=50.0):
    """Pendiente (%) calculada sobre ventanas de ``paso_m`` metros recorridos
    (no de tiempo), para que no dependa de la velocidad."""
    dist_m = np.asarray(dist_m, float)
    ini = np.searchsorted(dist_m, dist_m - paso_m / 2)
    fin = np.clip(np.searchsorted(dist_m, dist_m + paso_m / 2), 0, len(dist_m) - 1)
    dx = dist_m[fin] - dist_m[ini]
    with np.errstate(invalid="ignore", divide="ignore"):
        g = 100 * (alt[fin] - alt[ini]) / dx
    return np.where(dx > paso_m / 2, g, 0.0)


def tiempo_en_zonas(fc, fs, fc_max=FC_MAXIMA):
    """Fraccion del tiempo en cada zona de FC."""
    p = np.asarray(fc) / fc_max
    n = len(p)
    return {z: float(np.sum((p >= lo) & (p < hi))) / n for z, (lo, hi) in ZONAS_FC.items()}


def tiempo_estabilizacion_fc(t, fc_filt, fraccion=0.95):
    """Tiempo (s) que tarda la FC en llegar al ``fraccion`` de su mediana en la
    segunda mitad de la sesion: marca el final del calentamiento cardiaco."""
    ref = np.median(fc_filt[len(fc_filt) // 2:])
    i = np.argmax(fc_filt >= fraccion * ref)
    return float(t[i] - t[0])


def desacoplamiento(u, mascara, descartar_s=600):
    """Desacoplamiento aerobico (Pa:FC), en %.

    Se compara la eficiencia EF = velocidad / FC de la primera y la segunda
    mitad del tramo en carrera (descartando los primeros ``descartar_s``
    segundos de calentamiento). Valores < 5 % indican buena base aerobica; si
    la FC sube a ritmo constante (deriva cardiaca) el valor crece."""
    t = u["time"].to_numpy()
    m = mascara & (t - t[0] >= descartar_s)
    idx = np.where(m)[0]
    if len(idx) < 120:
        return np.nan
    mitad = idx[len(idx) // 2]
    ef = u["v_filt"] / u["fc_filt"]
    ef1, ef2 = ef[idx[idx < mitad]].mean(), ef[idx[idx >= mitad]].mean()
    return float(100 * (ef1 - ef2) / ef1)


def parciales_km(u):
    """Tabla de parciales por kilometro (sobre la distancia corregida)."""
    d = u["distance_corr"].to_numpy() / 1000
    t = u["time"].to_numpy()
    filas = []
    for k in range(int(np.floor(d[-1])) + 1):
        m = (d >= k) & (d < k + 1)
        if m.sum() < 2:
            continue
        dist = d[m][-1] - d[m][0]
        dur = t[m][-1] - t[m][0]
        sube, _ = desnivel(u["alt_filt"].to_numpy()[m], 0.5)
        filas.append({"km": k + 1, "distancia_km": dist, "tiempo_s": dur,
                      "ritmo_min_km": dur / 60 / dist if dist > 0 else np.nan,
                      "fc_media": u["heartrate"][m].mean(), "desnivel_pos_m": sube})
    return pd.DataFrame(filas)


def resumen(u, estados=None):
    """Indicadores globales de una sesion.

    ``estados`` (opcional) es la salida de ``deteccion.clasificar_estados``;
    si se da, el ritmo medio se calcula solo sobre el tramo en carrera.
    """
    fs = u.attrs.get("fs", 1.0)
    t = u["time"].to_numpy()
    v = u["v_filt"].to_numpy()
    mov = v > V_MOVIMIENTO
    corre = (estados == 2) if estados is not None else mov
    dist_km = u["distance_corr"].iloc[-1] / 1000
    t_mov = mov.sum() / fs
    sube, baja = desnivel(u["alt_filt"].to_numpy())
    g = pendiente(u["distance_corr"].to_numpy(), u["alt_filt"].to_numpy())
    zonas = tiempo_en_zonas(u["heartrate"][corre], fs)
    vc = u["speed_kmh"][corre]
    r = {
        "fecha": u.attrs.get("nombre", ""),
        "duracion_min": len(t) / fs / 60,  # n muestras * Ts (coherente con los tiempos por estado)
        "tiempo_mov_min": t_mov / 60,
        "tiempo_carrera_min": corre.sum() / fs / 60,
        "distancia_km": dist_km,
        "distancia_strava_km": u["distance"].iloc[-1] / 1000,
        "v_media_kmh": dist_km / (t_mov / 3600),
        "v_carrera_kmh": vc.mean(),
        "ritmo_carrera_min_km": 60 / vc.mean(),
        "cv_velocidad_pct": 100 * u["v_filt"][corre].std() / u["v_filt"][corre].mean(),
        "fc_media": u["heartrate"][corre].mean(),
        "fc_max": u["heartrate"].max(),
        "desnivel_pos_m": sube,
        "desnivel_neg_m": baja,
        "pendiente_max_pct": float(np.max(g)),
        "t_estab_fc_min": tiempo_estabilizacion_fc(t, u["fc_filt"].to_numpy()) / 60,
        "desacoplamiento_pct": desacoplamiento(u, corre),
        "ef_m_por_latido": float((u["velocity"][corre] / (u["heartrate"][corre] / 60)).mean()),
    }
    r.update({f"t_{z}_pct": 100 * f for z, f in zonas.items()})
    return r
