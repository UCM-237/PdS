"""Hito 4: STFT, silbido y sustracción espectral. Completa las partes TODO."""
import matplotlib.pyplot as plt
import numpy as np

from utilidades import cargar, dibujar_stft, guardar, guardar_wav, istft, snr_db, stft

fs, x = cargar()
_, s = cargar("audio_limpio.wav")
n0 = int(1.0 * fs)

y3 = x            # TODO: sustituye por la salida de tu cadena del Hito 3
NPS = 512         # TODO: justifica la longitud de ventana (prueba al menos tres)

f, t, Z = stft(y3, fs, NPS)
# Comprobación: la STFT con este solape se invierte sin error
print(f"error de reconstrucción: {np.max(np.abs(istft(Z, fs, NPS, len(y3)) - y3)):.1e}")

# 1. TODO: en cada trama, busca el pico en la banda del silbido; quédate con las tramas
#    donde destaca; ajusta una recta f(t) (np.polyfit) y pon a cero las celdas a ±ancho Hz.

# 2. TODO: sustracción espectral con la potencia media del ruido en el primer segundo:
#    G = sqrt(max(1 - alfa * Pn / |Z|^2, beta^2))

y4 = istft(Z, fs, NPS, len(x))
fig, ax = plt.subplots(figsize=(8, 3.5), constrained_layout=True)
dibujar_stft(ax, f, t, Z)
guardar(fig, "h4_espectrograma.png")
print(f"SNR final: {snr_db(s, y4):.2f} dB")
guardar_wav("audio_restaurado.wav", y4, fs)
