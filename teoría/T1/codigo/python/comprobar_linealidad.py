import numpy as np

def T(x):                    # sistema a estudiar
    return x**2

rng = np.random.default_rng(0)
x1, x2 = rng.standard_normal((2, 50))
a, b = 2.0, -3.0
izq = T(a*x1 + b*x2)
der = a*T(x1) + b*T(x2)
print("¿Lineal?", np.allclose(izq, der))
