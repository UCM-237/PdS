import numpy as np
from scipy import signal

fs, rng = 8000, np.random.default_rng(1)
t = np.arange(0, 3, 1/fs)
s = np.sin(2*np.pi*440*t)*(t > 1)
x = s + 0.3*rng.standard_normal(t.size)
f, tt, X = signal.stft(x, fs, nperseg=256)
A = abs(X)**2
Pv = A[:, tt < 0.9].mean(axis=1,
                         keepdims=True)
a, b = 2.0, 0.02              # alfa, beta
P = np.maximum(A - a*Pv, b*A)
S = np.sqrt(P)*np.exp(1j*np.angle(X))
_, y = signal.istft(S, fs, nperseg=256)
y = y[:x.size]
snr = lambda z: 10*np.log10(
    np.sum(s**2)/np.sum((z - s)**2))
print(snr(x), snr(y))         # dB
