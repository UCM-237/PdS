"""Hito 3: detección de QRS y variabilidad del ritmo. Completa las partes marcadas con TODO."""
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

from utilidades import FS, anotaciones, cargar, evaluar, guardar

t, x = cargar("ecg_A.csv")
ref, _ = anotaciones()
# TODO: aplica aquí tu cadena de preprocesado del Hito 2
y = x

# Etapas de Pan-Tompkins
sos = signal.butter(2, [5, 15], "bandpass", fs=FS, output="sos")
xf = signal.sosfiltfilt(sos, y)
d = np.gradient(xf) * FS
c = d ** 2
N = int(0.150 * FS)
mwi = np.convolve(c, np.ones(N) / N, mode="same")

# Umbral fijo provisional: sustitúyelo por el umbral adaptativo
picos, _ = signal.find_peaks(mwi, distance=int(0.2 * FS), height=0.3 * mwi.max())
# TODO: umbral adaptativo con SPK y NPK, búsqueda hacia atrás y localización del pico R
#       en xf (la integración va retrasada media ventana).
print("umbral fijo:", evaluar(picos, ref))

# TODO: tacograma, FC media, SDNN, RMSSD, histograma de los RR y PSD del tacograma
#       remuestreado a 4 Hz (np.interp + signal.welch) con potencias LF y HF.
