import numpy as np
from scipy import signal

fs = 44_100                     # Hz (CD)
t = np.arange(0, 0.1, 1/fs)
x = np.sin(2*np.pi*1000*t)      # 1 kHz
# Diezmado por 4 con filtro antialiasing
x4 = signal.decimate(x, 4)      # fs/4
# Cambio racional 44,1 kHz -> 48 kHz
y = signal.resample_poly(x, 160, 147)
print(len(x), len(x4), len(y))
