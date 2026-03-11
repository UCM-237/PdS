import numpy as np
from bokeh.plotting import figure, show
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource
from bokeh.io import curdoc, output_file, save

# Definir las funciones de los retenedores
def ideal_impulse_response(t):
    return np.sinc(t)

def zero_order_hold_impulse_response(t):
    return np.where((t >= 0.0) & (t <= 1), 1, 0)

def first_order_causal_impulse_response(t):
    return np.where((t >= 0) & (t < 1), 1 + t, 0) + np.where((t >= 1) & (t <= 2), 1 - t, 0)

def first_order_non_causal_impulse_response(t):
    return np.where((t >= -1) & (t <= 1), 1 - np.abs(t), 0)

# Definir las funciones de respuesta en frecuencia
def ideal_frequency_response(f):
    return np.where(np.abs(f) <= 0.5, 1, 0)

def zero_order_hold_frequency_response(f):
    return np.abs(np.sinc(f))

def first_order_causal_frequency_response(f):
    return np.sqrt(1 + (2 * np.pi * f)**2) * np.sinc(f)**2

def first_order_non_causal_frequency_response(f):
    return np.sinc(f)**2

# Crear los datos para las gráficas
t = np.linspace(-5, 5, 1000)
f = np.linspace(-2, 2, 1000)

ideal_ir = ideal_impulse_response(t)
zero_order_ir = zero_order_hold_impulse_response(t)
first_order_causal_ir = first_order_causal_impulse_response(t)
first_order_non_causal_ir = first_order_non_causal_impulse_response(t)

ideal_fr = ideal_frequency_response(f)
zero_order_fr = zero_order_hold_frequency_response(f)
first_order_causal_fr = first_order_causal_frequency_response(f)
first_order_non_causal_fr = first_order_non_causal_frequency_response(f)

# Crear ColumnDataSource para las gráficas
source_ir = ColumnDataSource(data=dict(t=t, ideal_ir=ideal_ir, zero_order_ir=zero_order_ir,
                                      first_order_causal_ir=first_order_causal_ir,
                                      first_order_non_causal_ir=first_order_non_causal_ir))

source_fr = ColumnDataSource(data=dict(f=f, ideal_fr=ideal_fr, zero_order_fr=zero_order_fr,
                                      first_order_causal_fr=first_order_causal_fr,
                                      first_order_non_causal_fr=first_order_non_causal_fr))

# Crear las figuras
p_ir = figure(width=800, height=400, title="Respuesta al Impulso", x_axis_label='t', y_axis_label='Amplitud')
p_fr = figure(width=800, height=400, title="Respuesta en Frecuencia", x_axis_label='f', y_axis_label='Magnitud')

# Añadir las líneas a las figuras
l_ideal_ir = p_ir.line('t', 'ideal_ir', source=source_ir, line_width=2, color="blue", legend_label="Ideal")
l_zero_order_ir = p_ir.line('t', 'zero_order_ir', source=source_ir, line_width=2, color="red", legend_label="Orden Cero")
l_first_order_causal_ir = p_ir.line('t', 'first_order_causal_ir', source=source_ir, line_width=2, color="green", legend_label="Primer Orden Causal")
l_first_order_non_causal_ir = p_ir.line('t', 'first_order_non_causal_ir', source=source_ir, line_width=2, color="orange", legend_label="Primer Orden No Causal")

l_ideal_fr = p_fr.line('f', 'ideal_fr', source=source_fr, line_width=2, color="blue", legend_label="Ideal")
l_zero_order_fr = p_fr.line('f', 'zero_order_fr', source=source_fr, line_width=2, color="red", legend_label="Orden Cero")
l_first_order_causal_fr = p_fr.line('f', 'first_order_causal_fr', source=source_fr, line_width=2, color="green", legend_label="Primer Orden Causal")
l_first_order_non_causal_fr = p_fr.line('f', 'first_order_non_causal_fr', source=source_fr, line_width=2, color="orange", legend_label="Primer Orden No Causal")

p_ir.legend.click_policy = "hide"
p_ir.legend.location = "top_left"
p_fr.legend.click_policy = "hide"
p_fr.legend.location = "top_left"

# Organizar el layout
layout = row(p_ir, p_fr)

# Mostrar la aplicación
curdoc().add_root(layout)
curdoc.title = 'Retenedores'
output_file("../html/T2_Retenedores.html")
save(layout)
