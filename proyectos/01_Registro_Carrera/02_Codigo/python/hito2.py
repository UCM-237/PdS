"""Hito 2: filtrado. Completa las partes marcadas con TODO."""
import numpy as np

from utilidades import cargar_actividad, verdad_desarrollo


def ema(t, x, tau):
    """Media móvil exponencial de entrenamiento/main.py, válida con muestreo irregular."""
    y = np.empty(len(x))
    y[0] = x[0]
    for k in range(1, len(x)):
        a = 1 - np.exp(-(t[k] - t[k - 1]) / tau)
        y[k] = a * x[k] + (1 - a) * y[k - 1]
    return y


d = cargar_actividad("desarrollo_01.csv")
v_ema = ema(d["time"].to_numpy(), d["v_kmh"].to_numpy(), 10)
print("cambios reales (s):", verdad_desarrollo()["desarrollo_01.csv"][2])
# TODO: H(z) de la EMA con Δt = 1 s, respuesta en frecuencia, corte y retardo.
# TODO: Butterworth de fase cero (scipy.signal.butter + sosfiltfilt) y mediana móvil sobre la
#       señal remuestreada; retardo de cada filtro en los cambios de las sintéticas.
# TODO: desnivel positivo de cada actividad real sin filtrar, filtrado y con histéresis.
