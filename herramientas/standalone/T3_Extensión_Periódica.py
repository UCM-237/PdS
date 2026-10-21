from bokeh.models import ColumnDataSource, Slider, CustomJS, Div
from bokeh.plotting import figure, output_file, save
from bokeh.layouts import column, row

# Configuración
MAX_POINTS = 64
L_INIT = 16
N_INIT = 20

# Fuentes de datos
x_axis = list(range(MAX_POINTS))
y_init = [0.6 if i < L_INIT else 0.0 for i in x_axis]

# Señal original (Azul) y Extensión Periódica (Gris)
source = ColumnDataSource(data=dict(x=x_axis, y=y_init))
periodic_source = ColumnDataSource(data=dict(x=x_axis, y=[0.0]*MAX_POINTS))

# Gráfico principal
p = figure(title="Dibujo de Secuencia x[n], Soporte L y Periodicidad N", 
           x_range=(-0.5, MAX_POINTS - 0.5), y_range=(-1.1, 1.1),
           width=900, height=450, tools="") #reset,save")

# Renderizadores
p.vbar(x='x', top='y', width=0.3, source=periodic_source, color="gray", alpha=0.3, legend_label="Extensión Periódica x_N[n]")
p.vbar(x='x', top='y', width=0.6, source=source, color="#00d4ff", legend_label="Secuencia Base x[n]")
p.scatter('x', 'y', marker='circle', source=source, size=8, color="#00d4ff", fill_color="white", line_width=2)

# Sliders
slider_l = Slider(start=1, end=MAX_POINTS, value=L_INIT, step=1, title="Longitud de Soporte (L)")
slider_n = Slider(start=1, end=MAX_POINTS, value=N_INIT, step=1, title="Periodo de Repetición (N)")

# Lógica JavaScript unificada
# 1. Recorta la señal al soporte L
# 2. Replica la señal según el periodo N
master_logic = """
    const data = src.data;
    const p_data = p_src.data;
    const L = sl_l.value;
    const N = sl_n.value;

    // Captura de dibujo si hay evento de mouse
    if (cb_obj.x !== undefined) {
        const idx = Math.round(cb_obj.x);
        if (idx >= 0 && idx < L) {
            data.y[idx] = Math.max(-1, Math.min(1, cb_obj.y));
        }
    }

    // Aplicar ventana L (hacer cero fuera del soporte)
    for (let i = 0; i < data.y.length; i++) {
        if (i < 0 || i >= L) {
            data.y[i] = 0;
        }
    }

    // Generar extensión periódica: x_p[n] = x[n mod N]
    for (let i = 0; i < p_data.y.length; i++) {
        let p_idx = ((i % N) + N) % N; 
        // Solo copiamos si el índice está dentro del soporte L original
        p_data.y[i] = (p_idx < L) ? data.y[p_idx] : 0;
    }

    src.change.emit();
    p_src.change.emit();
"""

callback = CustomJS(args=dict(src=source, p_src=periodic_source, sl_l=slider_l, sl_n=slider_n), code=master_logic)

# Asignación de eventos
slider_l.js_on_change('value', callback)
slider_n.js_on_change('value', callback)
p.js_on_event('tap', callback)
p.js_on_event('pan', callback)
p.js_on_event('panstart', callback)
p.js_on_event('panend', callback)
p.js_on_event('mousemove', CustomJS(args=dict(src=source, p_src=periodic_source, sl_l=slider_l, sl_n=slider_n), 
                                    code=f"if (cb_obj.buttons == 1) {{ {master_logic} }}"))

# Nota didáctica
desc = Div(text="""
<div style="padding: 10px; background-color: #f0f0f0; border-radius: 5px;">
    <b>Instrucciones:</b><br>
    1. <b>Dibuja</b> sobre la gráfica azul para definir la forma de la señal.<br>
    2. Ajusta <b>L</b> para ver cómo se trunca la señal original.<br>
    3. Ajusta <b>N</b> para ver el efecto de la repetición periódica. 
    <i>Si N < L, observarás <b>aliasing temporal</b> (el final de un periodo pisa al siguiente).</i>
</div>
""")

# Exportación
layout = column(p, row(slider_l, slider_n), desc)
output_file("html/T3_Extension_Periodica.html", title="PdS - Extensión Periódica")
save(layout)