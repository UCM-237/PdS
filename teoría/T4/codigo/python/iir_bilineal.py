import numpy as np
from scipy import signal

fs = 200e3                     # Hz
Wp = 2*np.pi*25e3/fs           # 0,25π
Ws = 2*np.pi*55e3/fs           # 0,55π
# 1) Predistorsión con T = 2
wp, ws = np.tan(Wp/2), np.tan(Ws/2)
# 2) Filtro continuo
N, wc = signal.buttord(wp, ws, 0.5, 15,
                       analog=True)
b, a = signal.butter(N, wc, analog=True)
# 3) Bilineal: fs = 1/T = 0,5
bz, az = signal.bilinear(b, a, fs=0.5)
# Lo mismo en un paso (frecuencias en Hz):
N2, Wn = signal.buttord(25e3, 55e3, 0.5,
                        15, fs=fs)
bz2, az2 = signal.butter(N2, Wn, fs=fs)
print(N, np.allclose(az, az2))  # 3 True
