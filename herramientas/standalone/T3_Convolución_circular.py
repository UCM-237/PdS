import numpy as np
from numpy import arange
from bokeh.models import CustomJS, ColumnDataSource, Slider, FreehandDrawTool, Button, Div, Range1d, LinearAxis
from bokeh.layouts import column, row
from bokeh.plotting import figure, output_file, save

# --- Configuración de Ejes ---
N_samples = 64  # Número de muestras en un período
N_periods = 3   # Número de períodos a visualizar
n = arange(N_samples)  # Un período base
n_extended = arange(N_samples * N_periods)  # Para visualización extendida

# --- Señales de prueba periódicas ---
# Señal x[n] - Un período base
x_base = np.zeros(N_samples)
x_base[:20] = np.sin(2 * np.pi * 3 * n[:20] / N_samples)

# Señal y[n] - Un período base
y_base = np.zeros(N_samples)
y_base[:25] = 1.0  # Pulso rectangular

# Extender señales para visualización (repetir el período)
def extend_periodic(signal_base, N_periods):
    return np.tile(signal_base, N_periods)

x_extended = extend_periodic(x_base, N_periods)
y_extended = extend_periodic(y_base, N_periods)

# Calcular convolución circular inicial
def circular_convolution(x, y):
    """Calcula la convolución circular de dos señales del mismo tamaño"""
    N = len(x)
    result = np.zeros(N)
    for n in range(N):
        for k in range(N):
            result[n] += x[k] * y[(n - k) % N]
    return result

conv_circular_base = circular_convolution(x_base, y_base)
conv_circular_extended = extend_periodic(conv_circular_base, N_periods)

# --- Fuentes de Datos ---
# source_x: dibujo de la primera señal (un período)
source_x = ColumnDataSource(data=dict(xs=[n.tolist()], ys=[x_base.tolist()])) 

# source_y: dibujo de la segunda señal (un período)
source_y = ColumnDataSource(data=dict(xs=[n.tolist()], ys=[y_base.tolist()]))

# source_calc: datos para la visualización de la convolución
source_calc = ColumnDataSource(data=dict(
    n=n_extended.tolist(),
    x_extended=x_extended.tolist(),
    y_rotated=y_extended.tolist(),
    x_y_product=np.zeros(N_samples * N_periods).tolist(),
    conv_result=conv_circular_extended.tolist(),
))

source_conv_point = ColumnDataSource(data=dict(
    conv_point=[0],
    conv_value=[0]
))

# Source para mostrar un período de la convolución
source_conv_period = ColumnDataSource(data=dict(
    n=n.tolist(),
    conv=conv_circular_base.tolist()
))

# --- Creación de los Paneles de Dibujo ---
def crear_panel_dibujo(titulo, color, src):
    p = figure(
        width=550, 
        height=350, 
        title=titulo,
        x_range=(-2, N_samples + 2), 
        y_range=(-1.5, 1.5),
        tools="pan,wheel_zoom,reset"
    )
    
    renderer = p.multi_line('xs', 'ys', source=src, line_width=3, line_color=color, 
                           line_dash='dotted', alpha=0.7)
    p.scatter('xs', 'ys', source=src, size=8, color=color, marker="circle", 
             fill_color="white", line_width=2)
    
    draw_tool = FreehandDrawTool(renderers=[renderer], num_objects=1)
    p.add_tools(draw_tool)
    p.toolbar.active_drag = draw_tool
    
    p.xaxis.axis_label = "n (muestras)"
    p.yaxis.axis_label = "Amplitud"
    p.xgrid.grid_line_alpha = 0.3
    p.ygrid.grid_line_alpha = 0.3
    
    return p

p1 = crear_panel_dibujo("Dibuja x[n] (un período)", "#FF6B35", source_x)
p2 = crear_panel_dibujo("Dibuja y[n] (un período)", "#4ECDC4", source_y)

# --- Gráfica de Visualización del Proceso ---
p3 = figure(
    width=1150, 
    height=400, 
    title="Visualización del Proceso de Convolución Circular",
    x_range=(-2, N_samples * N_periods + 2),
    y_range=(-2, 2)
)

