import numpy as np
from bokeh.plotting import figure, output_file, save
from bokeh.layouts import row, column
from bokeh.models import Slider, ColumnDataSource, CustomJS, Spacer
from bokeh.io import curdoc

# Parámetros iniciales
fm = 1  # Frecuencia de la señal sinc
Ts_initial = 0.15  # Periodo de muestreo inicial
tau_initial = 0.1  # Periodo de muestreo inicial
t = np.linspace(-2, 2, 10000)  # Dominio del tiempo
f = np.linspace(-10, 10, 10000)  # Dominio de la frecuencia

# Señal x(t) = sinc(fm * t)^2
x_t = np.sinc(fm * t)**2

# Transformada de Fourier de x(t) (es una función triangular)
fi = (f - 1/2/Ts_initial) % (1 / Ts_initial) - 1/2/Ts_initial
X_f = np.where(np.abs(fi) <= 2*fm, (1 - np.abs(fi)/fm/2)/np.abs(fm)/Ts_initial, 0)

# Función para generar el tren de impulsos en el tiempo
def train_of_pulses(t, Ts):
    return np.where(np.abs(t % Ts) < 0.5*Ts, 1, 0)

# Función para generar el tren de impulsos en la frecuencia
def train_of_pulses_freq(f, Ts):
    return np.where(np.abs(f % (1 / Ts)) < 0.01, 10, 0)

# Crear ColumnDataSource para las gráficas
source_time = ColumnDataSource(data=dict(t=t, x_t=x_t, pulses=train_of_pulses(t, Ts_initial)))
source_freq = ColumnDataSource(data=dict(f=f, X_f=X_f, pulses_freq=train_of_pulses_freq(f, Ts_initial)))

# Crear las figuras
p_time = figure(width=600, height=400, title="Se\\~{n}al $$x(t)$$ y tren de impulsos $$p(t)=\\substack{\\infty \\\\ \\sum \\\\ n=-\\infty}\\delta(t-nT_s)$$", x_axis_label='t', y_axis_label='Amplitud')
p_freq = figure(width=600, height=400, title="Transformada de Fourier $$X_d(f)$$, efecto del muestreo", x_axis_label='f', y_axis_label='Magnitud')

# Añadir las líneas a las figuras
p_time.line('t', 'x_t', source=source_time, line_width=2, color="blue", legend_label="x(t) = sinc^2(fm t)")
p_time.line('t', 'pulses', source=source_time, line_width=1, color="red", legend_label="Tren de Impulsos")
p_time.legend.click_policy = "hide"
p_freq.line('f', 'X_f', source=source_freq, line_width=2, color="blue", legend_label="X(f)")
p_freq.line('f', 'pulses_freq', source=source_freq, line_width=1, color="red", legend_label="Tren de impulsos")
p_freq.legend.click_policy = "hide"
p_time.legend.visible = False
p_freq.legend.visible = False
p_time.title.standoff = 30
p_freq.title.standoff = 30

# Crear un slider para modificar el periodo de muestreo Ts
slider_Ts = Slider(title="Periodo de Muestreo (Ts)", value=Ts_initial, start=0.1, end=0.5, step=0.01, sizing_mode="stretch_width")
slider_tau = Slider(title="Ampitud de Muestreo (tau)", value=tau_initial, start=0.1, end=0.9, step=0.1, sizing_mode="stretch_width")

# JavaScript callback para actualizar las gráficas cuando se modifica el slider
callback = CustomJS(args=dict(source_time=source_time, source_freq=source_freq, slider_Ts=slider_Ts, slider_tau=slider_tau, t=t, f=f, fm=fm),
                    code="""
    function sinc(x) { return x===0 ? 1 : Math.sin(x) / x; }                    
    const Ts = slider_Ts.value;
    const tau = slider_tau.value;
    const x_t = source_time.data['x_t'];
    const X_f = source_freq.data['X_f'];
    const pulses = source_time.data['pulses'];
    const pulses_freq = source_freq.data['pulses_freq'];

    // Actualizar tren de impulsos en el tiempo
    for (let i = 0; i < t.length; i++) {
        pulses[i] = (((t[i]) % Ts) + 0.5*Ts*(1 - Math.sign(t[i]))) < 0.5*tau*Ts ? 1 : 0;
    }
    // Actualizar tren de impulsos en la frecuencia
    for (let i = 0; i < f.length; i++) {
        let k = Math.round(f[i] / (1 / Ts));
        let ck = (tau/Ts)*sinc(k*(tau/Ts));
        pulses_freq[i] = Math.abs(f[i] % (1 / Ts)) < 0.01 ? ck*5 : 0;
        let fi = (f[i] - 1/2/Ts) % (1 / Ts) - Math.sign(f[i] - 1/2/Ts)/2/Ts;
        X_f[i] = Math.abs(fi) < 2*fm ? ck*(1 - Math.abs(fi)/fm/2)/Math.abs(fm)/Ts : 0;
    }

    // Actualizar las gráficas
    source_time.change.emit();
    source_freq.change.emit();
""")

slider_Ts.js_on_change('value', callback)
slider_tau.js_on_change('value', callback)

# Organizar el layout
layout = column(row(p_time, p_freq), slider_Ts, slider_tau)
curdoc().title = "Muestreo períodico"

# Especificar el archivo de salida HTML
output_file("../html/T2_Muestreo natural.html")

# Guardar el layout en el archivo HTML
save(layout)