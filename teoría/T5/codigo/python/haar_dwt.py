import numpy as np
def dwt_haar(x, J):      # [d1, ..., dJ, aJ]
    a, c = np.asarray(x, float), []
    for _ in range(J):            # análisis
        c.append((a[0::2] - a[1::2])/2**.5)
        a = (a[0::2] + a[1::2])/2**.5
    return c + [a]

def idwt_haar(c):
    a = c[-1]
    for d in reversed(c[:-1]):    # síntesis
        x = np.empty(2*a.size)
        x[0::2] = (a + d)/2**.5
        x[1::2] = (a - d)/2**.5
        a = x
    return a
n = np.arange(1024)
x = np.sin(2*np.pi*n/512) + (n > 300)
c = dwt_haar(x, 4)
print([v.size for v in c])      # 512 ... 64
E = [np.sum(v**2) for v in c]
print(np.round(E, 2), np.sum(x**2))
print(abs(idwt_haar(c) - x).max())  # ~1e-15
