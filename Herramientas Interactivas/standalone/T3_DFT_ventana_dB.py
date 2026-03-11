from bokeh.io import output_file, save
from bokeh.layouts import column, row
from bokeh.plotting import figure
from bokeh.models import Slider, Button, ColumnDataSource, Div, CustomJS, Span
import numpy as np

# Configuración inicial
num_points = 128
window_length_initial = 32
window_start_initial = 0

# Inicializar datos con onda combinada
time_data = np.sin(2 * np.pi * 3 * np.arange(num_points) / num_points) + \
            0.5 * np.sin(2 * np.pi * 7 * np.arange(num_points) / num_points)
x_time = np.arange(num_points)

# Extraer ventana inicial
window_data = time_data[window_start_initial:window_start_initial + window_length_initial]

# Calcular DFT de la ventana
def compute_dft(signal):
    dft = np.fft.fft(signal)
    magnitude = np.abs(dft)
    phase = np.angle(dft)
    return magnitude, phase

freq_magnitude, freq_phase = compute_dft(window_data)
x_freq = np.arange(len(window_data))

# Crear ColumnDataSource
source_signal = ColumnDataSource(data={
    'x': x_time.tolist(),
    'y': time_data.tolist()
})

source_window = ColumnDataSource(data={
    'x': np.arange(window_start_initial, window_start_initial + window_length_initial).tolist(),
    'y': window_data.tolist()
})

source_freq_magnitude = ColumnDataSource(data={
    'x': x_freq.tolist(),
    'y': freq_magnitude.tolist()
})

source_freq_phase = ColumnDataSource(data={
    'x': x_freq.tolist(),
    'y': freq_phase.tolist()
})

# Calcular densidad espectral en dB
freq_magnitude_db = 20 * np.log10(freq_magnitude + 1e-10)  # Evitar log(0)

source_freq_db = ColumnDataSource(data={
    'x': x_freq.tolist(),
    'y': freq_magnitude_db.tolist()
})

# Crear figura para señal completa
plot_signal = figure(
    title="Secuencia Discreta Completa (Haz clic y arrastra para editar)",
    width=900,
    height=400,
    tools="",
    toolbar_location=None
)

# Línea de señal completa (gris)
plot_signal.line('x', 'y', source=source_signal, line_width=2, color="#888888", alpha=0.5)
plot_signal.circle('x', 'y', source=source_signal, size=6, color="#888888", 
                   fill_color="white", line_width=1.5, alpha=0.6)

# Ventana seleccionada (destacada)
plot_signal.line('x', 'y', source=source_window, line_width=3, color="#00d4ff", alpha=1)
plot_signal.circle('x', 'y', source=source_window, size=10, color="#00d4ff", 
                   fill_color="white", line_width=2, alpha=1)

plot_signal.xaxis.axis_label = "Índice de muestra"
plot_signal.yaxis.axis_label = "Amplitud"
plot_signal.y_range.start = -2
plot_signal.y_range.end = 2
plot_signal.xgrid.grid_line_alpha = 0.3
plot_signal.ygrid.grid_line_alpha = 0.3

# Crear figura para magnitud DFT de la ventana
plot_freq_mag = figure(
    title="DFT - Magnitud de la Ventana",
    width=450,
    height=350,
    tools="",
    toolbar_location=None
)

plot_freq_mag.vbar(x='x', top='y', source=source_freq_magnitude, width=0.8, 
                   color="#7b2cbf", alpha=0.8)

plot_freq_mag.xaxis.axis_label = "Índice de frecuencia"
plot_freq_mag.yaxis.axis_label = "Magnitud"
plot_freq_mag.y_range.start = 0
plot_freq_mag.y_range.end = 30
plot_freq_mag.xgrid.grid_line_alpha = 0.3
plot_freq_mag.ygrid.grid_line_alpha = 0.3

# Crear figura para densidad espectral en dB
plot_freq_db = figure(
    title="Densidad Espectral de Potencia (dB)",
    width=450,
    height=350,
    tools="",
    toolbar_location=None
)

