import numpy as np
from scipy import signal

rng = np.random.default_rng(8)
a, N = 0.9, 200000
w = rng.standard_normal(N)    # blanco, s2=1
x = signal.lfilter([1], [1, -a], w)
x = x[1000:]               # sin transitorio
for l in (0, 1, 5, 10):
    est = np.mean(x[l:]*x[:len(x)-l])
    teo = a**l/(1 - a**2)
    print(l, est, teo)
