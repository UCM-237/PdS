"""Genera todas las figuras del Tema 6 (señales aleatorias).

    python generar_figuras.py               # todas
    python generar_figuras.py realizaciones # solo las indicadas

Las figuras se guardan en PDF junto a este script.
"""

from __future__ import annotations

import pathlib
import sys

import numpy as np
from scipy import signal, stats

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


def ticks_pi(ax, simetrico=False):
    if simetrico:
        ax.set_xticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi],
                      [r"$-\pi$", r"$-\pi/2$", "0", r"$\pi/2$", r"$\pi$"])
    else:
        ax.set_xticks([0, np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi],
                      ["0", r"$\pi/4$", r"$\pi/2$", r"$3\pi/4$", r"$\pi$"])


def histo(ax, x, bins, color=pe.AZUL, **kw):
    ax.hist(x, bins=bins, density=True, color=color, alpha=0.45, edgecolor="none", **kw)


def autocorr(x, L, sesgado=False):
    """phi[l] = media de x[n+l] x[n], l = -L..L."""
    N = len(x)
    c = np.correlate(x, x, "full")[N - 1 - L:N + L]
    l = np.arange(-L, L + 1)
    return l, c / (N if sesgado else (N - np.abs(l)))


# ---------------------------------------------------------------------
# Parte 1 · Una variable aleatoria
# ---------------------------------------------------------------------

@figura
def deterministas_aleatorias():
    rng = np.random.default_rng(1)
    t = np.linspace(0, 1, 500)
    fig, axs = pe.figura(1, 2, ancho=6.4, alto=1.7, sharey=True)
    axs[0].plot(t, np.sin(2 * np.pi * 3 * t), color=pe.AZUL)
    axs[0].set_title(r"Determinista: $x(t)=\sin(2\pi\,3t)$, siempre igual")
    for c in (pe.AZUL, pe.ROJO, pe.VERDE):
        x = np.sin(2 * np.pi * 3 * t + rng.uniform(0, 2 * np.pi)) + 0.3 * rng.standard_normal(t.size)
        axs[1].plot(t, x, color=c, lw=0.6)
    axs[1].set_title("Aleatoria: cada realización es distinta")
    for ax in axs:
        ax.set_xlabel("$t$ (s)")
        pe.ejes_centrados(ax)
    guardar(fig, "deterministas_aleatorias")


@figura
def pmf_pdf_cdf():
    fig, axs = pe.figura(2, 3, ancho=6.4, alto=2.9)
    k = np.arange(1, 7)
    pe.stem(axs[0, 0], k, np.ones(6) / 6)
    axs[0, 0].set_title("Dado: $p_X(x_i)=1/6$")
    axs[0, 0].set_ylim(0, 0.25)
    xx = np.linspace(0, 7.5, 1000)
    axs[1, 0].step(np.r_[0, k, 7.5], np.r_[0, k / 6, 1], where="post", color=pe.AZUL)
    axs[1, 0].set_title("$F_X(x)$: escalones de 1/6")
    x = np.linspace(0, 8, 1000)
    a, b = 2, 6
    axs[0, 1].plot(x, stats.uniform.pdf(x, a, b - a), color=pe.AZUL)
    axs[0, 1].set_title(r"Uniforme $\mathcal{U}[2,6]$: $f_X(x)$")
    axs[1, 1].plot(x, stats.uniform.cdf(x, a, b - a), color=pe.AZUL)
    axs[1, 1].set_title("$F_X(x)$")
    x = np.linspace(-4, 4, 1000)
    axs[0, 2].plot(x, stats.norm.pdf(x), color=pe.AZUL)
    axs[0, 2].fill_between(x, stats.norm.pdf(x), where=(x > -2) & (x < 0.5), color=pe.AZUL, alpha=0.2)
    axs[0, 2].text(-1.1, 0.07, "$P(-2<X\\leq0{,}5)$", fontsize=6, ha="center")
    axs[0, 2].set_title(r"Gaussiana $\mathcal{N}(0,1)$: $f_X(x)$")
    axs[1, 2].plot(x, stats.norm.cdf(x), color=pe.AZUL)
    axs[1, 2].vlines([-2, 0.5], 0, stats.norm.cdf([-2, 0.5]), color=pe.GRIS, lw=0.6, ls="--")
    axs[1, 2].set_title("$F_X(x)$")
    for ax in axs[1]:
        ax.set_xlabel("$x$")
        ax.set_ylim(-0.05, 1.1)
    guardar(fig, "pmf_pdf_cdf")