# Señal x[n] extendida (fija)
p3.scatter('n', 'x_extended', source=source_calc, size=4, color='#FF6B35', 
          legend_label="x[n] (periódica)", alpha=0.8)
p3.line('n', 'x_extended', source=source_calc, line_width=2, color='#FF6B35', alpha=0.5)

# Señal y[n] rotada y desplazada
p3.scatter('n', 'y_rotated', source=source_calc, size=4, color='#4ECDC4', 
          legend_label="y[n-m] (rotada)", alpha=0.8)
p3.line('n', 'y_rotated', source=source_calc, line_width=2, color='#4ECDC4', alpha=0.5)

# Producto x[n] * y[n-m]
p3.varea('n', 0, 'x_y_product', source=source_calc, color='#9B59B6', alpha=0.3,
         legend_label="x[n]·y[n-m]")

# Punto actual de la convolución
p3.extra_y_ranges = {"y2": Range1d(start=-20, end=20)}
p3.add_layout(LinearAxis(y_range_name="y2", axis_label="Eje Secundario"), 'right')
p3.scatter('n', 'conv_result', source=source_calc, y_range_name="y2", size=4, color="#179617", 
          fill_color="white", line_width=1, legend_label="Convolución Circular (x ⊛ y)[n]")
p3.scatter('conv_point', 'conv_value', source=source_conv_point, y_range_name="y2", size=6, color="#179617", 
          marker='circle', legend_label="Punto actual")

p3.varea([N_samples, N_samples*N_periods], [-2,  -2], [2, 2], color='#909090', alpha=0.3)
p3.varea('conv_point', 0, 'conv_value', source=source_conv_point, y_range_name="y2", color="#179617")

p3.xaxis.axis_label = "n (muestras)"
p3.yaxis.axis_label = "Amplitud"
p3.legend.location = "top_right"
p3.legend.click_policy = "hide"
p3.xgrid.grid_line_alpha = 0.3
p3.ygrid.grid_line_alpha = 0.3

# --- Lógica de Procesamiento en JavaScript ---
callback_code = """
    const data_calc = source_calc.data;
    const data_conv = source_conv_period.data;
    const data_conv_point = source_conv_point.data;
    const dx = source_x.data;
    const dy = source_y.data;
    const m = m_slider.value;
    const N = N_samples;
    const N_periods = N_total / N;

    // Función auxiliar para proyectar el dibujo manual al eje discreto
    function proyectar(draw_data, target_array) {
        const xs = draw_data['xs'][0] || [];
        const ys = draw_data['ys'][0] || [];
        
        for (let i = 0; i < N; i++) {
            target_array[i] = 0;
        }
        
        for (let i = 0; i < N; i++) {
            for (let j = 0; j < xs.length - 1; j++) {
                const x_j = xs[j];
                const x_j1 = xs[j + 1];
                
                if (i >= x_j && i <= x_j1) {
                    // Interpolación lineal
                    const t = (i - x_j) / (x_j1 - x_j);
                    target_array[i] = ys[j] * (1 - t) + ys[j + 1] * t;
                    break;
                }
            }
        }
    }

    // Función para extender señal periódicamente
    function extend_periodic(signal_base, extended_array) {
        for (let i = 0; i < extended_array.length; i++) {
            extended_array[i] = signal_base[i % N];
        }
    }

    // Función para rotar circularmente
    function circular_flip(signal_base, rotated_extended, shift) {
        for (let i = 0; i < N_periods * N; i++) {
            const i_base = i % N;
            const i_rotated = (N - i_base + shift) % N;
            rotated_extended[i] = signal_base[i_rotated];
        }
    }

    // Función para calcular convolución circular
    function circular_convolution(x, y, result) {
        for (let n = 0; n < N; n++) {
            result[n] = 0;
            for (let k = 0; k < N; k++) {
                const idx = (n - k + N) % N;
                result[n] += x[k] * y[idx];
            }
        }
    }

    // 1. Obtener formas actuales de x[n] y y[n] (un período)
    const x_base = new Float64Array(N);
    const y_base = new Float64Array(N);
    proyectar(dx, x_base);
    proyectar(dy, y_base);
    
    // 2. Extender x[n] periódicamente
    const x_ext = new Float64Array(N * N_periods);
    extend_periodic(x_base, x_ext);
    
    // 3. Rotar y[n] circularmente y extender
    const y_rot = new Float64Array(N * N_periods);
    circular_flip(y_base, y_rot, m);
    
    // 4. Calcular producto punto a punto (solo para visualización)
    const product = new Float64Array(N * N_periods);
    for (let i = 0; i < N * N_periods; i++) {
        product[i] = x_ext[i] * y_rot[i];
    }
    
    // 5. Calcular convolución circular completa
    const conv_result = new Float64Array(N);
    circular_convolution(x_base, y_base, conv_result);
    
    // 6. Actualizar datos
    for (let i = 0; i < N * N_periods; i++) {
        data_calc['x_extended'][i] = x_ext[i];
        data_calc['y_rotated'][i] = y_rot[i];
        data_calc['x_y_product'][i] = product[i];
        data_calc['conv_result'][i] = conv_result[i % N];
    }
    
    // Marcar el punto actual en la convolución
    data_conv_point['conv_point'][0] = m;  // Posición en el período central
    data_conv_point['conv_value'][0] = conv_result[m];

    source_calc.change.emit();
    source_conv_period.change.emit();
    source_conv_point.change.emit();
"""

