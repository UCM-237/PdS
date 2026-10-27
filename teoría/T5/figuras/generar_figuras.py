"""Genera todas las figuras del Tema 5 (aplicaciones: STFT, wavelets e imágenes).

    python generar_figuras.py               # todas
    python generar_figuras.py espectrograma # solo las indicadas

Las figuras se guardan en PDF junto a este script.
"""

from __future__ import annotations

import pathlib
import sys

import numpy as np
from matplotlib.patches import Rectangle
from scipy import signal

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[1] / "comun"))
sys.path.insert(0, str(AQUI.parent / "codigo" / "python"))
import pds_estilo as pe  # noqa: E402
from imagen_prueba import imagen_prueba  # noqa: E402

pe.aplicar()
FIGURAS: dict[str, callable] = {}
MAPA = "viridis"


def figura(func):
    FIGURAS[func.__name__] = func
    return func


def guardar(fig, nombre):
    pe.guardar(fig, nombre, AQUI)


def db(x, piso=-120):
    return np.maximum(20 * np.log10(np.abs(x) + 1e-300), piso)


def ticks_pi(ax):
    ax.set_xticks([0, np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi],
                  ["0", r"$\pi/4$", r"$\pi/2$", r"$3\pi/4$", r"$\pi$"])


def espectrograma(ax, x, fs, L, R, rango=60, nfft=None):
    w = np.hanning(L + 2)[1:-1]
    f, t, S = signal.spectrogram(x, fs, window=w, noverlap=L - R, nfft=nfft or max(L, 256),
                                 mode="magnitude", detrend=False)
    SdB = 20 * np.log10(S + 1e-12)
    SdB -= SdB.max()
    ax.pcolormesh(t, f, np.maximum(SdB, -rango), cmap=MAPA, shading="auto", rasterized=True)
    ax.grid(False)
    ax.set_xlabel("$t$ (s)")
    ax.set_ylabel("$f$ (Hz)")
    return f, t, S


def imagen(ax, f, titulo=None, vmin=0, vmax=1, cmap="gray"):
    ax.imshow(f, cmap=cmap, vmin=vmin, vmax=vmax, interpolation="nearest")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(True)
        s.set_linewidth(0.4)
        s.set_color(pe.GRIS_CLARO)
    if titulo:
        ax.set_title(titulo)


def senal_prueba(fs=1000, T=2.0):
    """Chirp de 50 a 400 Hz, tono de 300 Hz entre 0,6 y 1,2 s y un clic en 1,6 s."""
    t = np.arange(0, T, 1 / fs)
    x = signal.chirp(t, 50, T, 400)
    x += 0.8 * np.sin(2 * np.pi * 300 * t) * ((t > 0.6) & (t < 1.2))
    x[int(1.6 * fs)] += 8
    return t, x


# ---------------------------------------------------------------------
# Parte 1 · STFT y espectrograma
# ---------------------------------------------------------------------

@figura
def no_estacionaria():
    fs = 1000
    t = np.arange(0, 1, 1 / fs)
    x1 = np.where(t < 0.5, np.sin(2 * np.pi * 50 * t), np.sin(2 * np.pi * 120 * t))
    x2 = np.where(t < 0.5, np.sin(2 * np.pi * 120 * t), np.sin(2 * np.pi * 50 * t))
    fig, axs = pe.figura(2, 2, ancho=6.4, alto=2.6)
    k = np.arange(len(t)) * fs / len(t)
    for i, (x, c) in enumerate(((x1, pe.AZUL), (x2, pe.ROJO))):
        axs[i, 0].plot(t, x, color=c, lw=0.5)
        axs[i, 0].set_xlim(0, 1)
        axs[i, 0].set_ylabel(f"$x_{i + 1}(t)$")
        X = np.abs(np.fft.fft(x)) / len(x)
        axs[i, 1].plot(k[:200], X[:200], color=c)
        axs[i, 1].set_ylabel(f"$|X_{i + 1}[k]|/N$")
    axs[1, 0].set_xlabel("$t$ (s)")
    axs[1, 1].set_xlabel("$f$ (Hz)")
    axs[0, 0].set_title("Dos señales distintas")
    axs[0, 1].set_title("... con el mismo módulo de la DFT")
    guardar(fig, "no_estacionaria")


