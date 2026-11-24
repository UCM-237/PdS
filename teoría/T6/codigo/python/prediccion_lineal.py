import numpy as np
from scipy import linalg, signal

rng = np.random.default_rng(2)
N, p = 8000, 4
w = rng.standard_normal(N)
x = signal.lfilter([1], [1, -1.6, 0.9], w)
x[[2000, 5000]] += 6          # clics
r = np.correlate(x, x, 'full')[N-1:]/N
a = linalg.solve_toeplitz(r[:p],
                          r[1:p+1])
# e[n] = x[n] - sum_k a_k x[n-k]
e = signal.lfilter(np.r_[1, -a], [1], x)
S = 1.4826*np.median(abs(e))
print(np.round(a, 2))   # 1.6 -0.9 0 0
print(np.flatnonzero(abs(e) > 5*S))
