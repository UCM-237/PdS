from bokeh.io import output_file, save, curdoc
from bokeh.layouts import column, row
from bokeh.plotting import figure
from bokeh.models import Slider, Button, ColumnDataSource, Div, CustomJS
import numpy as np

# Configuración inicial
num_points = 64
dft_points_initial = 64

# Inicializar datos con onda seno
time_data = np.sin(2 * np.pi * 3 * np.arange(num_points) / num_points)
x_time = np.arange(num_points)

# Calcular DFT inicial
def compute_dft(signal, N):
    dft = np.fft.fft(signal, n=N)
    magnitude = np.abs(dft)
    phase = np.angle(dft)
    return magnitude, phase

freq_magnitude, freq_phase = compute_dft(time_data, dft_points_initial)
x_freq = np.arange(dft_points_initial)

# Crear ColumnDataSource
source_time = ColumnDataSource(data={
    'x': x_time.tolist(),
    'y': time_data.tolist()
})

source_freq = ColumnDataSource(data={
    'x': x_freq.tolist(),
    'y': freq_magnitude.tolist()
})

source_phase = ColumnDataSource(data={
    'x': x_freq.tolist(),
    'phase': freq_phase.tolist()
})

# Crear figura para dominio temporal
plot_time = figure(
    title="Secuencia Temporal (Haz clic y arrastra para editar)",
    width=700,
    height=350,
    tools="",
    toolbar_location=None
)

plot_time.line('x', 'y', source=source_time, line_width=3, color="#00d4ff", alpha=0.8)
plot_time.circle('x', 'y', source=source_time, size=10, color="#00d4ff", 
                 fill_color="white", line_width=2, alpha=0.9)

plot_time.xaxis.axis_label = "Índice de muestra"
plot_time.yaxis.axis_label = "Amplitud"
plot_time.y_range.start = -1.5
plot_time.y_range.end = 1.5
plot_time.xgrid.grid_line_alpha = 0.3
plot_time.ygrid.grid_line_alpha = 0.3

# Crear figura para magnitud DFT
plot_freq = figure(
    title="DFT - Magnitud (Haz clic y arrastra para editar)",
    width=350,
    height=350,
    tools="",
    toolbar_location=None
)

plot_freq.vbar(x='x', top='y', source=source_freq, width=0.8, 
               color="#7b2cbf", alpha=0.8)

plot_freq.xaxis.axis_label = "Índice de frecuencia"
plot_freq.yaxis.axis_label = "Magnitud"
plot_freq.y_range.start = 0
plot_freq.y_range.end = 20
plot_freq.xgrid.grid_line_alpha = 0.3
plot_freq.ygrid.grid_line_alpha = 0.3

# Crear figura para fase DFT
plot_phase = figure(
    title="DFT - Fase (Haz clic y arrastra para editar)",
    width=350,
    height=350,
    tools="",
    toolbar_location=None
)

plot_phase.line('x', 'phase', source=source_phase, line_width=3, color="#ff006e", alpha=0.8)
plot_phase.circle('x', 'phase', source=source_phase, size=10, color="#ff006e", 
                  fill_color="white", line_width=2, alpha=0.9)

plot_phase.xaxis.axis_label = "Índice de frecuencia"
plot_phase.yaxis.axis_label = "Fase (radianes)"
plot_phase.y_range.start = -np.pi - 0.5
plot_phase.y_range.end = np.pi + 0.5
plot_phase.xgrid.grid_line_alpha = 0.3
plot_phase.ygrid.grid_line_alpha = 0.3

# CustomJS para editar dominio temporal
callback_time_edit = CustomJS(
    args=dict(
        source_time=source_time,
        source_freq=source_freq,
        source_phase=source_phase,
        plot=plot_time
    ),
    code="""
    function updatePoint(sx, sy) {
        const data_time = source_time.data;
        const data_freq = source_freq.data;
        const phase = source_phase.data['phase'];
        
        const x = sx;
        const y = sy;
        
        let min_dist = Infinity;
        let idx = 0;
        
        for (let i = 0; i < data_time['x'].length; i++) {
            const dist = Math.abs(data_time['x'][i] - x);
            if (dist < min_dist) {
                min_dist = dist;
                idx = i;
            }
        }
        
        if (min_dist < 1.5) {
            data_time['y'][idx] = Math.max(-1.5, Math.min(1.5, y));
            
            const N = data_freq['x'].length;
            const signal_length = data_time['x'].length;
            
            const real = new Array(N).fill(0);
            const imag = new Array(N).fill(0);
            
            for (let k = 0; k < N; k++) {
                for (let n = 0; n < signal_length; n++) {
                    const angle = -2 * Math.PI * k * n / N;
                    real[k] += data_time['y'][n] * Math.cos(angle);
                    imag[k] += data_time['y'][n] * Math.sin(angle);
                }
                data_freq['y'][k] = Math.sqrt(real[k] * real[k] + imag[k] * imag[k]);
                phase[k] = Math.atan2(imag[k], real[k]);
            }
            
            source_time.change.emit();
            source_freq.change.emit();
            source_phase.change.emit();
        }
    }
    
    if (cb_obj.event_name == 'tap' || cb_obj.event_name == 'pan' || 
        cb_obj.event_name == 'panstart' || cb_obj.event_name == 'panend') {
        updatePoint(cb_obj.x, cb_obj.y);
    }
"""
)

