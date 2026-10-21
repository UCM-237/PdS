"""Funciones de apoyo del proyecto «Códigos de barras». No hace falta modificarlas."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy import ndimage

DATOS = Path(__file__).resolve().parents[2] / "01_Datos"
FIGURAS = Path(__file__).resolve().parent / "figuras"
FIGURAS.mkdir(exist_ok=True)


def cargar(i):
    """Imagen codigo_i.png como matriz float entre 0 y 1."""
    return np.asarray(Image.open(DATOS / f"codigo_{i}.png"), dtype=float) / 255


def codigos_desarrollo():
    """Diccionario {número de imagen: código} de las imágenes de desarrollo."""
    out = {}
    for linea in (DATOS / "codigos_desarrollo.csv").read_text().splitlines()[1:]:
        nombre, codigo = linea.split(",")
        out[int(nombre.split("_")[1].split(".")[0])] = codigo
    return out


def enderezar(img, angulo):
    """Gira la imagen `angulo` grados para dejar horizontal un código cuyo eje forma ese
    ángulo con la horizontal (positivo: el código baja hacia la derecha)."""
    return ndimage.rotate(img, angulo, reshape=True, order=3, mode="constant", cval=np.median(img))


def guardar_lecturas(lecturas):
    """lecturas: {número de imagen: código o None}. Escribe lecturas.csv."""
    with open("lecturas.csv", "w") as f:
        f.write("imagen,codigo\n")
        for i, c in sorted(lecturas.items()):
            f.write(f"codigo_{i}.png,{c or ''}\n")


def guardar(fig, nombre):
    fig.savefig(FIGURAS / nombre, dpi=130, bbox_inches="tight")
    plt.close(fig)
    print("figura:", FIGURAS / nombre)
