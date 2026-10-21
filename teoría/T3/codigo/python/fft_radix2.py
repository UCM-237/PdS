import numpy as np

rng = np.random.default_rng(0)
x = rng.standard_normal(1024)
N = len(x)
b = int(np.log2(N))             # N = 2^b
# Reordenación por inversión de bits
r = [int(f"{i:0{b}b}"[::-1], 2)
     for i in range(N)]
X = x[r].astype(complex)
m = 2                           # tamaño DFT
while m <= N:                   # b etapas
    B = X.reshape(N // m, m)    # bloques
    F, G = B[:, :m//2], B[:, m//2:]
    W = np.exp(-2j*np.pi*np.arange(m//2)/m)
    X = np.hstack([F + W*G, F - W*G]).ravel()
    m *= 2                      # mariposas
print(np.allclose(X, np.fft.fft(x)))
