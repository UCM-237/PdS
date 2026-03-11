import numpy as np
from scipy.signal import firwin, freqz, windows
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, RadioButtonGroup
from bokeh.plotting import figure

# Configuración inicial
window_length = 64
window_type = 'rectangular'

# Funciones para generar las ventanas y los filtros
def get_window(window_length, window_type):
    if window_type == 'rectangular':
        return np.ones(window_length)
    elif window_type == 'hann':
        return windows.hann(window_length)
    elif window_type == 'bartlett':
        return windows.bartlett(window_length)
    else:
        return np.ones(window_length)

def design_fir_filter(window_length, cutoff, window_type):
    window = get_window(window_length, window_type)
    coeffs = firwin(window_length, cutoff, window=window_type, scale=False)
    return coeffs, window

# Fuentes de datos para las gráficas
source_time = ColumnDataSource(data=dict(x=[], y=[]))
source_freq = ColumnDataSource(data=dict(x=[], y=[]))
source_ideal = ColumnDataSource(data=dict(x=[], y=[]))
source_window = ColumnDataSource(data=dict(x=[], y=[]))

# Configuración de las gráficas
plot_time = figure(title="Ventana en el dominio del tiempo", width=800, height=300, x_range=(-64, 64))
plot_time.scatter('x', 'y', source=source_time, line_width=1)

plot_freq = figure(title="Respuesta en frecuencia", width=800, height=300, x_range=(-np.pi, np.pi))
# plot_freq.line('x', 'y', source=source_freq, line_width=2, legend_label="Ventana")
# plot_freq.line('x', 'y', source=source_ideal, line_width=1, line_color="red", legend_label="Ideal")
plot_freq.scatter('x', 'y', source=source_window, line_width=1, line_color="navy") #, legend_label="ventana")

# Controles
window_length_slider = Slider(title="Longitud de la ventana", value=64, start=16, end=128, step=16)
window_type_radio = RadioButtonGroup(labels=["Rectangular", "Hanning", "Bartlett"], active=0)

# Callback para actualizar las gráficas
def update(attr, old, new):
    window_length = window_length_slider.value
    window_type = ['rectangular', 'hann', 'bartlett'][window_type_radio.active]
    
    # Diseñar el filtro FIR
    coeffs, window = design_fir_filter(window_length, 0.5, window_type)
    
    # Actualizar la gráfica del dominio del tiempo
    x_time = np.arange(window_length)
    source_time.data = dict(x=x_time-window_length/2, y=window)
    
    # Calcular la respuesta en frecuencia del filtro FIR
    w, h = freqz(coeffs, worN=8000)
    source_freq.data = dict(x=w, y=np.abs(h))
    
    # Calcular la respuesta en frecuencia de la ventana
    wh = np.fft.fftshift(np.fft.fftfreq(8000,d=1/2/np.pi))
    h = np.fft.fftshift(np.fft.fft(window, 8000))
    source_window.data = dict(x=wh, y=np.abs(h)/np.max(np.abs(h)))

    # Calcular la respuesta en frecuencia del filtro ideal
    ideal_h = np.zeros_like(w)
    ideal_h[w <= np.pi * 0.5] = 1
    source_ideal.data = dict(x=w, y=ideal_h)

# Asignar el callback a los controles
window_length_slider.on_change('value', update)
window_type_radio.on_change('active', update)

# Inicializar la interfaz
update(None, None, None)

# Diseño de la interfaz
controls = column(window_length_slider, window_type_radio)
layout = column(plot_time, plot_freq, controls)

# Añadir el diseño al documento
curdoc().add_root(layout)