"""Genera todas las figuras del Tema 2 (muestreo y reconstrucción).

    python generar_figuras.py               # todas
    python generar_figuras.py alias_mapa    # solo las indicadas

Las figuras se guardan en PDF junto a este script.
"""

from __future__ import annotations

import pathlib
import sys

import numpy as np

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


def senal_ejemplo(t):
    """Señal suave de banda (casi) limitada usada en varias figuras."""
    return 0.6 * np.sin(2 * np.pi * 0.45 * t + 0.3) + 0.3 * np.cos(2 * np.pi * 1.05 * t) + 0.1


def espectro_triangular(w, wm):
    """Espectro de ejemplo: triángulo de altura 1 y ancho de banda wm."""
    return np.clip(1 - np.abs(w) / wm, 0, None)


def ticks_pi(ax, maximo=3, eje="x", denominador="", factor=np.pi):
    valores = np.arange(-maximo, maximo + 1)
    etiquetas = []
    for k in valores:
        if k == 0:
            etiquetas.append("0")
        elif abs(k) == 1:
            etiquetas.append(("$-" if k < 0 else "$") + r"\pi" + denominador + "$")
        else:
            etiquetas.append(f"${k}" + r"\pi" + denominador + "$")
    (ax.set_xticks if eje == "x" else ax.set_yticks)(valores * factor, etiquetas)


# ---------------------------------------------------------------------
# Parte 1 · Muestreo
# ---------------------------------------------------------------------

@figura
def muestreo_cuant_cod():
    t = np.linspace(0, 4, 800)
    Ts = 0.25
    n = np.arange(0, 17)
    x = senal_ejemplo(t)
    xn = senal_ejemplo(n * Ts)
    D = 0.25
    xq = D * np.round(xn / D)
    fig, axs = pe.figura(1, 3, ancho=6.4, alto=1.75, sharey=True)
    axs[0].plot(t, x)
    axs[0].set_title("Analógica $x(t)$")
    axs[0].set_xlabel("$t$ (s)")
    axs[1].plot(t, x, color=pe.GRIS_CLARO, lw=0.8)
    pe.stem(axs[1], n * Ts, xn)
    axs[1].set_title("Muestreada $x[n]=x(nT_s)$")
    axs[1].set_xlabel("$t=nT_s$")
    for k in np.arange(-4, 5) * D:
        axs[2].axhline(k, color="#E3E4EC", lw=0.5, zorder=0)
    pe.stem(axs[2], n, xq, color=pe.ROJO)
    axs[2].set_title(r"Cuantificada ($\Delta=0{,}25$)")
    axs[2].set_xlabel("$n$")
    for i in (0, 4, 8):
        codigo = format(int(round(xq[i] / D)) + 8, "04b")
        axs[2].annotate(codigo, (i, xq[i]), xytext=(0, 5), textcoords="offset points",
                        ha="center", fontsize=6, color=pe.GRIS)
    guardar(fig, "muestreo_cuant_cod")


@figura
def muestreo_periodico():
    Ts = 0.2
    t = np.linspace(0, 3, 800)
    n = np.arange(0, 16)
    fig, axs = pe.figura(1, 2, ancho=5.4, alto=1.7)
    axs[0].plot(t, senal_ejemplo(t), color=pe.GRIS_CLARO, lw=0.9, label="$x(t)$")
    pe.stem(axs[0], n * Ts, senal_ejemplo(n * Ts))
    axs[0].set_xlabel("$t$ (s)")
    axs[0].set_title("Frente al tiempo: muestras en $t=nT_s$")
    pe.stem(axs[1], n, senal_ejemplo(n * Ts))
    axs[1].set_xlabel("$n$")
    axs[1].set_title("Frente al índice: $x[n]$")
    guardar(fig, "muestreo_periodico")