# CustomJS para editar magnitud
callback_freq_edit = CustomJS(
    args=dict(
        source_time=source_time,
        source_freq=source_freq,
        source_phase=source_phase,
        plot=plot_freq
    ),
    code="""
    function updateBar(sx, sy) {
        const data_time = source_time.data;
        const data_freq = source_freq.data;
        const phase = source_phase.data['phase'];
        
        const x = sx;
        const y = Math.max(0, sy);
        
        let min_dist = Infinity;
        let idx = 0;
        
        for (let i = 0; i < data_freq['x'].length; i++) {
            const dist = Math.abs(data_freq['x'][i] - x);
            if (dist < min_dist) {
                min_dist = dist;
                idx = i;
            }
        }
        
        if (min_dist < 1.5) {
            const N = data_freq['x'].length;
            data_freq['y'][idx] = y;
            data_freq['y'][N - idx] = y;
            
            const signal_length = data_time['x'].length;
            
            for (let n = 0; n < signal_length; n++) {
                data_time['y'][n] = 0;
                for (let k = 0; k < N; k++) {
                    const angle = 2 * Math.PI * k * n / N + phase[k];
                    data_time['y'][n] += data_freq['y'][k] * Math.cos(angle) / N;
                }
            }
            
            source_time.change.emit();
            source_freq.change.emit();
        }
    }
    
    if (cb_obj.event_name == 'tap' || cb_obj.event_name == 'pan' || 
        cb_obj.event_name == 'panstart' || cb_obj.event_name == 'panend') {
        updateBar(cb_obj.x, cb_obj.y);
    }
"""
)

# CustomJS para editar fase
callback_phase_edit = CustomJS(
    args=dict(
        source_time=source_time,
        source_freq=source_freq,
        source_phase=source_phase,
        plot=plot_phase
    ),
    code="""
    function updatePhase(sx, sy) {
        const data_time = source_time.data;
        const data_freq = source_freq.data;
        const phase = source_phase.data['phase'];
        
        const x = sx;
        const y = sy;
        
        let min_dist = Infinity;
        let idx = 0;
        
        for (let i = 0; i < phase.length; i++) {
            const dist = Math.abs(source_phase.data['x'][i] - x);
            if (dist < min_dist) {
                min_dist = dist;
                idx = i;
            }
        }
        
        if (min_dist < 1.5) {
            const N = data_freq['x'].length;
            // Limitar fase entre -π y π
            phase[idx] = Math.max(-Math.PI, Math.min(Math.PI, y));
            phase[N - idx] = -phase[idx]; // Simetría conjugada
            
            // Recalcular señal temporal (IDFT) con nueva fase
            const signal_length = data_time['x'].length;
            
            for (let n = 0; n < signal_length; n++) {
                data_time['y'][n] = 0;
                for (let k = 0; k < N; k++) {
                    const angle = 2 * Math.PI * k * n / N + phase[k];
                    data_time['y'][n] += data_freq['y'][k] * Math.cos(angle) / N;
                }
            }
            
            source_phase.change.emit();
            source_time.change.emit();
        }
    }
    
    if (cb_obj.event_name == 'tap' || cb_obj.event_name == 'pan' || 
        cb_obj.event_name == 'panstart' || cb_obj.event_name == 'panend') {
        updatePhase(cb_obj.x, cb_obj.y);
    }
"""
)

# Registrar eventos
plot_time.js_on_event('tap', callback_time_edit)
plot_time.js_on_event('pan', callback_time_edit)
plot_time.js_on_event('panstart', callback_time_edit)
plot_time.js_on_event('panend', callback_time_edit)

