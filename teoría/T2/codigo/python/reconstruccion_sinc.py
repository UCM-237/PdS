import numpy as np
import matplotlib.pyplot as plt

Ts = 0.1                        # s
n = np.arange(-50, 51)
xn = np.cos(2*np.pi*2*n*Ts)     # 2 Hz < fs/2
t = np.linspace(-1, 1, 1001)
# y(t) = Σ x[n] sinc((t - nTs)/Ts)
S = np.sinc((t[:, None] - n*Ts) / Ts)
y = S @ xn
print(np.max(np.abs(y - np.cos(4*np.pi*t))))
plt.plot(t, y); plt.stem(n*Ts, xn)
plt.xlim(-1, 1); plt.show()