@figura
def alias_sinusoides():
    Ts = 2.0
    t = np.linspace(0, 20, 2000)
    n = np.arange(0, 11)
    w1, w2 = 2 * np.pi / 10, 2 * np.pi / (10 / 6)
    fig, ax = pe.figura(ancho=4.6, alto=1.7)
    ax.plot(t, np.sin(w2 * t), color=pe.ROJO, lw=0.8, label=r"$\sin(\frac{2\pi}{10/6}t)$")
    ax.plot(t, np.sin(w1 * t), label=r"$\sin(\frac{2\pi}{10}t)$")
    pe.stem(ax, n * Ts, np.sin(w1 * Ts * n), color="black", ms=3.5)
    ax.set_xlabel("$t$ (s)")
    ax.set_title(r"Mismas muestras con $T_s=2$ s")
    ax.legend(loc="upper right", ncol=2, fontsize=6)
    ax.set_ylim(-1.3, 1.6)
    guardar(fig, "alias_sinusoides")


@figura
def alias_mapa():
    fs = 1.0
    f = np.linspace(0, 2.6 * fs, 2000)
    fa = np.abs(((f + fs / 2) % fs) - fs / 2)
    fig, ax = pe.figura(ancho=4.0, alto=1.8)
    ax.plot(f, fa)
    ax.axvspan(0, fs / 2, color=pe.VERDE, alpha=0.08, lw=0)
    for k in range(1, 6):
        ax.axvline(k * fs / 2, color=pe.GRIS_CLARO, lw=0.5, ls="--")
    f0 = 1.3
    ax.plot([f0, f0], [0, abs(((f0 + 0.5) % 1) - 0.5)], color=pe.ROJO, lw=0.8)
    ax.plot([f0], [0.3], "o", color=pe.ROJO, ms=3)
    ax.annotate(r"$f_0=1{,}3f_s\ \to\ 0{,}3f_s$", (f0, 0.3), xytext=(8, -2), textcoords="offset points",
                fontsize=6.5, color=pe.ROJO)
    ax.set_xticks([0, 0.5, 1, 1.5, 2, 2.5], ["0", r"$\frac{f_s}{2}$", "$f_s$", r"$\frac{3f_s}{2}$",
                                              "$2f_s$", r"$\frac{5f_s}{2}$"])
    ax.set_yticks([0, 0.25, 0.5], ["0", r"$\frac{f_s}{4}$", r"$\frac{f_s}{2}$"])
    ax.set_xlabel("frecuencia de la señal continua $f$")
    ax.set_ylabel("frecuencia aparente")
    guardar(fig, "alias_mapa")


@figura
def tren_impulsos():
    Ts = 0.25
    t = np.linspace(0, 3, 800)
    n = np.arange(0, 13)
    fig, axs = pe.figura(1, 3, ancho=6.4, alto=1.55, sharey=True)
    axs[0].plot(t, senal_ejemplo(t))
    axs[0].set_title("$x(t)$")
    for k in n:
        axs[1].annotate("", (k * Ts, 1), (k * Ts, 0),
                        arrowprops=dict(arrowstyle="-|>", color=pe.ROJO, lw=0.9, mutation_scale=6))
    axs[1].set_title(r"$p(t)=\sum_n\delta(t-nT_s)$")
    xs = senal_ejemplo(n * Ts)
    axs[2].plot(t, senal_ejemplo(t), color=pe.GRIS_CLARO, lw=0.8)
    for k, v in zip(n, xs):
        axs[2].annotate("", (k * Ts, v), (k * Ts, 0),
                        arrowprops=dict(arrowstyle="-|>", color=pe.AZUL, lw=0.9, mutation_scale=6))
    axs[2].set_title(r"$x_s(t)=x(t)\,p(t)$")
    for ax in axs:
        ax.set_xlim(-0.1, 3.1)
        ax.set_ylim(-1.0, 1.15)
        ax.set_xlabel("$t$")
        pe.ejes_centrados(ax)
    guardar(fig, "tren_impulsos")


