import numpy as np
import scipy.signal as signal
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, PointDrawTool, Button, Div, BoxAnnotation, HoverTool, Slider, Select
from bokeh.layouts import row, column, layout

# --- 1. FUENTES DE DATOS ---
pz_source = ColumnDataSource(data={'x': [-0.5], 'y': [0.0], 'type': ['polo'], 'mode': ['real'], 
                                   'pair_id': [99], 'color': ['#e74c3c'], 'marker': ['x']})

# Plano Z
z_source = ColumnDataSource(data={'x': [], 'y': [], 'type': [], 'color': [], 'marker': []})
unit_circle_source = ColumnDataSource(data={'x': [0], 'y': [0], 'w': [2], 'h': [2]})

# Líneas que conectan el punto de prueba con polos/ceros
vector_lines_source = ColumnDataSource(data={'xs': [], 'ys': []})

# Punto sobre la curva de Bode
bode_dot_source = ColumnDataSource(data={'w': [0.0], 'mag': [0.0], 'mag_db': [0.0], 'phase': [0.0]})

w_range = np.logspace(-2, 2, 600)
bode_source = ColumnDataSource(data={'w': w_range, 'mag': np.zeros(600), 'mag_db': np.zeros(600), 'phase': np.zeros(600)})
bode_z_source = ColumnDataSource(data={'w': w_range, 'mag': np.zeros(600), 'mag_db': np.zeros(600), 'phase': np.zeros(600)})
estabilidad_div = Div(text="ESTABLE", width=200)

# Respuesta al impulso (no se actualiza en tiempo real, pero lo dejamos preparado)
step_source = ColumnDataSource(data={'t': np.linspace(0, 10, 1000), 'y': np.zeros(1000)})
step_z_source = ColumnDataSource(data={'t': np.linspace(0, 10, 1000), 'y': np.zeros(1000)})

# --- 2. WIDGETS ---
method_select = Select(title="Método de Discretización:", value="impulse", 
                       options=[("bilinear", "Transformada Bilineal"), 
                                ("impulse", "Invarianza al Impulso")])
ts_slider = Slider(start=0.1, end=10, value=1, step=0.01, title="Periodo de Muestreo (Ts) [s]", width=400)
estabilidad_div = Div(text="ESTABLE", width=200)

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
    
    estabilidad_div.text = "<b>SISTEMA:</b><br/>" + ("<span style='color:red'>INESTABLE ⚠️</span>" if any(p.real > 0 for p in polos) else "<span style='color:green'>ESTABLE ✅</span>")
    estabilidad_div.text += ("<span style='color:red'>NO REALIZABLE ⚠️</span>" if len(polos) < len(ceros)else "<span style='color:green'>REALIZABLE ✅</span>")

    # --- DISCRETIZACIÓN (PLANO Z) ---
    ts = ts_slider.value
    method = method_select.value
    dt = ts
    try:
        # Convertir a espacio de estados para mayor estabilidad numérica
        sys_disc = signal.cont2discrete((sys.zeros, sys.poles, sys.gain), dt, method=method)
        z_zeros = sys_disc[0]
        z_poles = sys_disc[1]
        z_gain = 1

        z_data = {'x': [], 'y': [], 'type': [], 'color': [], 'marker': []}
        for p in z_poles:
            z_data['x'].append(p.real); z_data['y'].append(p.imag)
            z_data['type'].append('polo'); z_data['color'].append('#e74c3c'); z_data['marker'].append('x')
            z_gain *= np.abs(1 - p)
        for c in z_zeros:
            z_data['x'].append(c.real); z_data['y'].append(c.imag)
            z_data['type'].append('cero'); z_data['color'].append('#3498db'); z_data['marker'].append('circle')
            z_gain /= np.abs(1 - c)
        z_source.data = z_data
        sys_disc = signal.dlti(z_zeros, z_poles, z_gain, dt=dt)
        t_d, y_d = signal.dstep(sys_disc, n=int(100/ts))
        step_z_source.data = {
            't': t_d.flatten(),
            'y': y_d[0].flatten()
        }
        
        w, mag, phase = signal.dbode(sys_disc, w=w_range*dt)
        bode_z_source.data = {'w': w, 'mag': np.power(10, mag/20), 'mag_db': mag, 'phase': phase}
        bode_dot_source.data = {'w': [2*np.pi/dt]}

    except ValueError as e:
        step_z_source.data = {'t': np.linspace(0, 100, 1000), 'y': np.zeros(1000)}
        print(f"Error discretizando: {e}")

    except Exception as e: print(f"Error discretizando: {e}")


# --- 3. INTERFAZ GRÁFICA ---
# Plano S
pz_plot = figure(title="PLANO S", x_range=(-2, 0.1), y_range=(-2, 2), width=400, height=400)
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
pz_plot.add_tools(PointDrawTool(renderers=[render_pz]))

# Plano Z
z_plot = figure(title="PLANO Z (Discreto)", x_range=(-1.5, 1.5), y_range=(-1.5, 1.5), width=400, height=400)
z_plot.ellipse(x='x', y='y', width='w', height='h', source=unit_circle_source, fill_alpha=0, line_color="black", line_dash="dotted")
z_plot.scatter('x', 'y', source=z_source, size=12, color='color', marker='marker', line_width=2)
method_select.on_change('value', update_all)

