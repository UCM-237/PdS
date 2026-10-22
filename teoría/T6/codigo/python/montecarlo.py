import numpy as np

rng = np.random.default_rng(4)
for N in (100, 10000, 1000000):
    x = rng.standard_normal(N)  # X ~ N(0,1)
    g = np.cos(x)                # E{cos X}?
    est = g.mean()
    err = g.std(ddof=1)/np.sqrt(N)
    print(N, est, err)
print(np.exp(-0.5))              # exacto