@figura
def gaussiana():
    x = np.linspace(-4, 4, 1000)
    fig, ax = pe.figura(1, 1, ancho=4.2, alto=1.8)
    ax.plot(x, stats.norm.pdf(x), color=pe.AZUL)
    for k, a in ((3, 0.12), (2, 0.2), (1, 0.3)):
        ax.fill_between(x, stats.norm.pdf(x), where=np.abs(x) <= k, color=pe.AZUL, alpha=a, lw=0)
    for k, p in ((1, "68,3 %"), (2, "95,4 %"), (3, "99,7 %")):
        ax.annotate("", xy=(-k, 0.43 - 0.045 * k), xytext=(k, 0.43 - 0.045 * k),
                    arrowprops=dict(arrowstyle="<->", color=pe.GRIS, lw=0.7))
        ax.text(0, 0.435 - 0.045 * k, p, ha="center", fontsize=6.5, va="bottom")
    ax.set_xticks([-3, -2, -1, 0, 1, 2, 3],
                  [r"$\mu-3\sigma$", r"$\mu-2\sigma$", r"$\mu-\sigma$", r"$\mu$", r"$\mu+\sigma$",
                   r"$\mu+2\sigma$", r"$\mu+3\sigma$"])
    ax.set_ylim(0, 0.45)
    ax.set_title(r"$\mathcal{N}(\mu,\sigma^2)$: probabilidad a $\pm k\sigma$ de la media")
    guardar(fig, "gaussiana")


@figura
def metodo_inversa():
    lam = 2
    x = np.linspace(0, 3, 500)
    F = 1 - np.exp(-lam * x)
    fig, axs = pe.figura(1, 2, ancho=6.4, alto=1.9)
    axs[0].plot(x, F, color=pe.AZUL)
    for u in (0.2, 0.5, 0.85):
        xi = -np.log(1 - u) / lam
        axs[0].annotate("", xy=(xi, u), xytext=(0, u), arrowprops=dict(arrowstyle="->", color=pe.ROJO, lw=0.7))
        axs[0].annotate("", xy=(xi, 0), xytext=(xi, u), arrowprops=dict(arrowstyle="->", color=pe.ROJO, lw=0.7))
        axs[0].text(-0.08, u, f"{u}", fontsize=6, ha="right", va="center", color=pe.ROJO)
    axs[0].set_xlabel("$x$")
    axs[0].set_title(r"$u\sim\mathcal{U}[0,1]\ \to\ x=F_X^{-1}(u)$")
    axs[0].set_xlim(-0.3, 3)
    rng = np.random.default_rng(0)
    xs = -np.log(1 - rng.random(5000)) / lam
    histo(axs[1], xs, np.linspace(0, 3, 40))
    axs[1].plot(x, lam * np.exp(-lam * x), color=pe.ROJO)
    axs[1].set_xlabel("$x$")
    axs[1].set_title(r"5000 muestras y $f_X(x)=2\,\mathrm{e}^{-2x}$")
    guardar(fig, "metodo_inversa")


@figura
def rechazo():
    rng = np.random.default_rng(3)
    x = np.linspace(0, 1, 400)
    f = 6 * x * (1 - x)
    M = 1.5
    xs = rng.random(1500)
    us = rng.random(1500) * M
    acept = us <= 6 * xs * (1 - xs)
    fig, axs = pe.figura(1, 2, ancho=6.4, alto=1.9)
    axs[0].plot(xs[acept], us[acept], ".", ms=1.6, color=pe.AZUL)
    axs[0].plot(xs[~acept], us[~acept], ".", ms=1.6, color=pe.GRIS_CLARO)
    axs[0].plot(x, f, color=pe.ROJO)
    axs[0].axhline(M, color=pe.GRIS, ls="--", lw=0.8)
    axs[0].text(0.02, M + 0.03, "$Mq(x)=1{,}5$", fontsize=6.5)
    axs[0].set_ylim(0, 1.7)
    axs[0].set_xlabel("$x$")
    axs[0].set_title(f"Aceptados {acept.mean() * 100:.0f} % (en azul); teórico $1/M=67$ %")
    histo(axs[1], xs[acept], np.linspace(0, 1, 25))
    axs[1].plot(x, f, color=pe.ROJO)
    axs[1].set_xlabel("$x$")
    axs[1].set_title("Muestras aceptadas y $f(x)=6x(1-x)$")
    guardar(fig, "rechazo")


