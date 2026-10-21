"""Hito 2: limpieza, remuestreo, analisis espectral y eleccion del filtro."""
import numpy as np
import pandas as pd

from carrera import caracteristicas as cr, carga, preprocesado as pp, sintetico as sy
from carrera.graficas import AMARILLO, AQUA, AZUL, GRIS, NARANJA, ROJO, TINTA, VIOLETA, guardar, plt

SALIDA = carga.DIR_HITOS / "Hito_2_Preprocesado"
FIG = SALIDA / "figuras"
FS = 1.0


def filtros(t, v):
    """Los candidatos comparados. Todos sobre la rejilla uniforme de 1 Hz."""
    return {
        "EMA tau=10 s (main.py)": pp.ema_irregular(t, v, 10),
        "EMA tau=30 s": pp.ema_irregular(t, v, 30),
        "Mediana 61 s": pp.mediana_movil(v, 61),
        "Butterworth fc=1/60 Hz (filtfilt)": pp.paso_bajo(v, FS, pp.FC_VELOCIDAD),
    }


COLORES = [NARANJA, AMARILLO, AQUA, AZUL]


def fig_espectros(acts):
    fig, axs = plt.subplots(1, 3, figsize=(11, 3), sharex=True)
    for nombre, d in acts.items():
        u = pp.remuestrear(pp.limpiar(d), FS)
        for ax, col in zip(axs, ["speed_kmh", "heartrate", "altitude"]):
            f, p = pp.espectro(u[col].to_numpy(), FS, nperseg=1024)
            ax.loglog(f[1:], p[1:], lw=0.9, label=nombre)
    titulos = ["Velocidad", "Frecuencia cardiaca", "Altitud"]
    cortes = [pp.FC_VELOCIDAD, pp.FC_FC, pp.FC_ALTITUD]
    for ax, ti, fc in zip(axs, titulos, cortes):
        ax.axvline(fc, color=ROJO, ls="--", lw=1)
        ax.axvline(1 / 8, color=TINTA, ls=":", lw=1)
        ax.set(title=f"PSD {ti}", xlabel="Frecuencia (Hz)")
        ax.text(fc * 1.1, ax.get_ylim()[0] * 3, f"fc=1/{1 / fc:.0f} Hz", color=ROJO, fontsize=7)
    axs[0].text(1 / 8 * 1.05, axs[0].get_ylim()[1] / 20, "Nyquist\nefectivo", fontsize=7, color=TINTA)
    axs[0].set_ylabel("PSD (unidades^2/Hz)")
    axs[0].legend(fontsize=6, ncol=1)
    fig.tight_layout()
    return guardar(fig, FIG / "h2_espectros.png")


def validacion_filtros(n=20):
    """Error y retardo de cada filtro frente a la velocidad 'verdadera' de
    sesiones sinteticas de series (escalones de ritmo conocidos)."""
    filas = []
    for s in range(n):
        d, cambios = sy.generar(sy.plan_series(), semilla=s)
        u = pp.remuestrear(pp.limpiar(d), FS)
        t = u["time"].to_numpy()
        plan = sy.plan_series()
        lim = np.cumsum([p[0] for p in plan])
        verdad = np.array([p[1] for p in plan])[np.searchsorted(lim, t, side="right").clip(0, len(plan) - 1)]
        for nombre, y in filtros(t, u["speed_kmh"].to_numpy()).items():
            # retardo = desplazamiento que maximiza la correlacion con la verdad
            lags = np.arange(-30, 31)
            r = [np.corrcoef(np.roll(y, -L)[60:-60], verdad[60:-60])[0, 1] for L in lags]
            filas.append({"filtro": nombre, "RMSE (km/h)": np.sqrt(np.mean((y - verdad)[60:-60] ** 2)),
                          "retardo (s)": lags[int(np.argmax(r))]})
    filas += [{"filtro": "Sin filtrar", "RMSE (km/h)": np.nan, "retardo (s)": 0}]
    return pd.DataFrame(filas).groupby("filtro", sort=False).mean().round(2)


def fig_filtros(acts):
    fig, axs = plt.subplots(2, 1, figsize=(10, 5.5))
    # sintetico: con verdad conocida
    d, _ = sy.generar(sy.plan_series(), semilla=1)
    u = pp.remuestrear(pp.limpiar(d), FS)
    t = u["time"].to_numpy()
    plan = sy.plan_series()
    lim = np.cumsum([p[0] for p in plan])
    verdad = np.array([p[1] for p in plan])[np.searchsorted(lim, t, side="right").clip(0, len(plan) - 1)]
    m = (t > 500) & (t < 1200)
    ax = axs[0]
    ax.plot(t[m] / 60, u["speed_kmh"][m], color=GRIS, lw=0.7, label="medida (sintetica)")
    ax.plot(t[m] / 60, verdad[m], color="k", lw=1.5, ls="--", label="verdad")
    for (nom, y), c in zip(filtros(t, u["speed_kmh"].to_numpy()).items(), COLORES):
        ax.plot(t[m] / 60, y[m], color=c, lw=1.4, label=nom)
    ax.set(title="Sesion sintetica de series: respuesta de cada filtro a los escalones",
           ylabel="Velocidad (km/h)")
    ax.legend(fontsize=7, ncol=3, loc="lower center")
    # real
    d = acts["2026-01-15"]
    u = pp.remuestrear(pp.limpiar(d), FS)
    t = u["time"].to_numpy()
    m = (t > 1200) & (t < 2400)
    ax = axs[1]
    ax.plot(t[m] / 60, u["speed_kmh"][m], color=GRIS, lw=0.7, label="velocidad remuestreada")
    for (nom, y), c in zip(filtros(t, u["speed_kmh"].to_numpy()).items(), COLORES):
        ax.plot(t[m] / 60, y[m], color=c, lw=1.4, label=nom)
    ax.set(title="Actividad real 15/01 (min 20-40)", xlabel="Tiempo (min)", ylabel="Velocidad (km/h)")
    fig.tight_layout()
    return guardar(fig, FIG / "h2_comparativa_filtros.png")


