"""Genera todas las figuras del Tema 3 (transformada discreta de Fourier).

    python generar_figuras.py               # todas
    python generar_figuras.py ventanas      # solo las indicadas

Las figuras se guardan en PDF junto a este script.
"""

from __future__ import annotations

import pathlib
import sys

import numpy as np
from scipy import signal

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[1] / "comun"))
import pds_estilo as pe  # noqa: E402

pe.aplicar()
FIGURAS: dict[str, callable] = {}


def figura(func):
    FIGURAS[func.__name__] = func
    return func


def guardar(fig, nombre):
    pe.guardar(fig, nombre, AQUI)


def dtft(x, Om):
    """DTFT de una secuencia finita que empieza en n = 0."""
    n = np.arange(len(x))
    return np.exp(-1j * np.outer(Om, n)) @ x


def ticks_2pi(ax, pasos=4):
    """Marcas en [0, 2π] con múltiplos de 2π/pasos."""
    v = np.arange(pasos + 1) * 2 * np.pi / pasos
    etiquetas = ["0"]
    for k in range(1, pasos + 1):
        num, den = 2 * k, pasos
        g = np.gcd(num, den)
        num, den = num // g, den // g
        s = (r"\pi" if num == 1 else f"{num}" + r"\pi")
        etiquetas.append(f"${s}$" if den == 1 else f"${s}/{den}$")
    ax.set_xticks(v, etiquetas)


def db(x, piso=-120):
    return np.maximum(20 * np.log10(np.abs(x) + 1e-300), piso)


# ---------------------------------------------------------------------
# Parte 1 · La DFT
# ---------------------------------------------------------------------

@figura
def dtft_dft():
    x = np.array([1.0, 2.0, 2.0, 1.0, 0.5])
    Om = np.linspace(0, 2 * np.pi, 800)
    X = np.abs(dtft(x, Om))
    fig, axs = pe.figura(1, 3, ancho=6.4, alto=1.7)
    pe.stem(axs[0], np.arange(len(x)), x)
    axs[0].set_xlim(-0.6, 8.6)
    axs[0].set_title(r"$x[n]$, $L=5$")
    axs[0].set_xlabel("$n$")
    for ax, N in zip(axs[1:], (8, 16)):
        ax.plot(Om, X, color=pe.GRIS_CLARO, lw=1.0)
        k = np.arange(N)
        pe.stem(ax, 2 * np.pi * k / N, np.abs(np.fft.fft(x, N)), color=pe.ROJO, ms=2.4)
        ticks_2pi(ax)
        ax.set_title(rf"$|X(e^{{j\Omega}})|$ y $|X[k]|$, $N={N}$")
        ax.set_xlabel(r"$\Omega$")
    guardar(fig, "dtft_dft")


@figura
def ventana_rect():
    N = 16
    Om = np.linspace(-np.pi, np.pi, 2000)
    W = np.exp(-1j * Om * (N - 1) / 2) * np.sin(Om * N / 2) / np.where(np.abs(np.sin(Om / 2)) < 1e-12, 1, np.sin(Om / 2))
    W[np.abs(np.sin(Om / 2)) < 1e-12] = N
    fig, axs = pe.figura(1, 2, ancho=5.4, alto=1.8)
    pe.stem(axs[0], np.arange(-4, 21), (np.arange(-4, 21) >= 0) & (np.arange(-4, 21) < N), ms=2.2)
    axs[0].set_title(r"$w[n]$, $N=16$")
    axs[0].set_xlabel("$n$")
    axs[1].plot(Om, np.abs(W))
    axs[1].set_xticks([-np.pi, -2 * np.pi / N * 2, 0, 2 * np.pi / N * 2, np.pi],
                      [r"$-\pi$", r"$-\frac{4\pi}{N}$", "0", r"$\frac{4\pi}{N}$", r"$\pi$"])
    axs[1].annotate("lóbulo principal\nanchura $4\\pi/N$", (0.25, 12), (1.0, 12), fontsize=6,
                    arrowprops=dict(arrowstyle="-", color=pe.GRIS, lw=0.5))
    axs[1].set_title(r"$|W(e^{j\Omega})|$")
    axs[1].set_xlabel(r"$\Omega$")
    guardar(fig, "ventana_rect")


