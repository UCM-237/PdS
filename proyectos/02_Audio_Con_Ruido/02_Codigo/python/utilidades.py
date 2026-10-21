"""Funciones de apoyo del proyecto «Audio con ruido». No hace falta modificarlas."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.io import wavfile

DATOS = Path(__file__).resolve().parents[2] / "01_Datos"
FIGURAS = Path(__file__).resolve().parent / "figuras"
FIGURAS.mkdir(exist_ok=True)


def cargar(nombre="audio_ruidoso.wav"):
    """Devuelve (fs, x) con x en [-1, 1)."""
    fs, x = wavfile.read(DATOS / nombre)
    return fs, x.astype(float) / 32768


def guardar_wav(nombre, x, fs):
    wavfile.write(nombre, fs, np.round(np.clip(x, -1, 1) * 32767).astype(np.int16))


def snr_db(ref, x):
    """SNR (dB) de x frente a la referencia limpia ref (mismo tamaño, sin retardo)."""
    return 10 * np.log10(np.sum(ref ** 2) / np.sum((x - ref) ** 2))


def alinear(x, retardo):
    """Adelanta x un número entero de muestras (para compensar el retardo de un FIR causal)."""
    return np.concatenate([x[retardo:], np.zeros(retardo)])


def espectro(x, fs, ventana="hann"):
    """Módulo de la DFT unilateral en dB, normalizado para que una sinusoide de amplitud A dé 20log10(A)."""
    w = signal.get_window(ventana, len(x))
    X = np.fft.rfft(x * w) / np.sum(w) * 2
    return np.fft.rfftfreq(len(x), 1 / fs), 20 * np.log10(np.abs(X) + 1e-12)


def stft(x, fs, nperseg=512):
    """STFT con ventana de Hann y 75 % de solape: devuelve (f, t, Z)."""
    return signal.stft(x, fs, nperseg=nperseg, noverlap=3 * nperseg // 4)


def istft(Z, fs, nperseg=512, n=None):
    """Inversa de stft(); n recorta la salida a la longitud original."""
    _, y = signal.istft(Z, fs, nperseg=nperseg, noverlap=3 * nperseg // 4)
    return y[:n] if n else y


def dibujar_stft(ax, f, t, Z, vmin=-100, vmax=-20):
    pc = ax.pcolormesh(t, f, 20 * np.log10(np.abs(Z) + 1e-9), shading="auto", vmin=vmin, vmax=vmax)
    ax.set(xlabel="t (s)", ylabel="f (Hz)")
    return pc


def guardar(fig, nombre):
    fig.savefig(FIGURAS / nombre, dpi=130, bbox_inches="tight")
    plt.close(fig)
    print("figura:", FIGURAS / nombre)
