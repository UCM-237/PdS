"""Hito 4: DFT 2D, desenfoque y cadena completa. Completa las partes marcadas con TODO."""
import matplotlib.pyplot as plt
import numpy as np

from utilidades import cargar, espectro_2d, frecuencias_2d, guardar, guardar_restaurada

y3 = cargar(3)
FX, FY = frecuencias_2d(y3.shape)
ext = (FX[0, 0], FX[0, -1], FY[-1, 0], FY[0, 0])
fig, ax = plt.subplots(1, 2, figsize=(10, 4))
for a, v in zip(ax, (False, True)):
    a.imshow(espectro_2d(y3, ventana=v), cmap="magma", extent=ext)
    a.set(title="con ventana" if v else "sin ventana", xlabel="fₓ (ciclos/px)", ylabel="f_y (ciclos/px)")
guardar(fig, "h4_espectro_imagen3.png")
# TODO: detecta los picos de la interferencia (por ejemplo, donde log|X| supera mucho a su
#       mediana local) y construye un filtro de muescas 2D. Ojo: espectro_2d está centrado
#       con fftshift y np.fft.fft2 no.

# TODO: imagen desenfocada: perfil radial de log|Y|², radio del disco y deconvolución de
#       Wiener X = conj(H)·Y / (|H|² + K).

for n in range(1, 7):
    restaurada = cargar(n)     # TODO: tu cadena
    guardar_restaurada(n, restaurada)