@figura
def mezcla():
    rng = np.random.default_rng(5)
    N = 5000
    comp = rng.random(N) < 0.4
    xs = np.where(comp, rng.normal(3, 0.5, N), rng.normal(6, 1, N))
    x = np.linspace(0, 10, 500)
    f1 = 0.4 * stats.norm.pdf(x, 3, 0.5)
    f2 = 0.6 * stats.norm.pdf(x, 6, 1)
    fig, ax = pe.figura(1, 1, ancho=4.2, alto=1.8)
    histo(ax, xs, np.linspace(0, 10, 60))
    ax.plot(x, f1, color=pe.VERDE, lw=0.8, ls="--")
    ax.plot(x, f2, color=pe.NARANJA, lw=0.8, ls="--")
    ax.plot(x, f1 + f2, color=pe.ROJO)
    ax.set_xlabel("$x$")
    ax.set_title(r"$0{,}4\,\mathcal{N}(3;0{,}5^2)+0{,}6\,\mathcal{N}(6;1)$: elegir componente y muestrearla")
    guardar(fig, "mezcla")


@figura
def histograma_n():
    rng = np.random.default_rng(2)
    x = np.linspace(-4, 4, 400)
    fig, axs = pe.figura(1, 3, ancho=6.4, alto=1.7, sharey=True)
    for ax, N in zip(axs, (100, 1000, 100000)):
        histo(ax, rng.standard_normal(N), np.linspace(-4, 4, 33))
        ax.plot(x, stats.norm.pdf(x), color=pe.ROJO, lw=0.9)
        ax.set_title(f"$N={N}$ muestras")
        ax.set_xlabel("$x$")
    guardar(fig, "histograma_n")


@figura
def montecarlo():
    rng = np.random.default_rng(7)
    Nmax = 100000
    x = rng.random(Nmax)
    y = rng.random(Nmax)
    dentro = (x ** 2 + y ** 2) <= 1
    N = np.arange(1, Nmax + 1)
    est = 4 * np.cumsum(dentro) / N
    fig, axs = pe.figura(1, 2, ancho=6.4, alto=1.9, gridspec_kw={"width_ratios": [1, 1.6]})
    n = 1500
    axs[0].plot(x[:n][dentro[:n]], y[:n][dentro[:n]], ".", ms=1.5, color=pe.AZUL)
    axs[0].plot(x[:n][~dentro[:n]], y[:n][~dentro[:n]], ".", ms=1.5, color=pe.GRIS_CLARO)
    th = np.linspace(0, np.pi / 2, 100)
    axs[0].plot(np.cos(th), np.sin(th), color=pe.ROJO)
    axs[0].set_aspect("equal")
    axs[0].set_title(r"$\pi\approx4\cdot$ (fracción dentro)")
    axs[1].semilogx(N, est, color=pe.AZUL, lw=0.8)
    s = 4 * np.sqrt(np.pi / 4 * (1 - np.pi / 4) / N)
    axs[1].fill_between(N, np.pi - 2 * s, np.pi + 2 * s, color=pe.GRIS_CLARO, alpha=0.5, lw=0)
    axs[1].axhline(np.pi, color=pe.ROJO, lw=0.7)
    axs[1].set_ylim(2.6, 3.7)
    axs[1].set_xlim(10, Nmax)
    axs[1].set_xlabel("$N$")
    axs[1].set_title(r"Estimación y banda $\pm2\sigma$: el error baja como $1/\sqrt{N}$")
    guardar(fig, "montecarlo")


# ---------------------------------------------------------------------
# Parte 2 · Varias variables
# ---------------------------------------------------------------------

@figura
def conjunta():
    rng = np.random.default_rng(4)
    N = 3000
    x1 = rng.uniform(2, 4, N)
    x2 = x1 + rng.standard_normal(N)
    fig = pe.plt.figure(figsize=(6.4, 2.3), constrained_layout=True)
    gs = fig.add_gridspec(2, 3, width_ratios=[1.3, 0.35, 1.4], height_ratios=[0.35, 1.3])
    ax = fig.add_subplot(gs[1, 0])
    axx = fig.add_subplot(gs[0, 0], sharex=ax)
    axy = fig.add_subplot(gs[1, 1], sharey=ax)
    ax.plot(x1, x2, ".", ms=1.2, color=pe.AZUL, alpha=0.6)
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    histo(axx, x1, 30)
    histo(axy, x2, 30, orientation="horizontal")
    axx.set_title("Muestras y marginales")
    for a in (axx, axy):
        a.tick_params(labelbottom=False, labelleft=False)
    ax3 = fig.add_subplot(gs[:, 2])
    g1, g2 = np.meshgrid(np.linspace(1, 5, 200), np.linspace(-1, 7, 200))
    f = stats.uniform.pdf(g1, 2, 2) * stats.norm.pdf(g2, g1, 1)
    ax3.contourf(g1, g2, f, levels=12, cmap="Blues")
    ax3.grid(False)
    ax3.set_xlabel("$x_1$")
    ax3.set_title(r"$f(x_1,x_2)=f(x_2|x_1)\,f(x_1)$")
    guardar(fig, "conjunta")


