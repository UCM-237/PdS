import pandas as pd
import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import Div, Range1d, LinearAxis, ColumnDataSource, Slider, Span
from bokeh.plotting import figure

APP_NAME = "Entrenamiento"

df = pd.read_csv("entrenamiento/data/data_2026-01-15T13:56:08Z.csv")

header = Div(
  text=f"""
  <div style="
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 15px;
  ">
    <img src="{APP_NAME.lower()}/static/icon.png" width="48" height="48">
    <div>
      <h1 style="margin: 0; font-size: 22px;">Training Analytics</h1>
      <p style="margin: 0; color: #666;">
        Efficient insight from your data
      </p>
    </div>
  </div>
  """,
  sizing_mode="stretch_width"
)
favicon = Div(
  text=f"""
  <link rel="icon" type="image/png" href="{APP_NAME.lower()}/static/icon.png">
  """
)


def ema_irregular(t, x, tau):
  """
  EMA (Exponential Moving Average) para muestreo no periódico.

  Parámetros:
  -----------
  t : array-like
    Tiempos de cada muestra (en segundos). Debe estar ordenado.
  x : array-like
    Señal a filtrar.
  tau : float
    Constante de tiempo del filtro (en segundos).

  Retorna:
  --------
  y : np.ndarray
    Señal suavizada.
  """
  t = np.asarray(t)
  x = np.asarray(x)
  y = np.zeros_like(x, dtype=float)

  if len(x) == 0:
    return y

  # Inicializamos con el primer valor
  y[0] = x[0]

  for k in range(1, len(x)):
    dt = t[k] - t[k-1]
    if dt < 0:
      raise ValueError("El vector de tiempos debe estar ordenado de manera creciente")
    # Coeficiente exacto
    alpha = 1 - np.exp(-dt / tau)
    # EMA discreta exacta
    y[k] = alpha * x[k] + (1 - alpha) * y[k-1]

  return y


def mean_t(t, x) -> np.ndarray:
  """
  Calcula la media ponderada en el tiempo para muestreo no periódico.
  """
  t = np.asarray(t)
  x = np.asarray(x)
  m = 0
  T = t[-1] - t[0]
  T = T if T else 1
  for k in range(len(x)):
    m = m + x[k]*(t[k] - t[k-1])/T

  return m


def derivative(t, x):
  t = np.asarray(t)
  x = np.asarray(x)

  dxdt = np.zeros_like(x, dtype=float)
  dxdt[0] = 0.0

  for k in range(1, len(x)):
    dt = t[k] - t[k-1]
    dxdt[k] = (x[k] - x[k-1]) / dt

  return dxdt


def detect_pace_changes(t, v_smooth, threshold_factor=3.5):
  """
  Detecta cambios de ritmo usando derivada + umbral adaptativo.

  Parámetros
  ----------
  t : array-like
    Tiempo (s)
  v_smooth : array-like
    Velocidad suavizada (km/h o m/s)
  threshold_factor : float
    Multiplicador del umbral (típico: 2–4)

  Retorna
  -------
  change_indices : list[int]
    Índices donde se detectan cambios
  """
  dvdt = derivative(t, v_smooth)
  # Umbral robusto usando MAD
  mad = np.median(np.abs(dvdt - np.median(dvdt)))
  threshold = threshold_factor * mad
  change_indices = np.where(np.abs(dvdt) > threshold)[0]
  return change_indices, dvdt, threshold



def plot_vs_distance(data: ColumnDataSource):
  p = figure(
    height=350,
    sizing_mode="stretch_width",
    title="Speed and Heart Rate vs Distance",
    tools="pan,wheel_zoom,box_zoom,reset"
  )
  p.line(
    x="distance_km",
    y="speed_kmh",
    source=data,
    line_width=2,
    legend_label="Speed (km/h)"
  )
  p.extra_y_ranges = {
    "hr": Range1d(start=60, end=190)
  }
  p.add_layout(LinearAxis(y_range_name="hr", axis_label="HR (bpm)"), "right")
  p.line(
    x="distance_km",
    y="heartrate",
    source=data,
    y_range_name="hr",
    line_color="firebrick",
    line_width=2,
    legend_label="HR (bpm)"
  )
  p.xaxis.axis_label = "Distance (km)"
  p.yaxis.axis_label = "Speed (km/h)"
  p.legend.location = "top_left"
  return p


def plot_vs_time(data: ColumnDataSource):
  p = figure(
    height=350,
    sizing_mode="stretch_width",
    title="Speed and Heart Rate vs Time",
    tools="pan,wheel_zoom,box_zoom,reset",
    y_range=Range1d(start=0, end=35),
  )