def _replicas(ax, ws, wm, rango, color=pe.AZUL, escala=1.0, solape=True):
    w = np.linspace(-rango, rango, 4000)
    total = np.zeros_like(w)
    for k in range(-6, 7):
        r = escala * espectro_triangular(w - k * ws, wm)
        total += r
        if k != 0:
            ax.plot(w, r, color=pe.GRIS_CLARO, lw=0.7)
    ax.plot(w, escala * espectro_triangular(w, wm), color=color, lw=1.0)
    if solape:
        ax.plot(w, total, color=pe.ROJO, lw=1.0, ls="-")
    ax.set_xlim(-rango, rango)
    return w


@figura
def espectro_replicas():
    wm = 1.0
    fig, axs = pe.figura(3, 1, ancho=4.6, alto=3.3, sharex=True)
    w = np.linspace(-4.5, 4.5, 2000)
    axs[0].plot(w, espectro_triangular(w, wm))
    axs[0].set_title(r"$|X(j\omega)|$: banda limitada a $\omega_m$", loc="left")
    axs[0].set_yticks([0, 1], ["0", "1"])
    _replicas(axs[1], 3.0, wm, 4.5, solape=False)
    axs[1].set_title(r"$\omega_s=3\omega_m>2\omega_m$: las réplicas no se solapan", loc="left")
    _replicas(axs[2], 1.5, wm, 4.5)
    axs[2].set_title(r"$\omega_s=1{,}5\omega_m<2\omega_m$: solapamiento (aliasing)", loc="left")
    for ax in axs[1:]:
        ax.set_yticks([0, 1], ["0", r"$\frac{1}{T_s}$"])
    axs[2].set_xticks([-3, -1.5, -1, 0, 1, 1.5, 3], [r"$-2\omega_s$", r"$-\omega_s$", "", "0", r"$\omega_m$",
                                                     r"$\omega_s$", r"$2\omega_s$"])
    axs[1].set_xticks([-3, -1, 0, 1, 3], [r"$-\omega_s$", r"$-\omega_m$", "0", r"$\omega_m$", r"$\omega_s$"])
    axs[1].tick_params(labelbottom=True)
    axs[2].set_xlabel(r"$\omega$")
    for ax in axs:
        ax.set_ylim(-0.05, 1.45)
    guardar(fig, "espectro_replicas")


@figura
def vision_continua_discreta():
    wm, Ts = 1.0, 2 * np.pi / 3.0
    ws = 2 * np.pi / Ts
    fig, axs = pe.figura(2, 1, ancho=4.6, alto=2.4)
    _replicas(axs[0], ws, wm, 2.2 * ws, solape=False)
    axs[0].set_xticks([-2 * ws, -ws, -ws / 2, 0, ws / 2, ws, 2 * ws],
                      [r"$-2\omega_s$", r"$-\omega_s$", r"$-\frac{\omega_s}{2}$", "0", r"$\frac{\omega_s}{2}$",
                       r"$\omega_s$", r"$2\omega_s$"])
    axs[0].set_xlabel(r"$\omega$ (rad/s)")
    axs[0].set_title(r"$X_s(j\omega)$: visión continua", loc="left")
    _replicas(axs[1], ws, wm, 2.2 * ws, solape=False, color=pe.VERDE)
    axs[1].set_xticks([-2 * ws, -ws, -ws / 2, 0, ws / 2, ws, 2 * ws],
                      [r"$-4\pi$", r"$-2\pi$", r"$-\pi$", "0", r"$\pi$", r"$2\pi$", r"$4\pi$"])
    axs[1].set_xlabel(r"$\Omega=\omega T_s$ (rad/muestra)")
    axs[1].set_title(r"$X(e^{j\Omega})$: visión discreta (DTFT de $x[n]$)", loc="left")
    for ax in axs:
        ax.set_yticks([0, 1], ["0", r"$\frac{1}{T_s}$"])
        ax.set_ylim(-0.05, 1.3)
    guardar(fig, "vision_continua_discreta")