def fig_limpieza(acts):
    fig, axs = plt.subplots(1, 3, figsize=(11, 3))
    d = acts["2026-01-09"]
    l = pp.limpiar(d)
    u = pp.preprocesar(d)
    ax = axs[0]
    m = d["time"] < 240
    ax.plot(d["time"][m], d["speed_kmh"][m], "o-", color=GRIS, ms=3, lw=0.7, label="original")
    mu = u["time"] < 240
    ax.plot(u["time"][mu], u["speed_kmh"][mu], color=AZUL, lw=1, label="limpia + remuestreo")
    ax.plot(u["time"][mu], u["v_filt"][mu], color=NARANJA, lw=1.6, label="filtrada")
    ax.set(ylim=(0, 25), title="(a) Outliers de velocidad (09/01)", xlabel="Tiempo (s)",
           ylabel="Velocidad (km/h)")
    ax.legend(fontsize=7)
    ax = axs[1]
    ax.plot(d["time"] / 60, d["distance"] / 1000, color=GRIS, label="Strava")
    ax.plot(l["time"] / 60, l["distance_corr"] / 1000, color=AZUL, label="corregida")
    ax.set(xlim=(0, 3), ylim=(0, 0.7), title="(b) Distancia acumulada (09/01)", xlabel="Tiempo (min)",
           ylabel="Distancia (km)")
    ax.legend(fontsize=7)
    d = acts["2026-01-07"]
    u = pp.preprocesar(d)
    ax = axs[2]
    m = d["time"] < 400
    ax.plot(d["time"][m], d["heartrate"][m], "o-", color=GRIS, ms=3, lw=0.7, label="original")
    mu = u["time"] < 400
    ax.plot(u["time"][mu], u["heartrate"][mu], color=AZUL, lw=1, label="meseta interpolada")
    ax.plot(u["time"][mu], u["fc_filt"][mu], color=NARANJA, lw=1.6, label="filtrada (1/30 Hz)")
    ax.set(title="(c) Meseta de FC (07/01)", xlabel="Tiempo (s)", ylabel="FC (ppm)")
    ax.legend(fontsize=7)
    fig.tight_layout()
    return guardar(fig, FIG / "h2_limpieza.png")


def fig_altitud(acts):
    d = acts["2026-01-15"]
    u = pp.preprocesar(d)
    fig, ax = plt.subplots(figsize=(10, 2.8))
    ax.plot(u["time"] / 60, u["altitude"], color=GRIS, lw=0.8, label="remuestreada")
    ax.plot(u["time"] / 60, u["alt_filt"], color=VIOLETA, lw=1.5, label="filtrada (1/60 Hz)")
    ax.set(title="Altitud 15/01", xlabel="Tiempo (min)", ylabel="Altitud (m)")
    ax.legend(fontsize=7)
    return guardar(fig, FIG / "h2_altitud.png")


def tabla_desnivel(acts):
    filas = []
    for nombre, d in acts.items():
        u = pp.preprocesar(d)
        bruto = np.sum(np.clip(np.diff(d["altitude"]), 0, None))
        filas.append({"Actividad": nombre,
                      "Suma dh>0 bruta (m)": round(bruto, 1),
                      "Filtrada, sin histeresis (m)": round(np.sum(np.clip(np.diff(u["alt_filt"]), 0, None)), 1),
                      "Filtrada + histeresis 1 m (m)": round(cr.desnivel(u["alt_filt"].to_numpy())[0], 1)})
    return pd.DataFrame(filas)


def tabla_ruido(acts):
    filas = []
    for nombre, d in acts.items():
        l = pp.limpiar(d)
        v = l["speed_kmh"].dropna().to_numpy()
        r = (v - pp.mediana_movil(v, 15))[30:-30]
        filas.append({"Actividad": nombre, "sigma residuo (km/h)": round(r.std(), 2),
                      "autocorrelacion lag 1": round(np.corrcoef(r[:-1], r[1:])[0, 1], 2),
                      "Distancia Strava (m)": round(d["distance"].iloc[-1]),
                      "Distancia corregida (m)": round(l["distance_corr"].iloc[-1])})
    return pd.DataFrame(filas)


def main():
    acts = carga.cargar_todas()
    fig_espectros(acts)
    fig_filtros(acts)
    fig_limpieza(acts)
    fig_altitud(acts)
    tv = validacion_filtros()
    texto = ["## Validacion de filtros (20 sesiones sinteticas)\n", tv.to_markdown(), "\n",
             "## Ruido de la velocidad y correccion de distancia\n",
             tabla_ruido(acts).to_markdown(index=False), "\n",
             "## Desnivel positivo segun el tratamiento\n",
             tabla_desnivel(acts).to_markdown(index=False), "\n"]
    (SALIDA / "resultados.md").write_text("\n".join(texto), encoding="utf-8")
    print("\n".join(texto))


if __name__ == "__main__":
    main()
