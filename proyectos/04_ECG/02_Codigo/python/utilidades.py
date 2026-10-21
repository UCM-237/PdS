"""Funciones de apoyo del proyecto «ECG». No hace falta modificarlas."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

FS = 360
DATOS = Path(__file__).resolve().parents[2] / "01_Datos"
FIGURAS = Path(__file__).resolve().parent / "figuras"
FIGURAS.mkdir(exist_ok=True)


def cargar(nombre):
    """Devuelve (t, x) en s y mV."""
    d = np.loadtxt(DATOS / nombre, delimiter=",", skiprows=1)
    return d[:, 0], d[:, 1]


def anotaciones(nombre="ecg_A_anotaciones.csv"):
    """Devuelve (muestra, tipo): índices de los picos R (desde 0) y 'N' o 'V'."""
    d = np.genfromtxt(DATOS / nombre, delimiter=",", skip_header=1, dtype=None, encoding="utf-8")
    return np.array([r[1] for r in d]), np.array([r[2] for r in d])


def evaluar(det, ref, tol=0.15):
    """Empareja cada latido de referencia con como mucho una detección a menos de tol s.
    Devuelve VP, FP, FN, sensibilidad (Se) y valor predictivo positivo (VPP)."""
    det = np.asarray(det)
    tol = int(tol * FS)
    usado = np.zeros(len(det), bool)
    vp = 0
    for r in ref:
        d = np.abs(det - r).astype(float)
        d[usado] = np.inf
        if len(d) and d.min() <= tol:
            usado[np.argmin(d)] = True
            vp += 1
    fn, fp = len(ref) - vp, len(det) - vp
    return {"VP": vp, "FP": fp, "FN": fn, "Se": vp / max(vp + fn, 1), "VPP": vp / max(vp + fp, 1)}


def guardar_latidos(nombre, muestras, tipos):
    with open(nombre, "w") as f:
        f.write("muestra,tipo\n")
        for m, t in zip(muestras, tipos):
            f.write(f"{int(m)},{t}\n")


def guardar(fig, nombre):
    fig.savefig(FIGURAS / nombre, dpi=130, bbox_inches="tight")
    plt.close(fig)
    print("figura:", FIGURAS / nombre)
