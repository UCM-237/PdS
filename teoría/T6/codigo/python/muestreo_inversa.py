import numpy as np

rng = np.random.default_rng(0)
lam, N = 2.0, 100000
u = rng.random(N)                # U[0,1)
x = -np.log(1 - u)/lam           # F^-1(u)
print(x.mean(), 1/lam)           # media
print(x.var(ddof=1), 1/lam**2)   # varianza
print(np.mean(x > 1), np.exp(-lam))
