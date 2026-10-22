import numpy as np

rng = np.random.default_rng(5)
N = 100000
x1 = rng.uniform(2, 4, N)        # U[2,4]
x2 = x1 + rng.standard_normal(N) # N(x1,1)
X = np.c_[x1, x2]                # N x 2
print(X.mean(axis=0))            # 3, 3
print(np.cov(X.T))      # [1/3 1/3; 1/3 4/3]
print(np.corrcoef(X.T)[0, 1])    # 0.5
