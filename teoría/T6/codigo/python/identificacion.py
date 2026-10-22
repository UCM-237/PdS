import numpy as np
from scipy import signal

rng = np.random.default_rng(11)
b, a = [0.2, 0.3], [1, -1.2, 0.72]
x = rng.standard_normal(50000)   # blanco
y = signal.lfilter(b, a, x)      # sistema
y += 0.3*rng.standard_normal(x.size)
f, Pxx = signal.welch(x, nperseg=256,
                      detrend=False)
_, Pxy = signal.csd(x, y, nperseg=256,
                    detrend=False)
H = Pxy/Pxx                  # Phi_yx/Phi_xx
_, Hr = signal.freqz(b, a, 2*np.pi*f)
k = [0, 32, 64]              # W=0,pi/4,pi/2
print(abs(H[k]), abs(Hr[k]))
