"""Genera todas las figuras del Tema 1 (señales y sistemas).

    python generar_figuras.py            # todas
    python generar_figuras.py par impar  # solo las indicadas

Las figuras se guardan en PDF junto a este script. Las fotografías
(imagen_bn.png, imagen_color.jpg) no se generan: son originales.
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


# ---------------------------------------------------------------------
# Deck 1 · Tipos de señales
# ---------------------------------------------------------------------

@figura
def tipos_escalar_1d():
    t = np.linspace(0, 1, 2000)
    rng = np.random.default_rng(3)
    x = (np.sin(2 * np.pi * 6 * t) * np.exp(-3 * t) + 0.5 * np.sin(2 * np.pi * 17 * t + 1)
         * np.exp(-((t - 0.6) / 0.15) ** 2) + 0.05 * rng.standard_normal(t.size))
    fig, ax = pe.figura(ancho=2.4, alto=1.5)
    ax.plot(t, x, lw=0.9)
    ax.set_xlabel("$t$ (s)")
    ax.set_ylabel("$x(t)$")
    guardar(fig, "tipos_escalar_1d")


@figura
def tipos_vectorial_1d():
    t = np.linspace(0, 2, 800)
    fig, ax = pe.figura(ancho=2.4, alto=1.5)
    ax.plot(t, np.sin(2 * np.pi * 1.2 * t), lw=1, label="$x_1(t)$")
    ax.plot(t, 0.6 * np.cos(2 * np.pi * 0.7 * t) + 0.3, lw=1, label="$x_2(t)$")
    ax.plot(t, 0.4 * np.sign(np.sin(2 * np.pi * 0.5 * t)) - 0.4, lw=1, label="$x_3(t)$")
    ax.set_xlabel("$t$ (s)")
    ax.legend(loc="upper right", ncol=3, fontsize=6, handlelength=1.2)
    ax.set_ylim(-1.3, 1.6)
    guardar(fig, "tipos_vectorial_1d")


@figura
def analogica_digital():
    t = np.linspace(0, 1, 1000)
    f = lambda t: np.sin(2 * np.pi * 1.5 * t) + 0.4 * np.sin(2 * np.pi * 4 * t)
    Ts = 1 / 20
    n = np.arange(0, 21)
    q = 0.25
    fig, axs = pe.figura(2, 2, ancho=4.6, alto=2.8, sharex=True, sharey=True)
    axs[0, 0].plot(t, f(t))
    axs[0, 0].set_title("Analógica: $t$ continuo, amplitud continua")
    axs[0, 1].plot(t, q * np.round(f(t) / q), drawstyle="steps-post")
    axs[0, 1].set_title("Cuantificada: $t$ continuo, amplitud discreta")
    pe.stem(axs[1, 0], n * Ts, f(n * Ts))
    axs[1, 0].set_title("Muestreada: $n$ discreto, amplitud continua")
    pe.stem(axs[1, 1], n * Ts, q * np.round(f(n * Ts) / q), color=pe.ROJO)
    axs[1, 1].set_title("Digital: $n$ discreto, amplitud discreta")
    for ax in axs[1]:
        ax.set_xlabel("tiempo")
    for ax in axs[:, 1]:
        ax.set_yticks(np.arange(-1.25, 1.5, 0.25), minor=True)
        ax.grid(True, which="minor", color="#EEEFF5", lw=0.4)
    guardar(fig, "analogica_digital")


@figura
def determinista_aleatoria():
    n = np.arange(0, 31)
    rng = np.random.default_rng(1)
    fig, axs = pe.figura(1, 2, ancho=4.6, alto=1.6, sharey=True)
    pe.stem(axs[0], n, np.sin(0.4 * n))
    axs[0].set_title(r"Determinista: $x[n]=\sin(0{,}4\,n)$")
    pe.stem(axs[1], n, rng.standard_normal(n.size), color=pe.ROJO)
    axs[1].set_title(r"Aleatoria: $x[n]\sim\mathcal{N}(0,1)$")
    for ax in axs:
        ax.set_xlabel("$n$")
    guardar(fig, "determinista_aleatoria")


@figura
def periodicas():
    t = np.linspace(-6, 6, 1200)
    T = 4
    xt = signal.sawtooth(2 * np.pi * t / T, width=0.3) * 0.5 + 0.5 * np.cos(2 * np.pi * t / (T / 2))
    n = np.arange(-12, 13)
    N = 6
    base = np.array([0, 1, 2, 1.5, 0.5, -0.5])
    xn = base[n % N]
    fig, axs = pe.figura(1, 2, ancho=4.6, alto=1.6)
    axs[0].plot(t, xt)
    axs[0].annotate("", xy=(2, 1.25), xytext=(-2, 1.25),
                    arrowprops=dict(arrowstyle="<->", color=pe.GRIS, lw=0.8))
    axs[0].text(0, 1.33, "$T$", ha="center", color=pe.GRIS)
    axs[0].set_ylim(-1.3, 1.55)
    axs[0].set_title("Continua, periodo $T=4$")
    axs[0].set_xlabel("$t$")
    pe.stem(axs[1], n, xn)
    axs[1].annotate("", xy=(6, 2.35), xytext=(0, 2.35),
                    arrowprops=dict(arrowstyle="<->", color=pe.GRIS, lw=0.8))
    axs[1].text(3, 2.45, "$N$", ha="center", color=pe.GRIS)
    axs[1].set_ylim(-1, 2.8)
    axs[1].set_title("Discreta, periodo $N=6$")
    axs[1].set_xlabel("$n$")
    guardar(fig, "periodicas")


@figura
def par_impar():
    t = np.linspace(-4, 4, 800)
    fig, axs = pe.figura(1, 2, ancho=4.6, alto=1.5, sharey=True)
    axs[0].plot(t, np.exp(-t ** 2 / 2) * np.cos(2 * t))
    axs[0].set_title("Par: $x(t)=x(-t)$")
    axs[1].plot(t, np.exp(-t ** 2 / 2) * np.sin(2 * t), color=pe.ROJO)
    axs[1].set_title("Impar: $x(t)=-x(-t)$")
    for ax in axs:
        ax.axvline(0, color=pe.GRIS, lw=0.6)
        ax.set_xlabel("$t$")
    guardar(fig, "par_impar")


@figura
def descomposicion_par_impar():
    n = np.arange(-6, 7)
    x = np.where(n >= 0, 0.8 ** n, 0.0) * 2
    xp = (x + x[::-1]) / 2
    xi = (x - x[::-1]) / 2
    fig, axs = pe.figura(1, 3, ancho=4.8, alto=1.4, sharey=True)
    for ax, s, tit, c in zip(axs, (x, xp, xi),
                             ("$x[n]=2\\,(0{,}8)^n u[n]$", "$x_p[n]$ (par)", "$x_i[n]$ (impar)"),
                             (pe.AZUL, pe.VERDE, pe.ROJO)):
        pe.stem(ax, n, s, color=c)
        ax.set_title(tit)
        ax.set_xlabel("$n$")
    guardar(fig, "descomposicion_par_impar")


@figura
def causalidad():
    t = np.linspace(-4, 4, 800)
    fig, axs = pe.figura(1, 3, ancho=4.8, alto=1.35, sharey=True)
    axs[0].plot(t, np.where(t >= 0, t * np.exp(-t) * 2.5, 0))
    axs[0].set_title("Causal")
    axs[1].plot(t, np.exp(-(t - 0.5) ** 2), color=pe.VERDE)
    axs[1].set_title("No causal")
    axs[2].plot(t, np.where(t <= 0, -t * np.exp(t) * 2.5, 0), color=pe.ROJO)
    axs[2].set_title("Anticausal")
    for ax in axs:
        ax.axvline(0, color=pe.GRIS, lw=0.6)
        ax.set_xlabel("$t$")
    guardar(fig, "causalidad")


@figura
def energia_potencia():
    t = np.linspace(-6, 6, 1000)
    fig, axs = pe.figura(1, 3, ancho=4.8, alto=1.45)
    axs[0].plot(t, np.exp(-np.abs(t)))
    axs[0].set_title("Energía finita ($P=0$)")
    axs[1].plot(t, np.cos(2 * t), color=pe.VERDE)
    axs[1].set_title(r"Potencia finita ($E=\infty$)")
    axs[2].plot(t, np.where(t >= 0, t, 0), color=pe.ROJO)
    axs[2].set_title(r"Ninguna ($E=P=\infty$)")
    for ax, txt in zip(axs, (r"$e^{-|t|}$", r"$\cos(2t)$", r"$r(t)=t\,u(t)$")):
        ax.set_xlabel("$t$")
        ax.text(0.03, 0.95, txt, transform=ax.transAxes, va="top", fontsize=7, color=pe.GRIS)
    guardar(fig, "energia_potencia")


@figura
def compleja():
    n = np.arange(0, 31)
    x = 0.95 ** n * np.exp(1j * 0.6 * n)
    fig, axs = pe.figura(2, 2, ancho=4.6, alto=2.4, sharex=True)
    pe.stem(axs[0, 0], n, x.real)
    axs[0, 0].set_ylabel(r"$\mathrm{Re}\{x[n]\}$")
    pe.stem(axs[1, 0], n, x.imag)
    axs[1, 0].set_ylabel(r"$\mathrm{Im}\{x[n]\}$")
    pe.stem(axs[0, 1], n, np.abs(x), color=pe.ROJO)
    axs[0, 1].set_ylabel(r"$|x[n]|$")
    pe.stem(axs[1, 1], n, np.angle(x), color=pe.ROJO)
    axs[1, 1].set_ylabel(r"$\arg\, x[n]$ (rad)")
    axs[1, 1].set_yticks([-np.pi, 0, np.pi], [r"$-\pi$", "0", r"$\pi$"])
    for ax in axs[1]:
        ax.set_xlabel("$n$")
    fig.suptitle(r"$x[n]=(0{,}95)^n\,e^{j0{,}6n}$", fontsize=8)
    guardar(fig, "compleja")


# ---------------------------------------------------------------------
# Deck 1 · Señales básicas
# ---------------------------------------------------------------------

@figura
def impulso_dirac():
    fig, ax = pe.figura(ancho=2.4, alto=1.6)
    t = np.linspace(-1.5, 1.5, 1500)
    for k, eps in enumerate((1.0, 0.5, 0.25)):
        ax.plot(t, np.where(np.abs(t) <= eps / 2, 1 / eps, 0), color=pe.GRIS_CLARO if k < 2 else pe.GRIS, lw=0.9)
    ax.annotate("", xy=(0, 5.2), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=pe.AZUL, lw=1.6))
    ax.text(0.12, 4.9, r"$\delta(t)$", color=pe.AZUL)
    ax.text(0.6, 1.6, r"$\frac{1}{\varepsilon}\Pi(t/\varepsilon)$", color=pe.GRIS, fontsize=7)
    ax.set_ylim(0, 5.6)
    ax.set_title(r"Pulsos de área 1, $\varepsilon=1,\ \frac{1}{2},\ \frac{1}{4}$")
    ax.set_xlabel("$t$")
    guardar(fig, "impulso_dirac")


@figura
def impulso_kronecker():
    fig, ax = pe.figura(ancho=2.4, alto=1.6)
    n = np.arange(-5, 6)
    pe.stem(ax, n, (n == 0).astype(float))
    ax.set_title(r"$\delta[n]$")
    ax.set_xlabel("$n$")
    ax.set_ylim(-0.1, 1.25)
    guardar(fig, "impulso_kronecker")


@figura
def escalon_rampa():
    t = np.linspace(-3, 4, 700)
    n = np.arange(-3, 5)
    fig, axs = pe.figura(2, 2, ancho=4.6, alto=2.5)
    axs[0, 0].plot(t, (t >= 0).astype(float))
    axs[0, 0].set_title("$u(t)$")
    pe.stem(axs[0, 1], n, (n >= 0).astype(float))
    axs[0, 1].set_title("$u[n]$")
    axs[1, 0].plot(t, np.where(t >= 0, t, 0), color=pe.ROJO)
    axs[1, 0].set_title(r"$r(t)=t\,u(t)$")
    pe.stem(axs[1, 1], n, np.where(n >= 0, n, 0), color=pe.ROJO)
    axs[1, 1].set_title(r"$r[n]=n\,u[n]$")
    axs[1, 0].set_xlabel("$t$")
    axs[1, 1].set_xlabel("$n$")
    guardar(fig, "escalon_rampa")


@figura
def pulsos():
    t = np.linspace(-2, 2, 801)
    fig, axs = pe.figura(1, 2, ancho=4.6, alto=1.45, sharey=True)
    axs[0].plot(t, (np.abs(t) <= 0.5).astype(float))
    axs[0].set_title(r"$\Pi(t)$")
    axs[1].plot(t, np.clip(1 - np.abs(t), 0, None), color=pe.ROJO)
    axs[1].set_title(r"$\Lambda(t)$")
    for ax in axs:
        ax.set_xlabel("$t$")
        ax.set_xticks([-1, -0.5, 0, 0.5, 1])
    axs[0].set_ylim(-0.1, 1.25)
    guardar(fig, "pulsos")


@figura
def exp_compleja_continua():
    t = np.linspace(0, 4, 800)
    W = 2 * np.pi
    fig, ax = pe.figura(ancho=3.6, alto=1.5)
    ax.plot(t, np.cos(W * t), label=r"$\mathrm{Re}\{e^{j\omega t}\}=\cos(\omega t)$")
    ax.plot(t, np.sin(W * t), color=pe.ROJO, label=r"$\mathrm{Im}\{e^{j\omega t}\}=\sin(\omega t)$")
    ax.set_xlabel("$t$ (s)")
    ax.set_ylim(-1.2, 1.9)
    ax.legend(loc="upper center", ncol=2, fontsize=6.5)
    ax.set_title(r"$\omega=2\pi$ rad/s, $T=1$ s")
    guardar(fig, "exp_compleja_continua")


@figura
def exp_general_continua():
    t = np.linspace(0, 6, 1200)
    fig, axs = pe.figura(1, 3, ancho=4.8, alto=1.4)
    for ax, r, tit in zip(axs, (-0.4, 0.0, 0.3), ("$r<0$", "$r=0$", "$r>0$")):
        env = np.exp(r * t)
        ax.plot(t, env * np.cos(2 * np.pi * t))
        ax.plot(t, env, color=pe.GRIS_CLARO, lw=0.8, ls="--")
        ax.plot(t, -env, color=pe.GRIS_CLARO, lw=0.8, ls="--")
        ax.set_title(tit)
        ax.set_xlabel("$t$")
    fig.suptitle(r"$\mathrm{Re}\{C e^{at}\}=|C|e^{rt}\cos(\omega t+\phi)$", fontsize=8)
    guardar(fig, "exp_general_continua")


@figura
def exp_general_discreta():
    n = np.arange(0, 25)
    fig, axs = pe.figura(1, 3, ancho=4.8, alto=1.4)
    for ax, a, tit in zip(axs, (0.85, 1.0, 1.08), ("$|\\alpha|<1$", "$|\\alpha|=1$", "$|\\alpha|>1$")):
        env = a ** n
        pe.stem(ax, n, env * np.cos(0.5 * n))
        ax.plot(n, env, color=pe.GRIS_CLARO, lw=0.8, ls="--")
        ax.plot(n, -env, color=pe.GRIS_CLARO, lw=0.8, ls="--")
        ax.set_title(tit)
        ax.set_xlabel("$n$")
    fig.suptitle(r"$\mathrm{Re}\{C\alpha^n\}=|C||\alpha|^n\cos(\Omega n+\phi)$, $\Omega=0{,}5$", fontsize=8)
    guardar(fig, "exp_general_discreta")


@figura
def coseno_discreto_frecuencias():
    n = np.arange(0, 17)
    tt = np.linspace(0, 16, 1000)
    casos = ((0, "0"), (np.pi / 4, r"\pi/4"), (np.pi, r"\pi"), (7 * np.pi / 4, r"7\pi/4"))
    fig, axs = pe.figura(1, 4, ancho=4.9, alto=1.35, sharey=True)
    for ax, (w, txt) in zip(axs, casos):
        ax.plot(tt, np.cos(w * tt), color=pe.GRIS_CLARO, lw=0.7)
        pe.stem(ax, n, np.cos(w * n), ms=2.4)
        ax.set_title(rf"$\Omega={txt}$")
        ax.set_xlabel("$n$")
    axs[0].set_ylim(-1.25, 1.25)
    guardar(fig, "coseno_discreto_frecuencias")


@figura
def sa_sinc_signo():
    t = np.linspace(-10, 10, 2001)
    fig, axs = pe.figura(1, 2, ancho=4.6, alto=1.5)
    axs[0].plot(t, np.sinc(t / np.pi), label=r"$\mathrm{Sa}(t)=\sin t/t$")
    axs[0].plot(t, np.sinc(t), color=pe.ROJO, label=r"$\mathrm{sinc}(t)=\sin(\pi t)/(\pi t)$")
    axs[0].legend(loc="upper center", fontsize=6)
    axs[0].set_ylim(-0.35, 1.75)
    axs[0].set_xlabel("$t$")
    t2 = np.linspace(-3, 3, 601)
    axs[1].plot(t2[t2 < 0], -np.ones((t2 < 0).sum()), color=pe.AZUL)
    axs[1].plot(t2[t2 > 0], np.ones((t2 > 0).sum()), color=pe.AZUL)
    axs[1].plot([0], [0], "o", color=pe.AZUL, ms=3)
    axs[1].set_title(r"$\mathrm{sgn}(t)$")
    axs[1].set_xlabel("$t$")
    axs[1].set_ylim(-1.4, 1.4)
    guardar(fig, "sa_sinc_signo")


@figura
def ondas():
    t = np.linspace(-10, 10, 4001)
    T = 5
    fig, axs = pe.figura(1, 3, ancho=4.9, alto=1.4)
    axs[0].plot(t, signal.square(2 * np.pi * t / T))
    axs[0].set_title("Cuadrada ($T=5$)")
    axs[1].plot(t, signal.sawtooth(2 * np.pi * t / T, width=0.5), color=pe.ROJO)
    axs[1].set_title("Triangular ($T=5$)")
    tc = np.linspace(0, 10, 4000)
    axs[2].plot(tc, signal.chirp(tc, f0=0.2, t1=10, f1=1.0), color=pe.VERDE, lw=1)
    axs[2].set_title("Chirp lineal, 0,2 → 1 Hz")
    for ax in axs:
        ax.set_xlabel("$t$ (s)")
        ax.set_ylim(-1.3, 1.3)
    guardar(fig, "ondas")


# ---------------------------------------------------------------------
# Deck 2 · Operaciones
# ---------------------------------------------------------------------

def _x_ejemplo(t):
    """Señal asimétrica para ilustrar transformaciones de la variable."""
    return np.where((t >= 0) & (t < 1), 1.0, 0) + np.where((t >= 1) & (t <= 2), 2 - t, 0)


@figura
def desplazamiento_inversion():
    t = np.linspace(-4, 5, 1801)
    fig, axs = pe.figura(1, 2, ancho=4.6, alto=1.5, sharey=True)
    axs[0].plot(t, _x_ejemplo(t), label="$x(t)$")
    axs[0].plot(t, _x_ejemplo(t - 2), color=pe.ROJO, label="$x(t-2)$")
    axs[0].annotate("", xy=(2.5, 1.15), xytext=(0.5, 1.15),
                    arrowprops=dict(arrowstyle="->", color=pe.GRIS, lw=0.8))
    axs[0].set_title("Desplazamiento ($t_0=2$: retardo)")
    axs[1].plot(t, _x_ejemplo(t), label="$x(t)$")
    axs[1].plot(t, _x_ejemplo(-t), color=pe.ROJO, label="$x(-t)$")
    axs[1].set_title("Inversión")
    for ax in axs:
        ax.legend(loc="upper left", fontsize=6.5)
        ax.set_xlabel("$t$")
        ax.set_ylim(-0.1, 1.6)
    guardar(fig, "desplazamiento_inversion")


@figura
def escalado_continuo():
    t = np.linspace(-1, 5, 1201)
    fig, ax = pe.figura(ancho=2.6, alto=1.5)
    ax.plot(t, _x_ejemplo(t), label="$x(t)$")
    ax.plot(t, _x_ejemplo(2 * t), color=pe.ROJO, label="$x(2t)$")
    ax.plot(t, _x_ejemplo(t / 2), color=pe.VERDE, label="$x(t/2)$")
    ax.legend(loc="upper right", fontsize=6.5)
    ax.set_xlabel("$t$")
    ax.set_ylim(-0.1, 1.6)
    guardar(fig, "escalado_continuo")


@figura
def diezmado_interpolacion():
    n = np.arange(0, 13)
    x = np.cos(0.35 * n) + 1.2
    fig, axs = pe.figura(1, 3, ancho=4.8, alto=1.45, sharey=True)
    pe.stem(axs[0], n, x)
    axs[0].set_title("$x[n]$")
    nd = np.arange(0, 7)
    pe.stem(axs[1], nd, x[2 * nd], color=pe.ROJO)
    axs[1].set_title("Diezmado: $x[2n]$")
    ni = np.arange(0, 13)
    xi = np.where(ni % 2 == 0, x[(ni // 2) % 13], 0)
    pe.stem(axs[2], ni, xi, color=pe.VERDE)
    axs[2].set_title("Expansión: $x[n/2]$ (0 si $n$ impar)")
    for ax in axs:
        ax.set_xlabel("$n$")
        ax.set_xlim(-0.8, 12.8)
    guardar(fig, "diezmado_interpolacion")


@figura
def transformacion_combinada():
    t = np.linspace(-3, 3, 1201)
    fig, axs = pe.figura(1, 3, ancho=4.8, alto=1.45, sharey=True)
    axs[0].plot(t, _x_ejemplo(t))
    axs[0].set_title("$x(t)$")
    axs[1].plot(t, _x_ejemplo(t + 1), color=pe.VERDE)
    axs[1].set_title("1) desplazar: $v(t)=x(t+1)$")
    axs[2].plot(t, _x_ejemplo(2 * t + 1), color=pe.ROJO)
    axs[2].set_title("2) escalar: $v(2t)=x(2t+1)$")
    for ax in axs:
        ax.set_xlabel("$t$")
        ax.set_xticks([-2, -1, 0, 1, 2])
        ax.set_ylim(-0.1, 1.3)
    guardar(fig, "transformacion_combinada")


@figura
def convolucion_pasos():
    """x(τ)=Π(τ-1/2) (pulso en [0,1]) y h(t)=e^{-t}u(t)."""
    tau = np.linspace(-2.5, 4, 2601)
    x = ((tau >= 0) & (tau <= 1)).astype(float)
    h = lambda t: np.where(t >= 0, np.exp(-t), 0)
    ts = (-0.5, 0.5, 2.0)
    fig, axs = pe.figura(1, 4, ancho=5.2, alto=1.45, sharey=True)
    for ax, t in zip(axs[:3], ts):
        ax.plot(tau, x, label=r"$x(\tau)$")
        ax.plot(tau, h(t - tau), color=pe.ROJO, label=r"$h(t-\tau)$")
        ax.fill_between(tau, 0, x * h(t - tau), color=pe.VERDE, alpha=0.35, lw=0)
        ax.axvline(t, color=pe.GRIS, lw=0.6, ls=":")
        ax.set_title(f"$t={t:g}$".replace(".", "{,}"))
        ax.set_xlabel(r"$\tau$")
    axs[0].legend(loc="upper left", fontsize=6)
    tt = np.linspace(-1, 4, 1001)
    y = np.where(tt < 0, 0, np.where(tt <= 1, 1 - np.exp(-tt), (np.e - 1) * np.exp(-tt)))
    axs[3].plot(tt, y, color=pe.VERDE)
    for t in ts:
        yy = 0 if t < 0 else (1 - np.exp(-t) if t <= 1 else (np.e - 1) * np.exp(-t))
        axs[3].plot([t], [yy], "o", color=pe.VERDE, ms=3)
    axs[3].set_title(r"$y(t)=(x*h)(t)$")
    axs[3].set_xlabel("$t$")
    axs[0].set_ylim(-0.05, 1.45)
    guardar(fig, "convolucion_pasos")


@figura
def convolucion_discreta():
    x = np.array([1, 2, 1])
    h = np.array([1, 1, 1, 1])
    y = np.convolve(x, h)
    fig, axs = pe.figura(1, 3, ancho=4.8, alto=1.4, sharey=True)
    pe.stem(axs[0], np.arange(x.size), x)
    axs[0].set_title("$x[n]$")
    pe.stem(axs[1], np.arange(h.size), h, color=pe.ROJO)
    axs[1].set_title("$h[n]$")
    pe.stem(axs[2], np.arange(y.size), y, color=pe.VERDE)
    axs[2].set_title(r"$y[n]=(x*h)[n]$")
    for ax in axs:
        ax.set_xlabel("$n$")
        ax.set_xlim(-0.7, 6.7)
    guardar(fig, "convolucion_discreta")


@figura
def serie_fourier_cuadrada():
    t = np.linspace(-1, 1, 4001)
    x = signal.square(2 * np.pi * (t + 0.25))  # par, T=1, amplitud ±1
    fig, axs = pe.figura(1, 2, ancho=4.8, alto=1.6, gridspec_kw=dict(width_ratios=[1.5, 1]))
    axs[0].plot(t, x, color=pe.GRIS_CLARO, lw=1)
    for K, c in ((1, pe.ROJO), (3, pe.NARANJA), (19, pe.AZUL)):
        s = np.zeros_like(t)
        for k in range(1, K + 1, 2):
            s += 4 / (np.pi * k) * np.sin(np.pi * k / 2) * np.cos(2 * np.pi * k * t)
        axs[0].plot(t, s, color=c, lw=1, label=f"$K={K}$")
    axs[0].legend(loc="upper center", ncol=3, fontsize=6)
    axs[0].set_xlabel("$t$ (s)")
    axs[0].set_title("Sumas parciales (fenómeno de Gibbs)")
    axs[0].set_ylim(-1.4, 2.0)
    k = np.arange(-9, 10)
    ck = np.where(k == 0, 0, np.sinc(k / 2))  # c_k = sin(πk/2)/(πk/2)·(1/2)·2
    pe.stem(axs[1], k, ck)
    axs[1].set_title("Coeficientes $c_k$")
    axs[1].set_xlabel("$k$")
    guardar(fig, "serie_fourier_cuadrada")


@figura
def espectro_ctft_pulso():
    W = np.linspace(-6 * np.pi, 6 * np.pi, 2001)
    T = 1.0
    fig, ax = pe.figura(ancho=2.6, alto=1.6)
    ax.plot(W, T * np.sinc(W * T / (2 * np.pi)))
    ax.set_xticks([-4 * np.pi, -2 * np.pi, 0, 2 * np.pi, 4 * np.pi],
                  [r"$-\frac{4\pi}{T}$", r"$-\frac{2\pi}{T}$", "0", r"$\frac{2\pi}{T}$", r"$\frac{4\pi}{T}$"])
    ax.set_title(r"CTFT de $\Pi(t/T)$")
    ax.set_xlabel(r"$\omega$")
    pe.ejes_centrados(ax)
    guardar(fig, "espectro_ctft_pulso")


@figura
def espectro_dtft_pulso():
    w = np.linspace(-3 * np.pi, 3 * np.pi, 3001)
    L = 5
    with np.errstate(invalid="ignore", divide="ignore"):
        D = np.sin(w * L / 2) / np.sin(w / 2)
    D[np.isclose(np.sin(w / 2), 0)] = L
    fig, ax = pe.figura(ancho=2.6, alto=1.6)
    ax.plot(w, np.abs(D), color=pe.ROJO)
    ax.set_xticks([-2 * np.pi, -np.pi, 0, np.pi, 2 * np.pi],
                  [r"$-2\pi$", r"$-\pi$", "0", r"$\pi$", r"$2\pi$"])
    ax.set_title(r"$|X(e^{j\Omega})|$, pulso de $L=5$ muestras")
    ax.set_xlabel(r"$\Omega$")
    guardar(fig, "espectro_dtft_pulso")


# ---------------------------------------------------------------------
# Deck 3 · Sistemas
# ---------------------------------------------------------------------

def _rc(t, x, tau=0.5):
    """Respuesta de y' = (x - y)/tau con condiciones iniciales nulas."""
    sis = signal.lti([1], [tau, 1])
    _, y, _ = signal.lsim(sis, x, t)
    return y


