import numpy as np
from scipy import signal

# Paso alto: Ωs = 0,4π, Ωp = 0,55π,
# rizado δ = 0,01 en las dos bandas
A = -20*np.log10(0.01)          # 40 dB
N, beta = signal.kaiserord(A, 0.15)
N += (N % 2 == 0)               # impar
h = signal.firwin(N, 0.475, pass_zero=False,
                  window=("kaiser", beta))
print(N, round(beta, 3))        # 31, 3.395
# Parks-McClellan: rizado uniforme
hpm = signal.remez(N, [0, 0.4, 0.55, 1],
                   [0, 1], fs=2)
