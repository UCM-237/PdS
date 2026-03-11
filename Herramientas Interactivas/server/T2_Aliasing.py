from bokeh.io import curdoc, output_file, save
from bokeh.layouts import column, row
from bokeh.plotting import figure
from bokeh.models import Slider, ColumnDataSource, CheckboxGroup
import numpy as np

# Inicializar valores predeterminados
x = np.linspace(0, 2 * np.pi, 1000)
freq1, freq2, freq3 = 0.5, 2.5, 4.5
Ts = 0.5  # Periodo de muestreo inicial

# Señales iniciales
y1 = np.sin(2 * np.pi * freq1 * x)
y2 = np.sin(2 * np.pi * freq2 * x)
y3 = np.sin(2 * np.pi * freq3 * x)

# Datos muestreados
t_sampled = np.arange(0, 2 * np.pi, Ts)
y1_sampled = np.sin(2 * np.pi * freq1 * t_sampled)

# Crear ColumnDataSource para datos continuos
source_continuous = ColumnDataSource(data={
    'x': x, 'y1': y1, 'y2': y2, 'y3': y3
})

# Crear ColumnDataSource para datos muestreados
source_sampled = ColumnDataSource(data={
    't_sampled': t_sampled, 'y1_sampled': y1_sampled
})

# Crear figura
plot = figure(title="Señales Senoidales Interactivas", width=800, height=400)
line1 = plot.line('x', 'y1', source=source_continuous, legend_label="Señal 1", line_width=2, color="blue")
line2 = plot.line('x', 'y2', source=source_continuous, legend_label="Señal 2", line_width=2, color="green")
line3 = plot.line('x', 'y3', source=source_continuous, legend_label="Señal 3", line_width=2, color="red")
scatter = plot.scatter('t_sampled', 'y1_sampled', source=source_sampled, size=8, color="black", legend_label="Muestreo de Señal 1")
plot.legend.location = "bottom_right"
plot.legend.click_policy = "hide"
plot.xaxis.axis_label = "Tiempo"
plot.yaxis.axis_label = "Amplitud"

# Sliders
slider_freq1 = Slider(start=0.1, end=10, value=freq1, step=0.1, title="Frecuencia Señal 1")
slider_freq2 = Slider(start=0.1, end=10, value=freq2, step=0.1, title="Frecuencia Señal 2")
slider_freq3 = Slider(start=0.1, end=10, value=freq3, step=0.1, title="Frecuencia Señal 3")
slider_Ts = Slider(start=0.1, end=1, value=Ts, step=0.01, title="Periodo de Muestreo Ts")

# Checkbox
checkbox = CheckboxGroup(labels=["Señal 1", "Señal 2", "Señal 3", "Muestreo Señal 1"], active=[0, 1, 2, 3])

# Callback para actualizar datos
def update_data(attr, old, new):
    freq1 = slider_freq1.value
    freq2 = slider_freq2.value
    freq3 = slider_freq3.value
    Ts = slider_Ts.value

    # Recalcular señales
    y1 = np.sin(2 * np.pi * freq1 * x)
    y2 = np.sin(2 * np.pi * freq2 * x)
    y3 = np.sin(2 * np.pi * freq3 * x)

    # Recalcular muestreo
    t_sampled = np.arange(0, 2 * np.pi, Ts)
    y1_sampled = np.sin(2 * np.pi * freq1 * t_sampled)

    # Actualizar ColumnDataSource
    source_continuous.data = {
        'x': x, 'y1': y1, 'y2': y2, 'y3': y3
    }
    source_sampled.data = {
        't_sampled': t_sampled, 'y1_sampled': y1_sampled
    }

def update_visibility(attr, old, new):
    line1.visible = 0 in checkbox.active
    line2.visible = 1 in checkbox.active
    line3.visible = 2 in checkbox.active
    scatter.visible = 3 in checkbox.active

# Asociar sliders con callback
slider_freq1.on_change('value', update_data)
slider_freq2.on_change('value', update_data)
slider_freq3.on_change('value', update_data)
slider_Ts.on_change('value', update_data)
checkbox.on_change('active', update_visibility)

# Layout
layout = column(
    row(
      column(slider_freq1, slider_freq2, slider_freq3, slider_Ts),
    #   checkbox,
      plot,
    ),
)

# Añadir al documento
curdoc().add_root(layout)
curdoc().title = "PdS - Aliasing"