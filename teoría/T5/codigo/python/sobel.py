import numpy as np
from scipy.signal import convolve2d
from imagen_prueba import imagen_prueba

f = imagen_prueba()
sx = np.array([[1, 0, -1],
               [2, 0, -2],
               [1, 0, -1]])      # d/dn
media = np.ones((5, 5))/25
gx = convolve2d(f, sx, mode="same")
gy = convolve2d(f, sx.T, mode="same")
g = np.hypot(gx, gy)           # |gradiente|
fs = convolve2d(f, media, mode="same")
bordes = g > 0.5
print(bordes.mean())             # 0.18
print(f[80, 10:20])              # degradado
print(gx[80, 10:20])            # 8*0.25/256
