"""Hito 3: extraccion de caracteristicas e indicadores de rendimiento."""
import numpy as np
import pandas as pd

from carrera import analisis, caracteristicas as cr, carga
from carrera.graficas import AZUL, GRIS, NARANJA, ROJO, TINTA, VIOLETA, guardar, plt

SALIDA = carga.DIR_HITOS / "Hito_3_Extraccion_Caracteristicas"
FIG = SALIDA / "figuras"
RAMPA_ZONAS = ["#cfe1f7", "#93bdee", "#4f93e0", "#2a78d6", "#14498a"]  # secuencial, un tono


def fig_parciales(res):
    u = res["u"]
    p = cr.parciales_km(u)
    p = p[p["distancia_km"] > 0.5]
    fig, axs = plt.subplots(2, 1, figsize=(9, 4.5), sharex=True)
    media = p["tiempo_s"].sum() / 60 / p["distancia_km"].sum()
    axs[0].plot(p["km"], p["ritmo_min_km"], "o-", color=AZUL, ms=5)
    axs[0].axhline(media, color=GRIS, ls="--", lw=1)
    axs[0].text(p["km"].iloc[-1] + 0.3, media, f"media {cr.formato_ritmo(media)}", va="center",
                fontsize=7, color=TINTA)
    axs[0].invert_yaxis()  # arriba = mas rapido
    axs[0].set(ylabel="Ritmo (min/km)\n(arriba = mas rapido)",
               title=f"Parciales por km - {u.attrs['nombre']}")
    for k, r in zip(p["km"], p["ritmo_min_km"]):
        axs[0].annotate(cr.formato_ritmo(r), (k, r), textcoords="offset points", xytext=(0, -11),
                        ha="center", fontsize=6, color=TINTA)
    axs[1].plot(p["km"], p["fc_media"], "o-", color=NARANJA, ms=4)
    axs[1].set(ylabel="FC media (ppm)", xlabel="Kilometro")
    fig.tight_layout()
    return guardar(fig, FIG / f"h3_parciales_{u.attrs['nombre']}.png")


def fig_deriva(res):
    """Velocidad, FC y eficiencia (v/FC) en la tirada larga: deriva cardiaca."""
    u = res["u"]
    corre = res["estados"] == 2
    tm = u["time"] / 60
    ef = np.where(corre, u["v_filt"] / u["fc_filt"] * 100, np.nan)
    fig, axs = plt.subplots(3, 1, figsize=(9, 5.5), sharex=True)
    axs[0].plot(tm, u["v_filt"], color=AZUL)
    axs[0].set(ylabel="v filtrada\n(km/h)", title=f"Deriva cardiaca - {u.attrs['nombre']}")
    axs[1].plot(tm, u["fc_filt"], color=NARANJA)
    axs[1].set_ylabel("FC filtrada\n(ppm)")
    axs[2].plot(tm, ef, color=VIOLETA)
    axs[2].set_ylabel("EF = v/FC\n(km/h por 100 ppm)")
    idx = np.where(corre & (u["time"] >= 600))[0]
    mitad = idx[len(idx) // 2]
    for i0, i1 in [(idx[0], mitad), (mitad, idx[-1])]:
        m = np.nanmean(ef[i0:i1])
        axs[2].hlines(m, tm[i0], tm[i1], color=ROJO, lw=2)
        axs[2].text((tm[i0] + tm[i1]) / 2, m + 0.3, f"{m:.2f}", color=ROJO, ha="center", va="bottom", fontsize=8)
    axs[2].set_xlabel("Tiempo (min)")
    fig.tight_layout()
    return guardar(fig, FIG / f"h3_deriva_{u.attrs['nombre']}.png")


def fig_subida(res):
    """Respuesta a la pendiente: la subida del 15/01."""
    u = res["u"]
    g = cr.pendiente(u["distance_corr"].to_numpy(), u["alt_filt"].to_numpy())
    tm = u["time"] / 60
    fig, axs = plt.subplots(4, 1, figsize=(9, 6.5), sharex=True)
    axs[0].plot(tm, u["alt_filt"], color=TINTA)
    axs[0].set(ylabel="Altitud (m)", title=f"Efecto de la pendiente - {u.attrs['nombre']}")
    axs[1].plot(tm, g, color=VIOLETA)
    axs[1].axhline(0, color=GRIS, lw=0.8)
    axs[1].set_ylabel("Pendiente (%)")
    axs[2].plot(tm, u["v_filt"], color=AZUL)
    axs[2].set_ylabel("v filtrada (km/h)")
    axs[3].plot(tm, u["fc_filt"], color=NARANJA)
    axs[3].set(ylabel="FC (ppm)", xlabel="Tiempo (min)")
    sube = g > 2
    for a in axs:
        a.fill_between(tm, 0, 1, where=sube, transform=a.get_xaxis_transform(), color=ROJO,
                       alpha=0.08, lw=0)
    fig.tight_layout()
    return guardar(fig, FIG / f"h3_pendiente_{u.attrs['nombre']}.png"), g


def fig_zonas(tabla):
    fig, ax = plt.subplots(figsize=(8, 2.8))
    izq = np.zeros(len(tabla))
    for z, c in zip(cr.ZONAS_FC, RAMPA_ZONAS):
        val = tabla[f"t_{z}_pct"].to_numpy()
        ax.barh(tabla["fecha"], val, left=izq, color=c, edgecolor="white", linewidth=1.5,
                label=f"{z} ({int(cr.ZONAS_FC[z][0] * 100)}-{min(100, int(cr.ZONAS_FC[z][1] * 100))} %)")
        for y, (x0, v) in enumerate(zip(izq, val)):
            if v >= 8:
                ax.text(x0 + v / 2, y, f"{v:.0f}", ha="center", va="center", fontsize=7,
                        color="white" if c in RAMPA_ZONAS[2:] else TINTA)
        izq += val
    ax.set(xlabel=f"% del tiempo corriendo (FCmax supuesta = {cr.FC_MAXIMA} ppm)",
           title="Tiempo en zonas de frecuencia cardiaca", xlim=(0, 100))
    ax.invert_yaxis()
    ax.grid(axis="y", visible=False)
    ax.legend(ncol=5, fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.28))
    return guardar(fig, FIG / "h3_zonas_fc.png")


