import numpy as np

n = np.arange(0, 1000)
x = 0.9**n                   # 0.9^n u[n]
E = np.sum(np.abs(x)**2)     # 1/(1-0.81)

N = 10_000
m = np.arange(-N, N + 1)
y = 3 * np.cos(0.1 * np.pi * m)
P = np.sum(np.abs(y)**2) / (2*N + 1)  # 9/2
print(f"E = {E:.3f}, P = {P:.3f}")
