import numpy as np

rng = np.random.default_rng(1)
x = rng.standard_normal(10_000)
h = np.ones(31) / 31           # FIR, M = 31
L = 226                         # bloque
M = len(h)
N = L + M - 1                   # 256 = 2^8
H = np.fft.fft(h, N)
y = np.zeros(len(x) + M - 1)
for i in range(0, len(x), L):
    xb = x[i:i+L]
    Yb = np.fft.fft(xb, N) * H
    yb = np.real(np.fft.ifft(Yb))
    n = min(N, len(y) - i)
    y[i:i+n] += yb[:n]      # solapa y suma
print(np.allclose(y, np.convolve(x, h)))
