"""Hito 2: iluminación y filtrado 2D. Completa las partes marcadas con TODO."""
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage

from utilidades import cargar, enderezar, guardar

img = cargar(4)
# TODO: estima la iluminación (por ejemplo, máximo local con ndimage.maximum_filter seguido
#       de ndimage.gaussian_filter) y divide. Compara con restar un paso bajo.
ilum = ndimage.gaussian_filter(img, 25)      # provisional: paso bajo lineal
fig, ax = plt.subplots(1, 3, figsize=(11, 3.3), constrained_layout=True)
for a, (im, t) in zip(ax, [(img, "original"), (ilum, "iluminación estimada"), (img / ilum, "cociente")]):
    a.imshow(im, cmap="gray")
    a.set_title(t)
    a.axis("off")
guardar(fig, "h2_iluminacion.png")

img2 = enderezar(cargar(2), 6.0)             # TODO: usa el ángulo que midas tú (H4)
# TODO: recorta la zona del código y compara filtros de media 5×5, 15×1 y 1×5
#       (ndimage.uniform_filter con size=(filas, columnas)); ¿con cuáles se lee una sola fila?
# TODO: respuesta en frecuencia 2D de cada núcleo (np.fft.fft2 con relleno de ceros, fftshift).
