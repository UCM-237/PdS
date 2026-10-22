import numpy as np

N = 1024
n = np.arange(N)
x = 1.5*(n > 100) - 2.2*(n > 240) \
    + 1.6*(n > 410) + 1.2*(n > 512)
rng = np.random.default_rng(4)
y = x + 0.4*rng.standard_normal(N)
c, a = [], y                      # análisis
for j in range(5):
    c.append((a[0::2] - a[1::2])/2**.5)
    a = (a[0::2] + a[1::2])/2**.5
s = np.median(abs(c[0]))/0.6745   # sigma
u = s*np.sqrt(2*np.log(N))        # umbral
for d in reversed(c):             # síntesis
    d = np.where(abs(d) > u, d, 0)  # duro
    z = np.empty(2*a.size)
    z[0::2] = (a + d)/2**.5
    z[1::2] = (a - d)/2**.5
    a = z
rms = lambda e: np.sqrt(np.mean(e**2))
print(s, u)                      # 0.40 1.49
print(rms(y - x), rms(a - x))    # 0.40 0.12
