import numpy as np

n = np.arange(0, 32)
x1 = np.cos(np.pi/4 * n)       # π/4
x2 = np.cos(7*np.pi/4 * n)     # 2π - π/4
x3 = np.cos(9*np.pi/4 * n)     # π/4 + 2π
print(np.max(np.abs(x1 - x2)))   # ≈ 0
print(np.max(np.abs(x1 - x3)))   # ≈ 0
