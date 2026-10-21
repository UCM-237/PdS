"""Hito 2: filtrado. Completa las partes marcadas con TODO."""
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

from utilidades import FS, anotaciones, cargar, guardar

t, x = cargar("ecg_A.csv")
_, s = cargar("ecg_A_limpio.csv")          # solo para medir la distorsión
s0 = s - np.median(s)
ref, _ = anotaciones()


def error_uv(y):
    """Error RMS (µV) frente a la señal limpia, sin tener en cuenta el nivel de continua."""
    return 1000 * np.sqrt(np.mean((y - np.median(y) - s0) ** 2))


# segmento ST: de 80 a 120 ms después de cada pico R
st = np.concatenate([np.arange(r + int(0.08 * FS), r + int(0.12 * FS)) for r in ref[2:-2]])

# 1. Línea base con un Butterworth paso alto de 0,5 Hz
sos = signal.butter(2, 0.5, "highpass", fs=FS, output="sos")
y_causal = signal.sosfilt(sos, x)
print(f"sin filtrar: {error_uv(x):.0f} µV; Butterworth causal: {error_uv(y_causal):.0f} µV")
# TODO: el mismo filtro con fase cero (sosfiltfilt), un FIR de fase lineal (kaiserord + firwin)
#       y un estimador de medianas (signal.medfilt de 200 ms y luego de 600 ms).
# TODO: error en el ST de cada opción: media de |y - s0| en las muestras st.

# 2. TODO: muesca de 50 Hz de segundo orden y paso bajo de unos 40 Hz.

m = (t > 30) & (t < 32.2)
fig, ax = plt.subplots(figsize=(8, 3), constrained_layout=True)
ax.plot(t[m], s0[m], "k", lw=1.5, label="limpia")
ax.plot(t[m], y_causal[m] - np.median(y_causal), label="Butterworth causal")
ax.set(xlabel="t (s)", ylabel="mV")
ax.legend()
guardar(fig, "h2_linea_base.png")
