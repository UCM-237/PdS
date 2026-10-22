import numpy as np
from imagen_prueba import imagen_prueba

f = imagen_prueba()
M, N = f.shape
F = np.fft.fft2(f)
k = np.fft.fftfreq(M)*M          # 0..-1
l = np.fft.fftfreq(N)*N
K, L = np.meshgrid(k, l, indexing="ij")
D2 = K**2 + L**2
D0 = 20
H = np.exp(-D2/(2*D0**2))        # gaussiano
g = np.real(np.fft.ifft2(H*F))
E = np.abs(F)**2
print(np.sum(E*H**2)/np.sum(E))  # 0.958
print(f.mean(), g.mean())        # H[0,0]=1