@figura
def correlacion():
    rng = np.random.default_rng(8)
    N = 600
    fig, axs = pe.figura(1, 5, ancho=6.4, alto=1.45)
    for ax, rho in zip(axs[:4], (-0.8, 0, 0.5, 0.95)):
        z = rng.standard_normal((2, N))
        x = z[0]
        y = rho * z[0] + np.sqrt(1 - rho ** 2) * z[1]
        ax.plot(x, y, ".", ms=1.2, color=pe.AZUL)
        ax.set_title(f"$\\rho={rho:g}$".replace(".", "{,}"))
    x = rng.uniform(-1, 1, N)
    axs[4].plot(x, x ** 2 + 0.03 * rng.standard_normal(N), ".", ms=1.2, color=pe.ROJO)
    axs[4].set_title(r"$Y=X^2$: $\rho=0$")
    for ax in axs:
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect("equal", adjustable="datalim")
    guardar(fig, "correlacion")


@figura
def gaussiana2d():
    mu = np.array([1.0, 2.0])
    S = np.array([[2.0, 1.2], [1.2, 1.0]])
    lam, V = np.linalg.eigh(S)
    rng = np.random.default_rng(1)
    L = np.linalg.cholesky(S)
    z = rng.standard_normal((2, 1500))
    x = mu[:, None] + L @ z
    g1, g2 = np.meshgrid(np.linspace(-4, 6, 300), np.linspace(-1.5, 5.5, 300))
    pos = np.dstack((g1, g2))
    f = stats.multivariate_normal(mu, S).pdf(pos)
    fig, axs = pe.figura(1, 2, ancho=6.4, alto=2.1)
    axs[0].contour(g1, g2, f, levels=6, colors=pe.AZUL, linewidths=0.7)
    for k in range(2):
        v = V[:, k] * np.sqrt(lam[k]) * 2
        axs[0].annotate("", xy=mu + v, xytext=mu, arrowprops=dict(arrowstyle="->", color=pe.ROJO, lw=1))
    axs[0].plot(*mu, "o", color=pe.ROJO, ms=3)
    axs[0].set_aspect("equal")
    axs[0].set_title(r"Curvas de nivel y ejes $2\sqrt{\lambda_k}\,\mathbf{v}_k$")
    axs[1].plot(x[0], x[1], ".", ms=1.2, color=pe.AZUL)
    axs[1].set_aspect("equal")
    axs[1].set_xlim(-4, 6)
    axs[1].set_ylim(-1.5, 5.5)
    axs[1].set_title(r"Muestras $\mathbf{x}=\boldsymbol{\mu}+\mathbf{L}\mathbf{z}$")
    for ax in axs:
        ax.set_xlabel("$x_1$")
        ax.set_ylabel("$x_2$")
    guardar(fig, "gaussiana2d")


@figura
def tcl():
    rng = np.random.default_rng(9)
    fig, axs = pe.figura(1, 4, ancho=6.4, alto=1.6, sharey=True)
    for ax, n in zip(axs, (1, 2, 3, 12)):
        s = rng.random((200000, n)).sum(1)
        z = (s - n / 2) / np.sqrt(n / 12)
        histo(ax, z, np.linspace(-4, 4, 50))
        x = np.linspace(-4, 4, 300)
        ax.plot(x, stats.norm.pdf(x), color=pe.ROJO, lw=0.8)
        ax.set_title(f"Suma de {n} uniforme{'s' if n > 1 else ''}")
        ax.set_xlabel("$z$")
    guardar(fig, "tcl")


# ---------------------------------------------------------------------
# Parte 3 · Señales aleatorias
# ---------------------------------------------------------------------

@figura
def realizaciones():
    rng = np.random.default_rng(11)
    N, M = 200, 300
    v = 0.5 * rng.standard_normal((M, N))
    x = np.cumsum(v, axis=1)
    n = np.arange(N)
    fig, axs = pe.figura(1, 2, ancho=6.4, alto=1.9)
    for i in range(6):
        axs[0].plot(n, x[i], lw=0.6, color=pe.CICLO[i % 5])
    axs[0].plot(n, 2 * 0.5 * np.sqrt(n + 1), color="k", ls="--", lw=0.8)
    axs[0].plot(n, -2 * 0.5 * np.sqrt(n + 1), color="k", ls="--", lw=0.8)
    axs[0].axvline(150, color=pe.GRIS, lw=0.5)
    axs[0].set_title(r"Paseo aleatorio: realizaciones y $\pm2\sigma_x[n]$")
    axs[0].set_xlabel("$n$")
    histo(axs[1], x[:, 50], 25, color=pe.AZUL, label="$n=50$")
    histo(axs[1], x[:, 150], 25, color=pe.ROJO, label="$n=150$")
    axs[1].set_title("Distribución de $x[n]$ sobre el conjunto (300 realizaciones)")
    axs[1].legend(fontsize=6.5)
    guardar(fig, "realizaciones")


