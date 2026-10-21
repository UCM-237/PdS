import numpy as np
import scipy.signal as signal
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, PointDrawTool, Button, Div, BoxAnnotation, HoverTool, Slider, Ellipse
from bokeh.layouts import row, column, layout

# --- 1. FUENTES DE DATOS ---
# Iniciamos con un polo en z = 0.5 (estable)
pz_source = ColumnDataSource(data={'x': [], 'y': [], 'type': [], 'mode': [], 
                                   'pair_id': [], 'color': [], 'marker': []})
# pz_source = ColumnDataSource(data={'x': [0.5], 'y': [0.0], 'type': ['polo'], 'mode': ['real'], 
#                                    'pair_id': [99], 'color': ['#e74c3c'], 'marker': ['x']})

test_point_source = ColumnDataSource(data={'x': [1.0], 'y': [0.0]}) 
vector_lines_source = ColumnDataSource(data={'xs': [], 'ys': []})
bode_dot_source = ColumnDataSource(data={'w': [0.0], 'mag': [0.0], 'mag_db': [0.0], 'phase': [0.0]})

# Frecuencias de 0 a PI (Nyquist)
w_range = np.linspace(0, np.pi, 600)
bode_source = ColumnDataSource(data={'w': w_range, 'mag': np.zeros(600), 'mag_db': np.zeros(600), 'phase': np.zeros(600)})
estabilidad_div = Div(text="ESTABLE", width=200)
step_source = ColumnDataSource(data={'t': np.arange(50), 'y': np.zeros(50)})

# --- 2. LÓGICA DE CÁLCULO (SISTEMAS DISCRETOS) ---
def update_all(attr, old, new):
    d = dict(pz_source.data)
    changed = False
    tol = 5e-2
    
    # Sincronización de simetría para pares conjugados
    for i in range(len(d['x'])):
        if d['mode'][i] == 'real' and abs(d['y'][i]) != 0:
            d['y'][i] = 0; changed = True
        if d['mode'][i] == 'conjugado':
            mid = d['pair_id'][i]
            mx, my = d['x'][i], d['y'][i]
            for j in range(len(d['x'])):
                if i != j and d['pair_id'][j] == mid:
                    if d['x'][j] != mx or d['y'][j] != -my:
                        d['x'][j], d['y'][j] = mx, -my; changed = True
    
    if changed: 
        pz_source.data = d
        return

    # Frecuencia de prueba (vía Slider)
    w_test = freq_slider.value
    test_point_source.data = {'x': [np.cos(w_test)], 'y': [np.sin(w_test)]}
    
    # Dibujar vectores desde polos/ceros al punto en el círculo unitario
    xs, ys = [], []
    for px, py in zip(d['x'], d['y']):
        xs.append([px, np.cos(w_test)])
        ys.append([py, np.sin(w_test)])
    vector_lines_source.data = {'xs': xs, 'ys': ys}

    # Definición del sistema en Z
    polos = [complex(x, y) for x, y, t in zip(d['x'], d['y'], d['type']) if t == 'polo']
    ceros = [complex(x, y) for x, y, t in zip(d['x'], d['y'], d['type']) if t == 'cero']
    
    # Ganancia K para normalizar a 1 en DC (z=1)
    num_dc = np.prod([1 - p for p in polos])
    den_dc = np.prod([1 - c for c in ceros]) if ceros else 1.0
    k = np.real(num_dc / den_dc) if abs(den_dc) > 1e-6 else 1.0
    print(k)
    # Crear sistema discreto
    try:
        sys_z = signal.dlti(ceros, polos, k, dt=1.0)
        
        # Bode Discreto
        w_out, mag_db, phase = signal.dbode(sys_z, w=w_range)
        bode_source.data = {'w': w_out, 'mag': np.power(10, mag_db/20), 'mag_db': mag_db, 'phase': phase}

        # Respuesta al escalón (50 muestras)
        t_d, y_d = signal.dstep(sys_z, n=50)
        step_source.data = {'t': t_d, 'y': np.squeeze(y_d)}
        
        # Punto exacto en frecuencia actual
        _, m_t, p_t = signal.dbode(sys_z, w=[w_test])
        bode_dot_source.data = {'w': [w_test], 'mag': [10**(m_t[0]/20)], 'mag_db': [m_t[0]], 'phase': [p_t[0]]}
    except:
        pass # Evitar errores en configuraciones singulares
    
    # Estabilidad en el Plano Z: Todos los polos dentro del círculo unitario (|z| < 1)
    estable = all(np.abs(p) < 1.0 for p in polos)
    realizable = len(polos) >= len(ceros)
    
    estabilidad_div.text = f"<b>SISTEMA Z:</b><br/>" \
                           f"{'<span style=color:green>ESTABLE ✅</span>' if estable else '<span style=color:red>INESTABLE ⚠️</span>'}<br/>" \
                           f"{'<span style=color:green>REALIZABLE ✅</span>' if realizable else '<span style=color:red>NO REALIZABLE ⚠️</span>'}"

