import numpy as np

x = np.array([1, 3, 4, 0])
N = len(x)
n = np.arange(N)
k = n.reshape(-1, 1)
W = np.exp(-2j*np.pi*k*n/N)     # matriz DFT
X = W @ x                       # O(N²)
print(np.round(X, 10))  # 8, -3-3j, 2, -3+3j
print(np.allclose(X, np.fft.fft(x)))
xr = (W.conj() @ X) / N         # IDFT
print(np.real_if_close(np.round(xr, 10)))
