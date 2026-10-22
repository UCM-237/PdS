import numpy as np

rng = np.random.default_rng(6)
mu = np.array([1.0, 2.0])
S = np.array([[2.0, 1.2],
              [1.2, 1.0]])      # covarianza
L = np.linalg.cholesky(S)        # S = L L^T
Z = rng.standard_normal((2, 100000))
X = mu[:, None] + L @ Z          # 2 x N
print(X.mean(axis=1))            # ~ mu
print(np.cov(X))                 # ~ S
lam, V = np.linalg.eigh(S)       # ejes
print(lam)                      # 0.2, 2.8
