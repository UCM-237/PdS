import numpy as np
from scipy import signal

fs, f0 = 5000, 50
L = fs // f0                    # 100
a = 0.9                         # polos
# H(z) = (1+a)/2 (1 - z^-L)/(1 - a z^-L)
b = np.zeros(L + 1); b[[0, L]] = [1, -1]
d = np.zeros(L + 1); d[[0, L]] = [1, -a]
b *= (1 + a) / 2
f = np.array([7, 50, 150, 175])     # Hz
_, H = signal.freqz(b, d, f, fs=fs)
print(np.round(abs(H), 3))  # 1 0 0 1