plot_freq_db.line('x', 'y', source=source_freq_db, line_width=3, color="#10b981", alpha=0.8)
plot_freq_db.circle('x', 'y', source=source_freq_db, size=6, color="#10b981", 
                    fill_color="white", line_width=2, alpha=0.9)

plot_freq_db.xaxis.axis_label = "Índice de frecuencia"
plot_freq_db.yaxis.axis_label = "Magnitud (dB)"
plot_freq_db.y_range.start = -60
plot_freq_db.y_range.end = 40
plot_freq_db.xgrid.grid_line_alpha = 0.3
plot_freq_db.ygrid.grid_line_alpha = 0.3

# Crear figura para fase DFT de la ventana
plot_freq_phase = figure(
    title="DFT - Fase de la Ventana",
    width=450,
    height=350,
    tools="",
    toolbar_location=None
)

plot_freq_phase.line('x', 'y', source=source_freq_phase, line_width=3, color="#ff006e", alpha=0.8)
plot_freq_phase.circle('x', 'y', source=source_freq_phase, size=8, color="#ff006e", 
                       fill_color="white", line_width=2, alpha=0.9)

plot_freq_phase.xaxis.axis_label = "Índice de frecuencia"
plot_freq_phase.yaxis.axis_label = "Fase (radianes)"
plot_freq_phase.y_range.start = -np.pi - 0.5
plot_freq_phase.y_range.end = np.pi + 0.5
plot_freq_phase.xgrid.grid_line_alpha = 0.3
plot_freq_phase.ygrid.grid_line_alpha = 0.3

# CustomJS para editar la señal
callback_signal_edit = CustomJS(
    args=dict(
        source_signal=source_signal,
        source_window=source_window,
        source_freq_magnitude=source_freq_magnitude,
        source_freq_phase=source_freq_phase,
        source_freq_db=source_freq_db,
        window_start_slider=None,  # Se asignará después
        window_length_slider=None  # Se asignará después
    ),
    code="""
    function updatePoint(sx, sy) {
        const data_signal = source_signal.data;
        const x = sx;
        const y = sy;
        
        let min_dist = Infinity;
        let idx = 0;
        
        for (let i = 0; i < data_signal['x'].length; i++) {
            const dist = Math.abs(data_signal['x'][i] - x);
            if (dist < min_dist) {
                min_dist = dist;
                idx = i;
            }
        }
        
        if (min_dist < 1.5) {
            data_signal['y'][idx] = Math.max(-2, Math.min(2, y));
            
            // Actualizar ventana y DFT
            const window_start = Math.floor(window_start_slider.value);
            const window_length = Math.floor(window_length_slider.value);
            
            const window_x = [];
            const window_y = [];
            
            for (let i = 0; i < window_length; i++) {
                const sig_idx = window_start + i;
                if (sig_idx < data_signal['x'].length) {
                    window_x.push(sig_idx);
                    window_y.push(data_signal['y'][sig_idx]);
                }
            }
            
            source_window.data = {'x': window_x, 'y': window_y};
            
            // Calcular DFT de la ventana
            const N = window_y.length;
            const real = new Array(N).fill(0);
            const imag = new Array(N).fill(0);
            
            for (let k = 0; k < N; k++) {
                for (let n = 0; n < N; n++) {
                    const angle = -2 * Math.PI * k * n / N;
                    real[k] += window_y[n] * Math.cos(angle);
                    imag[k] += window_y[n] * Math.sin(angle);
                }
            }
            
            const freq_x = [];
            const freq_mag = [];
            const freq_phase = [];
            const freq_db = [];
            
            for (let i = 0; i < N; i++) {
                freq_x.push(i);
                const mag = Math.sqrt(real[i] * real[i] + imag[i] * imag[i]);
                freq_mag.push(mag);
                freq_phase.push(Math.atan2(imag[i], real[i]));
                freq_db.push(20 * Math.log10(mag + 1e-10));
            }
            
            source_freq_magnitude.data = {'x': freq_x, 'y': freq_mag};
            source_freq_phase.data = {'x': freq_x, 'y': freq_phase};
            source_freq_db.data = {'x': freq_x, 'y': freq_db};
            
            source_signal.change.emit();
            source_window.change.emit();
            source_freq_magnitude.change.emit();
            source_freq_phase.change.emit();
            source_freq_db.change.emit();
        }
    }
    
    if (cb_obj.event_name == 'tap' || cb_obj.event_name == 'pan' || 
        cb_obj.event_name == 'panstart' || cb_obj.event_name == 'panend') {
        updatePoint(cb_obj.x, cb_obj.y);
    }
"""
)

