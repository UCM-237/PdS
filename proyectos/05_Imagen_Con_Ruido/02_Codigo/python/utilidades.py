"""Funciones de apoyo del proyecto «Imagen con ruido». No hace falta modificarlas."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy import ndimage

DATOS = Path(__file__).resolve().parents[2] / "01_Datos"
FIGURAS = Path(__file__).resolve().parent / "figuras"
FIGURAS.mkdir(exist_ok=True)


def cargar(n, limpia=False):
    """imagen_n.png (o imagen_n_limpia.png, solo n = 1, 2, 3) como matriz float entre 0 y 1."""
    nombre = f"imagen_{n}_limpia.png" if limpia else f"imagen_{n}.png"
    return np.asarray(Image.open(DATOS / nombre), dtype=float) / 255


def guardar_restaurada(n, img):
    """Escribe restaurada_n.png (8 bits) en la carpeta actual."""
    Image.fromarray(np.round(np.clip(img, 0, 1) * 255).astype(np.uint8)).save(f"restaurada_{n}.png")


def psnr(x, ref):
    """PSNR en dB con pico 1."""
    return 10 * np.log10(1 / np.mean((np.clip(x, 0, 1) - ref) ** 2))


def ssim(x, ref, sigma=1.5):
    """SSIM medio (Wang et al., 2004) con ventana gaussiana σ = 1,5 px, L = 1."""
    x = np.clip(x, 0, 1)
    c1, c2 = 0.01 ** 2, 0.03 ** 2
    f = lambda a: ndimage.gaussian_filter(a, sigma, mode="reflect", truncate=3.5)
    mx, my = f(x), f(ref)
    vx, vy, cxy = f(x * x) - mx ** 2, f(ref * ref) - my ** 2, f(x * ref) - mx * my
    m = ((2 * mx * my + c1) * (2 * cxy + c2)) / ((mx ** 2 + my ** 2 + c1) * (vx + vy + c2))
    return float(m.mean())


def filtrar_sep(img, h_filas, h_cols):
    """Aplica h_filas a lo largo de cada fila (eje x) y h_cols a lo largo de cada columna,
    con los bordes reflejados."""
    out = ndimage.convolve1d(img, h_filas, axis=1, mode="reflect")
    return ndimage.convolve1d(out, h_cols, axis=0, mode="reflect")


def placa_zonal(n=512):
    """cos(π r² / n): la frecuencia local crece con el radio hasta 0,5 ciclos/px en el borde."""
    y, x = np.mgrid[0:n, 0:n] - n / 2
    return 0.5 + 0.5 * np.cos(np.pi * (x ** 2 + y ** 2) / n)


def espectro_2d(img, ventana=True):
    """log10 |DFT 2D| centrada (fftshift), con ventana de Hann separable si ventana=True."""
    x = img - img.mean()
    if ventana:
        x = x * np.outer(np.hanning(img.shape[0]), np.hanning(img.shape[1]))
    return np.fft.fftshift(np.log10(np.abs(np.fft.fft2(x)) + 1e-9))


def frecuencias_2d(forma):
    """Matrices FX, FY (ciclos/px) en el mismo orden que espectro_2d."""
    fy = np.fft.fftshift(np.fft.fftfreq(forma[0]))
    fx = np.fft.fftshift(np.fft.fftfreq(forma[1]))
    return np.meshgrid(fx, fy)


def guardar(fig, nombre):
    fig.savefig(FIGURAS / nombre, dpi=130, bbox_inches="tight")
    plt.close(fig)
    print("figura:", FIGURAS / nombre)
