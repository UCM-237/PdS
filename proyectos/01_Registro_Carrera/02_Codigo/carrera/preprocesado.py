"""Deteccion de anomalias, limpieza, remuestreo y filtrado de la senal."""
import numpy as np
import pandas as pd
from scipy import signal

# Limites fisiologicos / fisicos razonables para un corredor popular
V_MAX_KMH = 25.0       # por encima es imposible corriendo -> error de GPS
FC_MIN, FC_MAX = 40, 220
HUECO_S = 15.0         # un intervalo entre muestras mayor que esto es un hueco


# ---------------------------------------------------------------------------
# Hito 1: diagnostico
# ---------------------------------------------------------------------------
def intervalos_muestreo(t):
    """Intervalos entre muestras consecutivas (s)."""
    return np.diff(np.asarray(t, dtype=float))


def detectar_huecos(t, umbral=HUECO_S):
    """Lista de (t_inicio, t_fin) de los intervalos sin datos mayores que ``umbral``."""
    t = np.asarray(t, dtype=float)
    idx = np.where(np.diff(t) > umbral)[0]
    return [(t[i], t[i + 1]) for i in idx]


def hampel(x, k=5, n_sigmas=3.0):
    """Filtro de Hampel: marca como outlier la muestra que se aleja mas de
    ``n_sigmas`` desviaciones robustas (1.4826*MAD) de la mediana de su ventana
    de 2k+1 muestras. Devuelve (mascara_outliers, mediana_local)."""
    x = pd.Series(np.asarray(x, dtype=float))
    med = x.rolling(2 * k + 1, center=True, min_periods=1).median()
    mad = (x - med).abs().rolling(2 * k + 1, center=True, min_periods=1).median()
    outlier = (x - med).abs() > n_sigmas * 1.4826 * mad
    return outlier.to_numpy(), med.to_numpy()


def detectar_outliers_velocidad(df, v_max=V_MAX_KMH, k=5, n_sigmas=4.0):
    """Outliers de velocidad: imposibles fisicamente o atipicos segun Hampel.

    Se usan dos criterios porque se complementan: el limite fisico no depende
    de parametros pero solo caza los picos enormes; Hampel caza picos mas
    pequenos pero, con un umbral bajo, marcaria variaciones reales de ritmo.
    Por eso se exige que el pico de Hampel sea ademas al alza (> 1.5 veces la
    mediana local), que es como se manifiestan los saltos de GPS.
    """
    v = df["speed_kmh"].to_numpy()
    fisico = v > v_max
    h, med = hampel(v, k=k, n_sigmas=n_sigmas)
    return fisico | (h & (v > 1.5 * med))


def detectar_meseta(t, x, min_dur_s=60.0, salto_min=10.0):
    """Tramos en los que la senal se queda congelada en un valor durante al
    menos ``min_dur_s`` segundos y al salir de ellos salta mas de
    ``salto_min`` unidades. Es la firma de una banda de pecho que aun no hace
    buen contacto: el reloj repite el ultimo valor y luego 'engancha' la FC
    real. (En regimen permanente la FC, entera, se repite 20-40 s sin que
    haya error, por eso se exige tambien el salto.)
    Devuelve lista de (i_inicio, i_fin)."""
    t, x = np.asarray(t, float), np.asarray(x, float)
    tramos, ini = [], 0
    for i in range(1, len(x) + 1):
        if i == len(x) or x[i] != x[ini]:
            fin = i - 1
            salto = abs(x[i] - x[fin]) if i < len(x) else 0.0
            if t[fin] - t[ini] >= min_dur_s and salto >= salto_min:
                tramos.append((ini, fin))
            ini = i
    return tramos


def velocidad_desde_distancia(df):
    """Velocidad (km/h) obtenida derivando la distancia acumulada."""
    return np.r_[0.0, np.diff(df["distance"]) / np.diff(df["time"])] * 3.6