# --- Slider para controlar la rotación ---
m_slider = Slider(
    start=0, 
    end=N_samples - 1, 
    value=0, 
    step=1, 
    title="Índice m (desplazamiento circular)",
    width=1150
)

callback = CustomJS(
    args=dict(
        source_calc=source_calc, 
        source_conv_period=source_conv_period,
        source_conv_point=source_conv_point,
        source_x=source_x, 
        source_y=source_y, 
        m_slider=m_slider,
        N_samples=N_samples,
        N_total=N_samples * N_periods
    ),
    code=callback_code
)

m_slider.js_on_change('value', callback)
source_x.js_on_change('data', callback)
source_y.js_on_change('data', callback)

# --- Botones para señales predefinidas ---
callback_reset_x = CustomJS(
    args=dict(source_x=source_x),
    code="""
    const N = source_x.data['xs'][0].length;
    const n = [];
    const x = [];
    
    for (let i = 0; i < N; i++) {
        n.push(i);
        x.push(0);
    }
    
    source_x.data = {'xs': [n], 'ys': [x]};
    source_x.change.emit();
"""
)

callback_sine_1_x = CustomJS(
    args=dict(source_x=source_x, N_samples=N_samples),
    code="""
    const N = N_samples;
    const n = [];
    const x = [];
    
    for (let i = 0; i < N; i++) {
        n.push(i);
        x.push((i < 20) * Math.sin(2 * Math.PI * 3 * i / N));
    }
    
    source_x.data = {'xs': [n], 'ys': [x]};
    source_x.change.emit();
"""
)

callback_sine_2_x = CustomJS(
    args=dict(source_x=source_x, N_samples=N_samples),
    code="""
    const N = N_samples;
    const n = [];
    const x = [];
    
    for (let i = 0; i < N; i++) {
        n.push(i);
        x.push((i < 50) * Math.sin(2 * Math.PI * 3 * i / N));
    }
    
    source_x.data = {'xs': [n], 'ys': [x]};
    source_x.change.emit();
"""
)

callback_reset_y = CustomJS(
    args=dict(source_y=source_y),
    code="""
    const N = source_y.data['xs'][0].length;
    const n = [];
    const y = [];
    
    for (let i = 0; i < N; i++) {
        n.push(i);
        y.push(0);
    }
    
    source_y.data = {'xs': [n], 'ys': [y]};
    source_y.change.emit();
"""
)

callback_pulse_y = CustomJS(
    args=dict(source_y=source_y, N_samples=N_samples),
    code="""
    const N = N_samples;
    const n = [];
    const y = [];
    
    for (let i = 0; i < N; i++) {
        n.push(i);
        y.push((i >= 0 && i < 25) ? 1.0 : 0.0);
    }
    
    source_y.data = {'xs': [n], 'ys': [y]};
    source_y.change.emit();
"""
)

