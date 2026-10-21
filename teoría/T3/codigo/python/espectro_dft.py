import numpy as np
import matplotlib.pyplot as plt

fs = 1000                       # Hz
N = 200                         # Δf = 5 Hz
n = np.arange(N)
x = 2*np.cos(2*np.pi*100*n/fs) \
    + 0.5*np.cos(2*np.pi*152*n/fs)
w = np.hanning(N)               # ventana
X = np.fft.rfft(x * w)          # k = 0..N/2
f = np.arange(len(X)) * fs / N  # Hz
A = 2 * np.abs(X) / np.sum(w)   # amplitud
print(f[np.argmax(A)], A.max()) # 100 Hz, 2
plt.plot(f, 20*np.log10(A + 1e-12))
plt.xlabel("f (Hz)"); plt.show()