@figura
def stft_tramos():
    fs = 1000
    t = np.arange(0, 1, 1 / fs)
    x = np.where(t < 0.5, np.sin(2 * np.pi * 50 * t), np.sin(2 * np.pi * 120 * t))
    L = 200
    fig, axs = pe.figura(1, 2, ancho=6.4, alto=1.9, gridspec_kw={"width_ratios": [1.4, 1]})
    axs[0].plot(t, x, color=pe.GRIS, lw=0.5)
    cols = (pe.AZUL, pe.VERDE, pe.ROJO)
    w = np.hanning(L + 2)[1:-1]
    for c, n0 in zip(cols, (150, 400, 650)):
        tt = t[n0:n0 + L]
        axs[0].plot(tt, w, color=c, lw=1.1)
        seg = x[n0:n0 + L] * w
        X = np.abs(np.fft.rfft(seg, 2048))
        f = np.fft.rfftfreq(2048, 1 / fs)
        axs[1].plot(f, X / X.max(), color=c, label=f"$n_0={n0}$")
    axs[0].set_xlabel("$t$ (s)")
    axs[0].set_title(f"Ventanas de Hann de $L={L}$ muestras")
    axs[1].set_xlim(0, 200)
    axs[1].set_xlabel("$f$ (Hz)")
    axs[1].set_title("Espectro de cada tramo")
    axs[1].legend(fontsize=6.5)
    guardar(fig, "stft_tramos")


@figura
def espectrograma_ejemplo():
    fs = 1000
    t, x = senal_prueba(fs)
    fig, axs = pe.figura(1, 2, ancho=6.4, alto=2.0, gridspec_kw={"width_ratios": [1, 1.3]})
    axs[0].plot(t, x, color=pe.AZUL, lw=0.3)
    axs[0].set_xlim(0, 2)
    axs[0].set_ylim(-2.5, 2.5)
    axs[0].set_xlabel("$t$ (s)")
    axs[0].set_title("Señal: chirp, tono de 300 Hz y un clic")
    espectrograma(axs[1], x, fs, L=128, R=16)
    axs[1].set_title("Espectrograma (Hann, $L=128$, $R=16$), dB")
    guardar(fig, "espectrograma_ejemplo")


