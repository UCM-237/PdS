import numpy as np

def alias(w, Ts):
    """Frecuencia discreta en [-π, π)."""
    W = w * Ts
    return (W + np.pi) % (2*np.pi) - np.pi

Ts = 2.0                        # s
w1 = 2*np.pi/10                 # rad/s
w2 = 2*np.pi/(10/6)             # rad/s
print(alias(w1, Ts), alias(w2, Ts))  # 0.4π
n = np.arange(20)
x1 = np.sin(w1 * Ts * n)
x2 = np.sin(w2 * Ts * n)
print(np.allclose(x1, x2))      # True
