import numpy as np
from scipy import signal

fs = 1000
t = np.arange(0, 2, 1/fs)
x = signal.chirp(t, 50, 2, 400)  # 50->400
L, R, N = 128, 32, 256       # L, salto, FFT
w = np.hanning(L)
ini = np.arange(0, len(x) - L + 1, R)
X = np.array([np.fft.rfft(x[i:i+L]*w, N)
              for i in ini]).T   # (f, t)
f = np.fft.rfftfreq(N, 1/fs)
tm = (ini + L/2)/fs              # centros
pico = f[np.argmax(np.abs(X), axis=0)]
print(X.shape)                   # (129, 59)
print(np.c_[tm, pico][::10])     # f(t)
# Igual: signal.spectrogram(x, fs, w, ...)
