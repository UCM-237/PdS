import numpy as np
from scipy import signal

wp = 2*np.pi*1e3; ws = 2*np.pi*5e3
ap, as_ = 1, 40
for f in (signal.buttord, signal.cheb1ord,
          signal.cheb2ord, signal.ellipord):
    N, wn = f(wp, ws, ap, as_, analog=True)
    print(f.__name__, N)   # 4, 3, 3, 3
b, a = signal.cheby1(3, ap, wp, analog=True)
b, a = signal.cheby2(3, as_, ws,
                     analog=True)
b, a = signal.ellip(3, ap, as_, wp,
                    analog=True)
