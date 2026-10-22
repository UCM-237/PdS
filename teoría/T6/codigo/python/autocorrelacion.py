import numpy as np

def xcorr(x, y, L):
    """Media de x[n+l]y[n] (insesgada)."""
    N = len(x)
    c = np.correlate(x, y, "full")
    c = c[N-1-L:N+L]
    l = np.arange(-L, L + 1)
    return l, c/(N - abs(l))

rng = np.random.default_rng(7)
N = 1001
x = 5 + rng.standard_normal(N)  # N(5,1) iid
u = 2 + 4*rng.random(N)         # U[2,6] iid
l, px = xcorr(x, x, 100)
_, pu = xcorr(u, u, 100)
print(px[100], px[150])         # ~ 26, ~ 25
print(pu[100], pu[150])       # ~ 17.3, ~ 16
