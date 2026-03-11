import numpy as np
import scipy.signal as signal
from bokeh.models import ColumnDataSource, Slider, Select, Button
from bokeh.layouts import column, row
from tool import ITApp 

class FIRDelayApp(ITApp):
  def __init__(self, title="Explorador de Retardo FIR y Fase Lineal"):
    super().__init__(title)
    # Layout: Entrada (u), Filtro (u), Comparativa (b)
    self.set_layout('2ux1b')

  def _setup_sources(self):
    self.N_points = 500  # Puntos de la señal de entrada
    x_init = np.linspace(0, self.N_points-1, self.N_points)
    y_init = np.sin(2*np.pi*10*x_init/self.N_points) #np.where((x_init > 15) & (x_init < 35), 1.0, 0.0) # Pulso inicial

    # 1. Señal Dibujable
    self.add_source('input', ColumnDataSource(data={'x': x_init, 'y': y_init}))
    
    # 2. Respuesta al Impulso del Filtro
    self.add_source('filter', ColumnDataSource(data={'n': [], 'h': []}))
    
    # 3. Comparativa de señales (Original vs Filtrada)
    self.add_source('output', ColumnDataSource(data={'n': x_init, 'original': y_init, 'filtered': y_init}))

  def _setup_controls(self):
    # Control del filtro
    order = Slider(start=2, end=256, value=20, step=2, title="Orden del Filtro (N)")
    fc = Slider(start=0.01, end=0.49, value=0.1, step=0.01, title="Frecuencia de Corte (Norm.)")
    win = Select(title="Ventana:", value="hamming", options=[("boxcar", "Rectangular"), ("hamming", "Hamming"), ("hann", "Hanning"), ("blackman", "Blackman"), ("bartlett", "Bartlett")])
    
    # Botón para limpiar dibujo
    btn_reset = Button(label="Resetear Señal", button_type="warning")
    btn_reset.on_click(lambda: self.sources['input'].patch({'y': [(i, 0.0) for i in range(self.N_points)]}))

    self.add_widget('order', order)
    self.add_widget('fc', fc)
    self.add_widget('win', win)
    self.add_widget('reset', btn_reset)

  def _setup_plots(self):
    # Plot 1: Entrada
    p1 = self.create_plot("1. SEÑAL DE ENTRADA", "Muestra [n]", "Amplitud", y_range=(-1.2, 1.2))
    p1.segment('x', 0, 'x', 'y', source=self.sources['input'], color="navy", line_dash="dotted", alpha=0.3)
    p1.scatter('x', 'y', source=self.sources['input'], size=6, color="navy")
    p1.line('x', 'y', source=self.sources['input'], color="navy", line_dash="dotted")

    # Plot 2: Filtro FIR (h[n])
    p2 = self.create_plot("2. RESPUESTA AL IMPULSO (FIR)", "Muestra [n]", "h[n]")
    p2.segment('n', 0, 'n', 'h', source=self.sources['filter'], color="firebrick", line_dash="dotted")
    p2.scatter('n', 'h', source=self.sources['filter'], color="firebrick", size=6)

    # Plot 3: Comparativa (Retardo)
    p3 = self.create_plot("3. SEÑAL ORIGINAL vs FILTRADA", "Muestra [n]", "Amplitud")
    p3.segment('n', 0, 'n', 'original', source=self.sources['output'], color="navy", line_dash="dotted", alpha=0.3)
    p3.scatter('n', 'original', source=self.sources['output'], color="navy", size=6, legend_label="Original")
    p3.segment('n', 0, 'n', 'filtered', source=self.sources['output'], color="firebrick", line_dash="dotted", alpha=0.3)
    p3.scatter('n', 'filtered', source=self.sources['output'], color="firebrick", size=6, legend_label="Filtrada")
    p3.legend.location = "top_left"

    self.plots.extend([p1, p2, p3])

  def update(self, attr, old, new):
    # 1. Obtener parámetros del filtro
    N = self.widgets['order'].value
    fc = self.widgets['fc'].value
    wt = self.widgets['win'].value
    
    # 2. Diseñar el filtro FIR
    taps = signal.firwin(N + 1, fc, window=wt)
    self.sources['filter'].data = {'n': np.arange(len(taps)), 'h': taps}

    # 3. Obtener señal dibujada y filtrar
    x_in = np.array(self.sources['input'].data['y'])
    
    # Aplicamos el filtro (lfilter introduce el retardo causal)
    y_out = signal.lfilter(taps, 1.0, x_in)

    # 4. Calcular el retardo teórico para información (opcional)
    delay = N / 2
    
    # 5. Actualizar gráfica comparativa
    self.sources['output'].data = {
        'n': np.arange(self.N_points),
        'original': x_in,
        'filtered': y_out
    }

app = FIRDelayApp()
app.start()