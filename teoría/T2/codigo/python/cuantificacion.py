import numpy as np

b = 8                       # bits
V = 1.0                     # margen [-V, V)
D = 2*V / 2**b              # escalón Δ
n = np.arange(100_000)
x = 0.99*V*np.sin(2*np.pi*0.01234*n)
xq = D * np.round(x / D)    # redondeo
e = xq - x
print(np.var(e), D**2/12)   # ≈ Δ²/12
snr = 10*np.log10(np.var(x) / np.var(e))
print(snr, 6.02*b + 1.76)   # dB