@figura
def resolucion_tf():
    fs = 1000
    t, x = senal_prueba(fs)
    fig, axs = pe.figura(1, 3, ancho=6.4, alto=1.9, sharey=True)
    for ax, L in zip(axs, (32, 128, 512)):
        espectrograma(ax, x, fs, L=L, R=max(L // 8, 4), nfft=1024)
        ax.set_title(f"$L={L}$: $\\Delta t={1000 * L / fs:.0f}$ ms, $\\Delta f\\approx{2 * fs / L:.0f}$ Hz")
    for ax in axs[1:]:
        ax.set_ylabel("")
    guardar(fig, "resolucion_tf")


@figura
def cola():
    L = 64
    n = np.arange(6 * L)
    fig, axs = pe.figura(1, 2, ancho=6.4, alto=1.7, sharey=True)
    w = 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(L) / L)  # Hann periódica
    for ax, R in zip(axs, (L // 2, 3 * L // 4)):
        s = np.zeros(n.size + L)
        for m in range(0, n.size, R):
            s[m:m + L] += w
            ax.plot(np.arange(m, m + L), w, color=pe.GRIS_CLARO, lw=0.7)
        ax.plot(n[L:5 * L], s[L:5 * L], color=pe.AZUL, lw=1.2)
        ax.set_xlim(L, 5 * L)
        ax.set_xlabel("$n$")
        ax.set_title(f"Hann, $L={L}$, $R={R}$" + (": suma constante" if R == L // 2 else ": la suma ondula"))
    axs[0].set_ylim(0, 1.25)
    guardar(fig, "cola")


def dtmf(digitos, fs=8000, T=0.12, pausa=0.06):
    filas = (697, 770, 852, 941)
    cols = (1209, 1336, 1477)
    tecla = {"1": (0, 0), "2": (0, 1), "3": (0, 2), "4": (1, 0), "5": (1, 1), "6": (1, 2),
             "7": (2, 0), "8": (2, 1), "9": (2, 2), "*": (3, 0), "0": (3, 1), "#": (3, 2)}
    t = np.arange(0, T, 1 / fs)
    trozos = []
    for d in digitos:
        i, j = tecla[d]
        trozos += [np.sin(2 * np.pi * filas[i] * t) + np.sin(2 * np.pi * cols[j] * t),
                   np.zeros(int(pausa * fs))]
    return np.concatenate(trozos)


@figura
def dtmf_espectrograma():
    fs = 8000
    x = dtmf("2025", fs)
    x = x + 0.3 * np.random.default_rng(1).standard_normal(x.size)
    fig, ax = pe.figura(1, 1, ancho=6.4, alto=2.0)
    espectrograma(ax, x, fs, L=256, R=32, rango=40)
    ax.set_ylim(500, 1600)
    for f0 in (697, 770, 852, 941, 1209, 1336, 1477):
        ax.axhline(f0, color="w", lw=0.3, ls=":")
        ax.text(0.725, f0, f"{f0}", fontsize=5.5, va="center")
    ax.set_xlim(0, 0.72)
    ax.set_title("Marcación DTMF de «2025» con ruido (Hann, $L=256$, $f_s=8$ kHz)")
    guardar(fig, "dtmf_espectrograma")


# ---------------------------------------------------------------------
# Parte 2 · Wavelets
# ---------------------------------------------------------------------

def morlet(t, w0=6.0):
    return np.pi ** -0.25 * np.exp(1j * w0 * t) * np.exp(-t ** 2 / 2)


def sombrero(t):
    return 2 / (np.sqrt(3) * np.pi ** 0.25) * (1 - t ** 2) * np.exp(-t ** 2 / 2)


def haar(t):
    return np.where((t >= 0) & (t < 0.5), 1.0, 0.0) - np.where((t >= 0.5) & (t < 1), 1.0, 0.0)


H0_DB2 = np.array([1 + np.sqrt(3), 3 + np.sqrt(3), 3 - np.sqrt(3), 1 - np.sqrt(3)]) / (4 * np.sqrt(2))
H0_HAAR = np.array([1, 1]) / np.sqrt(2)


def paso_alto(h0):
    L = len(h0)
    return np.array([(-1) ** n * h0[L - 1 - n] for n in range(L)])


def cascada(h0, niveles=8):
    """phi y psi por el algoritmo de cascada (iterar el banco de síntesis)."""
    h1 = paso_alto(h0)
    phi = np.array([1.0])
    for _ in range(niveles):
        up = np.zeros(2 * len(phi) - 1)
        up[::2] = phi
        phi = np.sqrt(2) * np.convolve(up, h0)
    t = np.arange(len(phi)) * 2.0 ** -niveles
    phi /= np.sum(phi) * 2.0 ** -niveles
    psi = sum(np.sqrt(2) * h1[k] * np.interp(2 * t - k, t, phi, left=0, right=0)
              for k in range(len(h1)))
    return t, phi, t, psi


@figura
def wavelets():
    fig, axs = pe.figura(1, 4, ancho=6.4, alto=1.6)
    t = np.linspace(-0.5, 1.5, 2001)
    axs[0].plot(t, haar(t), color=pe.AZUL)
    axs[0].set_title("Haar")
    _, _, tpsi, psi = cascada(H0_DB2)
    axs[1].plot(tpsi, psi / np.max(np.abs(psi)), color=pe.AZUL)
    axs[1].set_title("Daubechies db2")
    t = np.linspace(-5, 5, 2001)
    axs[2].plot(t, sombrero(t), color=pe.AZUL)
    axs[2].set_title("Sombrero mexicano")
    m = morlet(t)
    axs[3].plot(t, m.real, color=pe.AZUL, label="Re")
    axs[3].plot(t, m.imag, color=pe.ROJO, lw=0.7, label="Im")
    axs[3].legend(fontsize=6, loc="lower left")
    axs[3].set_title(r"Morlet ($\omega_0=6$)")
    for ax in axs:
        pe.ejes_centrados(ax)
        ax.set_xlabel("$t$")
    guardar(fig, "wavelets")


@figura
def escalado_wavelet():
    t = np.linspace(-6, 14, 3000)
    fig, ax = pe.figura(1, 1, ancho=6.4, alto=1.6)
    for (a, b), c in zip(((0.5, -2), (1, 3), (2, 9)), (pe.AZUL, pe.VERDE, pe.ROJO)):
        ax.plot(t, sombrero((t - b) / a) / np.sqrt(a), color=c, label=f"$a={a}$, $b={b}$")
    pe.ejes_centrados(ax)
    ax.legend(fontsize=6.5, ncol=3)
    ax.set_xlabel("$t$")
    ax.set_title(r"$\psi_{a,b}(t)=a^{-1/2}\,\psi((t-b)/a)$: comprimir para ver detalles finos, dilatar para ver tendencias")
    guardar(fig, "escalado_wavelet")


@figura
def teselas():
    fig, axs = pe.figura(1, 2, ancho=6.4, alto=1.9)
    ax = axs[0]
    for i in range(8):
        for j in range(4):
            ax.add_patch(Rectangle((i / 8, j / 4), 1 / 8, 1 / 4, fill=False, ec=pe.AZUL, lw=0.8))
    ax.set_title("STFT: la misma resolución en todo el plano")
    ax = axs[1]
    for nivel in range(4):
        h = 1 / 2 ** (nivel + 1)
        n = 2 ** (3 - nivel)
        for i in range(n):
            ax.add_patch(Rectangle((i / n, h), 1 / n, h, fill=False, ec=pe.ROJO, lw=0.8))
    ax.add_patch(Rectangle((0, 0), 1, 1 / 16, fill=False, ec=pe.ROJO, lw=0.8))
    ax.set_title("Wavelet: $\\Delta t$ corto en alta frecuencia, largo en baja")
    for ax in axs:
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel("tiempo")
        ax.set_ylabel("frecuencia")
    guardar(fig, "teselas")


def cwt_morlet(x, fs, frecs, w0=6.0):
    W = np.zeros((len(frecs), len(x)), complex)
    for i, f in enumerate(frecs):
        a = w0 / (2 * np.pi * f)               # escala en segundos
        tt = np.arange(-4 * a, 4 * a + 1 / fs, 1 / fs)
        psi = morlet(tt / a, w0) / np.sqrt(a)
        W[i] = signal.fftconvolve(x, np.conj(psi[::-1]), mode="same") / fs
    return W


@figura
def escalograma():
    fs = 1000
    t = np.arange(0, 1.5, 1 / fs)
    x = np.sin(2 * np.pi * 20 * t) * (t < 0.75) + np.sin(2 * np.pi * 120 * t) * (t >= 0.75)
    x[int(0.4 * fs)] += 6
    fig, axs = pe.figura(1, 3, ancho=6.4, alto=1.9)
    axs[0].plot(t, x, color=pe.AZUL, lw=0.4)
    axs[0].set_xlabel("$t$ (s)")
    axs[0].set_title("20 Hz, 120 Hz y un clic")
    espectrograma(axs[1], x, fs, L=128, R=8, rango=40)
    axs[1].set_ylim(0, 250)
    axs[1].set_title("Espectrograma, $L=128$")
    frecs = np.geomspace(5, 250, 80)
    W = np.abs(cwt_morlet(x, fs, frecs))
    WdB = 20 * np.log10(W / W.max() + 1e-9)
    axs[2].pcolormesh(t, frecs, np.maximum(WdB, -40), cmap=MAPA, shading="auto", rasterized=True)
    axs[2].grid(False)
    axs[2].set_yscale("log")
    axs[2].set_yticks([5, 10, 20, 50, 100, 200], ["5", "10", "20", "50", "100", "200"])
    axs[2].set_xlabel("$t$ (s)")
    axs[2].set_ylabel(r"$f\approx\omega_0/(2\pi a)$ (Hz)")
    axs[2].set_title("Escalograma (Morlet)")
    guardar(fig, "escalograma")


@figura
def banco_filtros():
    fig, axs = pe.figura(1, 2, ancho=6.4, alto=1.7, sharey=True)
    for ax, h0, nombre in zip(axs, (H0_HAAR, H0_DB2), ("Haar", "db2")):
        h1 = paso_alto(h0)
        w, H0 = signal.freqz(h0, 1, 1024)
        _, H1 = signal.freqz(h1, 1, 1024)
        ax.plot(w, np.abs(H0) / np.sqrt(2), color=pe.AZUL, label="$|H_0|$ (paso bajo)")
        ax.plot(w, np.abs(H1) / np.sqrt(2), color=pe.ROJO, label="$|H_1|$ (paso alto)")
        ax.plot(w, (np.abs(H0) ** 2 + np.abs(H1) ** 2) / 2, color=pe.GRIS, ls="--", lw=0.8,
                label=r"$(|H_0|^2+|H_1|^2)/2$")
        ticks_pi(ax)
        ax.set_xlabel(r"$\Omega$")
        ax.set_title(f"Filtros de análisis {nombre} (normalizados)")
    axs[0].legend(fontsize=6)
    guardar(fig, "banco_filtros")


def dwt_haar(x, niveles):
    """Coeficientes [d1, d2, ..., dJ, aJ] de la DWT de Haar."""
    a = np.asarray(x, float)
    salida = []
    for _ in range(niveles):
        d = (a[0::2] - a[1::2]) / np.sqrt(2)
        a = (a[0::2] + a[1::2]) / np.sqrt(2)
        salida.append(d)
    salida.append(a)
    return salida


def idwt_haar(coefs):
    a = coefs[-1]
    for d in reversed(coefs[:-1]):
        x = np.empty(2 * len(a))
        x[0::2] = (a + d) / np.sqrt(2)
        x[1::2] = (a - d) / np.sqrt(2)
        a = x
    return a


def senal_bloques(N=1024):
    t = np.arange(N) / N
    x = np.sin(2 * np.pi * 2 * t) + 1.2 * (t > 0.3) - 1.6 * (t > 0.62) \
        + 0.3 * np.sin(2 * np.pi * 40 * t) * (t > 0.75)
    return t, x


@figura
def multiresolucion():
    N = 1024
    t, x = senal_bloques(N)
    J = 4
    c = dwt_haar(x, J)
    partes = []
    for j in range(J + 1):
        cc = [np.zeros_like(v) for v in c]
        cc[j] = c[j]
        partes.append(idwt_haar(cc))
    fig, axs = pe.figura(J + 2, 1, ancho=6.4, alto=3.6, sharex=True)
    axs[0].plot(t, x, color=pe.AZUL, lw=0.7)
    axs[0].set_ylabel("$x$")
    axs[1].plot(t, partes[J], color=pe.VERDE, lw=0.8)
    axs[1].set_ylabel(f"$A_{J}$")
    for j in range(J):
        axs[2 + j].plot(t, partes[J - 1 - j], color=pe.ROJO, lw=0.6)
        axs[2 + j].set_ylabel(f"$D_{J - j}$")
    axs[-1].set_xlabel("$n/N$")
    axs[0].set_title(f"Descomposición de Haar en {J} niveles: $x=A_{J}+D_{J}+\\cdots+D_1$")
    for ax in axs:
        ax.yaxis.set_label_coords(-0.05, 0.5)
    guardar(fig, "multiresolucion")


def umbral_duro(c, u):
    return np.where(np.abs(c) > u, c, 0)


def senal_escalones(N=1024):
    t = np.arange(N) / N
    x = np.zeros(N)
    for t0, h in ((0.1, 1.5), (0.23, -2.2), (0.4, 1.6), (0.5, 1.2), (0.62, -2.6), (0.75, 1.9), (0.85, -1.0)):
        x += h * (t > t0)
    return t, x


@figura
def eliminacion_ruido():
    N = 1024
    t, x = senal_escalones(N)
    rng = np.random.default_rng(4)
    sigma = 0.4
    y = x + sigma * rng.standard_normal(N)
    J = 5
    c = dwt_haar(y, J)
    s_est = np.median(np.abs(c[0])) / 0.6745
    u = s_est * np.sqrt(2 * np.log(N))
    cu = [umbral_duro(v, u) for v in c[:-1]] + [c[-1]]
    xr = idwt_haar(cu)
    b = np.ones(8) / 8
    xm = signal.filtfilt(b, 1, y)
    fig, axs = pe.figura(1, 3, ancho=6.4, alto=1.8, sharey=True)
    axs[0].plot(t, y, color=pe.GRIS, lw=0.4)
    axs[0].set_title(f"Con ruido, $\\sigma={sigma}$")
    axs[1].plot(t, xm, color=pe.NARANJA, lw=0.8)
    axs[1].set_title("Media móvil de 8 (ida y vuelta)")
    axs[2].plot(t, xr, color=pe.AZUL, lw=0.8)
    axs[2].set_title(f"Umbral duro, Haar, $J={J}$")
    for ax, z in zip(axs, (y, xm, xr)):
        ax.plot(t, x, color=pe.ROJO, lw=0.5, ls="--")
        ax.set_xlabel("$n/N$")
        if z is not y:
            err = np.sqrt(np.mean((z - x) ** 2))
            ax.text(0.02, 0.05, f"error rms {err:.3f}", transform=ax.transAxes, fontsize=6.5)
    guardar(fig, "eliminacion_ruido")


@figura
def compresion():
    N = 1024
    t, x = senal_bloques(N)
    c = dwt_haar(x, 6)
    v = np.concatenate(c)
    fig, axs = pe.figura(1, 2, ancho=6.4, alto=1.7, sharey=True)
    for ax, frac in zip(axs, (0.05, 0.02)):
        k = int(frac * N)
        u = np.sort(np.abs(v))[-k]
        cc = [np.where(np.abs(w) >= u, w, 0) for w in c]
        xr = idwt_haar(cc)
        ax.plot(t, x, color=pe.GRIS_CLARO, lw=1.6)
        ax.plot(t, xr, color=pe.AZUL, lw=0.8)
        snr = 10 * np.log10(np.sum(x ** 2) / np.sum((x - xr) ** 2))
        ax.set_title(f"Con el {100 * frac:.0f} % de los coeficientes ({k}): SNR {snr:.0f} dB")
        ax.set_xlabel("$n/N$")
    guardar(fig, "compresion")


# ---------------------------------------------------------------------
# Parte 3 · Imágenes
# ---------------------------------------------------------------------

@figura
def imagen_pixeles():
    f = imagen_prueba()
    fig, axs = pe.figura(1, 3, ancho=6.4, alto=2.0, gridspec_kw={"width_ratios": [1, 1, 1.3]})
    imagen(axs[0], f, "Imagen $f[m,n]$ de $256\\times256$")
    m0, n0 = 74, 24
    axs[0].add_patch(Rectangle((n0 - 0.5, m0 - 0.5), 16, 16, fill=False, ec=pe.ROJO, lw=0.8))
    axs[0].axhline(200, color=pe.NARANJA, lw=0.6)
    trozo = np.round(255 * f[m0:m0 + 16, n0:n0 + 16])
    imagen(axs[1], trozo, "Detalle de $16\\times16$ píxeles", vmin=0, vmax=255)
    for i in range(0, 16, 3):
        for j in range(0, 16, 3):
            axs[1].text(j, i, f"{trozo[i, j]:.0f}", fontsize=4.2, ha="center", va="center",
                        color="k" if trozo[i, j] > 128 else "w")
    axs[2].plot(np.arange(256), 255 * f[200], color=pe.NARANJA, lw=0.8)
    axs[2].set_xlim(0, 255)
    axs[2].set_ylim(0, 255)
    axs[2].set_xlabel("$n$ (columna)")
    axs[2].set_ylabel("nivel de gris")
    axs[2].set_title("Perfil de la fila $m=200$")
    guardar(fig, "imagen_pixeles")


@figura
def transformaciones_puntuales():
    f = imagen_prueba()
    r = np.linspace(0, 1, 256)
    fig, axs = pe.figura(1, 4, ancho=6.4, alto=1.75, gridspec_kw={"width_ratios": [1.15, 1, 1, 1]})
    curvas = [("negativo", 1 - r, pe.GRIS), (r"$\gamma=0{,}5$", r ** 0.5, pe.VERDE),
              (r"$\gamma=2$", r ** 2, pe.ROJO), ("umbral 0,5", (r > 0.5) * 1.0, pe.NARANJA)]
    for nombre, s, c in curvas:
        axs[0].plot(r, s, color=c, label=nombre)
    axs[0].plot(r, r, color=pe.GRIS_CLARO, lw=0.6, ls="--")
    axs[0].set_xlabel("$r$ (entrada)")
    axs[0].set_ylabel("$s=T(r)$")
    axs[0].legend(fontsize=5.5, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2,
                  handlelength=1.2, columnspacing=0.8)
    axs[0].set_aspect("equal")
    imagen(axs[1], f ** 0.5, r"$\gamma=0{,}5$: aclara")
    imagen(axs[2], f ** 2, r"$\gamma=2$: oscurece")
    imagen(axs[3], (f > 0.5) * 1.0, "Umbral en 0,5")
    guardar(fig, "transformaciones_puntuales")


def ecualizar(g, niveles=256):
    hist = np.bincount(g.ravel(), minlength=niveles)
    cdf = np.cumsum(hist) / g.size
    T = np.round((niveles - 1) * cdf).astype(int)
    return T[g], hist, cdf, T


@figura
def histograma_ecualizacion():
    f = imagen_prueba()
    g = np.round(255 * (0.35 + 0.3 * f)).astype(int)      # poco contraste
    ge, h, cdf, T = ecualizar(g)
    he = np.bincount(ge.ravel(), minlength=256)
    fig, axs = pe.figura(1, 4, ancho=6.4, alto=1.75)
    imagen(axs[0], g, "Poco contraste", vmin=0, vmax=255)
    axs[1].bar(np.arange(256), h / g.size, width=1, color=pe.AZUL)
    ax2 = axs[1].twinx()
    ax2.plot(np.arange(256), cdf, color=pe.ROJO, lw=0.8)
    ax2.set_ylim(0, 1.05)
    ax2.tick_params(labelsize=6)
    ax2.grid(False)
    axs[1].set_xlim(0, 255)
    axs[1].set_title("Histograma y $F(r)$")
    axs[1].set_xlabel("$r$")
    imagen(axs[2], ge, "Ecualizada", vmin=0, vmax=255)
    axs[3].bar(np.arange(256), he / g.size, width=1, color=pe.AZUL)
    ax4 = axs[3].twinx()
    ax4.plot(np.arange(256), np.cumsum(he) / g.size, color=pe.ROJO, lw=0.8)
    ax4.set_ylim(0, 1.05)
    ax4.tick_params(labelsize=6)
    ax4.grid(False)
    axs[3].set_xlim(0, 255)
    axs[3].set_title("Histograma ecualizado")
    axs[3].set_xlabel("$s$")
    guardar(fig, "histograma_ecualizacion")


def conv2_same(f, h):
    return signal.convolve2d(f, h, mode="same", boundary="symm")


@figura
def filtros_espaciales():
    f = imagen_prueba()
    rng = np.random.default_rng(2)
    fr = f + 0.08 * rng.standard_normal(f.shape)
    media = np.ones((5, 5)) / 25
    x = np.arange(-6, 7)
    g = np.exp(-x ** 2 / (2 * 2 ** 2))
    gauss = np.outer(g, g) / np.sum(g) ** 2
    sx = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
    lap = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
    gx = conv2_same(f, sx)
    gy = conv2_same(f, sx.T)
    fig, axs = pe.figura(1, 5, ancho=6.4, alto=1.55)
    imagen(axs[0], fr, "Con ruido")
    imagen(axs[1], conv2_same(fr, media), "Media $5\\times5$")
    imagen(axs[2], conv2_same(fr, gauss), "Gaussiano, $\\sigma=2$")
    imagen(axs[3], np.hypot(gx, gy), "Sobel $|\\nabla f|$", vmax=2)
    imagen(axs[4], np.abs(conv2_same(f, lap)), "Laplaciano $|\\nabla^2 f|$", vmax=0.5)
    guardar(fig, "filtros_espaciales")


def dft2_log(f):
    F = np.fft.fftshift(np.fft.fft2(f))
    return np.log10(1 + np.abs(F))


@figura
def dft2_patrones():
    N = 128
    n = np.arange(N)
    m, nn = np.meshgrid(n, n, indexing="ij")
    casos = [("$\\cos(2\\pi\\,8n/N)$", np.cos(2 * np.pi * 8 * nn / N)),
             ("$\\cos(2\\pi\\,16m/N)$", np.cos(2 * np.pi * 16 * m / N)),
             ("$\\cos(2\\pi\\,(8m+8n)/N)$", np.cos(2 * np.pi * (8 * m + 8 * nn) / N)),
             ("Cuadrado de $32\\times32$", ((np.abs(m - 64) < 16) & (np.abs(nn - 64) < 16)) * 1.0)]
    fig, axs = pe.figura(2, 4, ancho=6.4, alto=3.1)
    for j, (nombre, f) in enumerate(casos):
        imagen(axs[0, j], (f - f.min()) / (np.ptp(f) or 1), nombre)
        F = np.abs(np.fft.fftshift(np.fft.fft2(f)))
        if j < 3:
            k, l = np.nonzero(F > 1e-6 * F.max())
            axs[1, j].set_facecolor("black")
            axs[1, j].plot(l - N // 2, k - N // 2, "o", color="#FCA50A", ms=3)
        else:
            axs[1, j].imshow(np.log10(1 + F), cmap="magma", interpolation="nearest",
                             extent=(-N / 2 - 0.5, N / 2 - 0.5, N / 2 - 0.5, -N / 2 - 0.5))
        axs[1, j].grid(False)
        axs[1, j].set_aspect("equal")
        axs[1, j].set_xlim(-32, 32)
        axs[1, j].set_ylim(32, -32)
        axs[1, j].tick_params(labelsize=5.5)
        axs[1, j].set_xlabel("$l$", fontsize=7)
    axs[1, 0].set_ylabel("$k$", fontsize=7)
    guardar(fig, "dft2_patrones")


@figura
def dft2_imagen():
    f = imagen_prueba()
    fig, axs = pe.figura(1, 3, ancho=6.4, alto=2.0)
    imagen(axs[0], f, "$f[m,n]$")
    F = np.fft.fft2(f)
    imagen(axs[1], np.log10(1 + np.abs(np.fft.fftshift(F))), "$\\log_{10}(1+|F[k,l]|)$, centrada",
           vmin=0, vmax=3.5, cmap="magma")
    fase = np.real(np.fft.ifft2(np.exp(1j * np.angle(F))))
    imagen(axs[2], (fase - fase.min()) / np.ptp(fase) * 4 - 1.5, "Solo la fase ($|F|=1$)")
    guardar(fig, "dft2_imagen")


@figura
def filtrado_frecuencia():
    f = imagen_prueba()
    N = f.shape[0]
    k = np.fft.fftfreq(N) * N
    K, L = np.meshgrid(k, k, indexing="ij")
    D = np.hypot(K, L)
    D0 = 20
    ideal = (D <= D0) * 1.0
    gauss = np.exp(-D ** 2 / (2 * D0 ** 2))
    pa = 1 - gauss
    F = np.fft.fft2(f)
    fig, axs = pe.figura(2, 3, ancho=6.4, alto=3.3)
    for j, (nombre, H) in enumerate((("Paso bajo ideal, $D_0=20$", ideal),
                                     ("Paso bajo gaussiano, $D_0=20$", gauss),
                                     ("Paso alto gaussiano", pa))):
        imagen(axs[0, j], np.fft.fftshift(H), nombre)
        g = np.real(np.fft.ifft2(F * H))
        if j == 2:
            imagen(axs[1, j], np.abs(g), vmax=0.4)
        else:
            imagen(axs[1, j], g)
    axs[1, 0].set_title("Anillos (fenómeno de Gibbs)")
    axs[1, 1].set_title("Suavizado sin anillos")
    axs[1, 2].set_title("Bordes (módulo)")
    guardar(fig, "filtrado_frecuencia")


# ---------------------------------------------------------------------
# Cápsulas: deconvolución y sustracción espectral
# ---------------------------------------------------------------------
@figura
def deconvolucion_wiener():
    rng = np.random.default_rng(5)
    N, L = 512, 9
    x = np.repeat(rng.integers(0, 2, 64), 8).astype(float)
    h = np.zeros(N)
    h[:L] = 1 / L
    H = np.fft.fft(h)
    y = np.real(np.fft.ifft(np.fft.fft(x) * H)) + 0.02 * rng.standard_normal(N)
    Y = np.fft.fft(y)
    k = np.arange(N // 2)
    fig, axs = pe.figura(1, 3, ancho=6.4, alto=1.8)
    ax = axs[0]
    ax.plot(k / N, db(H[:N // 2]), color=pe.AZUL, label=r"$|H|$")
    ax.plot(k / N, db(1 / (np.abs(H[:N // 2]) + 1e-12)), color=pe.ROJO, lw=0.8, label=r"$1/|H|$")
    for m in range(1, 5):
        ax.axvline(m / L, color=pe.GRIS_CLARO, lw=0.6, ls="--")
    ax.set_ylim(-60, 60)
    ax.set_xlabel("$F$ (ciclos/muestra)")
    ax.set_ylabel("dB")
    ax.set_title(r"Ceros en $F=m/L$")
    ax.legend(loc="upper left", ncol=2)
    n = np.arange(N)
    sl = slice(100, 260)
    for ax, K, c, tit in ((axs[1], 1e-6, pe.ROJO, r"Casi inversa, $K=10^{-6}$"),
                          (axs[2], 1e-2, pe.VERDE, r"Wiener, $K=0{,}01$")):
        G = np.conj(H) / (np.abs(H) ** 2 + K)
        ax.plot(n[sl], x[sl], color=pe.GRIS_CLARO, lw=1.8)
        ax.plot(n[sl], y[sl], color=pe.GRIS, lw=0.7)
        ax.plot(n[sl], np.real(np.fft.ifft(G * Y))[sl], color=c, lw=0.9)
        ax.set_ylim(-0.6, 1.6)
        ax.set_xlabel("$n$")
        ax.set_title(tit)
    guardar(fig, "deconvolucion_wiener")


@figura
def sustraccion_espectral():
    fs = 8000
    rng = np.random.default_rng(1)
    t = np.arange(0, 3, 1 / fs)
    s = np.sin(2 * np.pi * (300 + 150 * t) * t) * (t > 1)
    x = s + 0.3 * rng.standard_normal(t.size)
    f, tt, X = signal.stft(x, fs, nperseg=256)
    Pv = np.mean(np.abs(X[:, tt < 0.9]) ** 2, axis=1, keepdims=True)
    P = np.maximum(np.abs(X) ** 2 - 2.0 * Pv, 0.02 * np.abs(X) ** 2)
    ref = np.max(np.abs(X) ** 2)
    fig, axs = pe.figura(1, 3, ancho=6.4, alto=1.8, gridspec_kw={"width_ratios": [1, 1, 0.9]})
    for ax, Z, tit in ((axs[0], np.abs(X) ** 2, "Ruidosa"),
                       (axs[1], P, r"Tras restar ($\alpha=2$, $\beta=0{,}02$)")):
        ZdB = np.maximum(10 * np.log10(Z / ref + 1e-12), -50)
        ax.pcolormesh(tt, f, ZdB, cmap=MAPA, vmin=-50, vmax=0, shading="auto", rasterized=True)
        ax.grid(False)
        ax.set_ylim(0, 2000)
        ax.set_xlabel("$t$ (s)")
        ax.set_title(tit)
    axs[0].set_ylabel("$f$ (Hz)")
    g = np.linspace(-5, 20, 400)
    G = 10 ** (g / 10)
    for a, b, c in ((1, 0.0, pe.AZUL), (2, 0.0, pe.ROJO), (2, 0.02, pe.VERDE)):
        gan = np.sqrt(np.maximum(1 - a / G, b))
        axs[2].plot(g, 20 * np.log10(gan + 1e-6), color=c,
                    label=rf"$\alpha={a}$, $\beta={b:g}$".replace(".", "{,}"))
    axs[2].set_ylim(-40, 2)
    axs[2].set_xlabel(r"$|X|^2/\hat\Phi_{vv}$ (dB)")
    axs[2].set_title("Ganancia (dB)")
    axs[2].legend(fontsize=5.5, loc="lower right")
    guardar(fig, "sustraccion_espectral")

if __name__ == "__main__":
    nombres = sys.argv[1:] or list(FIGURAS)
    for nombre in nombres:
        FIGURAS[nombre]()
        print("ok", nombre)
