import numpy as np

def hampel_movil(x, K=10, t=3):
    y, at = x.copy(), np.zeros(x.size, bool)
    for n in range(K, x.size - K):
        v = x[n-K:n+K+1]
        m = np.median(v)
        S = 1.4826*np.median(abs(v - m))
        if abs(x[n] - m) > t*S:
            y[n], at[n] = m, True
    return y, at

rng = np.random.default_rng(6)
x = rng.standard_normal(1000)
x[::97] += 8                  # atípicos
mad = np.median(abs(x - np.median(x)))
print(x.std(), 1.4826*mad)    # sigma = 1
y, at = hampel_movil(x)
print(at[::97].sum(), at.sum())
