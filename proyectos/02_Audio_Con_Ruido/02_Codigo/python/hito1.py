"""Hito 1: señal y espectro. Completa las partes marcadas con TODO."""
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

from utilidades import cargar, espectro, guardar, snr_db, stft, dibujar_stft

fs, x = cargar()
_, s = cargar("audio_limpio.wav")          # solo para medir la SNR real
t = np.arange(len(x)) / fs
n0 = int(1.0 * fs)                          # el primer segundo solo tiene ruido
print(f"fs = {fs} Hz, {len(x)} muestras, SNR real = {snr_db(s, x):.2f} dB")

# 1. Señal en el tiempo
fig, ax = plt.subplots(2, 1, figsize=(8, 4.5), constrained_layout=True)
ax[0].plot(t, x, lw=0.4)
ax[0].set(xlabel="t (s)", ylabel="x(t)", title="Señal completa")
# TODO: en ax[1], dibuja un detalle de unas decenas de ms donde se vea un clic
guardar(fig, "h1_tiempo.png")

# 2. Espectro del primer segundo y de la señal completa
f0, X0 = espectro(x[:n0], fs)
f, X = espectro(x, fs)
fig, ax = plt.subplots(figsize=(8, 3), constrained_layout=True)
ax.plot(f, X, lw=0.4, label="señal completa")
ax.plot(f0, X0, lw=0.4, label="primer segundo")
ax.set(xlabel="f (Hz)", ylabel="|X| (dB)", ylim=(-110, -10))
ax.legend()
guardar(fig, "h1_espectro.png")

# 3. TODO: localiza las rayas del zumbido en X0 (por ejemplo con signal.find_peaks)
#    y escribe su frecuencia y su amplitud.

# 4. TODO: estima σ del soplido con la PSD de Welch del primer segundo
#    (signal.welch). Pista: para ruido blanco, PSD unilateral = 2σ²/fs.

# 5. Espectrograma: localiza el silbido
fz, tz, Z = stft(x, fs, 512)
fig, ax = plt.subplots(figsize=(8, 3.5), constrained_layout=True)
dibujar_stft(ax, fz, tz, Z)
guardar(fig, "h1_espectrograma.png")
# TODO: mide los instantes de inicio y fin del silbido y sus frecuencias.

# Pregunta 1: TODO repite el espectro con N = 256, 1024, 4096 y 16000 muestras.
