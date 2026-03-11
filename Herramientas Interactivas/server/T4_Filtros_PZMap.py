import numpy as np
import scipy.signal as signal
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, PointDrawTool, Button, Div, BoxAnnotation, HoverTool, Slider
from bokeh.layouts import row, column, layout

# --- 1. FUENTES DE DATOS ---
pz_source = ColumnDataSource(data={'x': [-0.5], 'y': [0.0], 'type': ['polo'], 'mode': ['real'], 
                                   'pair_id': [99], 'color': ['#e74c3c'], 'marker': ['x']})

# Punto de prueba en el eje imaginario (s = jw)
test_point_source = ColumnDataSource(data={'x': [0.0], 'y': [0.0]}) # x siempre 0

# Líneas que conectan el punto de prueba con polos/ceros
vector_lines_source = ColumnDataSource(data={'xs': [], 'ys': []})

# Punto sobre la curva de Bode
bode_dot_source = ColumnDataSource(data={'w': [0.0], 'mag': [0.0], 'mag_db': [0.0], 'phase': [0.0]})

w_range = np.logspace(-2, 2, 600)
bode_source = ColumnDataSource(data={'w': w_range, 'mag': np.zeros(600), 'mag_db': np.zeros(600), 'phase': np.zeros(600)})
estabilidad_div = Div(text="ESTABLE", width=200)

# Respuesta al impulso (no se actualiza en tiempo real, pero lo dejamos preparado)
step_source = ColumnDataSource(data={'t': np.linspace(0, 10, 1000), 'y': np.zeros(1000)})

# --- 2. LÓGICA DE CÁLCULO Y VECTORES ---
def update_all(attr, old, new):
    d = dict(pz_source.data)
    # 1. Sincronización de simetría (lo que ya teníamos)
    changed = False
    tol = 5e-2
    for i in range(len(d['x'])):
        if d['mode'][i] == 'real' and d['y'][i] != 0:
            d['y'][i] = 0; changed = True
            if abs(d['x'][i]) < tol: # Si x es prácticamente cero
                d['x'][i] = 0.0; changed = True
        if d['mode'][i] == 'conjugado':
            mid = d['pair_id'][i]
            mx, my = d['x'][i], d['y'][i]
            for j in range(len(d['x'])):
                if i != j and d['pair_id'][j] == mid:
                    if abs(mx) < tol: # Si x es prácticamente cero
                        mx = 0.0                    
                    if d['x'][j] != mx or d['y'][j] != -my:
                        d['x'][j], d['y'][j] = mx, -my; changed = True
    

    if changed: 
        pz_source.data = d
        return

    # 2. Forzar punto de prueba al eje imaginario positivo
    tp = test_point_source.data
    if tp['x'][0] != 0 or tp['y'][0] < 0:
        test_point_source.data = {'x': [0.0], 'y': [max(0, tp['y'][0])]}
        return

    # Sincronización entre Slider y Punto de Prueba
    # Si el cambio viene del slider, actualizamos el punto. 
    # Si viene del punto (arrastre), actualizamos el slider.
    if attr == 'value': # Cambio originado en el Slider
        w_test = freq_slider.value
        test_point_source.data = {'x': [0.0], 'y': [w_test]}
    else: # Cambio originado por arrastre del punto rojo
        w_test = test_point_source.data['y'][0]
        if w_test <= 0: w_test = 1e-3
        freq_slider.value = w_test

    w_test = tp['y'][0]
    
    # 3. Dibujar líneas de vectores
    xs, ys = [], []
    for px, py in zip(d['x'], d['y']):
        xs.append([px, 0.0]) # De polo/cero a eje jw
        ys.append([py, w_test])
    vector_lines_source.data = {'xs': xs, 'ys': ys}

    # 4. Respuesta en frecuencia y punto en Bode
    polos = [complex(x, y) for x, y, t in zip(d['x'], d['y'], d['type']) if t == 'polo']
    ceros = [complex(x, y) for x, y, t in zip(d['x'], d['y'], d['type']) if t == 'cero']
    
    # Ganancia unitaria k = prod(polos)/prod(ceros)
    k = np.real(np.prod([-p for p in polos]) / np.prod([-c for c in ceros])) if ceros else np.real(np.prod([-p for p in polos]))
    sys = signal.lti(ceros, polos, k)
    
    w, mag, phase = signal.bode(sys, w=w_range)
    bode_source.data = {'w': w, 'mag': np.power(10, mag/20), 'mag_db': mag, 'phase': phase}

    try:
        t, y = signal.step(sys, T=np.linspace(0, 100, 1000)) 
        step_source.data = {'t': t, 'y': y}
    except ValueError as e:
        step_source.data = {'t': np.linspace(0, 10, 1000), 'y': np.zeros(1000)}
    
    # Calcular magnitud exacta en el punto de prueba
    _, m_test, p_test = signal.bode(sys, w=[w_test] if w_test > 0 else [1e-6])
    bode_dot_source.data = {'w': [w_test], 'mag': [10**(m_test[0]/20)], 'mag_db': [m_test[0]], 'phase': [p_test[0]]}
    
    estabilidad_div.text = "<b>SISTEMA:</b><br/>" + ("<span style='color:red'>INESTABLE ⚠️</span>" if any(p.real > 0 for p in polos) else "<span style='color:green'>ESTABLE ✅</span>")
    estabilidad_div.text += ("<span style='color:red'>NO REALIZABLE ⚠️</span>" if len(polos) < len(ceros)else "<span style='color:green'>REALIZABLE ✅</span>")

