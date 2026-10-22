import numpy as np

rng = np.random.default_rng(2)
N = 50000
u1, u2 = rng.random(N), rng.random(N)
r = np.sqrt(-2*np.log(1 - u1))   # radio
th = 2*np.pi*u2                  # ángulo
z1, z2 = r*np.cos(th), r*np.sin(th)
x = 5 + 2*z1                     # N(5, 4)
print(z1.mean(), z1.std(), z2.std())
print(np.corrcoef(z1, z2)[0, 1]) # ~ 0
print(x.mean(), x.var())         # ~ 5, 4
print(np.mean(abs(z1) < 1))      # ~ 0.683
