import numpy as np
from bokeh.plotting import figure, output_file, save
from bokeh.layouts import row, column
from bokeh.models import Slider, ColumnDataSource, CustomJS, Spacer
from bokeh.io import curdoc

# Parámetros iniciales
fm = 1  # Frecuencia de la señal sinc
Ts_initial = 0.15  # Periodo de muestreo inicial
t = np.linspace(-2, 2, 10000)  # Dominio del tiempo
f = np.linspace(-10, 10, 10000)  # Dominio de la frecuencia

# Señal x(t) = sinc(fm * t)^2
x_t = np.sinc(fm * t)**2

# Transformada de Fourier de x(t) (es una función triangular)
fi = (f - 1/2/Ts_initial) % (1 / Ts_initial) - 1/2/Ts_initial
X_f = np.where(np.abs(fi) <= 2*fm, (1 - np.abs(fi)/fm/2)/np.abs(fm)/Ts_initial, 0)

# Función para generar el tren de impulsos en el tiempo
def train_of_impulses(t, Ts):
    return np.where(np.abs(t % Ts) < 0.01, 1, 0)

# Función para generar el tren de impulsos en la frecuencia
def train_of_impulses_freq(f, Ts):
    return np.where(np.abs(f % (1 / Ts)) < 0.01, 10, 0)

# Crear ColumnDataSource para las gráficas
source_time = ColumnDataSource(data=dict(t=t, x_t=x_t, impulses=train_of_impulses(t, Ts_initial)))
source_freq = ColumnDataSource(data=dict(f=f, X_f=X_f, impulses_freq=train_of_impulses_freq(f, Ts_initial)))

# Crear las figuras
p_time = figure(width=600, height=400, title="Se\\~{n}al $$x(t)$$ y tren de impulsos $$p(t)=\\substack{\\infty \\\\ \\sum \\\\ n=-\\infty}\\delta(t-nT_s)$$", x_axis_label='t', y_axis_label='Amplitud')
p_freq = figure(width=600, height=400, title="Transformada de Fourier $$X_d(f)$$, efecto del muestreo", x_axis_label='f', y_axis_label='Magnitud')

# Añadir las líneas a las figuras
p_time.line('t', 'x_t', source=source_time, line_width=2, color="blue", legend_label="x(t) = sinc^2(fm t)")
p_time.line('t', 'impulses', source=source_time, line_width=1, color="red", legend_label="Tren de Impulsos")
p_time.legend.click_policy = "hide"
p_freq.line('f', 'X_f', source=source_freq, line_width=2, color="blue", legend_label="X(f)")
p_freq.line('f', 'impulses_freq', source=source_freq, line_width=1, color="red", legend_label="Tren de impulsos")
p_freq.legend.click_policy = "hide"
p_time.legend.visible = False
p_freq.legend.visible = False
p_time.title.standoff = 30
p_freq.title.standoff = 30

# Crear un slider para modificar el periodo de muestreo Ts
slider_Ts = Slider(title="Periodo de Muestreo (Ts)", value=Ts_initial, start=0.1, end=0.5, step=0.01, sizing_mode="stretch_width")

# JavaScript callback para actualizar las gráficas cuando se modifica el slider
callback = CustomJS(args=dict(source_time=source_time, source_freq=source_freq, slider_Ts=slider_Ts, t=t, f=f, fm=fm),
                    code="""
    const Ts = slider_Ts.value;
    const x_t = source_time.data['x_t'];
    const X_f = source_freq.data['X_f'];
    const impulses = source_time.data['impulses'];
    const impulses_freq = source_freq.data['impulses_freq'];

    // Actualizar tren de impulsos en el tiempo
    for (let i = 0; i < t.length; i++) {
        impulses[i] = Math.abs(t[i] % Ts) < 0.01 ? 1 : 0;
    }

    // Actualizar tren de impulsos en la frecuencia
    for (let i = 0; i < f.length; i++) {
        impulses_freq[i] = Math.abs(f[i] % (1 / Ts)) < 0.01 ? 10 : 0;
        let fi = (f[i] - 1/2/Ts) % (1 / Ts) - Math.sign(f[i] - 1/2/Ts)/2/Ts;
        X_f[i] = Math.abs(fi) < 2*fm ? (1 - Math.abs(fi)/fm/2)/Math.abs(fm)/Ts : 0;
        //if (1/Ts < 2*fm) {
        //    X_f[i] += ((1/Ts - 2*fm) < Math.abs(fi) && 2*fm < Math.abs(fi)) ? (1 - Math.abs(1/Ts - fi)/fm/2)/Math.abs(fm)/Ts : 0;
        //}
    }

    // Actualizar las gráficas
    source_time.change.emit();
    source_freq.change.emit();
""")

slider_Ts.js_on_change('value', callback)

# Organizar el layout
layout = column(row(p_time, p_freq), slider_Ts)

# Especificar el archivo de salida HTML
output_file("../html/T2_Muestreo periódico.html")

# Guardar el layout en el archivo HTML
save(layout)

# Mostrar la aplicación
curdoc().add_root(layout)
curdoc().title = "Muestreo períodico"