@figura
def linealidad():
    t = np.linspace(0, 8, 1601)
    x1 = (t >= 1).astype(float)
    x2 = -2 * ((t >= 2).astype(float))
    y1, y2, y12 = _rc(t, x1), _rc(t, x2), _rc(t, x1 + x2)
    fig, axs = pe.figura(2, 3, ancho=4.9, alto=2.3, sharex=True)
    for j, (x, y, tx, ty) in enumerate(((x1, y1, "$x_1$", "$y_1$"), (x2, y2, "$x_2$", "$y_2$"),
                                        (x1 + x2, y12, "$x_1+x_2$", r"$\mathcal{T}\{x_1+x_2\}$"))):
        axs[0, j].plot(t, x)
        axs[0, j].set_title(tx)
        axs[1, j].plot(t, y, color=pe.ROJO)
        axs[1, j].set_title(ty)
        axs[1, j].set_xlabel("$t$")
    axs[1, 2].plot(t, y1 + y2, color=pe.VERDE, ls="--", lw=1.1, label="$y_1+y_2$")
    axs[1, 2].legend(loc="upper right", fontsize=6)
    guardar(fig, "linealidad")


@figura
def invarianza():
    t = np.linspace(0, 8, 1601)
    x1 = ((t >= 1) & (t < 2)).astype(float)
    x2 = ((t >= 4) & (t < 5)).astype(float)
    fig, axs = pe.figura(2, 2, ancho=4.6, alto=2.2, sharex=True, sharey=True)
    for j, (x, tx, ty) in enumerate(((x1, "$x(t)$", "$y(t)$"), (x2, "$x(t-3)$", "$y(t-3)$"))):
        axs[0, j].plot(t, x)
        axs[0, j].set_title(tx)
        axs[1, j].plot(t, _rc(t, x), color=pe.ROJO)
        axs[1, j].set_title(ty)
        axs[1, j].set_xlabel("$t$")
    guardar(fig, "invarianza")


