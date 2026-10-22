import numpy as np
from scipy import signal

# Ωp = 0,3π, Ωs = 0,5π, αs = 40 dB -> Hann
Wc = 0.4*np.pi              # (Ωp + Ωs)/2
L = 16                      # 3,11π/(0,2π)
n = np.arange(-L, L+1)
hd = Wc/np.pi * np.sinc(Wc/np.pi * n)
w = np.hanning(2*L + 3)[1:-1]
h = hd * w                  # 33 coef.
# h ya es causal si se indexa desde 0
W, H = signal.freqz(h, 1, 4096)
As = -20*np.log10(abs(H[W >= 0.5*np.pi]))
print(As.min())             # 44 dB
# Casi igual (extremos nulos):
h2 = signal.firwin(2*L + 1, 0.4,
                   window="hann")
