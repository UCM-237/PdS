import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

wp = 2*np.pi*1e3; ws = 2*np.pi*5e3  # rad/s
ap, as_ = 1, 40                    # dB
N, wc = signal.buttord(wp, ws, ap, as_,
                       analog=True)
print(N, wc)                       # 4, 7439
b, a = signal.butter(N, wc, analog=True)
w = np.linspace(0, 2*np.pi*8e3, 1000)
w, H = signal.freqs(b, a, w)
plt.plot(w/(2*np.pi), 20*np.log10(abs(H)))
plt.xlabel("f (Hz)"); plt.ylabel("dB")
plt.show()
