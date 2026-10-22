import numpy as np
from imagen_prueba import imagen_prueba

f = imagen_prueba()
g = np.round(255*(0.35 + 0.3*f))
g = g.astype(int)           # contraste bajo
h = np.bincount(g.ravel(), minlength=256)
F = np.cumsum(h)/g.size       # distribución
T = np.round(255*F).astype(int)  # s = T(r)
ge = T[g]
print(g.min(), g.max())          # 97 158
print(ge.min(), ge.max())        # 3 255
print(np.std(g), np.std(ge))     # 16.7 73.3
