import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

fm = 1.0                        # banda (Hz)
fs = 3.0                        # fs > 2 fm
Ts = 1 / fs
n = np.arange(-300, 301)
x = np.sinc(fm * n * Ts)**2     # banda fm
W, X = signal.freqz(x, 1, worN=2048,
                    whole=True)     # [0, 2π)
W = W - np.pi                   # [-π, π)
X = np.fft.fftshift(X)
plt.plot(W / Ts, np.abs(X) * Ts)  # ω = Ω/Ts
plt.xlabel("ω (rad/s)")
plt.show()