@figura
def antialiasing():
    w = np.linspace(-4, 4, 2000)
    X = 0.8 * np.exp(-(w / 1.6) ** 2) + 0.25 * np.exp(-((np.abs(w) - 2.6) / 0.25) ** 2)
    wc = 1.2
    H = 1 / np.sqrt(1 + (w / wc) ** 16)
    fig, axs = pe.figura(1, 2, ancho=5.6, alto=1.7, sharey=True)
    axs[0].plot(w, X, label="señal + ruido")
    axs[0].plot(w, H, color=pe.NARANJA, lw=0.9, ls="--", label="filtro")
    axs[0].set_title("Antes del filtro antialiasing")
    axs[0].legend(loc="upper right", fontsize=6)
    axs[1].plot(w, X * H)
    axs[1].set_title("Después: banda limitada a $\\omega_c<\\omega_s/2$")
    for ax in axs:
        ax.set_xticks([-2.5, -1.2, 0, 1.2, 2.5], [r"$-\frac{\omega_s}{2}$", r"$-\omega_c$", "0",
                                                  r"$\omega_c$", r"$\frac{\omega_s}{2}$"])
        ax.axvline(2.5, color=pe.GRIS_CLARO, lw=0.6, ls=":")
        ax.axvline(-2.5, color=pe.GRIS_CLARO, lw=0.6, ls=":")
        ax.set_xlabel(r"$\omega$")
    guardar(fig, "antialiasing")


@figura
def muestreo_natural():
    Ts, tau = 0.2, 0.07
    t = np.linspace(0, 3, 3000)
    x = senal_ejemplo(t)
    pulso = ((t % Ts) < tau).astype(float)
    k = np.floor(t / Ts)
    plano = senal_ejemplo(k * Ts) * pulso
    fig, axs = pe.figura(1, 2, ancho=5.6, alto=1.6, sharey=True)
    axs[0].plot(t, x, color=pe.GRIS_CLARO, lw=0.8)
    axs[0].plot(t, x * pulso)
    axs[0].set_title("Natural: $x(t)\\,p_\\tau(t)$")
    axs[1].plot(t, x, color=pe.GRIS_CLARO, lw=0.8)
    axs[1].plot(t, plano, color=pe.ROJO)
    axs[1].set_title("De techo plano (muestreo y retención)")
    for ax in axs:
        ax.set_xlabel("$t$")
        pe.ejes_centrados(ax)
    guardar(fig, "muestreo_natural")


# ---------------------------------------------------------------------
# Parte 2 · Reconstrucción
# ---------------------------------------------------------------------

@figura
def reconstruccion_ideal():
    wm, ws = 1.0, 3.0
    fig, ax = pe.figura(ancho=4.6, alto=1.6)
    _replicas(ax, ws, wm, 7.5, solape=False)
    wc = ws / 2
    ax.plot([-7.5, -wc, -wc, wc, wc, 7.5], [0, 0, 1.15, 1.15, 0, 0], color=pe.NARANJA, lw=1.0, ls="--",
            label=r"$H(j\omega)=T_s\,\Pi(\omega/2\omega_c)$")
    ax.set_xticks([-ws, -wc, -wm, 0, wm, wc, ws], [r"$-\omega_s$", r"$-\omega_c$", "", "0", r"$\omega_m$",
                                                    r"$\omega_c$", r"$\omega_s$"])
    ax.set_yticks([0, 1], ["0", r"$\frac{1}{T_s}$"])
    ax.set_ylim(-0.05, 1.5)
    ax.legend(loc="upper right", fontsize=6)
    ax.set_xlabel(r"$\omega$")
    guardar(fig, "reconstruccion_ideal")