# Diagrama de Bode
bode_mag_plot = figure(title="RESPUESTA EN FRECUENCIA", x_axis_type='log', width=600, height=250, x_range=(1e-2, 1e2), y_range=(-40, 40))
bode_mag_plot.line('w', 'mag_db', source=bode_source, line_width=4, color="#3e5e7e")
# bode_mag_plot.scatter('w', 'mag', source=bode_dot_source, size=8, color="red", marker="square", line_width=3)
bode_mag_plot.line('w', 'mag_db', source=bode_z_source, line_width=3, color="red")
bode_mag_plot.segment(x0='w', y0=-40, x1='w', y1=40, source=bode_dot_source, color="red", line_dash="dotted")

step_response_plot = figure(title="RESPUESTA AL ESCALÓN", width=600, height=250, x_range=(0, 50), y_range=(-0.2, 2),)
step_response_plot.line('t', 'y', source=step_source, line_width=4, color="#3e5e7e")
step_response_plot.line('t', 1, source=step_source, line_width=1, color="#3e5e7e", dash="dashed")

# Por esto:
step_response_plot.step('t', 'y', source=step_z_source, color="firebrick", mode="after", line_width=2, legend_label="Discreto")

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
def clear_pz():
  setattr(pz_source, 'data', {'x':[],'y':[],'type':[],'mode':[],'pair_id':[],'color':[],'marker':[]})
  setattr(z_source, 'data', {'x':[],'y':[],'type':[],'mode':[],'pair_id':[],'color':[],'marker':[]})
btn_reset.on_click(clear_pz)

pz_source.on_change('data', update_all)
ts_slider.on_change('value', update_all)

# --- LAYOUT ---
sidebar = column(
    Div(text="<h2>Analizador LTI</h2>"),
    estabilidad_div,
    row(btn_p_r, btn_p_c), 
    row(btn_c_r, btn_c_c), 
    btn_reset, 
    method_select,
    ts_slider,
    spacing=10)
# bode_plot = column(bode_mag_plot, step_response_plot)

# --- LAYOUT ---
layout = column(
    row(Div(text="<h1>Herramienta Interactiva - Discretización</h1>")),
    row(
        sidebar, 
        column(pz_plot),
        column(z_plot),
        column(bode_mag_plot, step_response_plot)
    )
)


curdoc().add_root(layout)
curdoc().title = "Herramienta Interactiva: Polos, Ceros - Respuesta temporal y en frecuencia"
update_all(None, None, None)











# import numpy as np
# import scipy.signal as signal
# from bokeh.plotting import figure, curdoc
# from bokeh.models import ColumnDataSource, PointDrawTool, Button, Div, BoxAnnotation, HoverTool, Slider, Select
# from bokeh.layouts import row, column

# # --- 1. FUENTES DE DATOS ---
# # Plano S
# pz_source = ColumnDataSource(data={'x': [-0.5], 'y': [0.0], 'type': ['polo'], 'mode': ['real'], 
#                                    'pair_id': [99], 'color': ['#e74c3c'], 'marker': ['x']})

# # Plano Z
# z_source = ColumnDataSource(data={'x': [], 'y': [], 'type': [], 'color': [], 'marker': []})
# unit_circle_source = ColumnDataSource(data={'x': [0], 'y': [0], 'w': [2], 'h': [2]})

# # Auxiliares
# test_point_source = ColumnDataSource(data={'x': [0.0], 'y': [0.0]})
# vector_lines_source = ColumnDataSource(data={'xs': [], 'ys': []})
# bode_dot_source = ColumnDataSource(data={'w': [0.0], 'mag': [0.0], 'mag_db': [0.0], 'phase': [0.0]})
# w_range = np.logspace(-2, 2, 600)
# bode_source = ColumnDataSource(data={'w': w_range, 'mag': np.zeros(600), 'mag_db': np.zeros(600), 'phase': np.zeros(600)})
# step_source = ColumnDataSource(data={'t': np.linspace(0, 10, 1000), 'y': np.zeros(1000)})

# --- 3. LÓGICA DE CÁLCULO ---
# def update_all(attr, old, new):
#     d = dict(pz_source.data)
    
#     # Sincronización de simetría en plano S
#     changed = False
#     tol = 5e-2
#     for i in range(len(d['x'])):
#         if d['mode'][i] == 'real' and d['y'][i] != 0:
#             d['y'][i] = 0; changed = True
#         if d['mode'][i] == 'conjugado':
#             mid = d['pair_id'][i]
#             mx, my = d['x'][i], d['y'][i]
#             for j in range(len(d['x'])):
#                 if i != j and d['pair_id'][j] == mid:
#                     if d['x'][j] != mx or d['y'][j] != -my:
#                         d['x'][j], d['y'][j] = mx, -my; changed = True
    
#     if changed: 
#         pz_source.data = d
#         return

