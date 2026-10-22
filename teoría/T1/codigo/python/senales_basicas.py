import numpy as np
import matplotlib.pyplot as plt

n = np.arange(-10, 11)          # eje temporal
delta = (n == 0).astype(float)  # δ[n]
u = (n >= 0).astype(float)      # u[n]
r = n * u                       # r[n] = n u[n]
x = 0.8**n * u                  # 0.8^n u[n]

plt.stem(n, x)
plt.xlabel("n"); plt.ylabel("x[n]")
plt.show()