@figura
def polos_estabilidad_s():
    t = np.linspace(0, 10, 1001)
    casos = (("Polo real $s=-0{,}5$", np.exp(-0.5 * t)),
             ("Par complejo, Re $<0$", np.exp(-0.3 * t) * np.cos(3 * t)),
             ("Par en el eje imaginario", np.cos(3 * t)),
             ("Polo real $s=+0{,}3$", np.exp(0.3 * t)))
    fig, axs = pe.figura(1, 4, ancho=5.2, alto=1.35)
    for ax, (tit, h) in zip(axs, casos):
        ax.plot(t, h, color=pe.AZUL if "<0" in tit or "-0" in tit else pe.ROJO)
        ax.set_title(tit, fontsize=7)
        ax.set_xlabel("$t$")
    axs[0].set_ylabel("$h(t)$")
    guardar(fig, "polos_estabilidad_s")


@figura
def polos_estabilidad_z():
    n = np.arange(0, 30)
    casos = (("Polo $z=0{,}8$", 0.8 ** n),
             (r"Par $0{,}9\,e^{\pm j\pi/4}$", 0.9 ** n * np.cos(np.pi / 4 * n)),
             (r"Par $e^{\pm j\pi/4}$ ($|z|=1$)", np.cos(np.pi / 4 * n)),
             ("Polo $z=-1{,}1$", (-1.1) ** n))
    fig, axs = pe.figura(1, 4, ancho=5.2, alto=1.35)
    for k, (ax, (tit, h)) in enumerate(zip(axs, casos)):
        pe.stem(ax, n, h, color=pe.AZUL if k < 2 else pe.ROJO, ms=2)
        ax.set_title(tit, fontsize=7)
        ax.set_xlabel("$n$")
    axs[0].set_ylabel("$h[n]$")
    guardar(fig, "polos_estabilidad_z")


