import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

fs = 8000
t = np.arange(0, 2, 1/fs)
x = signal.chirp(t, 200, 2, 3000)
# STFT: tramos de 256, solape del 75 %
Nw, paso = 256, 64
w = np.hanning(Nw)
ini = range(0, len(x) - Nw, paso)
S = np.array([np.fft.rfft(w*x[i:i+Nw])
              for i in ini]).T
S = np.abs(S)
f = np.arange(Nw//2 + 1) * fs / Nw
tt = (np.array(ini) + Nw/2) / fs
print(S.shape)                  # (129, 121)
plt.pcolormesh(tt, f, 20*np.log10(S + 1e-9))
plt.xlabel("t (s)"); plt.ylabel("f (Hz)")
plt.show()