@figura
def interpolacion_sinc():
    Ts = 1.0
    n = np.arange(-3, 6)
    xn = np.array([0.1, 0.4, 0.9, 0.6, -0.2, -0.5, 0.2, 0.7, 0.3])
    t = np.linspace(-4, 7, 2000)
    fig, ax = pe.figura(ancho=4.6, alto=1.8)
    total = np.zeros_like(t)
    for k, v in zip(n, xn):
        c = v * np.sinc((t - k * Ts) / Ts)
        total += c
        ax.plot(t, c, color=pe.GRIS_CLARO, lw=0.7)
    ax.plot(t, total, label=r"$y(t)=\sum_n x[n]\,\mathrm{sinc}((t-nT_s)/T_s)$")
    pe.stem(ax, n * Ts, xn, color=pe.ROJO)
    ax.set_xlim(-4, 7)
    ax.set_xlabel("$t/T_s$")
    ax.legend(loc="upper right", fontsize=6)
    ax.set_ylim(-0.75, 1.35)
    guardar(fig, "interpolacion_sinc")


@figura
def ejemplo_reconstruccion():
    w0, Ts = 2 * np.pi / 10, 4.0
    n = np.arange(-30, 31)
    xn = np.sin(w0 * Ts * n)
    t = np.linspace(0, 40, 2000)
    fig, axs = pe.figura(1, 2, ancho=5.8, alto=1.7, sharey=True)
    for ax, wc, titulo in ((axs[0], np.pi / Ts, r"$\omega_c=\omega_s/2=\frac{2\pi}{8}$"),
                           (axs[1], 2 * np.pi / 7, r"$\omega_c=\frac{2\pi}{7}$")):
        y = (wc * Ts / np.pi) * (np.sinc(wc * (t[:, None] - n * Ts) / np.pi) @ xn)
        ax.plot(t, np.sin(w0 * t), color=pe.GRIS_CLARO, lw=2.2, label="original")
        ax.plot(t, y, lw=1.0, label="reconstruida")
        m = (n * Ts >= 0) & (n * Ts <= 40)
        pe.stem(ax, n[m] * Ts, xn[m], color=pe.ROJO)
        ax.set_title(titulo)
        ax.set_xlabel("$t$ (s)")
    axs[0].legend(loc="lower left", fontsize=6)
    guardar(fig, "ejemplo_reconstruccion")


@figura
def retenedores_tiempo():
    Ts = 1.0
    n = np.arange(0, 9)
    xn = senal_ejemplo(0.3 * n)
    t = np.linspace(0, 8, 2000)
    k = np.minimum(np.floor(t).astype(int), n[-1])
    zoh = xn[k]
    foh = np.interp(t, n, xn)
    pred = xn[k] + (xn[k] - xn[np.maximum(k - 1, 0)]) * (t - k)
    fig, axs = pe.figura(1, 3, ancho=6.4, alto=1.6, sharey=True)
    for ax, y, titulo, c in ((axs[0], zoh, "Orden cero (ZOH)", pe.AZUL),
                             (axs[1], foh, "Orden uno no causal", pe.VERDE),
                             (axs[2], pred, "Orden uno causal (predictivo)", pe.NARANJA)):
        ax.plot(t, senal_ejemplo(0.3 * t), color=pe.GRIS_CLARO, lw=1.6)
        ax.plot(t, y, color=c, lw=1.0)
        pe.stem(ax, n, xn, color=pe.ROJO, ms=2.6)
        ax.set_title(titulo)
        ax.set_xlabel("$t/T_s$")
    guardar(fig, "retenedores_tiempo")