@figura
def fir_iir():
    n = np.arange(0, 25)
    L = 5
    hf = np.where(n < L, 1 / L, 0)
    a = 0.8
    hi = (1 - a) * a ** n
    fig, axs = pe.figura(1, 2, ancho=4.8, alto=1.6)
    pe.stem(axs[0], n, hf, etiqueta="FIR: media móvil, $L=5$")
    mk, st = pe.stem(axs[0], n + 0.25, hi, color=pe.ROJO, etiqueta="IIR: $a=0{,}8$")
    axs[0].legend(loc="upper right", fontsize=6)
    axs[0].set_title("Respuesta al impulso $h[n]$")
    axs[0].set_xlabel("$n$")
    w, Hf = signal.freqz(np.ones(L) / L, 1, worN=1024)
    _, Hi = signal.freqz([1 - a], [1, -a], worN=1024)
    axs[1].plot(w, np.abs(Hf), label="FIR")
    axs[1].plot(w, np.abs(Hi), color=pe.ROJO, label="IIR")
    axs[1].set_xticks([0, np.pi / 2, np.pi], ["0", r"$\pi/2$", r"$\pi$"])
    axs[1].set_title(r"$|H(e^{j\Omega})|$")
    axs[1].set_xlabel(r"$\Omega$ (rad/muestra)")
    axs[1].legend(loc="upper right", fontsize=6)
    guardar(fig, "fir_iir")