# --- 3. INTERFAZ GRÁFICA ---
# Plano S
pz_plot = figure(title="PLANO S", x_range=(-2, 0.1), y_range=(-2, 2), width=500, height=500)
pz_plot.add_layout(BoxAnnotation(left=0, fill_color="yellow", fill_alpha=0.1))
pz_plot.xaxis.fixed_location = 0
pz_plot.xaxis.axis_line_dash = "dotted"
pz_plot.xaxis.axis_line_width = 1
pz_plot.yaxis.fixed_location = 0
pz_plot.yaxis.axis_line_dash = "dotted"
pz_plot.yaxis.axis_line_width = 1

# Líneas de vectores (Discontinuas)
pz_plot.multi_line('xs', 'ys', source=vector_lines_source, color="gray", line_dash="dashed", line_alpha=0.6)

# Polos y Ceros
render_pz = pz_plot.scatter('x', 'y', source=pz_source, size=15, color='color', fill_color=None, marker='marker', line_width=2)

# Punto de prueba (Rojo en eje jw)
render_test = pz_plot.scatter('x', 'y', source=test_point_source, size=8, color="red", marker="square")
pz_plot.add_tools(PointDrawTool(renderers=[render_pz, render_test]), HoverTool(tooltips=[("S", "$x + $iy")]))

# Diagrama de Bode
bode_mag_plot = figure(title="MAGNITUD", x_axis_type='log', width=600, height=250, x_range=(1e-2, 1e2), y_range=(0, 2))
bode_mag_plot.line('w', 'mag', source=bode_source, line_width=4, color="#3e5e7e")
bode_mag_plot.scatter('w', 'mag', source=bode_dot_source, size=8, color="red", marker="square", line_width=3)
bode_mag_plot.segment(x0='w', y0=-60, x1='w', y1='mag', source=bode_dot_source, color="red", line_dash="dotted")

# bode_mag_db_plot = figure(title="FASE", x_axis_type='log', width=600, height=250, x_range=(1e-2, 1e2), y_range=(-60, 40))
# bode_mag_db_plot.line('w', 'mag_db', source=bode_source, line_width=4, color="#2c3e50", line_alpha=0.8)
# bode_mag_db_plot.scatter('w', 'mag_db', source=bode_dot_source, size=12, color="red", line_width=3)
# bode_mag_db_plot.segment(x0='w', y0=0, x1='w', y1='mag_db', source=bode_dot_source, color="red", line_dash="dotted")

step_response_plot = figure(title="RESPUESTA AL ESCALÓN", width=600, height=250, x_range=(0, 50), y_range=(-0.2, 2),)
step_response_plot.line('t', 'y', source=step_source, line_width=4, color="#3e5e7e")
step_response_plot.line('t', 1, source=step_source, line_width=1, color="#3e5e7e", dash="dashed")


freq_slider = Slider(start=0, end=100, value=0, step=0.01, title="Frecuencia (rad/s)", width=400)

# --- BOTONES Y CALLBACKS ---
def add_real(t):
    pz_source.stream({'x':[-0.5], 'y':[0.0], 'type':[t], 'mode':['real'], 'pair_id':[np.random.randint(1000)], 
                      'color':['#e74c3c' if t=='polo' else '#3498db'], 'marker':['x' if t=='polo' else 'circle']})

def add_conj(t):
    nid = np.random.randint(1000)
    pz_source.stream({'x':[-0.5, -0.5], 'y':[0.5, -0.5], 'type':[t, t], 'mode':['conjugado', 'conjugado'], 
                      'pair_id':[nid, nid], 'color':['#e74c3c']*2 if t=='polo' else ['#3498db']*2, 'marker':['x']*2 if t=='polo' else ['circle']*2})

btn_p_r = Button(label="✕ Polo Real", button_type="danger")
btn_p_r.on_click(lambda: add_real('polo'))
btn_c_r = Button(label="○ Cero Real", button_type="primary")
btn_c_r.on_click(lambda: add_real('cero'))
btn_p_c = Button(label="✕✕ Par Polos Conj.", button_type="danger")
btn_p_c.on_click(lambda: add_conj('polo'))
btn_c_c = Button(label="○○ Par Ceros Conj.", button_type="primary")
btn_c_c.on_click(lambda: add_conj('cero'))
btn_reset = Button(label="↺ Reiniciar", button_type="warning", width=200)
btn_reset.on_click(lambda: setattr(pz_source, 'data', {'x':[],'y':[],'type':[],'mode':[],'pair_id':[],'color':[],'marker':[]}))

pz_source.on_change('data', update_all)
freq_slider.on_change('value', update_all)
test_point_source.on_change('data', update_all)

# --- LAYOUT ---
sidebar = column(Div(text="<h2>Analizador LTI</h2>"), estabilidad_div, 
                 row(btn_p_r, btn_p_c), row(btn_c_r, btn_c_c), btn_reset, spacing=10)
bode_plot = column(bode_mag_plot, step_response_plot)
curdoc().add_root(row(
    sidebar,
    column(pz_plot, freq_slider),
    bode_plot)
)
curdoc().title = "Herramienta Interactiva: Polos, Ceros - Respuesta temporal y en frecuencia"
update_all(None, None, None)