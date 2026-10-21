"""Hito 2: filtrado lineal del zumbido y del soplido. Completa las partes TODO."""
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

from utilidades import alinear, cargar, guardar, snr_db

fs, x = cargar()
_, s = cargar("audio_limpio.wav")


def muesca(f0, r, fs):
    """Muesca de segundo orden en f0 con polos de radio r. Devuelve (b, a)."""
    w0 = 2 * np.pi * f0 / fs
    b = np.array([1, -2 * np.cos(w0), 1])
    a = np.array([1, -2 * r * np.cos(w0), r ** 2])
    return b, a


# 1. Zumbido
r = 0.99   # TODO: elige r a partir del ancho de muesca que necesitas (ancho ≈ (1 - r) fs / pi)
sos = np.array([np.concatenate(muesca(50 * k, r, fs)) for k in range(1, 7)])
# Las secciones van en formato sos: una fila [b0 b1 b2 a0 a1 a2] por muesca
w, H = signal.sosfreqz(sos, 2 ** 16, fs=fs)
fig, ax = plt.subplots(figsize=(8, 3), constrained_layout=True)
ax.plot(w, 20 * np.log10(np.abs(H) + 1e-9))
ax.set(xlim=(0, 400), ylim=(-50, 5), xlabel="f (Hz)", ylabel="|H| (dB)")
guardar(fig, "h2_muescas.png")
y_causal = signal.sosfilt(sos, x)
y_cero = signal.sosfiltfilt(sos, x)
print(f"SNR: original {snr_db(s, x):.2f} dB, muescas causal {snr_db(s, y_causal):.2f} dB, "
      f"fase cero {snr_db(s, y_cero):.2f} dB")
# TODO: diseña también el filtro peine (1 - z^-N) / (1 - rho z^-N) y compáralo.

# 2. Paso bajo con la misma especificación, FIR e IIR
FP, FST, RP, AS = None, None, 0.5, 60      # TODO: bandas de paso y de rechazo en Hz (H1, pregunta 4)
if FP is not None:
    # FIR por ventana de Kaiser
    L, beta = signal.kaiserord(AS, (FST - FP) / (fs / 2))
    L |= 1                                  # longitud impar
    h = signal.firwin(L, (FP + FST) / 2, window=("kaiser", beta), fs=fs)
    y_fir = alinear(signal.lfilter(h, 1, y_cero), (L - 1) // 2)
    print(f"FIR L = {L}: SNR = {snr_db(s, y_fir):.2f} dB")
    # TODO: diseña un IIR (buttord/butter, cheb1ord/cheby1 o ellipord/ellip) con la misma especificación,
    #       dibuja |H| y el retardo de grupo de los dos, y mide la SNR con filtrado causal y de fase cero.
