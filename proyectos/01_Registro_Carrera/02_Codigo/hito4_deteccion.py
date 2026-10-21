"""Hito 4: deteccion de estados y cambios de ritmo, clasificacion de sesiones
y validacion con senales sinteticas de verdad conocida."""
import numpy as np
import pandas as pd

from carrera import analisis, carga, deteccion as dt, preprocesado as pp, sintetico as sy
from carrera.graficas import (AZUL, COLOR_ESTADO, GRIS, NARANJA, ROJO, TINTA, guardar, plt)

SALIDA = carga.DIR_HITOS / "Hito_4_Clasificacion_o_Deteccion"
FIG = SALIDA / "figuras"
TOL_S = 20  # tolerancia para dar por acertado un cambio de ritmo

# Etiqueta asignada a mano mirando las graficas del Hito 1 (no la ve el clasificador)
ETIQUETA_MANUAL = {"2026-01-07": "Rodaje", "2026-01-09": "Tempo", "2026-01-11": "Tirada larga",
                   "2026-01-14": "Tempo", "2026-01-15": "Rodaje"}


def cambios_metodo_derivada(u):
    """Metodo de partida (main.py): EMA tau=10 s + |dv/dt| > 5*MAD."""
    t = u["time"].to_numpy()
    v = pp.ema_irregular(t, u["speed_kmh"].to_numpy(), 10)
    c, dv, umbral = dt.cambios_derivada(t, v, factor=5.0)
    n_bruto = int(np.sum(np.abs(dv) > umbral))
    return c, n_bruto


def sombrear_estados(ax, t_min, estados):
    for e, a, b in dt.tramos(estados):
        if e != dt.CORRIENDO:
            ax.axvspan(t_min[a], t_min[b], color=COLOR_ESTADO[e], alpha=0.45, lw=0)


def fig_sesiones(resultados):
    n = len(resultados)
    fig, axs = plt.subplots(n, 1, figsize=(10, 1.9 * n))
    for ax, (nombre, r) in zip(axs, resultados.items()):
        u, c = r["u"], r["cortes"]
        tm = (u["time"] / 60).to_numpy()
        sombrear_estados(ax, tm, r["estados"])
        ax.plot(tm, u["speed_kmh"], color=GRIS, lw=0.5)
        ax.plot(tm, u["v_filt"], color=AZUL, lw=1)
        ax.plot(tm, dt.medias_por_tramo(u["speed_kmh"].to_numpy(), c), color=NARANJA, lw=1.8)
        for k in c:
            ax.axvline(tm[k], color=TINTA, ls=":", lw=0.8)
        ax.set_ylim(0, 18)
        ax.set_ylabel("km/h")
        ax.set_title(f"{nombre}: {r['tipo']}  ({r['motivo']})", loc="left", fontsize=9)
    axs[-1].set_xlabel("Tiempo (min)")
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    leyenda = [Line2D([], [], color=GRIS, lw=0.8, label="velocidad"),
               Line2D([], [], color=AZUL, label="filtrada"),
               Line2D([], [], color=NARANJA, lw=1.8, label="media por tramo (seg. binaria)"),
               Line2D([], [], color=TINTA, ls=":", label="cambio de ritmo"),
               Patch(color=COLOR_ESTADO[1], alpha=0.45, label="andando"),
               Patch(color=COLOR_ESTADO[0], alpha=0.45, label="parado")]
    axs[0].legend(handles=leyenda, ncol=6, fontsize=7, loc="lower center", bbox_to_anchor=(0.5, 1.25))
    fig.tight_layout()
    return guardar(fig, FIG / "h4_sesiones_reales.png")


def fig_sintetica(semilla=3):
    d, verdad = sy.generar(sy.plan_series(), semilla=semilla)
    r = analisis.analizar(d)
    u = r["u"]
    tm = (u["time"] / 60).to_numpy()
    cd, n_bruto = cambios_metodo_derivada(u)
    fig, axs = plt.subplots(2, 1, figsize=(10, 4.6), sharex=True)
    for ax, cortes, titulo in [
            (axs[0], cd, f"(a) Derivada + MAD (main.py corregido): {len(cd)} cambios "
                         f"[sin agrupar: {n_bruto} muestras sobre el umbral]"),
            (axs[1], r["cortes"], f"(b) Segmentacion binaria: {len(r['cortes'])} cambios")]:
        sombrear_estados(ax, tm, r["estados"])
        ax.plot(tm, u["speed_kmh"], color=GRIS, lw=0.5)
        ax.plot(tm, dt.medias_por_tramo(u["speed_kmh"].to_numpy(), cortes), color=NARANJA, lw=1.6)
        for v in verdad:
            ax.axvline(v / 60, color=TINTA, ls="--", lw=0.8)
        ax.plot(tm[cortes], np.full(len(cortes), 17), "v", color=ROJO, ms=6)
        ax.set(ylim=(0, 19), ylabel="km/h")
        ax.set_title(titulo, loc="left", fontsize=9)
    axs[1].set_xlabel("Tiempo (min)  -  lineas discontinuas: cambios reales; triangulos: detectados")
    fig.tight_layout()
    return guardar(fig, FIG / "h4_validacion_sintetica.png")