@figura
def rc_respuestas():
    RC = 1e-3
    t = np.linspace(0, 6e-3, 600)
    sis = signal.lti([1], [RC, 1])
    _, s = signal.step(sis, T=t)
    W = np.logspace(1, 6, 400)
    _, H = signal.freqs([1], [RC, 1], worN=W)
    fig, axs = pe.figura(1, 2, ancho=4.8, alto=1.55)
    axs[0].plot(t * 1e3, s)
    axs[0].axvline(RC * 1e3, color=pe.GRIS, ls=":", lw=0.8)
    axs[0].text(RC * 1e3 + 0.1, 0.3, r"$\tau=RC$", fontsize=7, color=pe.GRIS)
    axs[0].set_title("Respuesta al escalón")
    axs[0].set_xlabel("$t$ (ms)")
    axs[1].semilogx(W, 20 * np.log10(np.abs(H)), color=pe.ROJO)
    axs[1].axvline(1 / RC, color=pe.GRIS, ls=":", lw=0.8)
    axs[1].set_title(r"$|H(j\omega)|$ (dB)")
    axs[1].set_xlabel(r"$\omega$ (rad/s)")
    guardar(fig, "rc_respuestas")


# ---------------------------------------------------------------------
# Deck 4 · Señales en aplicaciones reales
# ---------------------------------------------------------------------

