import numpy as np
import scipy.signal as signal
from bokeh.models import ColumnDataSource, PointDrawTool, Button, Div, BoxAnnotation, HoverTool, Slider, Select
from bokeh.layouts import row, column, layout

from tool import ITApp

class IIRDiscretizationApp(ITApp):

  def __init__(self, title):
    super().__init__(title)

    self.set_layout('2x2')

  def _setup_sources(self):
    self.w_range = np.logspace(-2, 2, 600)
    # --- FUENTES DE DATOS ---
    self.add_source('pz', ColumnDataSource(data={'x': [], 'y': [], 'type': [], 'mode': [], 'pair_id': [], 'color': [], 'marker': []}), trigger_update=True)
    self.add_source('z', ColumnDataSource(data={'x': [], 'y': [], 'type': [], 'color': [], 'marker': []}))
    self.add_source('unit_circle', ColumnDataSource(data={'x': [0], 'y': [0], 'w': [2], 'h': [2]}))
    self.add_source('vector_lines', ColumnDataSource(data={'xs': [], 'ys': []}))
    self.add_source('bode_dot', ColumnDataSource(data={'w': [0.0], 'mag': [0.0], 'mag_db': [0.0], 'phase': [0.0]}))
    self.add_source('bode', ColumnDataSource(data={'w': self.w_range, 'mag': np.zeros(600), 'mag_db': np.zeros(600), 'phase': np.zeros(600)}))
    self.add_source('bode_z', ColumnDataSource(data={'w': self.w_range, 'mag': np.zeros(600), 'mag_db': np.zeros(600), 'phase': np.zeros(600)}))
    self.add_source('step', ColumnDataSource(data={'t': np.linspace(0, 10, 1000), 'y': np.zeros(1000)}))
    self.add_source('step_z', ColumnDataSource(data={'t': np.linspace(0, 10, 1000), 'y': np.zeros(1000)}))

  def _setup_controls(self):
    """ Crea la interfaz de control """
    method_select = Select(title="Método de Discretización:", value="impulse", 
                          options=[("bilinear", "Transformada Bilineal"), 
                                    ("impulse", "Invarianza al Impulso")])
    ts_slider = Slider(start=0.1, end=10, value=1, step=0.01, title="Periodo de Muestreo (Ts) [s]", width=400)
    estabilidad_div = Div(text="ESTABLE", width=200)

    self.add_widget('estabilidad', estabilidad_div)
    self.add_widget('ts', ts_slider)
    self.add_widget('method', method_select)

    # --- BOTONES Y CALLBACKS ---
    def add_real(t):
        self.sources['pz'].stream({'x':[-0.5], 'y':[0.0], 'type':[t], 'mode':['real'], 'pair_id':[np.random.randint(1000)], 
                          'color':['#e74c3c' if t=='polo' else '#3498db'], 'marker':['x' if t=='polo' else 'circle']})

    def add_conj(t):
        nid = np.random.randint(1000)
        self.sources['pz'].stream({'x':[-0.5, -0.5], 'y':[0.5, -0.5], 'type':[t, t], 'mode':['conjugado', 'conjugado'], 
                          'pair_id':[nid, nid], 'color':['#e74c3c']*2 if t=='polo' else ['#3498db']*2, 'marker':['x']*2 if t=='polo' else ['circle']*2})

    def clear_pz():
      setattr(self.sources['pz'], 'data', {'x':[],'y':[],'type':[],'mode':[],'pair_id':[],'color':[],'marker':[]})
      setattr(self.sources['z'], 'data', {'x':[],'y':[],'type':[],'mode':[],'pair_id':[],'color':[],'marker':[]})

    btn_p_r = Button(label="✕ Polo Real", button_type="danger")
    btn_p_r.on_click(lambda: add_real('polo'))
    btn_c_r = Button(label="○ Cero Real", button_type="primary")
    btn_c_r.on_click(lambda: add_real('cero'))
    btn_p_c = Button(label="✕✕ Par Polos Conj.", button_type="danger")
    btn_p_c.on_click(lambda: add_conj('polo'))
    btn_c_c = Button(label="○○ Par Ceros Conj.", button_type="primary")
    btn_c_c.on_click(lambda: add_conj('cero'))
    btn_reset = Button(label="↺ Reiniciar", button_type="warning", width=200)
    btn_reset.on_click(clear_pz)

    self.add_widget('buttons', column(row(btn_p_r, btn_p_c), row(btn_c_r, btn_c_c), btn_reset))


  def _setup_plots(self):
    """Aquí se definen y organizan los gráficos"""    
 
    # Plano S
    pz_plot = self.create_plot("PLANO S", "Real", "Imag", x_range=(-2, 0.1), y_range=(-2, 2))
    pz_plot.add_layout(BoxAnnotation(left=0, fill_color="yellow", fill_alpha=0.1))
    pz_plot.xaxis.fixed_location = 0
    pz_plot.xaxis.axis_line_dash = "dotted"
    pz_plot.xaxis.axis_line_width = 1
    pz_plot.yaxis.fixed_location = 0
    pz_plot.yaxis.axis_line_dash = "dotted"
    pz_plot.yaxis.axis_line_width = 1
    # Líneas de vectores (Discontinuas)
    pz_plot.multi_line('xs', 'ys', source=self.sources['vector_lines'], color="gray", line_dash="dashed", line_alpha=0.6)
    # Polos y Ceros
    render_pz = pz_plot.scatter('x', 'y', source=self.sources['pz'], size=15, color='color', fill_color=None, marker='marker', line_width=2)
    pz_plot.add_tools(PointDrawTool(renderers=[render_pz]))
    self.plots.append(pz_plot)

    # Plano Z
    z_plot = self.create_plot("PLANO Z (Discreto)", "Real", "Imag", x_range=(-1.5, 1.5), y_range=(-1.5, 1.5))
    z_plot.ellipse(x='x', y='y', width='w', height='h', source=self.sources['unit_circle'], fill_alpha=0, line_color="black", line_dash="dotted")
    z_plot.scatter('x', 'y', source=self.sources['z'], size=12, color='color', marker='marker', line_width=2)
    self.plots.append(z_plot)

    # Diagrama de Bode
    bode_mag_plot = self.create_plot("RESPUESTA EN FRECUENCIA", "Frecuencia [rad/s]", "Magnitud [dB]", x_axis_type='log', x_range=(1e-2, 1e2), y_range=(-40, 40))
    bode_mag_plot.line('w', 'mag_db', source=self.sources['bode'], line_width=4, color="#3e5e7e")
    bode_mag_plot.line('w', 'mag_db', source=self.sources['bode_z'], line_width=3, color="red")
    bode_mag_plot.segment(x0='w', y0=-40, x1='w', y1=40, source=self.sources['bode_dot'], color="red", line_dash="dotted")
    self.plots.append(bode_mag_plot)

    step_response_plot = self.create_plot("RESPUESTA AL ESCALÓN", "Tiempo [s]", "Amplitud", x_range=(0, 50), y_range=(-0.2, 2))
    step_response_plot.line('t', 'y', source=self.sources['step'], line_width=4, color="#3e5e7e")
    step_response_plot.line('t', 1, source=self.sources['step'], line_width=1, color="#3e5e7e", dash="dashed")
    self.plots.append(step_response_plot)

    # Por esto:
    step_response_plot.step('t', 'y', source=self.sources['step_z'], color="firebrick", mode="after", line_width=2, legend_label="Discreto")


  def update(self, attr, old, new):
    # --- 2. LÓGICA DE CÁLCULO Y VECTORES ---
    d = dict(self.sources['pz'].data)

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
        self.sources['pz'].data = d
        return

    # Respuesta en frecuencia y punto en Bode
    polos = [complex(x, y) for x, y, t in zip(d['x'], d['y'], d['type']) if t == 'polo']
    ceros = [complex(x, y) for x, y, t in zip(d['x'], d['y'], d['type']) if t == 'cero']
    
    # Ganancia unitaria k = prod(polos)/prod(ceros)
    k = np.real(np.prod([-p for p in polos]) / np.prod([-c for c in ceros])) if ceros else np.real(np.prod([-p for p in polos]))
    sys = signal.lti(ceros, polos, k)
    
    w, mag, phase = signal.bode(sys, w=self.w_range)
    self.sources['bode'].data = {'w': w, 'mag': np.power(10, mag/20), 'mag_db': mag, 'phase': phase}

    try:
        t, y = signal.step(sys, T=np.linspace(0, 100, 1000)) 
        self.sources['step'].data = {'t': t, 'y': y}
    except ValueError as e:
        self.sources['step'].data = {'t': np.linspace(0, 10, 1000), 'y': np.zeros(1000)}
    
    self.widgets['estabilidad'].text = "<b>SISTEMA:</b><br/>" + ("<span style='color:red'>INESTABLE ⚠️</span>" if any(p.real > 0 for p in polos) else "<span style='color:green'>ESTABLE ✅</span>")
    self.widgets['estabilidad'].text += ("<span style='color:red'>NO REALIZABLE ⚠️</span>" if len(polos) < len(ceros) else "<span style='color:green'>REALIZABLE ✅</span>")

    # --- DISCRETIZACIÓN (PLANO Z) ---
    ts = self.widgets['ts'].value
    method = self.widgets['method'].value
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
        self.sources['z'].data = z_data
        sys_disc = signal.dlti(z_zeros, z_poles, z_gain, dt=dt)
        t_d, y_d = signal.dstep(sys_disc, n=int(100/ts))
        self.sources['step_z'].data = {
            't': t_d.flatten(),
            'y': y_d[0].flatten()
        }
        
        w, mag, phase = signal.dbode(sys_disc, w=self.w_range*dt)
        self.sources['bode_z'].data = {'w': w, 'mag': np.power(10, mag/20), 'mag_db': mag, 'phase': phase}
        self.sources['bode_dot'].data = {'w': [2*np.pi/dt]}

    except ValueError as e:
        self.sources['step_z'].data = {'t': np.linspace(0, 100, 1000), 'y': np.zeros(1000)}
        print(f"Error discretizando: {e}")

    except Exception as e: print(f"Error discretizando: {e}")

app = IIRDiscretizationApp(title="Herramienta Interactiva: Polos, Ceros - Respuesta temporal y en frecuencia")
app.start()