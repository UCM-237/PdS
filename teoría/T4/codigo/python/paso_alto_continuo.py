import numpy as np
from scipy import signal

# Paso 4 kHz, 0,1 dB; supresión 1 kHz, 40 dB
wp_ = 2*np.pi*4e3; ws_ = 2*np.pi*1e3
# 1) Prototipo paso bajo con wp = 1
ws = wp_ / ws_                      # = 4
N, wc = signal.buttord(1, ws, 0.1, 40,
                       analog=True)
b, a = signal.butter(N, wc, analog=True)
# 2) Paso bajo -> paso alto: s = wp_/s
bh, ah = signal.lp2hp(b, a, wp_)
# Equivale a hacerlo en un solo paso:
N2, wn = signal.buttord(wp_, ws_, 0.1, 40,
                        analog=True)
b2, a2 = signal.butter(N2, wn, "highpass",
                       analog=True)
print(N, N2)                        # 5, 5
