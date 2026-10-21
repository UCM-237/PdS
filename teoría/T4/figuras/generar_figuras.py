"""Genera todas las figuras del Tema 4 (filtros).

    python generar_figuras.py               # todas
    python generar_figuras.py ventanas_fir  # solo las indicadas

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


def db(x, piso=-120):
    return np.maximum(20 * np.log10(np.abs(x) + 1e-300), piso)


def ticks_pi(ax, simetrico=False):
    if simetrico:
        ax.set_xticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi],
                      [r"$-\pi$", r"$-\pi/2$", "0", r"$\pi/2$", r"$\pi$"])
    else:
        ax.set_xticks([0, np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi],
                      ["0", r"$\pi/4$", r"$\pi/2$", r"$3\pi/4$", r"$\pi$"])


def mascara_pb(ax, wp, ws, ap, as_, wmax, en_db=True, color=pe.GRIS):
    """Dibuja la plantilla de un paso bajo: zonas prohibidas sombreadas."""
    kw = dict(color=pe.GRIS_CLARO, alpha=0.45, lw=0)
    if en_db:
        ax.fill_between([0, wp], [-ap, -ap], [-200, -200], **kw)
        ax.fill_between([ws, wmax], [-as_, -as_], [10, 10], **kw)
    else:
        ax.fill_between([0, wp], [10 ** (-ap / 20)] * 2, [0, 0], **kw)
        ax.fill_between([ws, wmax], [10 ** (-as_ / 20)] * 2, [2, 2], **kw)


def zplano(ax, z, p, lim=1.6):
    t = np.linspace(0, 2 * np.pi, 400)
    ax.plot(np.cos(t), np.sin(t), color=pe.GRIS, lw=0.6)
    ax.plot(np.real(z), np.imag(z), "o", mfc="none", mec=pe.AZUL, ms=4.5, mew=1.0)
    ax.plot(np.real(p), np.imag(p), "x", color=pe.ROJO, ms=4.5, mew=1.1)
    ax.set_aspect("equal")
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.axhline(0, color=pe.GRIS, lw=0.4)
    ax.axvline(0, color=pe.GRIS, lw=0.4)
    ax.set_xlabel(r"$\mathrm{Re}\,z$")
    ax.set_ylabel(r"$\mathrm{Im}\,z$")


# ---------------------------------------------------------------------
# Parte 1 · Introducción
# ---------------------------------------------------------------------

@figura
def ideales():
    w = np.linspace(-np.pi, np.pi, 2001)
    wc, w1, w2 = 0.4 * np.pi, 0.3 * np.pi, 0.6 * np.pi
    casos = [("Paso bajo", np.abs(w) < wc), ("Paso alto", np.abs(w) > wc),
             ("Paso banda", (np.abs(w) > w1) & (np.abs(w) < w2)),
             ("Supresor de banda", ~((np.abs(w) > w1) & (np.abs(w) < w2)))]
    fig, axs = pe.figura(1, 4, ancho=6.6, alto=1.45, sharey=True)
    for ax, (tit, H) in zip(axs, casos):
        ax.fill_between(w, H.astype(float), color=pe.AZUL, alpha=0.18, lw=0)
        ax.plot(w, H, color=pe.AZUL)
        ax.set_title(tit)
        ax.set_xticks([-np.pi, 0, np.pi], [r"$-\pi$", "0", r"$\pi$"])
        ax.set_xlabel(r"$\Omega$")
        ax.set_ylim(-0.05, 1.25)
    axs[0].set_ylabel(r"$|H(e^{j\Omega})|$")
    guardar(fig, "ideales")


@figura
def sinc_ideal():
    n = np.arange(-20, 21)
    wc = 0.3 * np.pi
    h = wc / np.pi * np.sinc(wc / np.pi * n)
    fig, ax = pe.figura(ancho=3.6, alto=1.6)
    pe.stem(ax, n, h, ms=2.2)
    ax.set_xlabel("$n$")
    ax.set_title(r"$h[n]=\sin(\Omega_c n)/(\pi n)$, $\Omega_c=0{,}3\pi$")
    guardar(fig, "sinc_ideal")


@figura
def especificaciones():
    b, a = signal.ellip(4, 1, 40, 1.0, analog=True)
    w = np.linspace(0, 3, 1500)
    _, H = signal.freqs(b, a, w)
    fig, axs = pe.figura(1, 2, ancho=6.2, alto=2.0)
    ws = 1.6
    for ax, en_db in zip(axs, (False, True)):
        mascara_pb(ax, 1.0, ws, 1, 40, 3, en_db)
        ax.plot(w, db(H) if en_db else np.abs(H), color=pe.AZUL)
        ax.set_xticks([0, 1, ws], ["0", r"$\omega_p$", r"$\omega_s$"])
        ax.set_xlabel(r"$\omega$")
    axs[0].set_ylim(0, 1.15)
    axs[0].set_yticks([10 ** (-2), 10 ** (-1 / 20), 1], ["$1/A$", "$1/E$", "1"])
    axs[0].annotate("banda de paso", (0.5, 0.6), ha="center", fontsize=6.5, color=pe.GRIS)
    axs[0].annotate("transición", (1.3, 0.3), ha="center", fontsize=6.5, color=pe.GRIS, rotation=90)
    axs[0].annotate("banda de supresión", (2.2, 0.6), ha="center", fontsize=6.5, color=pe.GRIS)
    axs[0].set_title(r"$|H(j\omega)|$")
    axs[1].set_ylim(-70, 5)
    axs[1].set_yticks([-40, -1], [r"$-\alpha_s$", r"$-\alpha_p$"])
    axs[1].set_title(r"$20\log_{10}|H(j\omega)|$ (dB)")
    guardar(fig, "especificaciones")


@figura
def retardo_grupo():
    fs = 1000
    t = np.arange(0, 0.5, 1 / fs)
    x = signal.square(2 * np.pi * 8 * t)
    b, a = signal.butter(6, 60, fs=fs)
    h = signal.firwin(101, 60, fs=fs)
    yi = signal.lfilter(b, a, x)
    yf = signal.lfilter(h, 1, x)
    fig, axs = pe.figura(1, 2, ancho=6.2, alto=1.8, sharey=True)
    for ax, y, tit, d in ((axs[0], yi, "IIR (Butterworth, $N=6$): fase no lineal", 0),
                          (axs[1], yf, "FIR de fase lineal (101 coef.): retardo de 50 muestras", 50)):
        ax.plot(t * 1e3, x, color=pe.GRIS_CLARO, lw=0.9)
        ax.plot((t - d / fs) * 1e3, y, color=pe.AZUL, lw=1.0)
        ax.set_xlim(150, 400)
        ax.set_title(tit)
        ax.set_xlabel("$t$ (ms)")
    axs[1].annotate("salida adelantada 50 muestras\npara compararla", (155, -1.45), fontsize=6, color=pe.GRIS)
    guardar(fig, "retardo_grupo")


@figura
def polos_ceros_continuo():
    w = np.logspace(-1, 2, 800)
    casos = [
        ("Polo simple $a/(s+a)$, $a=10$", [10], [1, 10]),
        ("Par de polos, $\\sigma=1$, $\\omega_a=3$", [10], [1, 2, 10]),
        ("Ceros en $\\pm j3$ y polos en $-3$", [1, 0, 9], [1, 6, 9]),
    ]
    fig, axs = pe.figura(1, 3, ancho=6.6, alto=1.7, sharey=True)
    for ax, (tit, b, a) in zip(axs, casos):
        _, H = signal.freqs(b, a, w)
        ax.semilogx(w, db(H, -60), color=pe.AZUL)
        ax.set_title(tit, fontsize=7)
        ax.set_xlabel(r"$\omega$ (rad/s)")
        ax.set_ylim(-45, 12)
    axs[0].set_ylabel("dB")
    guardar(fig, "polos_ceros_continuo")


@figura
def notch_discreto():
    W0 = np.pi / 3
    fig, axs = pe.figura(1, 2, ancho=5.6, alto=2.0, gridspec_kw=dict(width_ratios=[1, 1.7]))
    z = np.exp(1j * W0 * np.array([1, -1]))
    zplano(axs[0], z, 0.9 * z, lim=1.3)
    axs[0].set_title(r"$r=0{,}9$, $\Omega_0=\pi/3$")
    Om = np.linspace(0, np.pi, 1500)
    for r, c in ((0.7, pe.NARANJA), (0.9, pe.ROJO), (0.98, pe.AZUL)):
        b = np.poly(z).real
        a = np.poly(r * z).real
        _, H = signal.freqz(b, a, Om)
        axs[1].plot(Om, np.abs(H), color=c, label=f"$r={r}$".replace(".", "{,}"))
    ticks_pi(axs[1])
    axs[1].set_xlabel(r"$\Omega$")
    axs[1].set_title(r"$|H(e^{j\Omega})|$ del filtro de muesca")
    axs[1].legend(loc="lower right")
    guardar(fig, "notch_discreto")


# ---------------------------------------------------------------------
# Parte 2 · Filtros continuos
# ---------------------------------------------------------------------

@figura
def butterworth_orden():
    w = np.linspace(0, 3, 800)
    fig, axs = pe.figura(1, 2, ancho=6.0, alto=1.9, gridspec_kw=dict(width_ratios=[1.6, 1]))
    for N, c in ((1, pe.GRIS), (2, pe.NARANJA), (4, pe.VERDE), (8, pe.AZUL)):
        axs[0].plot(w, 1 / np.sqrt(1 + w ** (2 * N)), color=c, label=f"$N={N}$")
    axs[0].axhline(1 / np.sqrt(2), color=pe.GRIS, ls="--", lw=0.6)
    axs[0].set_xticks([0, 1, 2, 3], ["0", r"$\omega_c$", r"$2\omega_c$", r"$3\omega_c$"])
    axs[0].set_yticks([0, 1 / np.sqrt(2), 1], ["0", "0,707", "1"])
    axs[0].set_title(r"$|H(j\omega)|$ de Butterworth")
    axs[0].legend()
    z, p, k = signal.buttap(5)
    t = np.linspace(np.pi / 2, 3 * np.pi / 2, 200)
    axs[1].plot(np.cos(t), np.sin(t), color=pe.GRIS_CLARO, lw=0.8)
    axs[1].plot(p.real, p.imag, "x", color=pe.ROJO, ms=5, mew=1.2)
    axs[1].set_aspect("equal")
    axs[1].set_xlim(-1.3, 0.4)
    axs[1].set_ylim(-1.25, 1.25)
    axs[1].axhline(0, color=pe.GRIS, lw=0.4)
    axs[1].axvline(0, color=pe.GRIS, lw=0.4)
    axs[1].set_title(r"Polos, $N=5$, $\omega_c=1$")
    axs[1].set_xlabel(r"$\sigma$")
    axs[1].set_ylabel(r"$j\omega$")
    guardar(fig, "butterworth_orden")


@figura
def tipos_continuos():
    w = np.linspace(0, 2.5, 1500)
    dis = [("Butterworth", signal.butter(4, 1, analog=True)),
           ("Chebyshev I", signal.cheby1(4, 1, 1, analog=True)),
           ("Chebyshev II", signal.cheby2(4, 30, 1.6, analog=True)),
           ("Elíptico", signal.ellip(4, 1, 30, 1, analog=True))]
    fig, axs = pe.figura(2, 4, ancho=6.6, alto=2.6, sharex=True)
    for j, (tit, (b, a)) in enumerate(dis):
        _, H = signal.freqs(b, a, w)
        axs[0, j].plot(w, np.abs(H), color=pe.AZUL)
        axs[0, j].set_title(tit)
        axs[0, j].set_ylim(0, 1.1)
        axs[1, j].plot(w, db(H), color=pe.ROJO)
        axs[1, j].set_ylim(-60, 5)
        axs[1, j].set_xlabel(r"$\omega$")
    axs[0, 0].set_ylabel(r"$|H|$")
    axs[1, 0].set_ylabel("dB")
    guardar(fig, "tipos_continuos")


@figura
def polos_tipos():
    fig, axs = pe.figura(1, 4, ancho=6.6, alto=1.9, sharey=True)
    dis = [("Butterworth", signal.buttap(6)),
           ("Chebyshev I", signal.cheb1ap(6, 1)),
           ("Chebyshev II", signal.cheb2ap(6, 30)),
           ("Elíptico", signal.ellipap(6, 1, 30))]
    for ax, (tit, (z, p, k)) in zip(axs, dis):
        ax.plot(z.real, z.imag, "o", mfc="none", mec=pe.AZUL, ms=4, mew=1.0)
        ax.plot(p.real, p.imag, "x", color=pe.ROJO, ms=4.5, mew=1.1)
        ax.set_xlim(-1.4, 0.4)
        ax.set_ylim(-2.3, 2.3)
        ax.axhline(0, color=pe.GRIS, lw=0.4)
        ax.axvline(0, color=pe.GRIS, lw=0.4)
        ax.set_title(tit)
        ax.set_xlabel(r"$\sigma$")
    axs[0].set_ylabel(r"$j\omega$")
    guardar(fig, "polos_tipos")


@figura
def ejemplo_continuo():
    wp, ws, ap, as_ = 2 * np.pi * 1e3, 2 * np.pi * 5e3, 1, 40
    f = np.linspace(0, 8e3, 2000)
    w = 2 * np.pi * f
    fig, ax = pe.figura(ancho=4.4, alto=2.1)
    mascara_pb(ax, 1, 5, ap, as_, 8)
    dis = [("Butterworth, $N=4$", signal.butter, signal.buttord, ()),
           ("Chebyshev I, $N=3$", signal.cheby1, signal.cheb1ord, (ap,)),
           ("Chebyshev II, $N=3$", signal.cheby2, signal.cheb2ord, (as_,)),
           ("Elíptico, $N=3$", signal.ellip, signal.ellipord, (ap, as_))]
    for (tit, dis_f, ord_f, extra), c in zip(dis, (pe.AZUL, pe.ROJO, pe.VERDE, pe.NARANJA)):
        N, wn = ord_f(wp, ws, ap, as_, analog=True)
        b, a = dis_f(N, *extra, wn, analog=True)
        _, H = signal.freqs(b, a, w)
        ax.plot(f / 1e3, db(H), color=c, lw=1.1, label=tit)
    ax.set_ylim(-80, 5)
    ax.set_xlabel("$f$ (kHz)")
    ax.set_ylabel("dB")
    ax.set_title(r"$\alpha_p=1$ dB hasta 1 kHz, $\alpha_s=40$ dB desde 5 kHz")
    ax.legend(loc="lower left", fontsize=6)
    guardar(fig, "ejemplo_continuo")


@figura
def transformaciones():
    b, a = signal.cheby1(4, 1, 1, analog=True)
    w = np.linspace(0, 3, 2000)
    fig, axs = pe.figura(1, 4, ancho=6.6, alto=1.6, sharey=True)
    tr = [("Prototipo paso bajo, $\\omega_p=1$", (b, a)),
          ("Paso alto, $\\hat\\omega_p=1{,}5$", signal.lp2hp(b, a, 1.5)),
          ("Paso banda, $[1, 2]$", signal.lp2bp(b, a, np.sqrt(2), 1)),
          ("Supresor, $[1, 2]$", signal.lp2bs(b, a, np.sqrt(2), 1))]
    for ax, (tit, (bb, aa)) in zip(axs, tr):
        _, H = signal.freqs(bb, aa, w)
        ax.plot(w, np.abs(H), color=pe.AZUL)
        ax.set_title(tit, fontsize=7)
        ax.set_xlabel(r"$\omega$" if ax is axs[0] else r"$\hat\omega$")
    guardar(fig, "transformaciones")


# ---------------------------------------------------------------------
# Parte 3 · Filtros IIR
# ---------------------------------------------------------------------

@figura
def invarianza():
    """Invarianza al impulso de un Butterworth de orden 2 con dos periodos de muestreo."""
    wc = 1.0
    b, a = signal.butter(2, wc, analog=True)
    fig, axs = pe.figura(1, 2, ancho=6.0, alto=1.8, sharey=True)
    for ax, T in zip(axs, (1.0, 2.0)):
        r, p, _ = signal.residue(b, a)
        Om = np.linspace(0, np.pi, 1000)
        z = np.exp(1j * Om)
        Hd = T * sum(ri / (1 - np.exp(pi * T) / z) for ri, pi in zip(r, p))
        _, Ha = signal.freqs(b, a, Om / T)
        ax.plot(Om, np.abs(Ha), color=pe.GRIS, ls="--", lw=1.0, label=r"$|H_a(j\Omega/T)|$")
        ax.plot(Om, np.abs(Hd), color=pe.AZUL, label=r"$|H(e^{j\Omega})|$")
        ticks_pi(ax)
        ax.set_xlabel(r"$\Omega$")
        ax.set_title(f"$T={T:g}$ s ($\\omega_c T={wc * T:g}$)")
    axs[0].legend()
    guardar(fig, "invarianza")


@figura
def bilineal():
    Om = np.linspace(0, 0.98 * np.pi, 500)
    fig, axs = pe.figura(1, 2, ancho=6.0, alto=2.0, gridspec_kw=dict(width_ratios=[1.2, 1]))
    axs[0].plot(Om, 2 * np.tan(Om / 2), color=pe.AZUL, label=r"$\omega=\tan(\Omega/2)\cdot2/T$")
    axs[0].plot(Om, Om, color=pe.GRIS, ls="--", lw=0.8, label=r"$\omega=\Omega/T$")
    axs[0].set_ylim(0, 8)
    ticks_pi(axs[0])
    axs[0].set_xlabel(r"$\Omega$ (discreta)")
    axs[0].set_ylabel(r"$\omega$ (continua), $T=1$")
    axs[0].set_title("Compresión de frecuencias de la bilineal")
    axs[0].legend(loc="upper left")
    # semiplano izquierdo -> interior del círculo
    t = np.linspace(0, 2 * np.pi, 400)
    axs[1].fill(np.cos(t), np.sin(t), color=pe.AZUL, alpha=0.15, lw=0)
    axs[1].plot(np.cos(t), np.sin(t), color=pe.AZUL, lw=1.0)
    for s in (-0.5 + 1j * np.linspace(-6, 6, 200), -2 + 1j * np.linspace(-20, 20, 400)):
        zz = (1 + s / 2) / (1 - s / 2)
        axs[1].plot(zz.real, zz.imag, color=pe.ROJO, lw=0.7)
    axs[1].set_aspect("equal")
    axs[1].set_xlim(-1.3, 1.3)
    axs[1].set_ylim(-1.3, 1.3)
    axs[1].axhline(0, color=pe.GRIS, lw=0.4)
    axs[1].axvline(0, color=pe.GRIS, lw=0.4)
    axs[1].set_title(r"$\mathrm{Re}\,s<0 \to |z|<1$")
    axs[1].annotate(r"$j\omega\to e^{j\Omega}$", (0.55, 0.95), fontsize=6.5, color=pe.AZUL)
    axs[1].annotate(r"rectas $\mathrm{Re}\,s=-0{,}5,\ -2$", (-1.25, -1.25), fontsize=6, color=pe.ROJO)
    guardar(fig, "bilineal")


@figura
def iir_paso_bajo():
    fs = 200e3
    N, Wn = signal.buttord(25e3, 55e3, 0.5, 15, fs=fs)
    b, a = signal.butter(N, Wn, fs=fs)
    f, H = signal.freqz(b, a, 2000, fs=fs)
    fig, axs = pe.figura(1, 2, ancho=6.2, alto=1.9)
    mascara_pb(axs[0], 25, 55, 0.5, 15, 100)
    axs[0].plot(f / 1e3, db(H), color=pe.AZUL)
    axs[0].set_ylim(-60, 3)
    axs[0].set_xlabel("$f$ (kHz)")
    axs[0].set_ylabel("dB")
    axs[0].set_title(f"Butterworth digital, $N={N}$, $f_s=200$ kHz")
    z, p, _ = signal.tf2zpk(b, a)
    zplano(axs[1], z, p, lim=1.25)
    axs[1].set_title("Ceros en $z=-1$")
    guardar(fig, "iir_paso_bajo")


@figura
def iir_ejemplos():
    fig, axs = pe.figura(1, 2, ancho=6.2, alto=1.9)
    N, Wn = signal.cheb1ord(700, 500, 1, 32, fs=2000)
    b, a = signal.cheby1(N, 1, Wn, "highpass", fs=2000)
    f, H = signal.freqz(b, a, 2000, fs=2000)
    kw = dict(color=pe.GRIS_CLARO, alpha=0.45, lw=0)
    axs[0].fill_between([700, 1000], [-1, -1], [-100, -100], **kw)
    axs[0].fill_between([0, 500], [-32, -32], [5, 5], **kw)
    axs[0].plot(f, db(H), color=pe.AZUL)
    axs[0].set_ylim(-70, 3)
    axs[0].set_xlabel("$f$ (Hz)")
    axs[0].set_title(f"Paso alto Chebyshev I, $N={N}$")
    N, Wn = signal.buttord([0.45, 0.65], [0.3, 0.75], 1, 40)
    sos = signal.butter(N, Wn, "bandpass", output="sos")
    Om, H = signal.sosfreqz(sos, 2000)
    axs[1].fill_between([0.45 * np.pi, 0.65 * np.pi], [-1, -1], [-100, -100], **kw)
    axs[1].fill_between([0, 0.3 * np.pi], [-40, -40], [5, 5], **kw)
    axs[1].fill_between([0.75 * np.pi, np.pi], [-40, -40], [5, 5], **kw)
    axs[1].plot(Om, db(H), color=pe.AZUL)
    axs[1].set_ylim(-80, 3)
    ticks_pi(axs[1])
    axs[1].set_xlabel(r"$\Omega$")
    axs[1].set_title(f"Paso banda Butterworth, $N={N}$ (orden {2 * N})")
    guardar(fig, "iir_ejemplos")


# ---------------------------------------------------------------------
# Parte 4 · Filtros FIR
# ---------------------------------------------------------------------

def h_ideal(L, wc):
    n = np.arange(-L, L + 1)
    return n, wc / np.pi * np.sinc(wc / np.pi * n)


@figura
def fir_ventana_metodo():
    L, wc = 12, 0.4 * np.pi
    n, hd = h_ideal(L, wc)
    nn = np.arange(-25, 26)
    hdd = wc / np.pi * np.sinc(wc / np.pi * nn)
    fig, axs = pe.figura(1, 3, ancho=6.6, alto=1.6, sharey=True)
    pe.stem(axs[0], nn, hdd, ms=1.8)
    axs[0].set_title(r"$h_d[n]$ ideal")
    w = np.hamming(2 * L + 1)
    pe.stem(axs[1], n, hd * w, ms=1.8, color=pe.ROJO)
    axs[1].plot(n, w * hd.max(), color=pe.GRIS_CLARO, lw=0.8)
    axs[1].set_xlim(-25, 25)
    axs[1].set_title(r"$h_d[n]\,w[n]$, $|n|\leq L=12$")
    pe.stem(axs[2], n + L, hd * w, ms=1.8, color=pe.VERDE)
    axs[2].set_xlim(-12, 38)
    axs[2].set_title(r"$h[n]=h_d[n-L]\,w[n-L]$")
    for ax in axs:
        ax.set_xlabel("$n$")
    guardar(fig, "fir_ventana_metodo")


@figura
def gibbs():
    Om = np.linspace(0, np.pi, 3000)
    fig, axs = pe.figura(1, 2, ancho=6.2, alto=1.9)
    for L, c in ((5, pe.NARANJA), (15, pe.ROJO), (45, pe.AZUL)):
        n, hd = h_ideal(L, 0.4 * np.pi)
        _, H = signal.freqz(hd, 1, Om)
        axs[0].plot(Om, np.abs(H), color=c, lw=0.9, label=f"$L={L}$")
        axs[1].plot(Om, db(H), color=c, lw=0.8)
    for ax in axs:
        ticks_pi(ax)
        ax.set_xlabel(r"$\Omega$")
        ax.axvline(0.4 * np.pi, color=pe.GRIS, ls="--", lw=0.5)
    axs[0].set_title("Truncamiento (ventana rectangular)")
    axs[0].legend(loc="upper right")
    axs[1].set_ylim(-60, 5)
    axs[1].axhline(-21, color=pe.GRIS, ls=":", lw=0.6)
    axs[1].set_title("En dB: el primer rizo no baja de unos $-21$ dB")
    guardar(fig, "gibbs")


@figura
def ventanas_fir():
    Om = np.linspace(0, np.pi, 3000)
    L = 20
    fig, axs = pe.figura(1, 2, ancho=6.2, alto=2.0, gridspec_kw=dict(width_ratios=[1, 1.7]))
    n = np.arange(-L, L + 1)
    vent = [("Rectangular", np.ones(2 * L + 1), pe.GRIS), ("Hann", np.hanning(2 * L + 3)[1:-1], pe.VERDE),
            ("Hamming", np.hamming(2 * L + 1), pe.ROJO), ("Blackman", np.blackman(2 * L + 3)[1:-1], pe.AZUL)]
    _, hd = h_ideal(L, 0.4 * np.pi)
    for tit, w, c in vent:
        axs[0].plot(n, w, color=c, label=tit)
        _, H = signal.freqz(hd * w, 1, Om)
        axs[1].plot(Om, db(H), color=c, lw=0.9, label=tit)
    axs[0].set_xlabel("$n$")
    axs[0].set_title(r"$w[n]$, $L=20$")
    axs[0].legend(fontsize=6, loc="lower center")
    axs[1].set_ylim(-110, 5)
    ticks_pi(axs[1])
    axs[1].set_xlabel(r"$\Omega$")
    axs[1].set_title(r"Paso bajo $\Omega_c=0{,}4\pi$ con cada ventana (dB)")
    guardar(fig, "ventanas_fir")


@figura
def ejemplo_fir():
    Om = np.linspace(0, np.pi, 3000)
    fig, ax = pe.figura(ancho=4.4, alto=2.0)
    kw = dict(color=pe.GRIS_CLARO, alpha=0.45, lw=0)
    ax.fill_between([0.5 * np.pi, np.pi], [-40, -40], [5, 5], **kw)
    L = 16
    n, hd = h_ideal(L, 0.4 * np.pi)
    for tit, w, c in (("Hann, $L=16$", np.hanning(2 * L + 3)[1:-1], pe.VERDE),
                      ("Kaiser $\\beta=3{,}40$, $L=12$", None, pe.AZUL)):
        if w is None:
            n2, hd2 = h_ideal(12, 0.4 * np.pi)
            h = hd2 * np.kaiser(25, 3.395)
        else:
            h = hd * w
        _, H = signal.freqz(h, 1, Om)
        ax.plot(Om, db(H), color=c, label=tit)
    ax.set_ylim(-90, 5)
    ticks_pi(ax)
    ax.set_xticks([0, 0.3 * np.pi, 0.5 * np.pi, np.pi], ["0", r"$0{,}3\pi$", r"$0{,}5\pi$", r"$\pi$"])
    ax.set_xlabel(r"$\Omega$")
    ax.set_ylabel("dB")
    ax.set_title(r"$\Omega_p=0{,}3\pi$, $\Omega_s=0{,}5\pi$, $\alpha_s=40$ dB")
    ax.legend(loc="upper right", fontsize=6.5)
    guardar(fig, "ejemplo_fir")


@figura
def kaiser():
    fig, axs = pe.figura(1, 2, ancho=6.2, alto=1.9)
    L = 20
    n = np.arange(-L, L + 1)
    Om = np.linspace(0, np.pi, 3000)
    _, hd = h_ideal(L, 0.4 * np.pi)
    for b, c in ((0, pe.GRIS), (3, pe.VERDE), (6, pe.ROJO), (9, pe.AZUL)):
        w = np.kaiser(2 * L + 1, b)
        axs[0].plot(n, w, color=c, label=rf"$\beta={b}$")
        _, H = signal.freqz(hd * w, 1, Om)
        axs[1].plot(Om, db(H), color=c, lw=0.9)
    axs[0].set_title(r"Ventana de Kaiser, $L=20$")
    axs[0].set_xlabel("$n$")
    axs[0].legend(fontsize=6)
    axs[1].set_ylim(-120, 5)
    ticks_pi(axs[1])
    axs[1].set_xlabel(r"$\Omega$")
    axs[1].set_title(r"$\beta$ mayor: menos rizado, transición más ancha")
    guardar(fig, "kaiser")


@figura
def equirrizado():
    Om = np.linspace(0, np.pi, 4000)
    N = 31
    h_pm = signal.remez(N, [0, 0.3, 0.5, 1], [1, 0], fs=2)
    h_k = signal.firwin(N, 0.4, window=("kaiser", 3.395), fs=2)
    fig, ax = pe.figura(ancho=4.4, alto=1.9)
    for h, tit, c in ((h_k, "Ventana de Kaiser", pe.GRIS), (h_pm, "Parks–McClellan (equirrizado)", pe.AZUL)):
        _, H = signal.freqz(h, 1, Om)
        ax.plot(Om, db(H), color=c, label=tit)
    ax.set_ylim(-80, 5)
    ax.set_xticks([0, 0.3 * np.pi, 0.5 * np.pi, np.pi], ["0", r"$0{,}3\pi$", r"$0{,}5\pi$", r"$\pi$"])
    ax.set_xlabel(r"$\Omega$")
    ax.set_title(f"Dos FIR de {N} coeficientes")
    ax.legend(loc="upper right", fontsize=6.5)
    guardar(fig, "equirrizado")


@figura
def tipos_fase_lineal():
    hs = [("Tipo I", np.array([1, 2, 3, 4, 3, 2, 1.0])),
          ("Tipo II", np.array([1, 2, 3, 3, 2, 1.0])),
          ("Tipo III", np.array([1, 2, 3, 0, -3, -2, -1.0])),
          ("Tipo IV", np.array([1, 2, 3, -3, -2, -1.0]))]
    fig, axs = pe.figura(2, 4, ancho=6.6, alto=2.8, gridspec_kw=dict(height_ratios=[1, 1.25]))
    for j, (tit, h) in enumerate(hs):
        pe.stem(axs[0, j], np.arange(len(h)), h, ms=2.2)
        axs[0, j].axvline((len(h) - 1) / 2, color=pe.GRIS_CLARO, ls="--", lw=0.6)
        axs[0, j].set_title(f"{tit}, $N={len(h)}$")
        axs[0, j].set_xlabel("$n$")
        zplano(axs[1, j], np.roots(h), np.zeros(0), lim=2.6)
        axs[1, j].set_xlabel("")
        axs[1, j].set_ylabel("")
    guardar(fig, "tipos_fase_lineal")


@figura
def multibanda():
    f = [0, 0.28, 0.3, 0.5, 0.52, 1]
    A = [0.3, 0.3, 1.0, 1.0, 0.7, 0.7]
    h = signal.firwin2(101, f, A, window="hamming")
    Om, H = signal.freqz(h, 1, 3000)
    fig, ax = pe.figura(ancho=4.0, alto=1.7)
    ax.plot(np.array(f) * np.pi, A, color=pe.GRIS_CLARO, lw=2.5, label="deseada")
    ax.plot(Om, np.abs(H), color=pe.AZUL, lw=1.0, label="FIR, 101 coef.")
    ticks_pi(ax)
    ax.set_xlabel(r"$\Omega$")
    ax.set_title("Diseño multibanda por muestreo en frecuencia y ventana")
    ax.legend(loc="lower right", fontsize=6.5)
    guardar(fig, "multibanda")


# ---------------------------------------------------------------------
# Parte 5 · Filtros especiales
# ---------------------------------------------------------------------

@figura
def fase_cero():
    fs = 500
    t = np.arange(0, 1, 1 / fs)
    rng = np.random.default_rng(3)
    x = np.exp(-((t - 0.4) / 0.05) ** 2) + 0.15 * rng.standard_normal(len(t))
    b, a = signal.butter(3, 15, fs=fs)
    y1 = signal.lfilter(b, a, x)
    y2 = signal.filtfilt(b, a, x)
    fig, ax = pe.figura(ancho=4.4, alto=1.8)
    ax.plot(t, x, color=pe.GRIS_CLARO, lw=0.7, label="señal ruidosa")
    ax.plot(t, y1, color=pe.ROJO, label="lfilter: retrasada y deformada")
    ax.plot(t, y2, color=pe.AZUL, label="filtfilt: fase cero")
    ax.set_xlim(0.15, 0.7)
    ax.set_xlabel("$t$ (s)")
    ax.legend(fontsize=6, loc="upper right")
    guardar(fig, "fase_cero")


@figura
def fase_minima():
    den = np.poly([0.5, 0.1 + 0.3j, 0.1 - 0.3j]).real / 4
    ceros = {"fase mínima": [0.3j, -0.3j, 0.25], "fase mixta": [0.3j, -0.3j, 4],
             "fase máxima": [1 / 0.3j, -1 / 0.3j, 4]}
    Om = np.linspace(0, np.pi, 1500)
    fig, axs = pe.figura(1, 3, ancho=6.6, alto=1.9, gridspec_kw=dict(width_ratios=[1, 1, 1.3]))
    ref = None
    for (tit, z), c in zip(ceros.items(), (pe.AZUL, pe.NARANJA, pe.ROJO)):
        num = np.poly(z)
        _, H = signal.freqz(num, den, Om)
        if ref is None:
            ref = np.abs(H[0])
        num = num * ref / np.abs(H[0])
        _, H = signal.freqz(num, den, Om)
        axs[0].plot(Om, np.abs(H), color=c, lw=1.0)
        axs[1].plot(Om, np.unwrap(np.angle(H)), color=c, label=tit)
        axs[2].plot(np.real(z), np.imag(z), "o", mfc="none", mec=c, ms=4.5, mew=1.0)
    t = np.linspace(0, 2 * np.pi, 300)
    axs[2].plot(np.cos(t), np.sin(t), color=pe.GRIS, lw=0.6)
    axs[2].set_aspect("equal")
    axs[2].set_xlim(-1.5, 4.5)
    axs[2].set_ylim(-3.6, 3.6)
    axs[2].set_title("Ceros")
    axs[0].set_title(r"$|H(e^{j\Omega})|$: idéntico")
    axs[1].set_title(r"$\arg H(e^{j\Omega})$")
    axs[1].legend(fontsize=6, loc="lower left")
    for ax in axs[:2]:
        ticks_pi(ax)
        ax.set_xlabel(r"$\Omega$")
    guardar(fig, "fase_minima")


@figura
def paso_todo():
    den = np.array([1, 0.4, 0.18, -0.3])
    num = den[::-1]
    Om = np.linspace(0, np.pi, 1500)
    _, H = signal.freqz(num, den, Om)
    _, gd = signal.group_delay((num, den), Om)
    fig, axs = pe.figura(1, 3, ancho=6.6, alto=1.9)
    zplano(axs[0], np.roots(num), np.roots(den), lim=2.0)
    axs[0].set_title("Polos y ceros recíprocos")
    axs[1].plot(Om, np.unwrap(np.angle(H)), color=pe.AZUL)
    axs[1].set_title(r"$\arg H(e^{j\Omega})$: de 0 a $-3\pi$")
    axs[1].set_yticks([0, -np.pi, -2 * np.pi, -3 * np.pi], ["0", r"$-\pi$", r"$-2\pi$", r"$-3\pi$"])
    axs[2].plot(Om, gd, color=pe.ROJO)
    axs[2].set_title(r"Retardo de grupo (muestras); $|H|=1$")
    for ax in axs[1:]:
        ticks_pi(ax)
        ax.set_xlabel(r"$\Omega$")
    guardar(fig, "paso_todo")


@figura
def peine():
    Om = np.linspace(0, np.pi, 3000)
    fig, axs = pe.figura(1, 2, ancho=6.4, alto=1.8)
    for L, c in ((1, pe.GRIS), (4, pe.AZUL)):
        b = np.zeros(L + 1)
        b[0] = b[L] = 0.5
        _, H = signal.freqz(b, 1, Om)
        axs[0].plot(Om, np.abs(H), color=c, label=f"$L={L}$")
    axs[0].set_title(r"$G(z^L)$ con $G(z)=\frac{1}{2}(1+z^{-1})$")
    axs[0].legend(fontsize=6.5)
    ticks_pi(axs[0])
    axs[0].set_xlabel(r"$\Omega$")
    fs = 5000
    b, a = signal.iircomb(50, 30, ftype="notch", fs=fs)
    f, H = signal.freqz(b, a, 20000, fs=fs)
    axs[1].plot(f, db(H, -50), color=pe.AZUL, lw=0.8)
    axs[1].set_xlim(0, 400)
    axs[1].set_xticks([0, 50, 100, 150, 200, 250, 300, 350, 400])
    axs[1].set_xlabel("$f$ (Hz)")
    axs[1].set_title("Peine de muescas: 50 Hz y armónicos, $f_s=5$ kHz")
    guardar(fig, "peine")


if __name__ == "__main__":
    nombres = sys.argv[1:] or list(FIGURAS)
    for nombre in nombres:
        FIGURAS[nombre]()
        print("ok", nombre)
