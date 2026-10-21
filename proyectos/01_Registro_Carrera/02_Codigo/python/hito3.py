"""Hito 3: ruido, atípicos y cambios de ritmo. Completa las partes marcadas con TODO."""
import numpy as np

from utilidades import cargar_actividad, evaluar_detecciones, verdad_desarrollo


def detectar_cambios(t, v):
    """TODO: instantes (s) de los cambios de ritmo. Prueba un umbral sobre la derivada de la
    velocidad filtrada y una segmentación binaria con penalización."""
    return []


total = np.zeros(3, int)
for fichero, (tipo, sigma, cambios) in verdad_desarrollo().items():
    d = cargar_actividad(fichero)
    det = detectar_cambios(d["time"].to_numpy(), d["v_kmh"].to_numpy())
    total += evaluar_detecciones(det, cambios)
tp, fp, fn = total
print(f"TP {tp}, FP {fp}, FN {fn}")
# TODO: estadística del ruido de la velocidad (histograma, σ, autocorrelación).
# TODO: atípicos con Hampel / MAD, FC congelada y distancia corregida.
# TODO: indicadores de cada sesión real.
