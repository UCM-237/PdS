import numpy as np

def emparejar(det, ref, tol):
    libres, vp = list(ref), 0
    for d in det:
        c = [r for r in libres
             if abs(r - d) <= tol]
        if c:   # el más cercano, una vez
            libres.remove(min(
                c, key=lambda r: abs(r - d)))
            vp += 1
    return vp, len(det) - vp, len(libres)

ref = [100, 300, 500, 700, 900]  # verdad
det = [102, 298, 450, 705, 898, 960]
vp, fp, fn = emparejar(det, ref, tol=10)
Se, VPP = vp/(vp + fn), vp/(vp + fp)
F1 = 2*Se*VPP/(Se + VPP)
print(vp, fp, fn, Se, VPP, F1)
