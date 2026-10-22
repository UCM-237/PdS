import numpy as np

x = np.array([1, 3, 4])
h = np.array([0, 2])
lin = np.convolve(x, h)     # [0, 2, 6, 8]
for N in (3, 4):            # N < 4 y N = 4
    Y = np.fft.fft(x, N) * np.fft.fft(h, N)
    y = np.real(np.fft.ifft(Y))
    print(N, np.round(y, 10))  # N=3: 8 2 6
print(lin)
