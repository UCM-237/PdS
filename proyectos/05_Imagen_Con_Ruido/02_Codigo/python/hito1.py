"""Hito 1: la imagen como señal. Completa las partes marcadas con TODO."""
import matplotlib.pyplot as plt
import numpy as np

from utilidades import cargar, guardar, placa_zonal, psnr

fig, ax = plt.subplots(2, 3, figsize=(12, 6.5))
for n, a in enumerate(ax.flat, 1):
    a.imshow(cargar(n), cmap="gray", vmin=0, vmax=1)
    a.set_title(f"imagen_{n}.png")
    a.axis("off")
guardar(fig, "h1_imagenes.png")

x = cargar(1, limpia=True)
for b in range(1, 8):
    xq = x          # TODO: cuantifica x con b bits (2**b niveles entre 0 y 1)
    print(f"{b} bits: PSNR = {psnr(xq, x):.2f} dB")
# TODO: representa la PSNR frente a b junto con el modelo Δ²/12.

z = placa_zonal(512)
# TODO: diezma z y la imagen 2 limpia por 4 (z[::4, ::4]) sin filtrar y con un paso bajo previo.

# TODO: periodograma medio de las filas: resta la media de cada fila, multiplica por
#       np.hanning, np.fft.rfft por filas, |X|² promediado sobre las filas.
