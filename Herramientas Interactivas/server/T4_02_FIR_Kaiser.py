import numpy as np
import scipy.signal as signal
from bokeh.models import ColumnDataSource, Slider, Select
from tool import ITApp 

class KaiserFilterApp(ITApp):
  def __init__(self, title="Filtros FIR: Ventana de Kaiser y Respuesta en Frecuencia"):
    super().__init__(title)
    self.set_layout('2ux1b')

  def _setup_sources(self):
    self.fs = 1000
    self.f_axis = np.linspace(0, self.fs/2, 512)
    
    # 1. Ventana Kaiser w[n]
    self.add_source('window', ColumnDataSource(data={'n': [], 'w': []}))
    
    # 2. Respuesta al Impulso h[n]
    self.add_source('taps', ColumnDataSource(data={'n': [], 'h': []}))
    
    # 3. Respuesta en Frecuencia H(f)
    self.add_source('freq_resp', ColumnDataSource(data={'f': [], 'mag_db': []}))

  def _setup_controls(self):
    # Parámetros específicos de Kaiser
    order = Slider(start=10, end=200, value=64, step=2, title="Orden del Filtro (N)")
    beta = Slider(start=0, end=14, value=5, step=0.5, title="Parámetro Beta (β)")
    fc = Slider(start=20, end=480, value=125, step=1, title="Frecuencia de Corte (Hz)")
    
    # Selector de tipo de filtro
    f_type = Select(title="Tipo:", value="lowpass", 
                    options=[("lowpass", "Paso Bajo"), ("highpass", "Paso Alto")])

    self.add_widget('order', order)
    self.add_widget('beta', beta)
    self.add_widget('fc', fc)
    self.add_widget('f_type', f_type)

  def _setup_plots(self):
    # Plot 1: La Ventana (Dominio del tiempo)
    p1 = self.create_plot("VENTANA DE KAISER w[n]", "n", "Amplitud")
    p1.segment('n', 0, 'n', 'w', source=self.sources['window'], color="navy", dash="dotted")
    p1.circle('n', 'w', source=self.sources['window'], color="navy", size=4)

    # Plot 2: Respuesta al Impulso h[n]
    p2 = self.create_plot("RESPUESTA AL IMPULSO h[n]", "n", "h[n]")
    p2.segment('n', 0, 'n', 'h', source=self.sources['taps'], color="firebrick", dash="dotted")
    p2.scatter('n', 'h', source=self.sources['taps'], color="firebrick", size=4)

    # Plot 3: Magnitud en Frecuencia (dB)
    p3 = self.create_plot("MAGNITUD EN FRECUENCIA |H(f)|", "Frecuencia [Hz]", "Magnitud [dB]", y_range=(-100, 5))
    p3.line('f', 'mag_db', source=self.sources['freq_resp'], color="black", line_width=2)
    
    # Línea de referencia a -3dB y Frecuencia de corte
    self.add_source('ref', ColumnDataSource(data={'x': [], 'y': []}))
    p3.line('x', 'y', source=self.sources['ref'], color="gray", line_dash="dashed")

    self.plots.extend([p1, p2, p3])

  def update(self, attr, old, new):
    N = self.widgets['order'].value
    beta = self.widgets['beta'].value
    fc = self.widgets['fc'].value
    ft = self.widgets['f_type'].value
    nyq = self.fs / 2

    # 1. Calcular Ventana de Kaiser
    # w = kaiser(M, beta) donde M es el número de puntos
    w = signal.windows.kaiser(N + 1, beta)
    n_axis = np.arange(N + 1)
    self.sources['window'].data = {'n': n_axis, 'w': w}

    # 2. Diseñar Filtro FIR con esa ventana
    taps = signal.firwin(N + 1, fc/nyq, window=('kaiser', beta), pass_zero=(ft == "lowpass"))
    self.sources['taps'].data = {'n': n_axis, 'h': taps}

    # 3. Respuesta en frecuencia
    f, h = signal.freqz(taps, worN=1024, fs=self.fs)
    mag_db = 20 * np.log10(np.abs(h) + 1e-10)
    self.sources['freq_resp'].data = {'f': f, 'mag_db': mag_db}
    
    # Actualizar referencia
    self.sources['ref'].data = {'x': [fc, fc], 'y': [-100, 5]}

app = KaiserFilterApp()
app.start()