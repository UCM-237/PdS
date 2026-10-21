"""Hito 4: wavelets, clasificación de latidos y alarma. Completa las partes marcadas con TODO."""
import numpy as np

from utilidades import FS, cargar, guardar_latidos


def a_trous(x, niveles=5):
    """Transformada wavelet diádica no diezmada (à trous).
    TODO: filtros h = [1 3 3 1]/8 y g = [2 -2]; en el nivel k intercala 2^(k-1) - 1 ceros
    entre sus coeficientes. Devuelve la lista de detalles W[k] y la aproximación final."""
    W = []
    a = x.copy()
    return W, a


t, x = cargar("ecg_B.csv")
# TODO: detector sobre la escala con más energía del QRS y comparación con Pan-Tompkins.
# TODO: anchura del QRS y adelanto (RR previo / mediana de los RR vecinos) de cada latido;
#       clasifica N o V.
# TODO: alarma de taquicardia (FC > 100 lpm durante varios latidos seguidos).

r = np.array([], dtype=int)             # tus detecciones en B (índices de muestra)
tipos = np.array([], dtype=str)         # 'N' o 'V'
guardar_latidos("ecg_B_latidos.csv", r, tipos)