# Sliders
window_length_slider = Slider(
    start=8,
    end=num_points,
    value=window_length_initial,
    step=1,
    title="Longitud de la Ventana",
    width=900
)

window_start_slider = Slider(
    start=0,
    end=num_points - window_length_initial,
    value=window_start_initial,
    step=1,
    title="Posición Inicial de la Ventana",
    width=900
)

# Asignar sliders al callback
callback_signal_edit.args['window_start_slider'] = window_start_slider
callback_signal_edit.args['window_length_slider'] = window_length_slider

# Callback para cambio de ventana
callback_window_change = CustomJS(
    args=dict(
        source_signal=source_signal,
        source_window=source_window,
        source_freq_magnitude=source_freq_magnitude,
        source_freq_phase=source_freq_phase,
        source_freq_db=source_freq_db,
        window_start_slider=window_start_slider,
        window_length_slider=window_length_slider
    ),
    code="""
    const data_signal = source_signal.data;
    const window_start = Math.floor(window_start_slider.value);
    const window_length = Math.floor(window_length_slider.value);
    
    // Actualizar rango del slider de posición
    window_start_slider.end = data_signal['x'].length - window_length;
    if (window_start > window_start_slider.end) {
        window_start_slider.value = window_start_slider.end;
        return;
    }
    
    const window_x = [];
    const window_y = [];
    
    for (let i = 0; i < window_length; i++) {
        const sig_idx = window_start + i;
        if (sig_idx < data_signal['x'].length) {
            window_x.push(sig_idx);
            window_y.push(data_signal['y'][sig_idx]);
        }
    }
    
    source_window.data = {'x': window_x, 'y': window_y};
    
    // Calcular DFT de la ventana
    const N = window_y.length;
    const real = new Array(N).fill(0);
    const imag = new Array(N).fill(0);
    
    for (let k = 0; k < N; k++) {
        for (let n = 0; n < N; n++) {
            const angle = -2 * Math.PI * k * n / N;
            real[k] += window_y[n] * Math.cos(angle);
            imag[k] += window_y[n] * Math.sin(angle);
        }
    }
    
    const freq_x = [];
    const freq_mag = [];
    const freq_phase = [];
    const freq_db = [];
    
    for (let i = 0; i < N; i++) {
        freq_x.push(i);
        const mag = Math.sqrt(real[i] * real[i] + imag[i] * imag[i]);
        freq_mag.push(mag);
        freq_phase.push(Math.atan2(imag[i], real[i]));
        freq_db.push(20 * Math.log10(mag + 1e-10));
    }
    
    source_freq_magnitude.data = {'x': freq_x, 'y': freq_mag};
    source_freq_phase.data = {'x': freq_x, 'y': freq_phase};
    source_freq_db.data = {'x': freq_x, 'y': freq_db};
    
    source_window.change.emit();
    source_freq_magnitude.change.emit();
    source_freq_phase.change.emit();
    source_freq_db.change.emit();
"""
)

window_length_slider.js_on_change('value', callback_window_change)
window_start_slider.js_on_change('value', callback_window_change)

# Registrar eventos de edición
plot_signal.js_on_event('tap', callback_signal_edit)
plot_signal.js_on_event('pan', callback_signal_edit)
plot_signal.js_on_event('panstart', callback_signal_edit)
plot_signal.js_on_event('panend', callback_signal_edit)

