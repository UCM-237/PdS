"""Hito 3: estadística del ruido. Completa las partes marcadas con TODO."""
import numpy as np
from scipy import ndimage

from utilidades import cargar, psnr, ssim

y1, x1 = cargar(1), cargar(1, limpia=True)
r = y1 - x1
print(f"imagen 1: media del residuo = {r.mean():.4f}, σ = {r.std():.4f}")
# TODO: histograma del residuo con su gaussiana; autocorrelación 2D (con fft2: |R|² y ifft2).


def estimar_sigma(img):
    """TODO: σ del ruido sin la imagen limpia (por ejemplo, con el núcleo N de la teoría mínima
    y la mediana de |img * N|)."""
    return 0.0


def wiener_local(img, sigma, k=5):
    """TODO: media y varianza en ventanas k×k y x̂ = m + max(v − σ², 0)/v · (y − m)."""
    return img


print(f"σ estimada en la imagen 1: {estimar_sigma(y1):.4f}")
# TODO: Monte Carlo del estimador (varias σ, 20 realizaciones).
# TODO: diagnóstico de las seis imágenes: fracción de impulsos, picos del espectro, σ,
#       pendiente de la varianza local frente a la media local en zonas planas.
r = wiener_local(y1, estimar_sigma(y1))
print(f"Wiener local: PSNR = {psnr(r, x1):.2f} dB, SSIM = {ssim(r, x1):.3f}")
# TODO: mediana que solo sustituye los impulsos (imagen 2) y Anscombe para el ruido de Poisson.
