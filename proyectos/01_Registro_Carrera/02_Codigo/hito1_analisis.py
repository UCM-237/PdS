"""Hito 1: carga, representacion temporal y diagnostico de anomalias."""
import numpy as np
import pandas as pd

from carrera import carga, preprocesado as pp
from carrera.graficas import AZUL, GRIS, NARANJA, ROJO, TINTA, guardar, plt

SALIDA = carga.DIR_HITOS / "Hito_1_Analisis_Senal"
FIG = SALIDA / "figuras"


def fig_senales(acts):
    fig, axs = plt.subplots(len(acts), 3, figsize=(11, 2.0 * len(acts)), sharex="row")
    for fila, (nombre, d) in zip(axs, acts.items()):
        tm = d["time"] / 60
        fila[0].plot(tm, d["speed_kmh"], color=AZUL, lw=0.8)
        fila[0].set_ylim(0, 25)
        fila[0].set_ylabel(f"{nombre}\nVelocidad (km/h)")
        fila[1].plot(tm, d["heartrate"], color=NARANJA, lw=0.9)
        fila[1].set_ylabel("FC (ppm)")
        fila[2].plot(tm, d["altitude"], color=TINTA, lw=0.9)
        fila[2].set_ylabel("Altitud (m)")
        for t0, t1 in pp.detectar_huecos(d["time"]):
            for a in fila:
                a.axvspan(t0 / 60, t1 / 60, color=ROJO, alpha=0.25, lw=0)
    for a in axs[-1]:
        a.set_xlabel("Tiempo (min)")
    axs[0, 0].set_title("Velocidad (velocity_smooth)")
    axs[0, 1].set_title("Frecuencia cardiaca")
    axs[0, 2].set_title("Altitud")
    if len(acts) > 1:
        axs[0, 0].text(0.99, 0.02, "sombreado rojo = hueco > 15 s", transform=axs[0, 0].transAxes,
                       ha="right", fontsize=7, color=TINTA)
    fig.tight_layout()
    return guardar(fig, FIG / "h1_senales_originales.png")


def fig_muestreo(acts):
    dts = np.concatenate([pp.intervalos_muestreo(d["time"]) for d in acts.values()])
    fig, ax = plt.subplots(figsize=(6, 2.6))
    bins = np.arange(0.5, dts.max() + 1.5, 1)
    ax.hist(dts, bins=bins, color=AZUL, rwidth=0.85)
    ax.set_yscale("log")
    ax.set_xlabel("Intervalo entre muestras dt (s)")
    ax.set_ylabel("N.o de intervalos")
    ax.set_title("Muestreo no uniforme (5 actividades)")
    ax.axvline(pp.HUECO_S, color=ROJO, ls="--", lw=1)
    ax.text(pp.HUECO_S + 0.5, ax.get_ylim()[1] * 0.3, "umbral de hueco", color=ROJO, fontsize=8)
    return guardar(fig, FIG / "h1_histograma_muestreo.png"), dts


def fig_anomalias(acts):
    fig, axs = plt.subplots(1, 3, figsize=(11, 3))
    # a) salto de GPS
    d = acts["2026-01-09"]
    m = d["time"] < 200
    ax = axs[0]
    ax.plot(d["time"][m], pp.velocidad_desde_distancia(d)[m], color=GRIS, marker=".",
            label="derivada de la distancia")
    ax.plot(d["time"][m], d["speed_kmh"][m], color=AZUL, marker=".", label="velocity_smooth")
    out = pp.detectar_outliers_velocidad(d)
    ax.plot(d["time"][out], d["speed_kmh"][out], "o", mfc="none", mec=ROJO, ms=10, label="outlier")
    ax.set(title="(a) 09/01: salto de GPS", xlabel="Tiempo (s)", ylabel="Velocidad (km/h)")
    ax.legend(fontsize=7)
    # b) meseta de FC
    d = acts["2026-01-07"]
    m = d["time"] < 400
    ax = axs[1]
    ax.plot(d["time"][m], d["heartrate"][m], color=NARANJA, marker=".", ms=4)
    for i0, i1 in pp.detectar_meseta(d["time"], d["heartrate"]):
        ax.axvspan(d["time"][i0], d["time"][i1], color=ROJO, alpha=0.2, lw=0)
    ax.set(title="(b) 07/01: FC congelada al inicio", xlabel="Tiempo (s)", ylabel="FC (ppm)")
    # c) huecos y final andando
    d = acts["2026-01-15"]
    m = d["time"] > 3200
    ax = axs[2]
    ax.plot(d["time"][m], d["speed_kmh"][m], color=AZUL, marker=".")
    for t0, t1 in pp.detectar_huecos(d["time"]):
        ax.axvspan(t0, t1, color=ROJO, alpha=0.2, lw=0)
    ax.set(title="(c) 15/01: huecos y vuelta a la calma", xlabel="Tiempo (s)",
           ylabel="Velocidad (km/h)")
    fig.tight_layout()
    return guardar(fig, FIG / "h1_anomalias.png")


def tabla_diagnostico(acts):
    filas = []
    for nombre, d in acts.items():
        dt = pp.intervalos_muestreo(d["time"])
        out = pp.detectar_outliers_velocidad(d)
        mes = pp.detectar_meseta(d["time"], d["heartrate"])
        filas.append({
            "Actividad": nombre, "Muestras": len(d),
            "Duracion (min)": round(d["time"].iloc[-1] / 60, 1),
            "Distancia Strava (km)": round(d["distance"].iloc[-1] / 1000, 2),
            "dt mediana (s)": np.median(dt), "dt max (s)": dt.max(),
            "Huecos >15 s": len(pp.detectar_huecos(d["time"])),
            "Outliers v": int(out.sum()),
            "v max (km/h)": round(d["speed_kmh"].max(), 1),
            "FC congelada (s)": sum(d["time"][b] - d["time"][a] for a, b in mes),
            "Altitud (m)": f"{d['altitude'].min():.0f}-{d['altitude'].max():.0f}",
        })
    return pd.DataFrame(filas)


def main():
    acts = carga.cargar_todas()
    fig_senales(acts)
    _, dts = fig_muestreo(acts)
    fig_anomalias(acts)
    tab = tabla_diagnostico(acts)
    texto = ["## Diagnostico por actividad\n", tab.to_markdown(index=False), "\n",
             f"Intervalo de muestreo global: media {dts.mean():.2f} s, mediana "
             f"{np.median(dts):.0f} s, p95 {np.percentile(dts, 95):.0f} s, max {dts.max():.0f} s\n"]
    (SALIDA / "resultados.md").write_text("\n".join(texto), encoding="utf-8")
    print("\n".join(texto))


if __name__ == "__main__":
    main()