@figura
def truncamiento():
    Om = np.linspace(0, np.pi, 3000)
    fig, ax = pe.figura(ancho=4.2, alto=1.7)
    for N, c in ((16, pe.ROJO), (64, pe.AZUL)):
        n = np.arange(N)
        x = np.cos(0.3 * np.pi * n)
        ax.plot(Om, np.abs(dtft(x, Om)) / N, color=c, lw=0.9, label=f"$N={N}$")
    ax.axvline(0.3 * np.pi, color=pe.GRIS, ls="--", lw=0.6)
    ax.set_xticks([0, 0.3 * np.pi, np.pi / 2, np.pi], ["0", r"$0{,}3\pi$", r"$\pi/2$", r"$\pi$"])
    ax.set_xlabel(r"$\Omega$")
    ax.set_title(r"$|X_N(e^{j\Omega})|/N$ de $\cos(0{,}3\pi n)$ truncado a $N$ muestras")
    ax.legend(loc="upper right")
    guardar(fig, "truncamiento")


@figura
def extension_periodica():
    x = np.array([3.0, 2.0, 1.5, 1.0, 0.6, 0.3])
    L = len(x)
    n = np.arange(-8, 16)
    fig, axs = pe.figura(2, 1, ancho=4.6, alto=2.4, sharex=True)
    for ax, N, titulo in ((axs[0], 8, r"$N=8\geq L$: un periodo es $x[n]$"),
                          (axs[1], 4, r"$N=4<L$: las copias se solapan (aliasing temporal)")):
        xp = np.zeros(len(n))
        for i, ni in enumerate(n):
            for m in range(-5, 6):
                j = ni - m * N
                if 0 <= j < L:
                    xp[i] += x[j]
        pe.stem(ax, n, xp, color=pe.GRIS_CLARO, ms=2.0)
        dentro = (n >= 0) & (n < N)
        pe.stem(ax, n[dentro], xp[dentro], color=pe.ROJO if N < L else pe.AZUL, ms=2.4)
        ax.axvspan(-0.5, N - 0.5, color=pe.NARANJA, alpha=0.08, lw=0)
        ax.set_title(titulo, loc="left")
    axs[1].set_xlabel("$n$")
    guardar(fig, "extension_periodica")