# Botones
callback_reset = CustomJS(
    args=dict(
        source_signal=source_signal,
        source_window=source_window,
        source_freq_magnitude=source_freq_magnitude,
        source_freq_phase=source_freq_phase,
        source_freq_db=source_freq_db,
        window_start_slider=window_start_slider,
        window_length_slider=window_length_slider
    ),
    code="""
    const N_signal = source_signal.data['x'].length;
    
    for (let i = 0; i < N_signal; i++) {
        source_signal.data['y'][i] = 0;
    }
    
    const window_start = Math.floor(window_start_slider.value);
    const window_length = Math.floor(window_length_slider.value);
    
    const window_x = [];
    const window_y = [];
    
    for (let i = 0; i < window_length; i++) {
        window_x.push(window_start + i);
        window_y.push(0);
    }
    
    source_window.data = {'x': window_x, 'y': window_y};
    
    const freq_x = [];
    const freq_mag = [];
    const freq_phase = [];
    const freq_db = [];
    
    for (let i = 0; i < window_length; i++) {
        freq_x.push(i);
        freq_mag.push(0);
        freq_phase.push(0);
        freq_db.push(-60);
    }
    
    source_freq_magnitude.data = {'x': freq_x, 'y': freq_mag};
    source_freq_phase.data = {'x': freq_x, 'y': freq_phase};
    source_freq_db.data = {'x': freq_x, 'y': freq_db};
    
    source_signal.change.emit();
    source_window.change.emit();
    source_freq_magnitude.change.emit();
    source_freq_phase.change.emit();
    source_freq_db.change.emit();
"""
)

callback_sine = CustomJS(
    args=dict(
        source_signal=source_signal,
        source_window=source_window,
        source_freq_magnitude=source_freq_magnitude,
        source_freq_phase=source_freq_phase,
        source_freq_db=source_freq_db,
        window_start_slider=window_start_slider,
        window_length_slider=window_length_slider
    ),
    code="""
    const N_signal = source_signal.data['x'].length;
    
    for (let i = 0; i < N_signal; i++) {
        source_signal.data['y'][i] = Math.sin(2 * Math.PI * i / N_signal);
    }
    
    const window_start = Math.floor(window_start_slider.value);
    const window_length = Math.floor(window_length_slider.value);
    
    const window_x = [];
    const window_y = [];
    
    for (let i = 0; i < window_length; i++) {
        const sig_idx = window_start + i;
        window_x.push(sig_idx);
        window_y.push(source_signal.data['y'][sig_idx]);
    }
    
    source_window.data = {'x': window_x, 'y': window_y};
    
    // Calcular DFT
    const N = window_y.length;
    const real = new Array(N).fill(0);
    const imag = new Array(N).fill(0);
    
    for (let k = 0; k < N; k++) {
        for (let n = 0; n < N; n++) {
            const angle = -2 * Math.PI * k * n / N;
            real[k] += window_y[n] * Math.cos(angle);
            imag[k] += window_y[n] * Math.sin(angle);
        }
    }
    
    const freq_x = [];
    const freq_mag = [];
    const freq_phase = [];
    const freq_db = [];
    
    for (let i = 0; i < N; i++) {
        freq_x.push(i);
        const mag = Math.sqrt(real[i] * real[i] + imag[i] * imag[i]);
        freq_mag.push(mag);
        freq_phase.push(Math.atan2(imag[i], real[i]));
        freq_db.push(20 * Math.log10(mag + 1e-10));
    }
    
    source_freq_magnitude.data = {'x': freq_x, 'y': freq_mag};
    source_freq_phase.data = {'x': freq_x, 'y': freq_phase};
    source_freq_db.data = {'x': freq_x, 'y': freq_db};
    
    source_signal.change.emit();
    source_window.change.emit();
    source_freq_magnitude.change.emit();
    source_freq_phase.change.emit();
    source_freq_db.change.emit();
"""
)