@figura
def estacionariedad():
    rng = np.random.default_rng(12)
    N = 100
    n = np.arange(N)
    casos = [
        (r"i.i.d. $\mathcal{U}[0,1]$", lambda: rng.random(N)),
        (r"$\mathcal{N}(0,\,0{,}97^{2n})$", lambda: rng.standard_normal(N) * 0.97 ** n),
        ("Paseo aleatorio", lambda: np.cumsum(0.5 * rng.standard_normal(N))),
        ("Constante aleatoria", lambda: np.full(N, rng.random())),
    ]
    fig, axs = pe.figura(1, 4, ancho=6.4, alto=1.6)
    for ax, (nombre, gen) in zip(axs, casos):
        for i in range(3):
            ax.plot(n, gen(), lw=0.6, color=pe.CICLO[i])
        ax.set_title(nombre)
        ax.set_xlabel("$n$")
    guardar(fig, "estacionariedad")


@figura
def autocorrelacion_ejemplos():
    rng = np.random.default_rng(13)
    Ts = 0.01
    t = np.arange(0, 10 + Ts / 2, Ts)
    casos = [
        (r"$\mathcal{N}(5,1)$ i.i.d.", 5 + rng.standard_normal(t.size), (26, 25)),
        (r"$\mathcal{U}[2,6]$ i.i.d.", 2 + 4 * rng.random(t.size), (52 / 3, 16)),
        ("Seno de 10 Hz", np.sin(2 * np.pi * 10 * t), None),
        (r"AR(1), $a=0{,}95$", signal.lfilter([1], [1, -0.95], rng.standard_normal(t.size)), None),
    ]
    fig, axs = pe.figura(2, 4, ancho=6.4, alto=2.9)
    for j, (nombre, x, teo) in enumerate(casos):
        axs[0, j].plot(t[:200], x[:200], color=pe.AZUL, lw=0.5)
        axs[0, j].set_title(nombre)
        axs[0, j].set_xlabel("$t$ (s)")
        l, c = autocorr(x, 100)
        axs[1, j].plot(l * Ts, c, color=pe.AZUL, lw=0.8)
        if teo:
            axs[1, j].axhline(teo[1], color=pe.ROJO, ls="--", lw=0.7)
        if j == 3:
            axs[1, j].plot(l * Ts, 0.95 ** np.abs(l) / (1 - 0.95 ** 2), color=pe.ROJO, ls="--", lw=0.7)
        axs[1, j].set_xlabel(r"$\tau=lT_s$ (s)")
    axs[1, 0].set_ylabel(r"$\hat\phi_{xx}$")
    guardar(fig, "autocorrelacion_ejemplos")


@figura
def fase_aleatoria():
    rng = np.random.default_rng(14)
    n = np.arange(60)
    W = 2 * np.pi / 20
    fig, axs = pe.figura(1, 2, ancho=6.4, alto=1.7)
    for i in range(4):
        th = rng.uniform(0, 2 * np.pi)
        axs[0].plot(n, np.cos(W * n + th), lw=0.7, color=pe.CICLO[i])
    axs[0].set_title(r"$x[n]=A\cos(\Omega_0n+\theta)$, $\theta\sim\mathcal{U}[0,2\pi)$")
    axs[0].set_xlabel("$n$")
    l = np.arange(-40, 41)
    pe.stem(axs[1], l, 0.5 * np.cos(W * l), ms=2)
    axs[1].set_title(r"$\phi_{xx}[l]=\frac{A^2}{2}\cos(\Omega_0 l)$ ($A=1$, $\Omega_0=2\pi/20$)")
    axs[1].set_xlabel("$l$")
    guardar(fig, "fase_aleatoria")