# ---------------------------------------------------------------------------
# Hito 2: limpieza y remuestreo
# ---------------------------------------------------------------------------
def limpiar(df):
    """Devuelve una copia con los outliers sustituidos por NaN y columnas de
    marca (``outlier_v``, ``fc_meseta``) para poder documentar que se toco."""
    d = df.copy()
    d["outlier_v"] = detectar_outliers_velocidad(d)
    d.loc[d["outlier_v"], ["velocity", "speed_kmh"]] = np.nan

    d["fc_meseta"] = False
    for i0, i1 in detectar_meseta(d["time"], d["heartrate"]):
        d.loc[d.index[i0:i1 + 1], "fc_meseta"] = True
    fuera = (d["heartrate"] < FC_MIN) | (d["heartrate"] > FC_MAX) | d["fc_meseta"]
    d.loc[fuera, "heartrate"] = np.nan

    # La distancia de Strava integra los saltos de GPS. En las muestras
    # marcadas como outlier se sustituye el incremento de distancia por
    # v_interpolada * dt; el resto de incrementos se respeta.
    v = d["velocity"].interpolate(limit_direction="both").to_numpy()
    dt = np.diff(d["time"].to_numpy())
    inc = np.diff(d["distance"].to_numpy())
    malo = d["outlier_v"].to_numpy()[1:]
    inc[malo] = 0.5 * (v[1:] + v[:-1])[malo] * dt[malo]
    d["distance_corr"] = np.r_[0.0, np.cumsum(inc)]
    return d


def remuestrear(df, fs=1.0, max_hueco=HUECO_S):
    """Remuestrea a una rejilla uniforme de periodo 1/fs por interpolacion lineal.

    La interpolacion es necesaria para poder aplicar filtros digitales y la
    transformada de Fourier, que suponen muestreo uniforme. Ojo: el periodo
    tipico original es ~4 s, asi que la rejilla de 1 s no anade informacion por
    encima de ~1/(2*4) = 0.125 Hz. Las muestras de la rejilla que caen dentro
    de un hueco largo se marcan con ``en_hueco``.
    """
    t = df["time"].to_numpy()
    tu = np.arange(t[0], t[-1] + 1e-9, 1.0 / fs)
    out = pd.DataFrame({"time": tu})
    for c in ["distance", "distance_corr", "heartrate", "velocity", "altitude"]:
        if c in df:
            s = df[c].to_numpy(dtype=float)
            ok = ~np.isnan(s)
            out[c] = np.interp(tu, t[ok], s[ok])
    out["speed_kmh"] = out["velocity"] * 3.6
    j = np.searchsorted(t, tu, side="right")
    j = np.clip(j, 1, len(t) - 1)
    out["en_hueco"] = (t[j] - t[j - 1]) > max_hueco
    out.attrs = dict(df.attrs, fs=fs)
    return out


# ---------------------------------------------------------------------------
# Hito 2: filtrado
# ---------------------------------------------------------------------------
def ema_irregular(t, x, tau):
    """Media movil exponencial (filtro RC de 1er orden) con muestreo irregular.

    Es el filtro de ``entrenamiento/main.py``: alpha = 1 - exp(-dt/tau).
    Es causal, por lo que introduce un retardo de ~tau segundos.
    """
    t, x = np.asarray(t, float), np.asarray(x, float)
    y = np.empty_like(x)
    y[0] = x[0]
    for k in range(1, len(x)):
        a = 1 - np.exp(-(t[k] - t[k - 1]) / tau)
        y[k] = a * x[k] + (1 - a) * y[k - 1]
    return y


def paso_bajo(x, fs, fc, orden=2):
    """Butterworth paso bajo de fase cero (filtfilt): no desplaza los eventos
    en el tiempo, que es lo que importa para localizar cambios de ritmo."""
    sos = signal.butter(orden, fc, btype="low", fs=fs, output="sos")
    return signal.sosfiltfilt(sos, np.asarray(x, float))


def mediana_movil(x, ventana):
    """Filtro de mediana (no lineal): conserva escalones y elimina impulsos."""
    return pd.Series(x).rolling(ventana, center=True, min_periods=1).median().to_numpy()


def espectro(x, fs, nperseg=512):
    """Densidad espectral de potencia (Welch) de la senal sin su media."""
    x = np.asarray(x, float)
    return signal.welch(x - x.mean(), fs=fs, nperseg=min(nperseg, len(x)))


# Frecuencias de corte elegidas en el Hito 2 (ver informe)
FC_VELOCIDAD = 1 / 60    # Hz: conserva cambios de ritmo de 1 min o mas
FC_ALTITUD = 1 / 60
FC_FC = 1 / 30


def preprocesar(df, fs=1.0):
    """Cadena completa del Hito 2: limpiar -> remuestrear -> filtrar."""
    u = remuestrear(limpiar(df), fs=fs)
    u["v_filt"] = paso_bajo(u["speed_kmh"], fs, FC_VELOCIDAD)
    u["alt_filt"] = paso_bajo(u["altitude"], fs, FC_ALTITUD)
    u["fc_filt"] = paso_bajo(u["heartrate"], fs, FC_FC)
    return u
