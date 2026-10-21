"""Hito 1: señal y espectro. Completa las partes marcadas con TODO."""
import matplotlib.pyplot as plt
import numpy as np

from utilidades import actividades, cargar_actividad, guardar

for fecha in actividades():
    d = cargar_actividad(fecha)
    dt = np.diff(d["time"])
    print(f"{fecha}: {len(d)} muestras, {d['time'].iloc[-1] / 60:.1f} min, dt mediana {np.median(dt):.0f} s")

d = cargar_actividad(actividades()[0])
fig, ax = plt.subplots(3, 1, figsize=(10, 6), sharex=True)
t = d["time"] / 60
ax[0].plot(t, d["v_kmh"]); ax[0].set_ylabel("km/h")
ax[1].plot(t, d["heartrate"]); ax[1].set_ylabel("ppm")
ax[2].plot(t, d["altitude"]); ax[2].set_ylabel("m"); ax[2].set_xlabel("tiempo (min)")
guardar(fig, "h1_senales.png")
# TODO: histograma de dt y huecos de más de 15 s.
# TODO: anomalías (velocidad imposible, saltos de distancia, FC congelada).
# TODO: remuestreo a una rejilla uniforme (np.interp) y PSD de Welch (scipy.signal.welch).
