import numpy as np
from scipy import signal

# y[n] = 0.8 y[n-1] + 0.2 x[n]
b, a = [0.2], [1, -0.8]
d = np.zeros(30); d[0] = 1     # δ[n]
h = signal.lfilter(b, a, d)    # 0.2·0.8^n
polos = np.roots(a)            # [0.8]
print("¿Estable?", np.all(np.abs(polos) < 1))
w, H = signal.freqz(b, a)      # [0, π)