@figura
def retenedores_h():
    t = np.linspace(-1.5, 2.5, 2000)
    zoh = ((t >= 0) & (t < 1)).astype(float)
    foh = np.clip(1 - np.abs(t), 0, None)
    pred = np.where((t >= 0) & (t < 1), 1 + t, 0) + np.where((t >= 1) & (t < 2), 1 - t, 0)
    fig, axs = pe.figura(1, 3, ancho=6.4, alto=1.55, sharey=True)
    for ax, y, titulo, c in ((axs[0], zoh, r"ZOH: $\Pi((t-T_s/2)/T_s)$", pe.AZUL),
                             (axs[1], foh, r"FOH no causal: $\Lambda(t/T_s)$", pe.VERDE),
                             (axs[2], pred, "FOH causal (predictivo)", pe.NARANJA)):
        ax.plot(t, y, color=c)
        pe.ejes_centrados(ax)
        ax.set_title(titulo)
        ax.set_xlabel("$t/T_s$")
        ax.set_xticks([-1, 0, 1, 2])
    guardar(fig, "retenedores_h")


@figura
def retenedores_frecuencia():
    u = np.linspace(-3, 3, 3000)  # ω/ωs
    x = np.pi * u                 # ωTs/2
    zoh = np.abs(np.sinc(u))
    foh = np.sinc(u) ** 2
    pred = np.sqrt(1 + (2 * np.pi * u) ** 2) * np.sinc(u) ** 2
    ideal = (np.abs(u) <= 0.5).astype(float)
    fig, ax = pe.figura(ancho=4.6, alto=1.9)
    ax.plot(u, ideal, color=pe.GRIS, lw=0.9, ls="--", label="ideal")
    ax.plot(u, zoh, label="ZOH")
    ax.plot(u, foh, color=pe.VERDE, label="FOH no causal")
    ax.plot(u, pred, color=pe.NARANJA, lw=0.9, label="FOH causal")
    ax.set_xticks([-3, -2, -1, -0.5, 0, 0.5, 1, 2, 3],
                  [r"$-3\omega_s$", r"$-2\omega_s$", r"$-\omega_s$", "", "0", r"$\frac{\omega_s}{2}$",
                   r"$\omega_s$", r"$2\omega_s$", r"$3\omega_s$"])
    ax.set_yticks([0, 0.5, 1], ["0", r"$\frac{T_s}{2}$", "$T_s$"])
    ax.set_xlabel(r"$\omega$")
    ax.set_title(r"$|H(j\omega)|$ de los retenedores")
    ax.set_ylim(0, 1.6)
    ax.legend(loc="upper right", fontsize=6, ncol=2)
    del x
    guardar(fig, "retenedores_frecuencia")


@figura
def zoh_espectro():
    wm, ws = 1.0, 4.0
    w = np.linspace(-10, 10, 4000)
    rep = sum(espectro_triangular(w - k * ws, wm) for k in range(-4, 5))
    H = np.abs(np.sinc(w / ws))
    fig, ax = pe.figura(ancho=4.6, alto=1.7)
    ax.plot(w, rep, color=pe.GRIS_CLARO, lw=0.8, label="$T_s|X_s(j\\omega)|$")
    ax.plot(w, H, color=pe.NARANJA, lw=0.9, ls="--", label="$|H_0(j\\omega)|/T_s$")
    ax.plot(w, rep * H, label="salida del ZOH")
    ax.set_xticks([-2 * ws, -ws, 0, ws, 2 * ws], [r"$-2\omega_s$", r"$-\omega_s$", "0", r"$\omega_s$",
                                                  r"$2\omega_s$"])
    ax.set_xlabel(r"$\omega$")
    ax.set_yticks([0, 1])
    ax.legend(loc="upper right", fontsize=6)
    ax.set_ylim(0, 1.5)
    guardar(fig, "zoh_espectro")


# ---------------------------------------------------------------------
# Parte 3 · Cuantificación
# ---------------------------------------------------------------------