# --- 3. INTERFAZ GRÁFICA ---
pz_plot = figure(title="PLANO Z", x_range=(-1.5, 1.5), y_range=(-1.5, 1.5), width=450, height=450)
# Dibujar círculo unitario
pz_plot.ellipse(x=0, y=0, width=2, height=2, fill_color="gray", fill_alpha=0.05, line_color="black", line_dash="dashed")
pz_plot.xaxis.fixed_location = 0
pz_plot.yaxis.fixed_location = 0

pz_plot.multi_line('xs', 'ys', source=vector_lines_source, color="gray", line_dash="dotted", line_alpha=0.5)
render_pz = pz_plot.scatter('x', 'y', source=pz_source, size=15, color='color', marker='marker', line_width=2)
render_test = pz_plot.scatter('x', 'y', source=test_point_source, size=10, color="red", marker="circle")
pz_plot.add_tools(PointDrawTool(renderers=[render_pz]), HoverTool(tooltips=[("z", "@x + @y i")]))

# Gráficos de respuesta
bode_mag_plot = figure(title="MAGNITUD (Frecuencia Normalizada)", width=550, height=250, x_range=(0, np.pi), y_range=(0, 2))
bode_mag_plot.line('w', 'mag', source=bode_source, line_width=3, color="#2980b9")
bode_mag_plot.scatter('w', 'mag', source=bode_dot_source, size=8, color="red")
bode_mag_plot.xaxis.axis_label = "Frecuencia [rad/muestra]"

step_plot = figure(title="RESPUESTA AL ESCALÓN h[n]", width=550, height=250, x_range=(0, 50))
step_plot.vbar(x='t', top='y', width=0.1, source=step_source, color="#3e5e7e", dash="dotted") # Estilo discreto
step_plot.scatter('t', 'y', source=step_source, color="#3e5e7e")

freq_slider = Slider(start=0, end=np.pi, value=0, step=0.02, title="Frecuencia angular ω (0 a π)", width=400)

# --- BOTONES ---
def add_pz(tipo, modo):
    nid = np.random.randint(1000)
    if modo == 'real':
        pz_source.stream({'x':[0.5], 'y':[0.0], 'type':[tipo], 'mode':['real'], 'pair_id':[nid], 
                          'color':['#e74c3c' if tipo=='polo' else '#3498db'], 'marker':['x' if tipo=='polo' else 'circle']})
    else:
        pz_source.stream({'x':[0.5, 0.5], 'y':[0.3, -0.3], 'type':[tipo, tipo], 'mode':['conjugado']*2, 'pair_id':[nid]*2, 
                          'color':['#e74c3c']*2 if tipo=='polo' else ['#3498db']*2, 'marker':['x']*2 if tipo=='polo' else ['circle']*2})

btn_p_r = Button(label="+ Polo Real", button_type="danger")
btn_p_r.on_click(lambda: add_pz('polo', 'real'))
btn_p_c = Button(label="✕✕ Par Polos Conj.", button_type="danger")
btn_p_c.on_click(lambda: add_pz('polo', 'conjugado'))
btn_c_r = Button(label="○ Cero Real", button_type="primary")
btn_c_r.on_click(lambda: add_pz('cero', 'real'))
btn_c_c = Button(label="○○ Par Ceros Conj.", button_type="primary")
btn_c_c.on_click(lambda: add_pz('cero', 'conjugado'))
btn_reset = Button(label="Reiniciar", button_type="warning")
btn_reset.on_click(lambda: setattr(pz_source, 'data', {'x':[],'y':[],'type':[],'mode':[],'pair_id':[],'color':[],'marker':[]}))

pz_source.on_change('data', update_all)
freq_slider.on_change('value', update_all)

# --- LAYOUT FINAL ---
layout_final = row(
    column(Div(text="<h1>Analizador Z</h1>"),
           estabilidad_div, 
           row(btn_p_r, btn_p_c),
           row(btn_c_r, btn_c_c), 
           btn_reset),
    column(pz_plot, freq_slider),
    column(bode_mag_plot, step_plot)
)

curdoc().add_root(layout_final)
curdoc().title = "Analizador de Sistemas Discretos"
update_all(None, None, None)