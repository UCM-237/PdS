import numpy as np
import scipy.signal as signal
from bokeh.models import ColumnDataSource, Slider, Select
from tool import ITApp 

class PhaseDelayApp(ITApp):
  def __init__(self, title="Análisis de Retardo (α) y Desplazamiento de Fase (β)"):
    super().__init__(title)

  def _setup_sources(self):
    self.fs = 1000
    self.f_axis = np.linspace(0, self.fs/2, 1024)
        
    # 1. Coeficientes h[n] (Complejos/Reales)
    self.add_source('taps', ColumnDataSource(data={'n': [], 'h_real': [], 'h_imag': []}))
        
    # 2. Respuesta de Fase
    self.add_source('freq', ColumnDataSource(data={'f': [], 'mag': [], 'phase': []}))

  def _setup_controls(self):
    # Slider para alfa (retardo de grupo)
    alpha = Slider(start=0, end=50, value=20, step=0.1, title="Retardo de Grupo (α)")
        
    # Slider para beta (fase constante)
    # Usamos nombres descriptivos para los valores de pi
    beta = Slider(start=0, end=1, value=0, step=0.1, title="Fase Constante (β en múltiplos de π)")
        
    self.add_widget('alpha', alpha)
    self.add_widget('beta', beta)

  def _setup_plots(self):
    # Plot 1: Coeficientes del filtro (Parte Real)
    p1 = self.add_plot("RESPUESTA AL IMPULSO h[n]", "n", "Amplitud")
    p1.segment('n', 0, 'n', 'mag', source=self.sources['taps'], color="navy", legend_label="Real")
    p1.scatter('n', 'mag', source=self.sources['taps'], color="navy")
    # p1.line('n', 'original', source=self.sources['signal'], color="gray", line_dash="dotted", alpha=0.5)
    # p1.line('n', 'shifted', source=self.sources['signal'], color="firebrick", line_width=2)
    
    # Plot 2: Efecto sobre una portadora con envolvente (Visualización del desfase)
    p3 = self.add_plot("EFECTO SOBRE UNA SINUSOIDE", "Tiempo [n]", "Amplitud")
    p3.line('f', 'mag', source=self.sources['freq'], color="green", line_width=2)
    # p3.line('n', 'original', source=self.sources['signal'], color="gray", line_dash="dotted", alpha=0.5)
    # p3.line('n', 'shifted', source=self.sources['signal'], color="firebrick", line_width=2)

    # Plot 3: Fase (Linealidad)
    p2 = self.add_plot("RESPUESTA DE FASE ∠H(ω)", "Frecuencia [Hz]", "Fase [rad]")
    p2.line('n', 'phase', source=self.sources['taps'], color="navy", line_width=2)

    # Plot 4: Efecto sobre una portadora con envolvente (Visualización del desfase)
    p4 = self.add_plot("EFECTO SOBRE UNA SINUSOIDE", "Tiempo [n]", "Amplitud")
    p4.line('f', 'phase', source=self.sources['freq'], color="navy")
    
    self.set_layout('2x2')

  def update(self, attr, old, new):
    alpha = self.widgets['alpha'].value
    beta = self.widgets['beta'].value * np.pi
    
    # 1. Definimos la respuesta en frecuencia ideal H(w) = exp(-j * (alpha*w + beta))
    w = np.linspace(0, 2*np.pi, 64)
    h_freq = ((w - np.pi) < 1) * np.exp(-1j * (alpha * w + beta)) * (w < 1)
    
    # 2. Obtenemos la respuesta al impulso h[n] mediante IFFT
    h_time = np.fft.ifft(h_freq)
    
    # Actualizar fuentes
    self.sources['taps'].data = {'n': np.arange(len(h_time)), 'mag': np.abs(h_time), 'phase': np.angle(h_time)}
    self.sources['freq'].data = {'f': w * (self.fs/(2*np.pi)), 'mag': np.abs(h_freq), 'phase': np.angle(h_freq)}

app = PhaseDelayApp()
app.start()