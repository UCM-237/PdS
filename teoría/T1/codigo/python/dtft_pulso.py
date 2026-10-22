import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

x = np.ones(5)                 # pulso, L = 5
w, X = signal.freqz(x, 1, worN=1024,
                    whole=True)   # [0, 2π)
plt.plot(w, np.abs(X))
plt.xlabel("Ω (rad/muestra)")
plt.show()
