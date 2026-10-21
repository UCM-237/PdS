"""Hito 2: filtros 1D aplicados por filas y columnas. Completa las partes marcadas con TODO."""
import numpy as np
from scipy import ndimage, signal

from utilidades import cargar, filtrar_sep, psnr, ssim

y1, x1 = cargar(1), cargar(1, limpia=True)
h = np.ones(3) / 3
r = filtrar_sep(y1, h, h)
print(f"media 3×3: PSNR = {psnr(r, x1):.2f} dB, SSIM = {ssim(r, x1):.3f}")
# TODO: gaussianos de varias σ y un FIR de 15 coeficientes por enventanado (barre fc).
# TODO: respuesta en frecuencia 2D de cada núcleo: |H(fx)|·|H(fy)| con np.fft.fft(h, 256).

y2, x2 = cargar(2), cargar(2, limpia=True)
r2 = ndimage.median_filter(y2, size=3, mode="reflect")
print(f"mediana 3×3: PSNR = {psnr(r2, x2):.2f} dB")
# TODO: compara con la media del mismo tamaño.

y3 = cargar(3)
# TODO: diseña una muesca IIR de 2.º orden en la frecuencia del pico del H1 y aplícala
#       fila a fila con fase cero: signal.filtfilt(b, a, y3, axis=1).
