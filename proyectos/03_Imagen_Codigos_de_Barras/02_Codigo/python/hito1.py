"""Hito 1: la fila como señal. Completa las partes marcadas con TODO."""
import matplotlib.pyplot as plt
import numpy as np

from ean13 import modulos
from utilidades import cargar, codigos_desarrollo, guardar

fig, ax = plt.subplots(2, 3, figsize=(11, 5.5), constrained_layout=True)
for i, a in enumerate(ax.flat, 1):
    a.imshow(cargar(i), cmap="gray", vmin=0, vmax=1)
    a.set_title(f"codigo_{i}.png")
    a.axis("off")
guardar(fig, "h1_imagenes.png")

img = cargar(1)
fila = img.shape[0] // 2          # TODO: elige una fila que cruce el código
p = img[fila]
fig, ax = plt.subplots(figsize=(9, 3), constrained_layout=True)
ax.plot(p)
ax.set(xlabel="columna (px)", ylabel="nivel", title=f"Fila {fila} de la imagen 1")
guardar(fig, "h1_fila.png")

codigo = codigos_desarrollo()[1]
ideal = np.array([int(c) for c in modulos(codigo)])     # 1 = barra (oscura), 95 módulos
print(f"código {codigo}: {len(ideal)} módulos")
# TODO: localiza el primer y el último borde del código en p y calcula m = anchura / 95.
# TODO: dibuja la señal ideal escalada a m píxeles por módulo sobre la fila muestreada.
# TODO: espectro de la fila (con ventana y relleno de ceros) y envolvente sinc²(f·m).
# TODO: repite la medida del módulo en la imagen 6 y compara las anchuras de las rachas.
