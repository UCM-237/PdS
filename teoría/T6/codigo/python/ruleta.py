import numpy as np

rng = np.random.default_rng(1)
p = np.array([.1, .1, .1, .1, .1, .5])
F = np.cumsum(p)                 # 0.1 ... 1
u = rng.random(60000)
x = np.searchsorted(F, u, 'right') + 1
frec = np.bincount(x, minlength=7)[1:]
print(frec/u.size)               # ~ p
print(x.mean(), np.sum(np.arange(1, 7)*p))
