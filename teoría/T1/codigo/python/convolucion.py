import numpy as np

x = np.array([1, 2, 1])      # n = 0..2
h = np.array([1, 1, 1, 1])   # n = 0..3
y = np.convolve(x, h)        # n = 0..5
print(y)                     # [1 3 4 4 3 1]
print(len(y) == len(x) + len(h) - 1)