@figura
def ejes_dft():
    fs, N = 1000, 16
    x = np.cos(2 * np.pi * 125 * np.arange(N) / fs) + 0.5 * np.cos(2 * np.pi * 312.5 * np.arange(N) / fs)
    X = np.abs(np.fft.fft(x))
    k = np.arange(N)
    fig, axs = pe.figura(1, 2, ancho=6.0, alto=1.8)
    pe.stem(axs[0], k, X, ms=2.4)
    axs[0].set_xlabel("$k$")
    axs[0].set_title(r"$|X[k]|$, $k=0,\dots,N-1$")
    axs[0].axvline(N / 2, color=pe.GRIS, ls="--", lw=0.6)
    axs[0].annotate(r"$k=N/2$" + "\n" + r"($f_s/2$)", (N / 2, 7.5), fontsize=6, ha="center")
    kc = np.arange(-N // 2, N // 2)
    pe.stem(axs[1], kc * fs / N, np.fft.fftshift(X), color=pe.VERDE, ms=2.4)
    axs[1].set_xlabel(r"$f=k\,f_s/N$ (Hz)")
    axs[1].set_title(r"Con fftshift: de $-f_s/2$ a $f_s/2$")
    guardar(fig, "ejes_dft")


# ---------------------------------------------------------------------
# Parte 2 · Propiedades
# ---------------------------------------------------------------------

@figura
def desplazamiento_circular():
    x = np.array([4.0, 3.0, 2.0, 1.0, 0.0, 0.0])
    N = len(x)
    n = np.arange(N)
    fig, axs = pe.figura(1, 3, ancho=6.4, alto=1.6, sharey=True)
    pe.stem(axs[0], n, x, ms=2.6)
    axs[0].set_title("$x[n]$")
    pe.stem(axs[1], n, np.roll(x, 2), color=pe.VERDE, ms=2.6)
    axs[1].set_title(r"$x[((n-2))_6]$")
    pe.stem(axs[2], n, x[(-n) % N], color=pe.NARANJA, ms=2.6)
    axs[2].set_title(r"$x[((-n))_6]$")
    for ax in axs:
        ax.set_xlabel("$n$")
        ax.set_xticks(n)
    guardar(fig, "desplazamiento_circular")


@figura
def simetria_dft():
    N = 16
    n = np.arange(N)
    x = 0.8 ** n * (1 + 0.5 * np.cos(2 * np.pi * 3 * n / N))
    X = np.fft.fft(x)
    k = np.arange(N)
    fig, axs = pe.figura(1, 2, ancho=5.6, alto=1.7)
    pe.stem(axs[0], k, np.abs(X), ms=2.4)
    axs[0].set_title(r"$|X[k]|=|X[N-k]|$ (par)")
    pe.stem(axs[1], k, np.angle(X), color=pe.ROJO, ms=2.4)
    axs[1].set_title(r"$\arg X[k]=-\arg X[N-k]$ (impar)")
    for ax in axs:
        ax.axvline(N / 2, color=pe.GRIS, ls="--", lw=0.6)
        ax.set_xlabel("$k$")
    guardar(fig, "simetria_dft")


@figura
def conv_circular():
    x = np.array([1.0, 3.0, 4.0, 2.0])
    h = np.array([1.0, 1.0, 1.0])
    lin = np.convolve(x, h)
    fig, axs = pe.figura(1, 3, ancho=6.4, alto=1.6, sharey=True)
    pe.stem(axs[0], np.arange(len(lin)), lin, ms=2.6)
    axs[0].set_title(r"Lineal, $L+M-1=6$")
    for ax, N, c in ((axs[1], 4, pe.ROJO), (axs[2], 6, pe.VERDE)):
        y = np.real(np.fft.ifft(np.fft.fft(x, N) * np.fft.fft(h, N)))
        pe.stem(ax, np.arange(N), y, color=c, ms=2.6)
        ax.set_title(rf"Circular, $N={N}$")
        ax.set_xlim(-0.5, 5.5)
    for ax in axs:
        ax.set_xlabel("$n$")
    guardar(fig, "conv_circular")


# ---------------------------------------------------------------------
# Parte 3 · Análisis espectral
# ---------------------------------------------------------------------

@figura
def fuga_espectral():
    N = 32
    n = np.arange(N)
    Om = np.linspace(0, 2 * np.pi, 3000)
    fig, axs = pe.figura(1, 2, ancho=6.0, alto=1.8, sharey=True)
    for ax, k0, titulo in ((axs[0], 4, r"$\Omega_0=2\pi\cdot4/N$: en una muestra"),
                           (axs[1], 4.5, r"$\Omega_0=2\pi\cdot4{,}5/N$: entre dos muestras")):
        x = np.cos(2 * np.pi * k0 * n / N)
        ax.plot(Om, np.abs(dtft(x, Om)), color=pe.GRIS_CLARO, lw=0.9)
        pe.stem(ax, 2 * np.pi * n / N, np.abs(np.fft.fft(x)), color=pe.AZUL if k0 == 4 else pe.ROJO, ms=2.2)
        ax.set_xlim(0, np.pi)
        ax.set_xticks([0, np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi], ["0", r"$\pi/4$", r"$\pi/2$", r"$3\pi/4$", r"$\pi$"])
        ax.set_title(titulo, loc="left")
        ax.set_xlabel(r"$\Omega$")
    guardar(fig, "fuga_espectral")


VENTANAS = (("rectangular", "boxcar", pe.GRIS), ("Hann", "hann", pe.AZUL),
            ("Hamming", "hamming", pe.VERDE), ("Blackman", "blackman", pe.ROJO))


@figura
def ventanas():
    N, M = 32, 4096
    fig, axs = pe.figura(1, 2, ancho=6.2, alto=2.0)
    for nombre, clave, c in VENTANAS:
        w = signal.get_window(clave, N, fftbins=False)
        axs[0].plot(np.arange(N), w, color=c, lw=1.0, label=nombre)
        W = np.fft.fftshift(np.fft.fft(w, M))
        Om = (np.arange(M) - M // 2) * 2 * np.pi / M
        axs[1].plot(Om, db(W / np.abs(W).max()), color=c, lw=0.8)
    axs[0].set_title("$w[n]$, $N=32$")
    axs[0].set_xlabel("$n$")
    axs[0].legend(fontsize=6, loc="lower center")
    axs[1].set_ylim(-110, 5)
    axs[1].set_xlim(0, np.pi)
    axs[1].set_xticks([0, np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi], ["0", r"$\pi/4$", r"$\pi/2$", r"$3\pi/4$", r"$\pi$"])
    axs[1].set_title(r"$|W(e^{j\Omega})|$ normalizada (dB)")
    axs[1].set_xlabel(r"$\Omega$")
    guardar(fig, "ventanas")


@figura
def ventana_tonos():
    fs, N, M = 1000, 64, 4096
    n = np.arange(N)
    x = np.cos(2 * np.pi * 100 * n / fs) + 0.01 * np.cos(2 * np.pi * 180 * n / fs)
    f = np.arange(M // 2) * fs / M
    fig, ax = pe.figura(ancho=4.4, alto=1.9)
    for nombre, clave, c in VENTANAS[:2] + VENTANAS[3:]:
        w = signal.get_window(clave, N, fftbins=False)
        X = np.fft.fft(x * w, M)[: M // 2]
        ax.plot(f, db(2 * X / w.sum()), color=c, lw=0.8, label=nombre)
    ax.set_ylim(-100, 5)
    ax.set_xlim(0, 500)
    ax.set_xlabel("$f$ (Hz)")
    ax.set_ylabel("dB")
    ax.set_title("Tonos de 100 Hz (amplitud 1) y 180 Hz (amplitud 0,01), $N=64$")
    ax.legend(fontsize=6, loc="upper right")
    guardar(fig, "ventana_tonos")


@figura
def resolucion():
    fs = 1000
    M = 4096
    f = np.arange(M // 2) * fs / M
    fig, axs = pe.figura(1, 3, ancho=6.4, alto=1.75, sharey=True)
    casos = ((axs[0], 32, 32, r"$N=32$"), (axs[1], 32, 256, r"$N=32$ + ceros hasta 256"),
             (axs[2], 128, 128, r"$N=128$"))
    for ax, N, Nfft, titulo in casos:
        n = np.arange(N)
        x = np.cos(2 * np.pi * 200 * n / fs) + np.cos(2 * np.pi * 220 * n / fs)
        X = np.fft.fft(x, M)[: M // 2]
        ax.plot(f, np.abs(X) / N * 2, color=pe.GRIS_CLARO, lw=0.8)
        k = np.arange(Nfft // 2)
        Xk = np.fft.fft(x, Nfft)[: Nfft // 2]
        ax.plot(k * fs / Nfft, np.abs(Xk) / N * 2, "o", ms=2.0, color=pe.AZUL)
        ax.set_xlim(100, 320)
        ax.set_title(titulo)
        ax.set_xlabel("$f$ (Hz)")
    guardar(fig, "resolucion")


@figura
def espectrograma():
    fs = 8000
    t = np.arange(0, 2, 1 / fs)
    x = signal.chirp(t, 200, 2, 3000) + 0.5 * np.sin(2 * np.pi * 1000 * t) * (t > 1)
    f, tt, S = signal.spectrogram(x, fs, window="hann", nperseg=256, noverlap=192)
    fig, ax = pe.figura(ancho=4.2, alto=2.0)
    ax.pcolormesh(tt, f, 10 * np.log10(S + 1e-12), shading="auto", cmap="viridis", vmin=-80, rasterized=True)
    ax.set_xlabel("$t$ (s)")
    ax.set_ylabel("$f$ (Hz)")
    ax.set_title("Barrido de 200 a 3000 Hz y tono de 1 kHz desde $t=1$ s")
    ax.grid(False)
    guardar(fig, "espectrograma")


# ---------------------------------------------------------------------
# Parte 4 · FFT y convolución rápida
# ---------------------------------------------------------------------

@figura
def complejidad():
    N = 2 ** np.arange(3, 15)
    fig, ax = pe.figura(ancho=3.4, alto=1.9)
    ax.loglog(N, N ** 2, "o-", ms=2.4, label=r"DFT directa, $N^2$")
    ax.loglog(N, N / 2 * np.log2(N), "o-", ms=2.4, color=pe.ROJO, label=r"FFT, $\frac{N}{2}\log_2N$")
    ax.set_xlabel("$N$")
    ax.set_ylabel("productos complejos")
    ax.legend(loc="upper left")
    guardar(fig, "complejidad")


@figura
def solapamiento_suma():
    rng = np.random.default_rng(3)
    x = np.convolve(rng.standard_normal(40), np.ones(4) / 4, mode="same")
    h = np.array([0.5, 0.3, 0.2, 0.1])
    Lb = 10
    fig, axs = pe.figura(3, 1, ancho=5.0, alto=2.8, sharex=True)
    pe.stem(axs[0], np.arange(len(x)), x, ms=1.8)
    for b in range(0, len(x), Lb):
        axs[0].axvspan(b - 0.5, b + Lb - 0.5, color=[pe.AZUL, pe.NARANJA][(b // Lb) % 2], alpha=0.08, lw=0)
    axs[0].set_title("Entrada dividida en bloques de $L=10$", loc="left")
    total = np.zeros(len(x) + len(h) - 1)
    colores = [pe.AZUL, pe.NARANJA, pe.VERDE, pe.ROJO]
    for i, b in enumerate(range(0, len(x), Lb)):
        yb = np.convolve(x[b:b + Lb], h)
        nb = np.arange(b, b + len(yb))
        axs[1].plot(nb, yb, "o-", ms=1.6, lw=0.7, color=colores[i])
        total[b:b + len(yb)] += yb
    axs[1].set_title(r"Salida de cada bloque, $L+M-1=13$ muestras (se solapan $M-1=3$)", loc="left")
    pe.stem(axs[2], np.arange(len(total)), total, color=pe.VERDE, ms=1.8)
    axs[2].set_title(r"Suma de los bloques $=x\ast h$", loc="left")
    axs[2].set_xlabel("$n$")
    guardar(fig, "solapamiento_suma")


@figura
def muestreo_frecuencia():
    a = 0.8
    n = np.arange(0, 24)
    h = a ** n
    fig, axs = pe.figura(1, 2, ancho=5.6, alto=1.7, sharey=True)
    for ax, N in zip(axs, (8, 16)):
        k = np.arange(N)
        H = 1 / (1 - a * np.exp(-2j * np.pi * k / N))
        hN = np.real(np.fft.ifft(H))
        ax.plot(n, h, "o", ms=2.0, color=pe.GRIS_CLARO)
        pe.stem(ax, np.arange(N), hN, color=pe.ROJO, ms=2.4)
        ax.set_title(rf"IDFT de $N={N}$ muestras de $H(e^{{j\Omega}})$")
        ax.set_xlabel("$n$")
    guardar(fig, "muestreo_frecuencia")


if __name__ == "__main__":
    pedidas = sys.argv[1:] or list(FIGURAS)
    for nombre in pedidas:
        FIGURAS[nombre]()