def validacion(n=30):
    """Precision / sensibilidad de los dos detectores en sesiones sinteticas
    variadas (numero y duracion de repeticiones, nivel de ruido)."""
    filas = []
    rng = np.random.default_rng(123)
    for s in range(n):
        plan = sy.plan_series(n_reps=int(rng.integers(4, 9)), t_rapido=int(rng.choice([60, 120, 180, 240])),
                              t_lento=int(rng.choice([60, 90, 120])), v_rapido=float(rng.uniform(13, 16)),
                              v_lento=float(rng.uniform(7.5, 9.5)))
        sigma = float(rng.choice([0.5, 1.0, 1.5]))
        d, verdad = sy.generar(plan, sigma=sigma, semilla=s)
        r = analisis.analizar(d)
        t = r["u"]["time"].to_numpy()
        cd, _ = cambios_metodo_derivada(r["u"])
        for metodo, cortes in [("Derivada + MAD", t[cd]), ("Segmentacion binaria", t[r["cortes"]])]:
            m = dt.evaluar_detecciones(cortes, verdad, TOL_S)
            filas.append({"metodo": metodo, "sigma": sigma, **m})
    df = pd.DataFrame(filas)
    agg = df.groupby("metodo")[["TP", "FP", "FN"]].sum()
    agg["precision"] = agg["TP"] / (agg["TP"] + agg["FP"])
    agg["sensibilidad"] = agg["TP"] / (agg["TP"] + agg["FN"])
    agg["F1"] = 2 * agg["precision"] * agg["sensibilidad"] / (agg["precision"] + agg["sensibilidad"])
    agg["error medio (s)"] = df.groupby("metodo")["error_medio_s"].mean()
    por_ruido = df.groupby(["metodo", "sigma"])["F1"].mean().unstack().round(2)
    return agg.round(3), por_ruido


def clasificacion_sintetica(n=10):
    """Comprueba el clasificador de sesion en sinteticos de cada tipo."""
    filas = []
    for s in range(n):
        casos = {
            "Series": sy.plan_series(n_reps=4 + s % 4),
            "Rodaje": sy.plan_rodaje(duracion=2400 + 120 * s, v=9.5 + 0.1 * s),
            "Tirada larga": sy.plan_rodaje(duracion=5400 + 120 * s, v=10.0),
        }
        for real, plan in casos.items():
            d, _ = sy.generar(plan, semilla=100 + s)
            r = analisis.analizar(d)
            tipo, _ = dt.clasificar_sesion(r["resumen"], 10.2, r["resumen"]["n_repeticiones"])
            filas.append({"real": real, "predicho": tipo})
    df = pd.DataFrame(filas)
    return pd.crosstab(df["real"], df["predicho"])


def main():
    resultados = {n: analisis.analizar(d) for n, d in carga.cargar_todas().items()}
    v_ref = float(np.median([r["resumen"]["v_carrera_kmh"] for r in resultados.values()]))
    filas = []
    for nombre, r in resultados.items():
        res = r["resumen"]
        r["tipo"], r["motivo"] = dt.clasificar_sesion(res, v_ref, res["n_repeticiones"])
        u = r["u"]
        cd, n_bruto = cambios_metodo_derivada(u)
        andando = [(u["time"][a] / 60, u["time"][b] / 60) for e, a, b in dt.tramos(r["estados"]) if e != 2]
        filas.append({
            "Actividad": nombre,
            "Tramos andando/parado (min)": ", ".join(f"{a:.1f}-{b:.1f}" for a, b in andando) or "-",
            "Cambios ritmo (seg. binaria)": len(r["cortes"]),
            "Instantes (min)": ", ".join(f"{u['time'][k] / 60:.1f}" for k in r["cortes"]),
            "Cambios derivada+MAD": len(cd),
            "Muestras > umbral (main.py)": n_bruto,
            "Repeticiones": res["n_repeticiones"],
            "Clase": r["tipo"], "Etiqueta manual": ETIQUETA_MANUAL[nombre], "Motivo": r["motivo"],
        })
    tabla = pd.DataFrame(filas)
    fig_sesiones(resultados)
    fig_sintetica()
    val, por_ruido = validacion()
    conf = clasificacion_sintetica()
    texto = [f"Velocidad de referencia del atleta (mediana de v en carrera): {v_ref:.2f} km/h\n",
             "## Resultados sobre las sesiones reales\n", tabla.to_markdown(index=False), "\n",
             f"## Validacion de cambios de ritmo (30 sesiones sinteticas, tolerancia {TOL_S} s)\n",
             val.to_markdown(), "\n", "### F1 medio segun el ruido (sigma, km/h)\n",
             por_ruido.to_markdown(), "\n",
             "## Matriz de confusion del clasificador de sesion (30 sinteticas)\n",
             conf.to_markdown(), "\n"]
    (SALIDA / "resultados.md").write_text("\n".join(texto), encoding="utf-8")
    tabla.to_csv(SALIDA / "deteccion_sesiones.csv", index=False)
    print("\n".join(texto))
    return resultados


if __name__ == "__main__":
    main()
