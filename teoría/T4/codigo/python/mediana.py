import numpy as np
from scipy import signal

rng = np.random.default_rng(4)
n = np.arange(200)
s = (n >= 100).astype(float)  # escalón
x = s + 0.05*rng.standard_normal(200)
x[[30, 31, 140]] += [2, 2, -2]  # impulsos
L = 7                           # 2K+1
media = np.convolve(x, np.ones(L)/L,
                    'same')
med = signal.medfilt(x, L)
for y in (media, med):
    e = abs(y - s)[20:180]
    print(e.max())              # error