plot_freq.js_on_event('tap', callback_freq_edit)
plot_freq.js_on_event('pan', callback_freq_edit)
plot_freq.js_on_event('panstart', callback_freq_edit)
plot_freq.js_on_event('panend', callback_freq_edit)

plot_phase.js_on_event('tap', callback_phase_edit)
plot_phase.js_on_event('pan', callback_phase_edit)
plot_phase.js_on_event('panstart', callback_phase_edit)
plot_phase.js_on_event('panend', callback_phase_edit)

# Slider para número de puntos DFT
dft_points_slider = Slider(
    start=64,
    end=512,
    value=dft_points_initial,
    step=2,
    title="Número de Puntos DFT",
    width=700
)

callback_slider = CustomJS(
    args=dict(
        source_time=source_time,
        source_freq=source_freq,
        source_phase=source_phase,
        slider=dft_points_slider
    ),
    code="""
    const new_N = slider.value;
    const data_time = source_time.data;
    
    const real = new Array(new_N).fill(0);
    const imag = new Array(new_N).fill(0);
    
    for (let k = 0; k < new_N; k++) {
        for (let n = 0; n < data_time['x'].length; n++) {
            const angle = -2 * Math.PI * k * n / new_N;
            real[k] += data_time['y'][n] * Math.cos(angle);
            imag[k] += data_time['y'][n] * Math.sin(angle);
        }
    }
    
    const new_x = [];
    const new_y = [];
    const new_phase = [];
    
    for (let i = 0; i < new_N; i++) {
        new_x.push(i);
        new_y.push(Math.sqrt(real[i] * real[i] + imag[i] * imag[i]));
        new_phase.push(Math.atan2(imag[i], real[i]));
    }
    
    source_freq.data = {'x': new_x, 'y': new_y};
    source_phase.data = {'x': new_x, 'phase': new_phase};
    
    source_freq.change.emit();
    source_phase.change.emit();
"""
)

dft_points_slider.js_on_change('value', callback_slider)

# Botones con callbacks
callback_reset_time = CustomJS(
    args=dict(source_time=source_time, source_freq=source_freq, source_phase=source_phase),
    code="""
    const N_time = source_time.data['x'].length;
    const N_freq = source_freq.data['x'].length;
    
    for (let i = 0; i < N_time; i++) {
        source_time.data['y'][i] = 0;
    }
    
    for (let i = 0; i < N_freq; i++) {
        source_freq.data['y'][i] = 0;
        source_phase.data['phase'][i] = 0;
    }
    
    source_time.change.emit();
    source_freq.change.emit();
    source_phase.change.emit();
"""
)

callback_sine = CustomJS(
    args=dict(source_time=source_time, source_freq=source_freq, source_phase=source_phase),
    code="""
    const N_time = source_time.data['x'].length;
    const N_freq = source_freq.data['x'].length;
    
    for (let i = 0; i < N_time; i++) {
        source_time.data['y'][i] = Math.sin(2 * Math.PI * 3 * i / N_time);
    }
    
    const real = new Array(N_freq).fill(0);
    const imag = new Array(N_freq).fill(0);
    
    for (let k = 0; k < N_freq; k++) {
        for (let n = 0; n < N_time; n++) {
            const angle = -2 * Math.PI * k * n / N_freq;
            real[k] += source_time.data['y'][n] * Math.cos(angle);
            imag[k] += source_time.data['y'][n] * Math.sin(angle);
        }
        source_freq.data['y'][k] = Math.sqrt(real[k] * real[k] + imag[k] * imag[k]);
        source_phase.data['phase'][k] = Math.atan2(imag[k], real[k]);
    }
    
    source_time.change.emit();
    source_freq.change.emit();
    source_phase.change.emit();
"""
)

callback_square = CustomJS(
    args=dict(source_time=source_time, source_freq=source_freq, source_phase=source_phase),
    code="""
    const N_time = source_time.data['x'].length;
    const N_freq = source_freq.data['x'].length;
    
    for (let i = 0; i < N_time; i++) {
        source_time.data['y'][i] = i < N_time / 2 ? 0.8 : -0.8;
    }
    
    const real = new Array(N_freq).fill(0);
    const imag = new Array(N_freq).fill(0);
    
    for (let k = 0; k < N_freq; k++) {
        for (let n = 0; n < N_time; n++) {
            const angle = -2 * Math.PI * k * n / N_freq;
            real[k] += source_time.data['y'][n] * Math.cos(angle);
            imag[k] += source_time.data['y'][n] * Math.sin(angle);
        }
        source_freq.data['y'][k] = Math.sqrt(real[k] * real[k] + imag[k] * imag[k]);
        source_phase.data['phase'][k] = Math.atan2(imag[k], real[k]);
    }
    
    source_time.change.emit();
    source_freq.change.emit();
    source_phase.change.emit();
"""
)

