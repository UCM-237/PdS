import numpy as np

rng = np.random.default_rng(5)
N, L = 512, 9           # L: longitud
x = np.repeat(rng.integers(0, 2, 64), 8)
h = np.zeros(N); h[:L] = 1/L  # movimiento
H = np.fft.fft(h)
y = np.real(np.fft.ifft(np.fft.fft(x)*H))
y += 0.02*rng.standard_normal(N)
Y = np.fft.fft(y)
for K in (0, 1e-3, 1e-2, 1e-1):
    G = np.conj(H)/(abs(H)**2 + K)
    xe = np.real(np.fft.ifft(G*Y))
    print(K, np.sqrt(np.mean((xe - x)**2)))
