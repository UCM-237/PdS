import numpy as np
from scipy import signal

fs = 500
t = np.arange(0, 1, 1/fs)
rng = np.random.default_rng(3)
x = np.exp(-((t - 0.4)/0.05)**2) \
    + 0.15*rng.standard_normal(t.size)
b, a = signal.butter(3, 15, fs=fs)
y1 = signal.lfilter(b, a, x)    # retrasa
y2 = signal.filtfilt(b, a, x)   # |H|^2
print(t[np.argmax(y1)], t[np.argmax(y2)])