@figura
def retardo():
    rng = np.random.default_rng(15)
    Ts = 0.01
    t = np.arange(0, 6, Ts)
    x = np.sinc(t - 2)
    y = np.sinc(t - 3) + rng.standard_normal(t.size)
    c = signal.correlate(y, x, "full")
    lags = signal.correlation_lags(len(y), len(x), "full") * Ts
    fig, axs = pe.figura(1, 2, ancho=6.4, alto=1.8)
    axs[0].plot(t, y, color=pe.GRIS_CLARO, lw=0.5, label="$y(t)$ con ruido")
    axs[0].plot(t, x, color=pe.AZUL, label="$x(t)=\\mathrm{sinc}(t-2)$")
    axs[0].plot(t, np.sinc(t - 3), color=pe.ROJO, lw=0.8, label="$\\mathrm{sinc}(t-3)$")
    axs[0].legend(fontsize=5.5, loc="upper right")
    axs[0].set_xlabel("$t$ (s)")
    axs[0].set_title("Señal buscada y señal recibida ($\\sigma=1$)")
    axs[1].plot(lags, c, color=pe.AZUL, lw=0.7)
    k = np.argmax(c)
    axs[1].plot(lags[k], c[k], "o", color=pe.ROJO, ms=3)
    axs[1].text(lags[k] + 0.2, c[k], f"máximo en $\\tau={lags[k]:.2f}$ s".replace(".", "{,}"), fontsize=6.5)
    axs[1].set_xlim(-4, 6)
    axs[1].set_xlabel(r"$\tau$ (s)")
    axs[1].set_title(r"Correlación cruzada $\hat\phi_{yx}(\tau)$")
    guardar(fig, "retardo")


# ---------------------------------------------------------------------
# Parte 4 · Análisis espectral
# ---------------------------------------------------------------------

@figura
def dep_ejemplos():
    W = np.linspace(-np.pi, np.pi, 1000)
    l = np.arange(-15, 16)
    fig, axs = pe.figura(2, 3, ancho=6.4, alto=2.9)
    for j, (a, nombre) in enumerate(((0.0, "Ruido blanco"), (0.8, "AR(1), $a=0{,}8$"), (-0.6, "AR(1), $a=-0{,}6$"))):
        phi = a ** np.abs(l) / (1 - a ** 2)
        pe.stem(axs[0, j], l, phi, ms=2)
        axs[0, j].set_title(nombre)
        axs[0, j].set_xlabel("$l$")
        Phi = 1 / np.abs(1 - a * np.exp(-1j * W)) ** 2
        axs[1, j].plot(W, Phi, color=pe.ROJO)
        axs[1, j].set_ylim(0, max(1.2, Phi.max() * 1.1))
        ticks_pi(axs[1, j], simetrico=True)
        axs[1, j].set_xlabel(r"$\Omega$")
    axs[0, 0].set_ylabel(r"$\phi_{xx}[l]$")
    axs[1, 0].set_ylabel(r"$\Phi_{xx}(\mathrm{e}^{j\Omega})$")
    guardar(fig, "dep_ejemplos")