callback_multisine = CustomJS(
    args=dict(
        source_signal=source_signal,
        source_window=source_window,
        source_freq_magnitude=source_freq_magnitude,
        source_freq_phase=source_freq_phase,
        window_start_slider=window_start_slider,
        window_length_slider=window_length_slider
    ),
    code="""
    const N_signal = source_signal.data['x'].length;
    
    for (let i = 0; i < N_signal; i++) {
        source_signal.data['y'][i] = Math.sin(2 * Math.PI * 3 * i / N_signal) + 
                                      0.5 * Math.sin(2 * Math.PI * 7 * i / N_signal);
    }
    
    const window_start = Math.floor(window_start_slider.value);
    const window_length = Math.floor(window_length_slider.value);
    
    const window_x = [];
    const window_y = [];
    
    for (let i = 0; i < window_length; i++) {
        const sig_idx = window_start + i;
        window_x.push(sig_idx);
        window_y.push(source_signal.data['y'][sig_idx]);
    }
    
    source_window.data = {'x': window_x, 'y': window_y};
    
    // Calcular DFT
    const N = window_y.length;
    const real = new Array(N).fill(0);
    const imag = new Array(N).fill(0);
    
    for (let k = 0; k < N; k++) {
        for (let n = 0; n < N; n++) {
            const angle = -2 * Math.PI * k * n / N;
            real[k] += window_y[n] * Math.cos(angle);
            imag[k] += window_y[n] * Math.sin(angle);
        }
    }
    
    const freq_x = [];
    const freq_mag = [];
    const freq_phase = [];
    
    for (let i = 0; i < N; i++) {
        freq_x.push(i);
        freq_mag.push(Math.sqrt(real[i] * real[i] + imag[i] * imag[i]));
        freq_phase.push(Math.atan2(imag[i], real[i]));
    }
    
    source_freq_magnitude.data = {'x': freq_x, 'y': freq_mag};
    source_freq_phase.data = {'x': freq_x, 'y': freq_phase};
    
    source_signal.change.emit();
    source_window.change.emit();
    source_freq_magnitude.change.emit();
    source_freq_phase.change.emit();
"""
)

callback_pulse = CustomJS(
    args=dict(
        source_signal=source_signal,
        source_window=source_window,
        source_freq_magnitude=source_freq_magnitude,
        source_freq_phase=source_freq_phase,
        source_freq_db=source_freq_db,
        window_start_slider=window_start_slider,
        window_length_slider=window_length_slider
    ),
    code="""
    const N_signal = source_signal.data['x'].length;
    const pulse_start = Math.floor(N_signal * 0.4);
    const pulse_end = Math.floor(N_signal * 0.6);
    
    for (let i = 0; i < N_signal; i++) {
        source_signal.data['y'][i] = (i >= pulse_start && i < pulse_end) ? 1.0 : 0.0;
    }
    
    const window_start = Math.floor(window_start_slider.value);
    const window_length = Math.floor(window_length_slider.value);
    
    const window_x = [];
    const window_y = [];
    
    for (let i = 0; i < window_length; i++) {
        const sig_idx = window_start + i;
        window_x.push(sig_idx);
        window_y.push(source_signal.data['y'][sig_idx]);
    }
    
    source_window.data = {'x': window_x, 'y': window_y};
    
    // Calcular DFT
    const N = window_y.length;
    const real = new Array(N).fill(0);
    const imag = new Array(N).fill(0);
    
    for (let k = 0; k < N; k++) {
        for (let n = 0; n < N; n++) {
            const angle = -2 * Math.PI * k * n / N;
            real[k] += window_y[n] * Math.cos(angle);
            imag[k] += window_y[n] * Math.sin(angle);
        }
    }
    
    const freq_x = [];
    const freq_mag = [];
    const freq_phase = [];
    const freq_db = [];
    
    for (let i = 0; i < N; i++) {
        freq_x.push(i);
        const mag = Math.sqrt(real[i] * real[i] + imag[i] * imag[i]);
        freq_mag.push(mag);
        freq_phase.push(Math.atan2(imag[i], real[i]));
        freq_db.push(20 * Math.log10(mag + 1e-10));
    }
    
    source_freq_magnitude.data = {'x': freq_x, 'y': freq_mag};
    source_freq_phase.data = {'x': freq_x, 'y': freq_phase};
    source_freq_db.data = {'x': freq_x, 'y': freq_db};
    
    source_signal.change.emit();
    source_window.change.emit();
    source_freq_magnitude.change.emit();
    source_freq_phase.change.emit();
    source_freq_db.change.emit();
"""
)

