"""Hito 1: señal y espectro. Completa las partes marcadas con TODO."""
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

from utilidades import FS, anotaciones, cargar, guardar

t, x = cargar("ecg_A.csv")
_, xb = cargar("ecg_B.csv")
ref, tipos = anotaciones()
print(f"{len(x)} muestras, {len(ref)} latidos anotados en A")

fig, ax = plt.subplots(2, 1, figsize=(9, 4.5), constrained_layout=True)
ax[0].plot(t, x, lw=0.4)
ax[0].set(xlabel="t (s)", ylabel="mV", title="Registro A")
m = (t > 20) & (t < 24)
ax[1].plot(t[m], x[m])
ax[1].set(xlabel="t (s)", ylabel="mV", title="Detalle de 4 s")
# TODO: señala las ondas P, QRS y T de un latido; dibuja también el registro B
guardar(fig, "h1_tiempo.png")

f, P = signal.welch(x, FS, nperseg=8192)
fig, ax = plt.subplots(figsize=(8, 3), constrained_layout=True)
ax.semilogy(f, P)
ax.set(xlabel="f (Hz)", ylabel="PSD (mV²/Hz)")
guardar(fig, "h1_psd.png")
# TODO: marca la línea base, la red, la banda del QRS y el ruido muscular.
# TODO: FC por las rayas del espectro en 0–6 Hz y por la autocorrelación (np.correlate o
#       signal.correlate); compáralas con 60 / mean(diff(ref) / FS).
# TODO: amplitud de la raya de 50 Hz a partir de la potencia en 49–51 Hz.
