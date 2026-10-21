"""Hito 4: orientación, desenfoque y lectura de las seis imágenes. Completa las partes TODO."""
import numpy as np

from utilidades import cargar, enderezar, guardar_lecturas


def orientacion(img):
    """TODO: ángulo del eje del código a partir de la energía de la DFT 2D por direcciones
    (np.fft.fft2 con ventana, ángulo de cada frecuencia con np.arctan2, histograma ponderado)."""
    return 0.0


def wiener_1d(p, h, snr=100):
    """TODO: deconvolución de Wiener X = conj(H) Y / (|H|² + 1/SNR)."""
    return p


lecturas = {}
for i in range(1, 7):
    img = cargar(i)
    rec = enderezar(img, orientacion(img))
    # TODO: iluminación, localización, perfil, umbral, deconvolución si hace falta y lectura
    lecturas[i] = None
guardar_lecturas(lecturas)
print(lecturas)
