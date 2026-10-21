"""Hito 3: estadística del ruido, detección de clics y filtro de Wiener. Completa las partes TODO."""
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal, stats

from utilidades import cargar, guardar, snr_db

fs, x = cargar()
_, s = cargar("audio_limpio.wav")
n0 = int(1.0 * fs)

# 1. Modelo del ruido (usa el primer segundo ya sin zumbido: copia aquí tus filtros del Hito 2)
ruido = x[:n0]           # TODO: quita el zumbido antes
print(f"media {ruido.mean():.2e}, σ {ruido.std():.4f}, curtosis {stats.kurtosis(ruido):.2f}")
f_p, P_p = signal.periodogram(ruido, fs)
f_w, P_w = signal.welch(ruido, fs, nperseg=512)
fig, ax = plt.subplots(figsize=(8, 3), constrained_layout=True)
ax.semilogy(f_p, P_p, lw=0.3, label="periodograma")
ax.semilogy(f_w, P_w, label="Welch")
ax.set(xlabel="f (Hz)", ylabel="PSD")
ax.legend()
guardar(fig, "h3_psd_ruido.png")
# TODO: histograma con la gaussiana superpuesta y autocorrelación normalizada.


def coef_ar(seg, orden):
    """Coeficientes a_1..a_p del predictor lineal por Yule-Walker."""
    r = np.correlate(seg, seg, "full")[len(seg) - 1:len(seg) + orden] / len(seg)
    R = r[np.abs(np.subtract.outer(np.arange(orden), np.arange(orden)))]
    return np.linalg.solve(R + 1e-9 * r[0] * np.eye(orden), r[1:orden + 1])


# 2. Residuo de predicción en un bloque de ejemplo
bloque = x[int(2.0 * fs):int(2.0 * fs) + 1024]
a = coef_ar(bloque, 16)
e = signal.lfilter(np.concatenate([[1], -a]), [1], bloque)
print(f"curtosis del residuo en el bloque: {stats.kurtosis(e):.1f}")
# TODO: calcula el residuo por bloques en toda la señal, fija un umbral robusto
#       (k · 1.4826 · MAD) y agrupa las muestras que lo superan en eventos.
# TODO: repara los clics por interpolación y decide el orden respecto a los filtros del H2.

# 3. TODO: filtro de Wiener con las PSD de Welch de la señal y del ruido:
#    H(f) = max(Px - Pn, 0) / Px, aplicado como FIR de fase cero.
