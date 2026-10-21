import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# Bordes normalizados a π (1 = fs/2)
Wp = [0.45, 0.65]; Ws = [0.3, 0.75]
N, Wn = signal.buttord(Wp, Ws, 1, 40)
print(N)                    # 7: orden 14
sos = signal.butter(N, Wn, "bandpass",
                    output="sos")
W, H = signal.sosfreqz(sos, 2000)
plt.plot(W/np.pi, 20*np.log10(abs(H) + 1e-12))
plt.xlabel("Ω/π"); plt.ylim(-80, 3)
plt.show()
# Filtrar una señal: signal.sosfilt(sos, x)
