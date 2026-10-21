from bokeh.io import output_file, save  
from bokeh.layouts import column, row
from bokeh.models import Slider, CheckboxGroup, ColumnDataSource
from bokeh.plotting import figure, curdoc
from bokeh.palettes import Category10
import numpy as np
import itertools

# Parámetros iniciales
fs = 500  # Frecuencia de muestreo para la señal original
T = 1  # Duración total de la señal en segundos
frequencies = [1, 2, 3]  # Frecuencias de las componentes armónicas
initial_Ts = 0.05  # Periodo de muestreo inicial

# Generar la señal original
def generate_signal(frequencies, t):
    return sum(np.sin(2 * np.pi * f * t) for f in frequencies)

t = np.linspace(0, T, int(fs * T))
signal = generate_signal(frequencies, t)

# Muestreo de la señal
def sample_signal(t, signal, Ts):
    indices = np.arange(0, len(t), int(Ts * fs))
    return t[indices], signal[indices]

sampled_t, sampled_signal = sample_signal(t, signal, initial_Ts)

# Reconstrucción ideal
def reconstruct_ideal(t, sampled_t, sampled_signal, Ts):
    components = [si * np.sinc((t - ti) / Ts) for ti, si in zip(sampled_t, sampled_signal)]
    reconstructed = sum(components)
    return reconstructed, components

# Reconstrucción con retenedor de orden cero
def reconstruct_zoh(t, sampled_t, sampled_signal):
    reconstructed = np.zeros_like(t)
    for i in range(len(sampled_t) - 1):
        mask = (t >= sampled_t[i]) & (t < sampled_t[i + 1])
        reconstructed[mask] = sampled_signal[i]
    reconstructed[t >= sampled_t[-1]] = sampled_signal[-1]
    return reconstructed

reconstructed_ideal, components_ideal = reconstruct_ideal(t, sampled_t, sampled_signal, initial_Ts)
reconstructed_zoh = reconstruct_zoh(t, sampled_t, sampled_signal)

# Crear fuentes de datos
source_continuous = ColumnDataSource(data={"t": t, "signal": signal})
source_sampled = ColumnDataSource(data={"sampled_t": sampled_t, "sampled_signal": sampled_signal})
source_reconstructed = ColumnDataSource(data={
    "t": t,
    "reconstructed_ideal": reconstructed_ideal,
    "reconstructed_zoh": reconstructed_zoh,
})
for i, c in enumerate(components_ideal):
    source_reconstructed.data[f"reconstructed_ideal_{i}"] = c

# Figura 1: Señal original y muestreada 
plot1 = figure(title="Señal Original (f1=1, f2=3, f3=6) y Muestreada", width=800, height=300)
plot1.line("t", "signal", source=source_continuous, color="blue", legend_label="Señal Original")
plot1.scatter("sampled_t", "sampled_signal", source=source_sampled, color="red", size=6, legend_label="Señal muestreada")
plot1.legend.click_policy = "hide"

# Figura 2: Señal muestreada y reconstrucciones
plot2 = figure(title="Retenedor ideal", width=800, height=300)
plot2.line("t", "signal", source=source_continuous, color="blue", legend_label="Señal original")
plot2.scatter("sampled_t", "sampled_signal", source=source_sampled, color="red", size=6, legend_label="Señal muestreada")
plot2.line("t", "reconstructed_ideal", source=source_reconstructed, color="red", line_width=2, legend_label="Reconstrucción Ideal")
for i, c in enumerate(components_ideal):
    plot2.line("t", f"reconstructed_ideal_{i}", source=source_reconstructed, color=Category10[10][i%10], line_width=2, line_dash="dashed", legend_label=f"reconstructed_ideal_{i}")
plot2.legend.visible = False
plot2.x_range.start = 0
plot2.x_range.end = T

# Figura 2: Señal muestreada y reconstrucciones
plot3 = figure(title="Retenedor de orden cero", width=800, height=300)
plot3.line("t", "signal", source=source_continuous, color="blue", legend_label="Señal original")
plot3.scatter("sampled_t", "sampled_signal", source=source_sampled, color="red", size=6, legend_label="Señal muestreada")
plot3.line("t", "reconstructed_zoh", source=source_reconstructed, color="red", line_width=2, legend_label="Retenedor de orden cero")
plot3.legend.click_policy = "hide"
plot3.x_range.start = 0
plot3.x_range.end = T

# Slider para el periodo de muestreo
slider = Slider(start=0.01, end=0.3, value=initial_Ts, step=0.01, title="Periodo de muestreo (Ts)", sizing_mode="stretch_width")

# Actualizar las señales
def update(attr, old, new):
    Ts = slider.value
    sampled_t, sampled_signal = sample_signal(t, signal, Ts)
    reconstructed_ideal, components_ideal = reconstruct_ideal(t, sampled_t, sampled_signal, Ts)
    reconstructed_zoh = reconstruct_zoh(t, sampled_t, sampled_signal)

    source_sampled.data = {"sampled_t": sampled_t, "sampled_signal": sampled_signal}
    source_reconstructed.data = {
        "t": t,
        "reconstructed_ideal": reconstructed_ideal,
        "reconstructed_zoh": reconstructed_zoh,
    }
    for i, c in enumerate(components_ideal):
        source_reconstructed.data[f"reconstructed_ideal_{i}"] = c

slider.on_change("value", update)

# Disposición
layout = column(plot1, plot3, plot2, slider)
curdoc().add_root(layout)
curdoc().title = "PdS - Reconstrucción de señales.html"
