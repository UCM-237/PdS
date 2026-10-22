import numpy as np

rng = np.random.default_rng(9)
Ts = 0.01
t = np.arange(0, 6, Ts)
x = np.sinc(t - 2)               # buscada
y = np.sinc(t - 3) \
    + rng.standard_normal(t.size) # recibida
c = np.correlate(y, x, "full")  # y[n+l]x[n]
lags = np.arange(-len(x) + 1, len(y))
tau = lags[np.argmax(c)]*Ts
print(tau)                       # ~ 1 s
