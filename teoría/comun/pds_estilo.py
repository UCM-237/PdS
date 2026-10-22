"""Estilo común de las figuras de la asignatura (Matplotlib).

Usa la misma paleta y tipografía (Fira Sans) que las transparencias y los
apuntes. Cada tema tiene un ``figuras/generar_figuras.py`` que importa este
módulo:

    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "comun"))
    import pds_estilo as pe
    pe.aplicar()
    fig, ax = pe.figura()
    ...
    pe.guardar(fig, "nombre")      # escribe nombre.pdf junto al script
"""

from __future__ import annotations

import pathlib
import subprocess

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402

AZUL = "#2B3A8C"
ROJO = "#C0392B"
VERDE = "#1E7B4F"
NARANJA = "#D9822B"
GRIS = "#5A5A66"
GRIS_CLARO = "#B8BAC6"
CICLO = [AZUL, ROJO, VERDE, NARANJA, GRIS]

# Tamaño base pensado para incluirse a ~6,5 cm de ancho en una
# transparencia 16:9 (o a media columna en los apuntes).
ANCHO = 3.3
ALTO = 1.9


def _registrar_fira() -> str:
    """Registra Fira Sans desde TeX Live si está disponible."""
    try:
        ruta = subprocess.run(["kpsewhich", "FiraSans-Regular.otf"], capture_output=True,
                              text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "DejaVu Sans"
    if not ruta:
        return "DejaVu Sans"
    carpeta = pathlib.Path(ruta).parent
    for nombre in ("FiraSans-Regular.otf", "FiraSans-Italic.otf", "FiraSans-SemiBold.otf"):
        f = carpeta / nombre
        if f.exists():
            font_manager.fontManager.addfont(str(f))
    return "Fira Sans"


def aplicar() -> None:
    familia = _registrar_fira()
    plt.rcParams.update({
        "font.family": familia,
        "font.size": 8,
        "axes.titlesize": 8,
        "axes.labelsize": 8,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "legend.fontsize": 7,
        "mathtext.fontset": "custom",
        "mathtext.rm": familia,
        "mathtext.it": f"{familia}:italic",
        "mathtext.bf": f"{familia}:bold",
        "mathtext.cal": f"{familia}:italic",
        "axes.prop_cycle": matplotlib.cycler(color=CICLO),
        "axes.edgecolor": GRIS,
        "axes.labelcolor": "#222222",
        "axes.linewidth": 0.6,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": "#E3E4EC",
        "grid.linewidth": 0.5,
        "xtick.color": GRIS,
        "ytick.color": GRIS,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "lines.linewidth": 1.4,
        "lines.markersize": 3.2,
        "legend.frameon": False,
        "figure.dpi": 150,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
        "pdf.fonttype": 3,  # Fira es OpenType/CFF: Type 42 no la incrusta bien
    })


def figura(filas: int = 1, columnas: int = 1, ancho: float = ANCHO, alto: float = ALTO, **kw):
    return plt.subplots(filas, columnas, figsize=(ancho, alto), constrained_layout=True, **kw)


def stem(ax, n, x, color=AZUL, etiqueta=None, ms=None):
    """Representación de secuencias: tallo fino y punto relleno."""
    mk, st, bl = ax.stem(n, x, linefmt="-", markerfmt="o", basefmt=" ", label=etiqueta)
    plt.setp(st, color=color, linewidth=0.9)
    plt.setp(mk, color=color, markersize=ms or plt.rcParams["lines.markersize"])
    ax.axhline(0, color=GRIS, linewidth=0.6, zorder=0)
    return mk, st


def ejes_centrados(ax):
    """Eje horizontal en y=0, útil para señales que cambian de signo."""
    ax.axhline(0, color=GRIS, linewidth=0.6, zorder=0)


def guardar(fig, nombre: str, carpeta: pathlib.Path | None = None) -> pathlib.Path:
    carpeta = carpeta or pathlib.Path.cwd()
    ruta = carpeta / f"{nombre}.pdf"
    fig.savefig(ruta, metadata={"CreationDate": None, "ModDate": None, "Producer": None})
    plt.close(fig)
    return ruta