callback_reset_freq = CustomJS(
    args=dict(source_time=source_time, source_freq=source_freq, source_phase=source_phase),
    code="""
    const N_time = source_time.data['x'].length;
    const N_freq = source_freq.data['x'].length;
    
    for (let i = 0; i < N_freq; i++) {
        source_freq.data['y'][i] = 0;
        source_phase.data['phase'][i] = 0;
    }
    
    for (let i = 0; i < N_time; i++) {
        source_time.data['y'][i] = 0;
    }
    
    source_time.change.emit();
    source_freq.change.emit();
    source_phase.change.emit();
"""
)

callback_lowpass = CustomJS(
    args=dict(source_time=source_time, source_freq=source_freq, source_phase=source_phase),
    code="""
    const N_freq = source_freq.data['x'].length;
    const N_time = source_time.data['x'].length;
    const cutoff = Math.floor(N_freq / 8);
    
    for (let i = cutoff; i < N_freq; i++) {
        source_freq.data['y'][i] = 0;
    }
    
    for (let n = 0; n < N_time; n++) {
        source_time.data['y'][n] = 0;
        for (let k = 0; k < N_freq; k++) {
            const angle = 2 * Math.PI * k * n / N_freq + source_phase.data['phase'][k];
            source_time.data['y'][n] += source_freq.data['y'][k] * Math.cos(angle) / N_freq;
        }
    }
    
    source_time.change.emit();
    source_freq.change.emit();
"""
)

callback_highpass = CustomJS(
    args=dict(source_time=source_time, source_freq=source_freq, source_phase=source_phase),
    code="""
    const N_freq = source_freq.data['x'].length;
    const N_time = source_time.data['x'].length;
    const cutoff = Math.floor(N_freq / 8);
    
    for (let i = 0; i < cutoff; i++) {
        source_freq.data['y'][i] = 0;
    }
    
    for (let n = 0; n < N_time; n++) {
        source_time.data['y'][n] = 0;
        for (let k = 0; k < N_freq; k++) {
            const angle = 2 * Math.PI * k * n / N_freq + source_phase.data['phase'][k];
            source_time.data['y'][n] += source_freq.data['y'][k] * Math.cos(angle) / N_freq;
        }
    }
    
    source_time.change.emit();
    source_freq.change.emit();
"""
)

callback_zero_phase = CustomJS(
    args=dict(source_time=source_time, source_freq=source_freq, source_phase=source_phase),
    code="""
    const N_freq = source_freq.data['x'].length;
    const N_time = source_time.data['x'].length;
    
    // Poner todas las fases a cero
    for (let i = 0; i < N_freq; i++) {
        source_phase.data['phase'][i] = 0;
    }
    
    // Recalcular señal temporal
    for (let n = 0; n < N_time; n++) {
        source_time.data['y'][n] = 0;
        for (let k = 0; k < N_freq; k++) {
            const angle = 2 * Math.PI * k * n / N_freq;
            source_time.data['y'][n] += source_freq.data['y'][k] * Math.cos(angle) / N_freq;
        }
    }
    
    source_phase.change.emit();
    source_time.change.emit();
"""
)

callback_linear_phase = CustomJS(
    args=dict(source_time=source_time, source_freq=source_freq, source_phase=source_phase),
    code="""
    const N_freq = source_freq.data['x'].length;
    const N_time = source_time.data['x'].length;
    
    // Aplicar fase lineal
    for (let i = 0; i < N_freq; i++) {
        source_phase.data['phase'][i] = -Math.PI * i / N_freq;
    }
    
    // Recalcular señal temporal
    for (let n = 0; n < N_time; n++) {
        source_time.data['y'][n] = 0;
        for (let k = 0; k < N_freq; k++) {
            const angle = 2 * Math.PI * k * n / N_freq + source_phase.data['phase'][k];
            source_time.data['y'][n] += source_freq.data['y'][k] * Math.cos(angle) / N_freq;
        }
    }
    
    source_phase.change.emit();
    source_time.change.emit();
"""
)