# Crear botones
btn_reset = Button(label="🔄 Reiniciar", button_type="primary", width=150)
btn_sine = Button(label="〜 Seno", button_type="success", width=150)
btn_multisine = Button(label="〜 Multiseno", button_type="success", width=150)
btn_pulse = Button(label="⊓ Pulso", button_type="success", width=150)

btn_reset.js_on_click(callback_reset)
btn_sine.js_on_click(callback_sine)
btn_multisine.js_on_click(callback_multisine)
btn_pulse.js_on_click(callback_pulse)

# Instrucciones
instructions = Div(text="""
<div style="background: linear-gradient(to right, #e8f4f8, #d4eef8); padding: 15px; 
            border-left: 4px solid #00d4ff; margin: 10px 0; border-radius: 6px;">
    <strong style="color: #00a8cc;">💡 Instrucciones:</strong><br>
    <span style="color: #2c3e50;">
        • Haz <strong>clic y arrastra</strong> sobre los puntos para modificar la señal<br>
        • Ajusta los <strong>sliders</strong> para cambiar la posición y longitud de la ventana<br>
        • La <strong>región azul</strong> muestra la ventana seleccionada cuya DFT se calcula<br>
        • Los botones permiten cargar señales predefinidas
    </span>
</div>
""", width=900)

# Título
title = Div(text="""
<div style="text-align: center; margin-bottom: 20px; padding: 15px; 
            border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
    <h2 style="color: blue; margin: 0; font-size: 1.5em;">
        🔍 Análisis DFT - Espectro de amplitud vs. Densidad espectral (dB)
    </h2>
</div>
""", width=1400)

# Layout
controls_row = row(btn_reset, btn_sine, btn_multisine, btn_pulse)
sliders_column = column(window_start_slider, window_length_slider)
freq_plots = column(plot_freq_mag, plot_freq_db)

signal_section = column(
    plot_signal,
    sliders_column,
    instructions,
    controls_row,
    sizing_mode="fixed"
)

dft_section = column(
    freq_plots,
    sizing_mode="fixed"
)

main_row = row(signal_section, dft_section)

layout = column(
    title,
    main_row
)


# Exportar
output_file("../html/T3_DFT_Ventana_dB.html", 
            title="Análisis DFT - Espectro de amplitud vs. Densidad espectral (dB)",)
save(layout)

print("=" * 70)
print("✓ Archivo 'ventana_dft_interactiva.html' generado exitosamente!")
print("=" * 70)
print("\n📖 CARACTERÍSTICAS:")
print("  • Señal discreta completa (128 muestras)")
print("  • Ventana deslizante ajustable (8-64 muestras)")
print("  • DFT calculada en tiempo real sobre la ventana")
print("  • Edición interactiva haciendo clic sobre los puntos")
print("\n📊 TRES GRÁFICAS DE ANÁLISIS:")
print("  • Magnitud DFT - Espectro de amplitud")
print("  • Densidad Espectral - Representación en dB")
print("  • Fase DFT - Información de fase")
print("\n🎯 CONTROLES:")
print("  • Slider superior: Posición inicial de la ventana")
print("  • Slider inferior: Longitud de la ventana")
print("  • Haz clic sobre puntos para modificar amplitudes")
print("=" * 70)