btn_reset_x = Button(label="🔄 Reiniciar x[n]", button_type="primary", width=130)
btn_sine_1_x = Button(label="〜 Seno x[n], L=20", button_type="success", width=130)
btn_sine_2_x = Button(label="〜 Seno x[n], L=60", button_type="success", width=130)
btn_reset_y = Button(label="🔄 Reiniciar y[n]", button_type="primary", width=130)
btn_pulse_y = Button(label="⊓ Pulso y[n]", button_type="success", width=130)

btn_reset_x.js_on_click(callback_reset_x)
btn_sine_1_x.js_on_click(callback_sine_1_x)
btn_sine_2_x.js_on_click(callback_sine_2_x)
btn_reset_y.js_on_click(callback_reset_y)
btn_pulse_y.js_on_click(callback_pulse_y)

# --- Instrucciones ---
titulo = Div(text="""
<div style="text-align: center; margin-bottom: 20px; padding: 15px;">
    <h2 style="color: blue; margin: 0; font-size: 1.8em;">
        🔄 Convolución Circular Interactiva
    </h2>
    <p style="color: white; margin: 5px 0 0 0; font-size: 1.1em;">
        Señales Discretas Periódicas
    </p>
</div>
""", width=1150)

instrucciones = Div(text="""
<div style="background: linear-gradient(to right, #e8f4f8, #d4eef8); padding: 15px; 
            border-left: 4px solid #667eea; margin: 10px 0; border-radius: 6px;">
    <strong style="color: #667eea;">💡 Instrucciones:</strong><br>
    <span style="color: #2c3e50;">
        • <strong>Dibuja</strong> las señales periódicas x[n] e y[n] (un período de cada una)<br>
        • Usa el <strong>slider</strong> para rotar circularmente y[n] y ver cómo se calcula (x ⊛ y)[m]<br>
        • La convolución circular se calcula sobre <strong>un período</strong> completo<br>
        • El área morada muestra el producto x[n]·y[n-m] en cada posición<br>
        • El diamante rojo indica el punto actual de la convolución
    </span>
</div>
""", width=1150)

info_matematica = Div(text="""
<div style="background: linear-gradient(to right, #fff4e6, #ffe8cc); padding: 12px; 
            border-left: 4px solid #FF6B35; margin: 10px 0; border-radius: 6px;">
    <strong style="color: #FF6B35;">📐 Convolución Circular:</strong>
    <span style="color: #2c3e50;">
        (x ⊛ y)[m] = Σ<sub>k=0</sub><sup>N-1</sup> x[k] · y[(m-k) mod N]
        &nbsp;&nbsp;|&nbsp;&nbsp; Señales periódicas con período N = 64
    </span>
</div>
""", width=1150)

# --- Layout ---
controls_x = row(btn_reset_x, btn_sine_1_x, btn_sine_2_x)
controls_y = row(btn_reset_y, btn_pulse_y)

panel_x = column(p1, controls_x)
panel_y = column(p2, controls_y)

layout = column(
    row(titulo),
    row(panel_x, panel_y, column(instrucciones, info_matematica)),
    p3,
    m_slider,
)

# --- Exportar ---
output_file("../html/T3_Convolucion_circular.html", 
            title="Convolución Circular de Señales Periódicas")
save(layout)

print("=" * 80)
print("✓ Archivo 'convolucion_circular.html' generado exitosamente!")
print("=" * 80)
print("\n📖 CARACTERÍSTICAS:")
print("  • Convolución circular de dos señales periódicas discretas")
print("  • Edición interactiva de señales mediante dibujo libre")
print("  • Visualización de la rotación circular de y[n]")
print("  • Cálculo en tiempo real de (x ⊛ y)[n]")
print("\n🔄 DIFERENCIAS CON CONVOLUCIÓN LINEAL:")
print("  • Las señales son PERIÓDICAS (se repiten cada N muestras)")
print("  • La rotación es CIRCULAR (módulo N)")
print("  • El resultado también es periódico con período N")
print("  • Se usa en procesamiento de señales periódicas y DFT")
print("\n🎮 CONTROLES:")
print("  • Dibuja las señales en los paneles superiores")
print("  • Mueve el slider para ver cada punto de la convolución")
print("  • Usa los botones para cargar señales predefinidas")
print("=" * 80)