#   p.extra_y_ranges = {
#     "hr": Range1d(start=60, end=190)
#   }
#   p.add_layout(LinearAxis(y_range_name="hr", axis_label="HR (bpm)"), "right")
  p.line(
    x="time",
    y="speed_kmh",
    source=data,
    line_width=2,
    legend_label="Speed (km/h)"
  ) 
  p.line(
    x="time",
    y="speed_kmh_filtered",
    source=data,
    line_color="red",
    line_width=2,
    legend_label="Speed (km/h)"
  ) 
  p.line(
    x="time",
    y="speed_kmh_derivative",
    source=data,
    line_color="green",
    line_width=2,
    legend_label="Accel (km/h2)"
  ) 
  p.line(
    x="time",
    y="speed_segment_mean",
    source=data,
    line_color="magenta",
    line_width=2,
    legend_label="Speed segment mean"
  )
  p.multi_line(
    xs="x",
    ys="y",
    source=change_source,
    line_color="gray",
    line_dash="dashed",
    line_alpha=0.8
  )

#   p.line(
#     x="time",
#     y="heartrate",
#     source=data,
#     y_range_name="hr",
#     line_color="firebrick",
#     line_width=2,
#     legend_label="HR (bpm)"
#   )

  p.xaxis.axis_label = "Time (s)"
  p.yaxis.axis_label = "Speed (km/h)"
  p.legend.location = "top_left"
  return p


def get_segment_mean(t, segment_t, segment_m):
  M = len(t)
  N = len(segment_m)
  i = 0 
  m = np.zeros((M,1))
  for j, ts in enumerate(t):
    while i < (N-1) and ts < segment_t[i]:
      i = i + 1
    m[j] = segment_m[i]
  return m


def pace_change_pipeline(t, v, tau=10.0, threshold_factor=3.5):
    """
    Pipeline completo para detección de cambios de ritmo.

    Retorna
    -------
    v_smooth : np.ndarray
        Velocidad suavizada
    dvdt : np.ndarray
        Derivada temporal
    change_indices : np.ndarray
        Índices de cambio detectados
    """
    # 1) Suavizado
    v_smooth = ema_irregular(t, v, tau)
    # 2) Detección
    change_indices, dvdt, threshold = detect_pace_changes(t, v_smooth, threshold_factor)
    idx = np.concatenate(([0], change_indices))
    segment_means = [mean_t(t[idx[i]:idx[i+1]], v[idx[i]:idx[i+1]]) for i in range(len(idx)-1)]
    return v_smooth, dvdt, change_indices, segment_means

# MAIN
v_smooth, dvdt, change_idx, segment_means = pace_change_pipeline(
  df["time"],
  df["speed_kmh"],
  tau=10.0,
  threshold_factor=5.0
)
df["speed_kmh_filtered"] = v_smooth
df["speed_kmh_derivative"] = dvdt
data_source = ColumnDataSource(data=df)
change_times = df["time"][change_idx].to_list()
change_source = ColumnDataSource(dict(
  x=[[df["time"], df["time"]] for t in change_times],
  y=[[0, 30] for _ in change_times]
))
data_source.data["speed_segment_mean"] = get_segment_mean(data_source.data["time"], change_times, segment_means)
tau_slider = Slider(title="EMA τ (s)", start=1, end=120, value=30)
threshold_slider = Slider(title="MAD threshold", start=1, end=10, value=3.0, step=0.1)
p1 = plot_vs_distance(data=data_source)
p2 = plot_vs_time(data=data_source)

def update_tau(attr, old, new):
  tau = tau_slider.value
  threshold = threshold_slider.value
  v_smooth, dvdt, change_idx, segment_means = pace_change_pipeline(
    data_source.data["time"],
    data_source.data["speed_kmh"],
    tau=tau,
    threshold_factor=threshold
  )
  data_source.data["speed_kmh_filtered"] = v_smooth
  data_source.data["speed_kmh_derivative"] = dvdt
  change_times = data_source.data["time"][change_idx]
  change_source.data = dict(
    x=[[t, t] for t in change_times],
    y=[[0, 30] for _ in change_times],
  )
  data_source.data["speed_segment_mean"] = get_segment_mean(data_source.data["time"], change_times, segment_means)

tau_slider.on_change("value", update_tau)
threshold_slider.on_change("value", update_tau)

layout = column(
    header,
    tau_slider,
    threshold_slider,
    p1,
    p2,
    sizing_mode="stretch_width"
)

curdoc().title = APP_NAME
curdoc().add_root(layout)
curdoc().add_root(favicon)
