"""Hito 3: ruido, umbral y lectura. Completa las partes marcadas con TODO."""
import numpy as np

from ean13 import G, L, PARIDAD, R, digito_control
from utilidades import cargar, codigos_desarrollo


def bordes(p, umbral):
    """Cruces del umbral con interpolación lineal (precisión subpíxel)."""
    s = p - umbral
    i = np.flatnonzero(np.sign(s[:-1]) != np.sign(s[1:]))
    return i + s[i] / (s[i] - s[i + 1])


def decodificar(rachas):
    """59 anchuras (barra, espacio, barra, ...) → código de 13 cifras o None.
    TODO: separa las guardas, normaliza cada grupo de 4 rachas a 7 módulos, busca el patrón
    más cercano en L, G (izquierda) y R (derecha), obtén el primer dígito con PARIDAD y
    comprueba el dígito de control con digito_control()."""
    return None


img = cargar(1)
p = img[img.shape[0] // 2]            # TODO: promedia N filas de la zona del código
umbral = 0.5                          # TODO: umbral de Otsu u otro justificado
e = bordes(p, umbral)
print(f"{len(e)} cruces del umbral")
# TODO: quédate con los 60 bordes del código y calcula las 59 anchuras (np.diff).
print("lectura:", decodificar(np.diff(e)), " correcto:", codigos_desarrollo()[1])
# TODO: estadística del ruido en una zona blanca, varianza frente a N y tasa de lectura
#       frente a σ del ruido añadido.