COLUMNAS = {
    "fecha": "Fecha", "distancia_km": "Distancia (km)", "duracion_min": "Duracion (min)",
    "tiempo_carrera_min": "T. corriendo (min)", "ritmo": "Ritmo carrera (min/km)",
    "v_carrera_kmh": "v carrera (km/h)", "cv_velocidad_pct": "CV v (%)",
    "fc_media": "FC media", "fc_max": "FC max", "desnivel_pos_m": "D+ (m)",
    "pendiente_max_pct": "Pend. max (%)", "t_estab_fc_min": "Estab. FC (min)",
    "desacoplamiento_pct": "Desacopl. (%)", "ef_m_por_latido": "m/latido",
}


def main():
    resultados = {n: analisis.analizar(d) for n, d in carga.cargar_todas().items()}
    tabla = pd.DataFrame([r["resumen"] for r in resultados.values()])
    tabla["ritmo"] = tabla["ritmo_carrera_min_km"].map(cr.formato_ritmo)
    tabla.to_csv(SALIDA / "indicadores.csv", index=False, float_format="%.3f")

    fig_parciales(resultados["2026-01-11"])
    fig_deriva(resultados["2026-01-11"])
    _, g = fig_subida(resultados["2026-01-15"])
    fig_zonas(tabla)

    corto = tabla[list(COLUMNAS)].rename(columns=COLUMNAS).round(2)
    zonas = tabla[["fecha"] + [f"t_{z}_pct" for z in cr.ZONAS_FC]].round(1)
    parc = cr.parciales_km(resultados["2026-01-11"]["u"]).round(2)
    parc["ritmo"] = parc["ritmo_min_km"].map(cr.formato_ritmo)

    # Respuesta a la pendiente en el 15/01: velocidad y FC en subida vs llano
    u = resultados["2026-01-15"]["u"]
    corre = resultados["2026-01-15"]["estados"] == 2
    sube, llano, baja = corre & (g > 2), corre & (np.abs(g) <= 1), corre & (g < -2)
    pend = pd.DataFrame({
        "Tramo": ["Subida (>2 %)", "Llano (+-1 %)", "Bajada (<-2 %)"],
        "Tiempo (min)": [m.sum() / 60 for m in (sube, llano, baja)],
        "v media (km/h)": [u["v_filt"][m].mean() for m in (sube, llano, baja)],
        "FC media (ppm)": [u["fc_filt"][m].mean() for m in (sube, llano, baja)],
    }).round(1)

    texto = ["## Indicadores por sesion\n", corto.to_markdown(index=False), "\n",
             "## Tiempo en zonas de FC (% del tiempo corriendo)\n", zonas.to_markdown(index=False), "\n",
             "## Parciales de la tirada larga (11/01)\n", parc.to_markdown(index=False), "\n",
             "## Respuesta a la pendiente (15/01)\n", pend.to_markdown(index=False), "\n"]
    (SALIDA / "resultados.md").write_text("\n".join(texto), encoding="utf-8")
    print("\n".join(texto))


if __name__ == "__main__":
    main()
