import numpy as np


def imagen_prueba(N=256):
    """Imagen sintética N x N en [0, 1]."""
    n = np.arange(N)/N
    x, y = np.meshgrid(n, n)
    f = 0.35 + 0.25*x            # degradado
    f[(x-.3)**2 + (y-.32)**2 < .18**2] = .85
    f[(x > 0.58) & (x < 0.9)
      & (y > 0.12) & (y < 0.45)] = 0.12
    fr = (y > 0.6) & (y < 0.9) \
        & (x > 0.08) & (x < 0.48)
    f[fr] = .5 + .4*np.cos(2*np.pi*16*x[fr])
    r = np.hypot(x - 0.73, y - 0.75)
    an = r < 0.16
    f[an] = 0.5 + 0.4*np.cos(2*np.pi*120
                              * r[an]**2)
    return f


if __name__ == "__main__":
    f = imagen_prueba()
    print(f.shape, f.min(), f.max())
