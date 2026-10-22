import numpy as np
import matplotlib.pyplot as plt

Ts = 0.1                        # s
n = np.arange(0, 11)
xn = np.sin(2*np.pi*1*n*Ts)     # 1 Hz
t = np.linspace(0, 1, 1001)
# Orden cero: se mantiene la última muestra
k = np.floor(t / Ts).astype(int)
y0 = xn[np.minimum(k, n[-1])]
# Orden uno (no causal): une las muestras
y1 = np.interp(t, n*Ts, xn)
x = np.sin(2*np.pi*t)
print(np.max(abs(y0 - x)), np.max(abs(y1 - x)))
plt.plot(t, y0, t, y1, t, x); plt.show()