@figura
def cuantificador():
    D = 0.25
    x = np.linspace(-1.1, 1.1, 3000)
    r = np.clip(D * np.round(x / D), -1, 1 - D)
    tr = np.clip(D * np.floor(x / D), -1, 1 - D)
    fig, axs = pe.figura(1, 2, ancho=5.4, alto=2.0)
    axs[0].plot(x, x, color=pe.GRIS_CLARO, lw=0.8)
    axs[0].plot(x, r, label="redondeo")
    axs[0].plot(x, tr, color=pe.ROJO, lw=0.9, label="truncamiento")
    axs[0].set_xlabel("$x$")
    axs[0].set_ylabel("$Q[x]$")
    axs[0].set_title(r"Característica, $b=3$ bits")
    axs[0].legend(loc="upper left", fontsize=6)
    m = np.abs(x) <= 0.95
    axs[1].plot(x[m], (r - x)[m], label="redondeo")
    axs[1].plot(x[m], (tr - x)[m], color=pe.ROJO, lw=0.9, label="truncamiento")
    axs[1].set_yticks([-D, -D / 2, 0, D / 2], [r"$-\Delta$", r"$-\frac{\Delta}{2}$", "0", r"$\frac{\Delta}{2}$"])
    axs[1].set_xlabel("$x$")
    axs[1].set_title(r"Error $e=Q[x]-x$")
    guardar(fig, "cuantificador")


@figura
def error_cuantificacion():
    b = 3
    D = 2 / 2 ** b
    n = np.arange(0, 64)
    x = 0.95 * np.sin(2 * np.pi * n / 40 + 0.4)
    xq = np.clip(D * np.round(x / D), -1, 1 - D)
    fig, axs = pe.figura(2, 1, ancho=4.6, alto=2.4, sharex=True)
    axs[0].plot(n, x, color=pe.GRIS_CLARO, lw=0.9)
    pe.stem(axs[0], n, xq, ms=2.4)
    axs[0].set_title(r"$x[n]$ cuantificada con $b=3$ bits ($\Delta=0{,}25$)", loc="left")
    pe.stem(axs[1], n, xq - x, color=pe.ROJO, ms=2.4)
    axs[1].axhline(D / 2, color=pe.GRIS, ls="--", lw=0.6)
    axs[1].axhline(-D / 2, color=pe.GRIS, ls="--", lw=0.6)
    axs[1].set_yticks([-D / 2, 0, D / 2], [r"$-\frac{\Delta}{2}$", "0", r"$\frac{\Delta}{2}$"])
    axs[1].set_title("Error de cuantificación $e[n]$", loc="left")
    axs[1].set_xlabel("$n$")
    guardar(fig, "error_cuantificacion")


@figura
def sqnr_bits():
    bits = np.arange(2, 17)
    n = np.arange(200_000)
    x = 0.999 * np.sin(2 * np.pi * 0.0123457 * n)
    medido = []
    for b in bits:
        D = 2 / 2 ** b
        e = np.clip(D * np.round(x / D), -1, 1 - D) - x
        medido.append(10 * np.log10(np.var(x) / np.var(e)))
    fig, ax = pe.figura(ancho=3.4, alto=1.9)
    ax.plot(bits, 6.02 * bits + 1.76, color=pe.GRIS, lw=0.9, ls="--", label=r"$6{,}02\,b+1{,}76$ dB")
    ax.plot(bits, medido, "o", ms=3, label="simulación")
    ax.set_xlabel("bits $b$")
    ax.set_ylabel("SQNR (dB)")
    ax.legend(loc="upper left", fontsize=6)
    guardar(fig, "sqnr_bits")


# ---------------------------------------------------------------------
# Parte 4 · Muestreo de señales discretas
# ---------------------------------------------------------------------

def _espectro_discreto(ax, Om, X, color=pe.AZUL, titulo=None):
    ax.plot(Om, X, color=color)
    ticks_pi(ax, 3)
    ax.set_xlim(-3 * np.pi, 3 * np.pi)
    ax.set_ylim(-0.05, 1.25)
    if titulo:
        ax.set_title(titulo, loc="left")