# Crear botones
btn_reset_time = Button(label="🔄 Reiniciar", button_type="primary", width=140)
btn_sine = Button(label="〜 Onda Seno", button_type="success", width=140)
btn_square = Button(label="⊓ Onda Cuadrada", button_type="success", width=140)

btn_reset_freq = Button(label="🔄 Reiniciar", button_type="primary", width=140)
btn_lowpass = Button(label="⬇ Paso Bajo", button_type="warning", width=140)
btn_highpass = Button(label="⬆ Paso Alto", button_type="warning", width=140)

btn_zero_phase = Button(label="⊘ Fase Cero", button_type="primary", width=140)
btn_linear_phase = Button(label="📐 Fase Lineal", button_type="success", width=140)

btn_reset_time.js_on_click(callback_reset_time)
btn_sine.js_on_click(callback_sine)
btn_square.js_on_click(callback_square)
btn_reset_freq.js_on_click(callback_reset_freq)
btn_lowpass.js_on_click(callback_lowpass)
btn_highpass.js_on_click(callback_highpass)
btn_zero_phase.js_on_click(callback_zero_phase)
btn_linear_phase.js_on_click(callback_linear_phase)

# Instrucciones
instructions_time = Div(text="""
<div style="background: linear-gradient(to right, #e8f4f8, #d4eef8); padding: 10px; 
            border-left: 4px solid #00d4ff; margin-top: 10px; border-radius: 6px;">
    <strong style="color: #00a8cc;">💡</strong> 
    <span style="color: #2c3e50;">Haz <strong>clic</strong> sobre los puntos para modificar amplitudes.</span>
</div>
""", width=700)

instructions_freq = Div(text="""
<div style="background: linear-gradient(to right, #f3e8f8, #ead4f8); padding: 10px; 
            border-left: 4px solid #7b2cbf; margin-top: 10px; border-radius: 6px;">
    <strong style="color: #7b2cbf;">💡</strong> 
    <span style="color: #2c3e50;">Haz <strong>clic</strong> sobre las barras para ajustar magnitudes.</span>
</div>
""", width=350)

instructions_phase = Div(text="""
<div style="background: linear-gradient(to right, #ffe8f3, #ffd4ea); padding: 10px; 
            border-left: 4px solid #ff006e; margin-top: 10px; border-radius: 6px;">
    <strong style="color: #ff006e;">💡</strong> 
    <span style="color: #2c3e50;">Haz <strong>clic</strong> sobre los puntos para modificar fases.</span>
</div>
""", width=350)

# Título
title = Div(text="""
<div style="text-align: center; margin-bottom: 20px; padding: 10px; 
            border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
    <p style="color: #000000; font-size: 1.3em; margin: 0;">
        Transformada Discreta de Fourier
    </p>
</div>
""", width=1500)

# Layout
time_controls = row(btn_reset_time, btn_sine, btn_square)
freq_controls = row(btn_reset_freq, btn_zero_phase)

time_section = column(
    plot_time,
    instructions_time,
    time_controls,
    sizing_mode="fixed"
)

freq_section = column(
    plot_freq,
    instructions_freq,
    btn_reset_freq,
    sizing_mode="fixed"
)

phase_section = column(
    plot_phase,
    instructions_phase,
    btn_zero_phase,
    sizing_mode="fixed"
)


dft_section = column(row(freq_section, phase_section), dft_points_slider)

plots_row = row(time_section, dft_section)

layout = column(
    title,
    plots_row
)

# Exportar
output_file("../html/T3_DFT_Editor_Interactivo.html", title = "Transformada de Fourier Discreta (DFT)")
save(layout)

print("=" * 70)
print("✓ Archivo 'DFT_Editor_Completo.html' generado exitosamente!")
print("=" * 70)
print("\n📖 INSTRUCCIONES DE USO:")
print("  1. Abre el archivo HTML en tu navegador")
print("  2. HAZ CLIC sobre puntos, barras o círculos para editarlos")
print("  3. Usa el slider para cambiar el número de puntos DFT")
print("  4. Prueba los botones de presets y filtros")
print("\n🎨 TRES GRÁFICAS INTERACTIVAS:")
print("  • Secuencia Temporal - Edita la señal en el dominio del tiempo")
print("  • Magnitud DFT - Modifica las amplitudes de cada frecuencia")
print("  • Fase DFT - Ajusta las fases de cada frecuencia")
print("\n🔄 SINCRONIZACIÓN:")
print("  • Los cambios en cualquier gráfica se reflejan automáticamente")
print("  • DFT ↔ IDFT en tiempo real")
print("=" * 70)