import numpy as np

rng = np.random.default_rng(3)
f = lambda x: 6*x*(1 - x)        # objetivo
M = 1.5                 # f <= M*q, q=U[0,1]
N = 100000
x = rng.random(N)          # candidatos de q
u = rng.random(N)
acept = u*M <= f(x)
xs = x[acept]
print(acept.mean(), 1/M)         # ~ 0.667
print(xs.mean(), xs.var())       # 0.5, 0.05
