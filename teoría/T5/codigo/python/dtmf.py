import numpy as np

fs = 8000
t = np.arange(0, 0.1, 1/fs)   # 800 muestras
x = np.sin(2*np.pi*852*t) \
    + np.sin(2*np.pi*1336*t)     # tecla 8
rng = np.random.default_rng(0)
x += 0.5*rng.standard_normal(t.size)
N = 4096
w = np.hamming(x.size)
X = np.abs(np.fft.rfft(x*w, N))
f = np.fft.rfftfreq(N, 1/fs)
baja = (f > 650) & (f < 1000)
alta = (f > 1150) & (f < 1550)
fb = f[baja][np.argmax(X[baja])]
fa = f[alta][np.argmax(X[alta])]
filas = np.array([697, 770, 852, 941])
cols = np.array([1209, 1336, 1477])
teclas = ["123", "456", "789", "*0#"]
i = np.argmin(abs(filas - fb))
j = np.argmin(abs(cols - fa))
print(fb, fa, teclas[i][j])      # ... 8