def _periodico(Om, Wm, escala=1.0, factor=1.0):
    """Triángulo de ancho Wm repetido cada 2π, evaluado en Om·factor."""
    u = (Om * factor + np.pi) % (2 * np.pi) - np.pi
    return escala * espectro_triangular(u, Wm)


@figura
def diezmado_espectro():
    Om = np.linspace(-3 * np.pi, 3 * np.pi, 6000)
    fig, axs = pe.figura(3, 1, ancho=4.6, alto=3.3, sharex=True)
    X = _periodico(Om, np.pi / 3)
    _espectro_discreto(axs[0], Om, X, titulo=r"$|X(e^{j\Omega})|$, banda $\Omega_m=\pi/3$")
    Y = 0.5 * (_periodico(Om / 2, np.pi / 3) + _periodico((Om - 2 * np.pi) / 2, np.pi / 3))
    _espectro_discreto(axs[1], Om, Y, color=pe.VERDE,
                       titulo=r"Diezmado por $M=2$: $\Omega_m M=2\pi/3<\pi$, sin aliasing")
    Xa = _periodico(Om, 2 * np.pi / 3)
    Ya = 0.5 * (_periodico(Om / 2, 2 * np.pi / 3) + _periodico((Om - 2 * np.pi) / 2, 2 * np.pi / 3))
    axs[2].plot(Om, 0.5 * _periodico(Om / 2, 2 * np.pi / 3), color=pe.GRIS_CLARO, lw=0.7)
    axs[2].plot(Om, 0.5 * _periodico((Om - 2 * np.pi) / 2, 2 * np.pi / 3), color=pe.GRIS_CLARO, lw=0.7)
    _espectro_discreto(axs[2], Om, Ya, color=pe.ROJO,
                       titulo=r"Si $\Omega_m=2\pi/3$, $\Omega_m M>\pi$: aliasing")
    del Xa
    axs[2].set_xlabel(r"$\Omega$")
    guardar(fig, "diezmado_espectro")


@figura
def expansion_espectro():
    Om = np.linspace(-3 * np.pi, 3 * np.pi, 6000)
    fig, axs = pe.figura(2, 1, ancho=4.6, alto=2.3, sharex=True)
    _espectro_discreto(axs[0], Om, _periodico(Om, 2 * np.pi / 3), titulo=r"$|X(e^{j\Omega})|$")
    _espectro_discreto(axs[1], Om, _periodico(Om, 2 * np.pi / 3, factor=2), color=pe.VERDE,
                       titulo=r"Expansión por $L=2$: $X(e^{j\Omega L})$, aparecen imágenes")
    axs[1].axvspan(-np.pi / 2, np.pi / 2, color=pe.NARANJA, alpha=0.1, lw=0)
    axs[1].annotate("filtro de interpolación", (0, 1.1), ha="center", fontsize=6, color=pe.NARANJA)
    axs[1].set_xlabel(r"$\Omega$")
    guardar(fig, "expansion_espectro")


@figura
def diezmado_tiempo():
    n = np.arange(0, 24)
    x = np.cos(2 * np.pi * n / 16) * np.exp(-n / 30) + 0.2
    fig, axs = pe.figura(1, 3, ancho=6.4, alto=1.55)
    pe.stem(axs[0], n, x, ms=2.4)
    axs[0].set_title("$x[n]$")
    pe.stem(axs[1], np.arange(0, 12), x[::2], color=pe.VERDE, ms=2.4)
    axs[1].set_title("Diezmado: $x[2n]$")
    up = np.zeros(48)
    up[::2] = x
    pe.stem(axs[2], np.arange(0, 48), up, color=pe.NARANJA, ms=2.0)
    axs[2].set_title("Expansión por $L=2$")
    for ax in axs:
        ax.set_xlabel("$n$")
    guardar(fig, "diezmado_tiempo")


if __name__ == "__main__":
    pedidas = sys.argv[1:] or list(FIGURAS)
    for nombre in pedidas:
        FIGURAS[nombre]()
        print("✓", nombre)
