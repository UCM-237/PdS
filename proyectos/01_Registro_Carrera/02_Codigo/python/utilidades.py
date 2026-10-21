"""Funciones de apoyo del proyecto «Registro de carrera». No hace falta modificarlas."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DATOS = Path(__file__).resolve().parents[2] / "01_Datos"
SINTETICAS = DATOS / "sinteticas"
FIGURAS = Path(__file__).resolve().parent / "figuras"
FIGURAS.mkdir(exist_ok=True)


def actividades():
    """Fechas de las actividades reales: ['2026-01-07', ...]."""
    return sorted(p.stem.replace("actividad_", "") for p in DATOS.glob("actividad_*.csv"))


def cargar_actividad(nombre):
    """DataFrame con time (s), distance (m), heartrate (ppm), velocity (m/s), altitude (m) y
    v_kmh. 'nombre' es una fecha ('2026-01-07') o un fichero de sinteticas ('desarrollo_01.csv')."""
    ruta = SINTETICAS / nombre if nombre.endswith(".csv") else DATOS / f"actividad_{nombre}.csv"
    df = pd.read_csv(ruta, index_col=0)[["time", "distance", "heartrate", "velocity", "altitude"]].astype(float)
    df["v_kmh"] = df["velocity"] * 3.6
    return df


def verdad_desarrollo():
    """{fichero: (tipo, sigma_kmh, array de instantes de cambio en s)} de las sintéticas de desarrollo."""
    out = {}
    for linea in (SINTETICAS / "desarrollo_verdad.csv").read_text().splitlines()[1:]:
        s, tipo, sigma, cambios = linea.split(",")
        out[s] = (tipo, float(sigma), np.array([float(c) for c in cambios.split()]))
    return out


def evaluar_detecciones(detectados, reales, tolerancia=20.0):
    """Empareja cada instante real con el detectado más cercano a menos de 'tolerancia' s.
    Devuelve (TP, FP, FN)."""
    det = sorted(detectados)
    tp = 0
    for r in reales:
        if not det:
            break
        j = int(np.argmin([abs(d - r) for d in det]))
        if abs(det[j] - r) <= tolerancia:
            det.pop(j)
            tp += 1
    return tp, len(det), len(reales) - tp


def guardar_prueba(resultados):
    """resultados: {fichero: (tipo, lista de instantes en s)}. Escribe prueba.csv."""
    with open("prueba.csv", "w") as f:
        f.write("sesion,tipo,cambios_s\n")
        for s, (tipo, c) in sorted(resultados.items()):
            f.write(f"{s},{tipo}," + " ".join(f"{x:.0f}" for x in c) + "\n")


def guardar(fig, nombre):
    fig.savefig(FIGURAS / nombre, dpi=130, bbox_inches="tight")
    plt.close(fig)
    print("figura:", FIGURAS / nombre)
