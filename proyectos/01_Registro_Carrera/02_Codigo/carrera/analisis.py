"""Cadena completa: carga -> preprocesado -> caracteristicas -> deteccion."""
import numpy as np

from . import caracteristicas as cr
from . import deteccion as dt
from . import preprocesado as pp

FS = 1.0        # Hz, rejilla de trabajo
DIEZMADO = 4    # la deteccion de cambios se hace a 0.25 Hz (~ periodo original)


def sigma_ruido(df_limpio):
    """Desviacion tipica del ruido de la velocidad estimada en las muestras
    ORIGINALES (no interpoladas) con las diferencias de primer orden."""
    v = df_limpio["speed_kmh"].dropna().to_numpy()
    return 1.4826 * np.median(np.abs(np.diff(v))) / np.sqrt(2)


def cambios_ritmo(u, df_limpio, min_seg_s=45.0, delta_min=1.0):
    """Instantes (indices de la rejilla de 1 Hz) de cambio de ritmo."""
    x = u["speed_kmh"].to_numpy()[::DIEZMADO]
    c = dt.detectar_cambios_ritmo(x, fs=FS / DIEZMADO, min_seg_s=min_seg_s,
                                  delta_min=delta_min, sigma=sigma_ruido(df_limpio))
    return c * DIEZMADO


def analizar(df):
    limpio = pp.limpiar(df)
    u = pp.preprocesar(df, fs=FS)
    estados = dt.clasificar_estados(u["v_filt"], FS)
    cortes = cambios_ritmo(u, limpio)
    resumen = cr.resumen(u, estados)
    resumen["n_tramos_ritmo"] = len(cortes) + 1
    resumen["n_repeticiones"] = dt.contar_repeticiones(u["speed_kmh"].to_numpy(), cortes)
    return {"df": df, "limpio": limpio, "u": u, "estados": estados,
            "cortes": cortes, "resumen": resumen}