@figura
def bandas_aplicaciones():
    bandas = [
        ("Ondas sísmicas superficiales", 0.01, 1, "Geofísica"),
        ("Ondas sísmicas P", 0.1, 10, "Geofísica"),
        ("EEG", 0.1, 100, "Biomedicina"),
        ("ECG (diagnóstico)", 0.05, 150, "Biomedicina"),
        ("EMG de superficie", 10, 500, "Biomedicina"),
        ("Sensores de fuerza / IMU", 1, 1e3, "Control y robótica"),
        ("Conmutación PWM", 1e3, 5e4, "Control y robótica"),
        ("Voz (telefonía)", 300, 3400, "Audio"),
        ("Audio de alta fidelidad", 20, 2e4, "Audio"),
        ("Ultrasonido médico", 1e6, 1.5e7, "Biomedicina"),
        ("Radio AM (onda media)", 5.3e5, 1.7e6, "Comunicaciones"),
        ("Radio FM", 8.75e7, 1.08e8, "Comunicaciones"),
        ("GPS (L1, L2, L5)", 1.17e9, 1.58e9, "Comunicaciones"),
        ("Wi-Fi (2,4 / 5 / 6 GHz)", 2.4e9, 7.1e9, "Comunicaciones"),
        ("Fibra óptica (1550 nm)", 1.9e14, 2.0e14, "Comunicaciones"),
    ]
    colores = {"Geofísica": pe.GRIS, "Biomedicina": pe.ROJO, "Control y robótica": pe.NARANJA,
               "Audio": pe.VERDE, "Comunicaciones": pe.AZUL}
    fig, ax = pe.figura(ancho=4.6, alto=2.6)
    for i, (nom, f1, f2, cat) in enumerate(bandas):
        ax.barh(i, np.log10(f2) - np.log10(f1) if f2 / f1 > 1.15 else 0.12, left=np.log10(f1),
                height=0.62, color=colores[cat])
        ax.text(np.log10(f2) + 0.15 if np.log10(f2) < 11 else np.log10(f1) - 0.15, i, nom,
                va="center", ha="left" if np.log10(f2) < 11 else "right", fontsize=6.5)
    ax.set_yticks([])
    ax.invert_yaxis()
    xt = np.arange(-2, 16, 1)
    etiquetas = {-2: "10 mHz", 0: "1 Hz", 3: "1 kHz", 6: "1 MHz", 9: "1 GHz", 12: "1 THz", 15: ""}
    ax.set_xticks(xt, [etiquetas.get(int(k), "") for k in xt])
    ax.set_xlim(-2.2, 15)
    ax.grid(axis="y", visible=False)
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("frecuencia (escala logarítmica)")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=c, label=k) for k, c in colores.items()], loc="upper right",
              fontsize=6, ncol=1)
    guardar(fig, "bandas_aplicaciones")


if __name__ == "__main__":
    pedidas = sys.argv[1:] or list(FIGURAS)
    for nombre in pedidas:
        FIGURAS[nombre]()
        print("✓", nombre)
