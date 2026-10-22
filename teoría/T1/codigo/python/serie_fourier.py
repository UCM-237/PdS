import numpy as np
import matplotlib.pyplot as plt

T = 1.0                        # periodo
t = np.linspace(-T, T, 2000)
K = 19                         # armónicos
xK = np.zeros_like(t)
for k in range(1, K + 1):
    ck = np.sinc(k / 2)        # c_k, cuadrada par
    xK += 2*ck*np.cos(2*np.pi*k*t/T)
plt.plot(t, xK); plt.xlabel("t (s)")
plt.show()
