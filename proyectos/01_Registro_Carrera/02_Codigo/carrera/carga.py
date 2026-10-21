"""Carga de los registros de actividad exportados de Strava.

Cada CSV contiene los *streams* de una actividad:

- ``time``       tiempo desde el inicio (s), muestreo NO uniforme
- ``distance``   distancia acumulada (m), calculada por Strava a partir del GPS
- ``heartrate``  frecuencia cardiaca (ppm) de la banda/pulsometro
- ``velocity``   velocidad (m/s) ya suavizada por Strava (``velocity_smooth``)
- ``altitude``   altitud (m)
"""
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
DIR_DATOS = RAIZ_PROYECTO / "01_Datos"
DIR_HITOS = RAIZ_PROYECTO / "03_Hitos"
DIR_ENTREGA = RAIZ_PROYECTO / "04_Entrega_Final"

COLUMNAS = ["time", "distance", "heartrate", "velocity", "altitude"]


def listar_actividades(directorio=DIR_DATOS):
    """Devuelve las rutas de los CSV de actividad ordenadas por fecha."""
    return sorted(Path(directorio).glob("actividad_*.csv"))


def nombre_actividad(ruta):
    """'actividad_2026-01-07.csv' -> '2026-01-07'."""
    return Path(ruta).stem.replace("actividad_", "")


def cargar_actividad(ruta):
    """Lee un CSV y devuelve un DataFrame con las columnas basicas.

    Se recalculan ``speed_kmh`` y ``distance_km`` en lugar de fiarse de las
    columnas derivadas que trae el fichero, y se comprueba que el tiempo es
    estrictamente creciente.
    """
    df = pd.read_csv(ruta, index_col=0)[COLUMNAS].astype(float)
    if np.any(np.diff(df["time"]) <= 0):
        raise ValueError(f"{ruta}: el vector de tiempos no es estrictamente creciente")
    df["speed_kmh"] = df["velocity"] * 3.6
    df["distance_km"] = df["distance"] / 1000
    df.attrs["nombre"] = nombre_actividad(ruta)
    return df


def cargar_todas(directorio=DIR_DATOS):
    """Diccionario {fecha: DataFrame} con todas las actividades."""
    return {nombre_actividad(r): cargar_actividad(r) for r in listar_actividades(directorio)}