@figura
def periodograma():
    rng = np.random.default_rng(16)
    a = 0.8
    fig, axs = pe.figura(1, 3, ancho=6.4, alto=1.8, sharey=True)
    W = np.linspace(0, np.pi, 500)
    teo = 1 / np.abs(1 - a * np.exp(-1j * W)) ** 2
    for ax, N in zip(axs[:2], (256, 4096)):
        x = signal.lfilter([1], [1, -a], rng.standard_normal(N + 500))[500:]
        f, P = signal.periodogram(x, fs=2 * np.pi, return_onesided=False, window="boxcar", detrend=False)
        ax.semilogy(f[: N // 2], 2 * np.pi * P[: N // 2], color=pe.GRIS, lw=0.4)
        ax.semilogy(W, teo, color=pe.ROJO, lw=0.9)
        ax.set_title(f"Periodograma, $N={N}$")
    x = signal.lfilter([1], [1, -a], rng.standard_normal(4096 + 500))[500:]
    f, P = signal.welch(x, fs=2 * np.pi, window="hann", nperseg=256, return_onesided=False, detrend=False)
    axs[2].semilogy(f[:128], 2 * np.pi * P[:128], color=pe.AZUL, lw=0.9)
    axs[2].semilogy(W, teo, color=pe.ROJO, lw=0.9)
    axs[2].set_title("Welch, $N=4096$, tramos de 256")
    for ax in axs:
        ticks_pi(ax)
        ax.set_xlabel(r"$\Omega$")
        ax.set_ylim(0.05, 100)
    guardar(fig, "periodograma")


@figura
def filtrado_ruido():
    rng = np.random.default_rng(17)
    N = 20000
    x = rng.standard_normal(N)
    b, a = signal.butter(4, 0.25)
    y = signal.lfilter(b, a, x)
    fig, axs = pe.figura(1, 2, ancho=6.4, alto=1.8)
    n = np.arange(200)
    axs[0].plot(n, x[:200], color=pe.GRIS_CLARO, lw=0.6, label="$x$: blanco")
    axs[0].plot(n, y[:200], color=pe.AZUL, lw=0.9, label="$y=h\\ast x$")
    axs[0].legend(fontsize=6, loc="upper right")
    axs[0].set_xlabel("$n$")
    axs[0].set_title("Ruido blanco filtrado: ruido coloreado")
    f, P = signal.welch(y, fs=2 * np.pi, nperseg=512, return_onesided=False, detrend=False)
    W, H = signal.freqz(b, a, 512)
    axs[1].plot(f[:256], 2 * np.pi * P[:256], color=pe.AZUL, lw=0.8, label="Welch")
    axs[1].plot(W, np.abs(H) ** 2, color=pe.ROJO, ls="--", lw=0.9, label="$|H|^2\\sigma_x^2$")
    axs[1].legend(fontsize=6)
    ticks_pi(axs[1])
    axs[1].set_xlabel(r"$\Omega$")
    axs[1].set_title(r"$\Phi_{yy}=|H|^2\,\Phi_{xx}$ (Butterworth, $\Omega_c=0{,}25\pi$)")
    guardar(fig, "filtrado_ruido")


@figura
def identificacion():
    rng = np.random.default_rng(18)
    N = 20000
    x = rng.standard_normal(N)
    b, a = [0.2, 0.3], [1, -1.2, 0.72]
    y = signal.lfilter(b, a, x) + 0.3 * rng.standard_normal(N)
    f, Pxx = signal.welch(x, fs=2 * np.pi, nperseg=256, detrend=False)
    _, Pxy = signal.csd(x, y, fs=2 * np.pi, nperseg=256, detrend=False)
    Hest = Pxy / Pxx
    W, H = signal.freqz(b, a, 512)
    fig, axs = pe.figura(1, 2, ancho=6.4, alto=1.8)
    axs[0].plot(f, np.abs(Hest), ".", ms=2.5, color=pe.AZUL, label="estimada")
    axs[0].plot(W, np.abs(H), color=pe.ROJO, lw=0.9, label="real")
    axs[0].set_title(r"$|\hat H|=|\hat\Phi_{yx}/\hat\Phi_{xx}|$")
    axs[0].legend(fontsize=6)
    axs[1].plot(f, np.unwrap(np.angle(Hest)), ".", ms=2.5, color=pe.AZUL)
    axs[1].plot(W, np.unwrap(np.angle(H)), color=pe.ROJO, lw=0.9)
    axs[1].set_title(r"$\arg\hat H$ (rad)")
    for ax in axs:
        ticks_pi(ax)
        ax.set_xlabel(r"$\Omega$")
    guardar(fig, "identificacion")


# ---------------------------------------------------------------------
# Cápsulas: estimadores robustos, predicción lineal, Wiener y detección
# ---------------------------------------------------------------------
@figura
def robusto_sigma():
    rng = np.random.default_rng(7)
    fr = np.linspace(0, 0.3, 31)
    sd, mad = [], []
    for p in fr:
        a, b = [], []
        for _ in range(200):
            x = rng.standard_normal(400)
            k = rng.random(400) < p
            x[k] += rng.choice([-8, 8], k.sum())
            a.append(x.std())
            b.append(1.4826 * np.median(np.abs(x - np.median(x))))
        sd.append(np.mean(a))
        mad.append(np.mean(b))
    fig, ax = pe.figura(1, 1, ancho=3.2, alto=1.9)
    ax.plot(100 * fr, sd, color=pe.ROJO, label="desviación típica")
    ax.plot(100 * fr, mad, color=pe.VERDE, label=r"$1{,}4826\cdot$MAD")
    ax.axhline(1, color=pe.GRIS, lw=0.6, ls="--")
    ax.set_xlabel("atípicos (%)")
    ax.set_ylabel(r"$\hat\sigma$ (real: 1)")
    ax.legend(loc="upper left")
    guardar(fig, "robusto_sigma")


@figura
def hampel_ejemplo():
    rng = np.random.default_rng(11)
    N, K, t = 300, 10, 3
    n = np.arange(N)
    s = 10 + 2 * (n > 150) + 0.5 * np.sin(2 * np.pi * n / 120)
    x = s + 0.3 * rng.standard_normal(N)
    idx = [40, 41, 95, 210, 260]
    x[idx] += [4, 4.5, -5, 6, -4]
    y, at = x.copy(), np.zeros(N, bool)
    for k in range(K, N - K):
        v = x[k - K:k + K + 1]
        m = np.median(v)
        S = 1.4826 * np.median(np.abs(v - m))
        if abs(x[k] - m) > t * S:
            y[k], at[k] = m, True
    fig, ax = pe.figura(1, 1, ancho=3.3, alto=1.9)
    ax.plot(n, x, color=pe.GRIS_CLARO, lw=0.8, label="$x[n]$")
    ax.plot(n, y, color=pe.AZUL, lw=1.1, label="limpia")
    ax.plot(n[at], x[at], "o", color=pe.ROJO, ms=3, label="marcadas")
    ax.set_xlabel("$n$")
    ax.legend(loc="lower right", ncol=3)
    guardar(fig, "hampel_ejemplo")


@figura
def prediccion_residuo():
    from scipy import linalg
    rng = np.random.default_rng(2)
    N, p = 1500, 4
    x = signal.lfilter([1], [1, -1.6, 0.9], rng.standard_normal(N))
    x[[400, 1100]] += [6, -6]
    r = np.correlate(x, x, "full")[N - 1:] / N
    a = linalg.solve_toeplitz(r[:p], r[1:p + 1])
    e = signal.lfilter(np.r_[1, -a], [1], x)
    S = 1.4826 * np.median(np.abs(e))
    n = np.arange(N)
    fig, axs = pe.figura(2, 1, ancho=3.3, alto=2.4, sharex=True)
    axs[0].plot(n, x, color=pe.AZUL, lw=0.7)
    axs[0].set_ylabel("$x[n]$")
    axs[1].plot(n, e, color=pe.GRIS, lw=0.7)
    axs[1].axhline(5 * S, color=pe.ROJO, lw=0.8, ls="--")
    axs[1].axhline(-5 * S, color=pe.ROJO, lw=0.8, ls="--")
    axs[1].set_ylabel("$e[n]$")
    axs[1].set_xlabel("$n$")
    guardar(fig, "prediccion_residuo")


@figura
def wiener_ganancia():
    W = np.linspace(0, np.pi, 512)
    Pss = 1 / np.abs(1 - 0.9 * np.exp(-1j * W)) ** 2
    Pvv = 1.0 * np.ones_like(W)
    H = Pss / (Pss + Pvv)
    fig, axs = pe.figura(1, 2, ancho=6.4, alto=1.8)
    axs[0].semilogy(W, Pss, color=pe.AZUL, label=r"$\Phi_{ss}$")
    axs[0].semilogy(W, Pvv, color=pe.ROJO, label=r"$\Phi_{vv}$")
    axs[0].legend()
    axs[0].set_title("DEP de la señal y del ruido")
    axs[1].plot(W, H, color=pe.VERDE)
    axs[1].set_ylim(0, 1.05)
    axs[1].set_title(r"$H(\mathrm{e}^{j\Omega})$ de Wiener")
    for ax in axs:
        ticks_pi(ax)
        ax.set_xlabel(r"$\Omega$")
    guardar(fig, "wiener_ganancia")


@figura
def deteccion_umbral():
    d = np.linspace(-4, 9, 600)
    p0 = stats.norm.pdf(d, 0, 1)
    p1 = stats.norm.pdf(d, 4, 1.3)
    u = 2.2
    N0, N1 = 2000, 50                     # muestras sin y con evento
    us = np.linspace(-1, 8, 200)
    vp = N1 * stats.norm.sf(us, 4, 1.3)
    fp = N0 * stats.norm.sf(us, 0, 1)
    se = vp / N1
    vpp = vp / np.maximum(vp + fp, 1e-12)
    fig, axs = pe.figura(1, 2, ancho=6.4, alto=1.9)
    ax = axs[0]
    ax.plot(d, p0, color=pe.GRIS, label="sin evento")
    ax.plot(d, p1, color=pe.AZUL, label="con evento")
    ax.fill_between(d[d > u], p0[d > u], color=pe.ROJO, alpha=0.35, lw=0, label="FP")
    ax.fill_between(d[d < u], p1[d < u], color=pe.NARANJA, alpha=0.45, lw=0, label="FN")
    ax.axvline(u, color=pe.ROJO, lw=0.8, ls="--")
    ax.set_xlabel("estadístico $d$")
    ax.set_title("Umbral $u$")
    ax.legend(loc="upper right", fontsize=6)
    ax = axs[1]
    ax.plot(us, se, color=pe.AZUL, label="Se")
    ax.plot(us, vpp, color=pe.VERDE, label="VPP")
    ax.plot(us, 2 * se * vpp / np.maximum(se + vpp, 1e-12), color=pe.NARANJA, label="F1")
    ax.set_xlabel("umbral $u$")
    ax.set_ylim(0, 1.05)
    ax.set_title("Métricas frente al umbral")
    ax.legend(loc="lower right")
    guardar(fig, "deteccion_umbral")


if __name__ == "__main__":
    nombres = sys.argv[1:] or list(FIGURAS)
    for nombre in nombres:
        FIGURAS[nombre]()
        print("ok", nombre)