#     # Lógica de punto de prueba y frecuencia
#     tp = test_point_source.data
#     if attr == 'value' and not isinstance(new, str): # Viene de un slider numérico
#         w_test = freq_slider.value
#         test_point_source.data = {'x': [0.0], 'y': [w_test]}
#     else:
#         w_test = tp['y'][0]
#         freq_slider.value = w_test

#     # Cálculo del Sistema Analógico
#     polos = [complex(x, y) for x, y, t in zip(d['x'], d['y'], d['type']) if t == 'polo']
#     ceros = [complex(x, y) for x, y, t in zip(d['x'], d['y'], d['type']) if t == 'cero']
    
#     if not polos: polos = [-1000] # Evitar sistema vacío
#     k = np.real(np.prod([-p for p in polos]) / np.prod([-c for c in ceros])) if ceros else np.real(np.prod([-p for p in polos]))
#     sys_analog = signal.lti(ceros, polos, k)
    
#     # Respuesta en frecuencia (Bode)
#     w, mag, phase = signal.bode(sys_analog, w=w_range)
#     bode_source.data = {'w': w, 'mag': np.power(10, mag/20), 'mag_db': mag, 'phase': phase}
    
#     # Respuesta al escalón
#     try:
#         t, y = signal.step(sys_analog, T=np.linspace(0, 50, 1000)) 
#         step_source.data = {'t': t, 'y': y}
#     except: pass

#     # --- DISCRETIZACIÓN (PLANO Z) ---
#     ts = ts_slider.value
#     method = method_select.value
#     dt = 1.0 / ts
#     try:
#         # Convertir a espacio de estados para mayor estabilidad numérica
#         sys_disc = signal.cont2discrete((sys_analog.zeros, sys_analog.poles, sys_analog.gain), dt, method=method)
#         z_zeros = sys_disc[0]
#         z_poles = sys_disc[1]
        
#         z_data = {'x': [], 'y': [], 'type': [], 'color': [], 'marker': []}
#         for p in z_poles:
#             z_data['x'].append(p.real); z_data['y'].append(p.imag)
#             z_data['type'].append('polo'); z_data['color'].append('#e74c3c'); z_data['marker'].append('x')
#         for c in z_zeros:
#             z_data['x'].append(c.real); z_data['y'].append(c.imag)
#             z_data['type'].append('cero'); z_data['color'].append('#3498db'); z_data['marker'].append('circle')
#         z_source.data = z_data
#     except Exception as e: print(f"Error discretizando: {e}")

#     # UI y Estabilidad
#     estabilidad_div.text = "<b>SISTEMA:</b><br/>" + ("<span style='color:red'>INESTABLE ⚠️</span>" if any(p.real > 0 for p in polos) else "<span style='color:green'>ESTABLE ✅</span>")

# --- 4. INTERFAZ GRÁFICA ---
# Plano S
# pz_plot = figure(title="PLANO S (Analógico)", x_range=(-2, 0.5), y_range=(-2, 2), width=400, height=400)
# pz_plot.add_layout(BoxAnnotation(left=0, fill_color="yellow", fill_alpha=0.1))
# render_pz = pz_plot.scatter('x', 'y', source=pz_source, size=15, color='color', marker='marker', line_width=2)
# render_test = pz_plot.scatter('x', 'y', source=test_point_source, size=8, color="red", marker="square")
# pz_plot.add_tools(PointDrawTool(renderers=[render_pz, render_test]))


# Bode y Respuesta Temporal
# bode_mag_plot = figure(title="MAGNITUD BODE", x_axis_type='log', width=500, height=200, y_range=(0, 2))
# bode_mag_plot.line('w', 'mag', source=bode_source, line_width=3)
# step_plot = figure(title="RESPUESTA AL ESCALÓN", width=500, height=200)
# step_plot.line('t', 'y', source=step_source, line_width=3)

# --- BOTONES Y CALLBACKS ---
# def add_real(t): pz_source.stream({'x':[-0.5], 'y':[0.0], 'type':[t], 'mode':['real'], 'pair_id':[np.random.randint(1000)], 'color':['#e74c3c' if t=='polo' else '#3498db'], 'marker':['x' if t=='polo' else 'circle']})
# btn_p_r = Button(label="+ Polo Real", button_type="danger", width=100)
# btn_p_r.on_click(lambda: add_real('polo'))
# btn_c_r = Button(label="+ Cero Real", button_type="primary", width=100)
# btn_c_r.on_click(lambda: add_real('cero'))

# freq_slider = Slider(start=0, end=20, value=0, step=0.1, title="Frecuencia de prueba (rad/s)")
# pz_source.on_change('data', update_all)
# ts_slider.on_change('value', update_all)
# method_select.on_change('value', update_all)

# # --- LAYOUT ---
# layout = column(
#     row(Div(text="<h1>Asesor de Procesamiento de Señales - Analizador S/Z</h1>")),
#     row(
#         column(sidebar := column(estabilidad_div, method_select, ts_slider, row(btn_p_r, btn_c_r))),
#         column(pz_plot, freq_slider),
#         column(z_plot),
#         column(bode_mag_plot, step_plot)
#     )
# )

# curdoc().add_root(layout)
# update_all(None, None, None)