import numpy as np
from scipy import signal

rng = np.random.default_rng(10)
a, N = 0.8, 2**14
x = signal.lfilter([1], [1, -a],
                   rng.standard_normal(N))
f, P = signal.welch(x, fs=1, nperseg=256,
                    return_onesided=False,
                    detrend=False)  # Phi
W = 2*np.pi*f                  # f en ciclos
teo = 1/abs(1 - a*np.exp(-1j*W))**2
print(P[0], teo[0])              # ~ 25
print(P[64], teo[64])         # W=pi/2: 0.61
print(np.mean(P), x.var())       # potencia
