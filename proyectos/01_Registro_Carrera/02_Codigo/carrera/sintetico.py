"""Sesiones sinteticas con eventos conocidos (verdad terreno) para validar los
detectores del Hito 4. Las registros reales no traen etiquetas, asi que la
unica forma de medir precision/sensibilidad es con senales en las que sabemos
donde estan los cambios.

El ruido imita al de los datos reales: residuo de la velocidad con desviacion
tipica ~1 km/h y autocorrelacion de lag 1 ~0.4 (medido en el Hito 2), muestreo
irregular con dt entre 2 y 6 s, algun pico de GPS y un hueco.
"""
import numpy as np
import pandas as pd


def plan_series(n_reps=6, t_rapido=120, t_lento=60, v_rapido=14.5, v_lento=8.5,
                t_cal=600, v_cal=10.0, t_vc=300, v_vc=9.0, t_andar=120, v_andar=5.0):
    """Lista de (duracion_s, velocidad_kmh) de una sesion de series."""
    plan = [(t_cal, v_cal)]
    for i in range(n_reps):
        plan.append((t_rapido, v_rapido))
        plan.append((t_lento, v_lento if i < n_reps - 1 else v_vc))
    plan[-1] = (t_lento + t_vc, v_vc)
    plan.append((t_andar, v_andar))
    return plan


def plan_rodaje(duracion=2400, v=10.0, t_andar=120, v_andar=5.0):
    return [(duracion, v), (t_andar, v_andar)]


def generar(plan, sigma=1.0, rho=0.4, n_picos=1, hueco=True, semilla=0):
    """Genera un DataFrame con el mismo formato que los CSV de Strava.

    Devuelve (df, cambios_s) donde ``cambios_s`` son los instantes reales de
    cambio de ritmo.
    """
    rng = np.random.default_rng(semilla)
    dur = np.array([p[0] for p in plan], float)
    vel = np.array([p[1] for p in plan], float)
    cambios = np.cumsum(dur)[:-1]
    T = dur.sum()

    # muestreo irregular
    t = [0.0]
    while t[-1] < T:
        t.append(t[-1] + rng.integers(2, 7))
    t = np.array(t[:-1])
    if hueco:  # hueco de 30 s en el ultimo cuarto
        k = np.searchsorted(t, 0.8 * T)
        t = np.r_[t[:k], t[k + 8:]]

    v_ideal = vel[np.searchsorted(np.cumsum(dur), t, side="right").clip(0, len(vel) - 1)]
    # transicion suave (aceleracion finita, ~5 s)
    v_ideal = pd.Series(v_ideal).rolling(2, min_periods=1).mean().to_numpy()
    e = np.zeros(len(t))
    w = rng.normal(0, sigma * np.sqrt(1 - rho ** 2), len(t))
    for k in range(1, len(t)):
        e[k] = rho * e[k - 1] + w[k]
    v = np.clip(v_ideal + e, 0, None)
    for k in rng.integers(10, len(t) - 10, n_picos):
        v[k] += rng.uniform(25, 45)  # salto de GPS

    # FC: respuesta de 1er orden (tau = 40 s) a la intensidad + deriva lenta
    fc = np.empty(len(t))
    fc[0] = 85
    for k in range(1, len(t)):
        objetivo = 60 + 7.0 * v_ideal[k] + 0.002 * t[k]
        a = 1 - np.exp(-(t[k] - t[k - 1]) / 40)
        fc[k] = fc[k - 1] + a * (objetivo - fc[k - 1])
    fc = np.round(fc + rng.normal(0, 1.0, len(t)))

    dist = np.r_[0.0, np.cumsum(0.5 * (v[1:] + v[:-1]) / 3.6 * np.diff(t))]
    alt = 604 + 3 * np.sin(2 * np.pi * dist / 2500) + rng.normal(0, 0.1, len(t))
    df = pd.DataFrame({"time": t, "distance": dist, "heartrate": fc,
                       "velocity": v / 3.6, "altitude": alt})
    df["speed_kmh"] = v
    df["distance_km"] = dist / 1000
    return df, cambios
