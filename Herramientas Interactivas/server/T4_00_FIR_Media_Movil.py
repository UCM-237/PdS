import numpy as np
import scipy.signal as signal
from bokeh.models import ColumnDataSource, Slider, HoverTool
from bokeh.layouts import gridplot
from tool import ITApp 

class MovingAverageApp(ITApp):
    def __init__(self, title="Explorador de Filtro de Media Móvil (Moving Average)"):
        super().__init__(title)
        self.set_layout('2ux1b')

    def _setup_sources(self):
        self.t_axis = np.arange(500)
        
        # 1. Respuesta al impulso
        self.add_source('taps', ColumnDataSource(data={'n': [], 'h': []}))

        # 2. Respuesta en Frecuencia
        self.add_source('freq_resp', ColumnDataSource(data={'w': [], 'mag': [], 'phase': []}))
        
        # 3. Señales en el Tiempo
        self.add_source('time_signals', ColumnDataSource(data={'t': self.t_axis, 'original': [], 'filtered': []}))

    def _setup_controls(self):
        L = Slider(start=2, end=100, value=10, step=1, title="Longitud del filtro (L)")
        noise = Slider(start=0, end=1.0, value=0.3, step=0.1, title="Amplitud del Ruido")
        
        self.add_widget('L', L)
        self.add_widget('noise', noise)

    def _setup_plots(self):
        # Plot 1: Magnitud (Respuesta tipo Sinc)
        p1 = self.create_plot("RESPUESTA EN MAGNITUD (dB)", "Muestra [n]", "Amplitud")
        p1.segment('n', 0, 'n', 'h', source=self.sources['taps'], color="navy", dash="dotted",line_width=2)
        p1.scatter('n', 'h', source=self.sources['taps'], color="navy", marker='circle', size=6, line_width=2)
        
        # Plot 2: Fase (Lineal con saltos)
        p2 = self.create_plot("RESPUESTA EN FRECUENCIA", "Frecuencia [rad/muestra]", "Amplitud [dB]", y_range=(-40, 5))
        p2.line('w', 'mag', source=self.sources['freq_resp'], color="firebrick", line_width=2)

        # Plot 3: Dominio del Tiempo
        p3 = self.create_plot("SUAVIZADO EN EL TIEMPO", "Muestras", "Amplitud")
        p3.line('t', 'original', source=self.sources['time_signals'], color="gray", alpha=0.5, legend_label="Entrada + Ruido")
        p3.line('t', 'filtered', source=self.sources['time_signals'], color="navy", line_width=2, legend_label="Salida Filtrada")
        
        self.plots.extend([p1, p2, p3])

    def update(self, attr, old, new):
        L = self.widgets['L'].value
        noise = self.widgets['noise'].value
        f_sig = 0.01
        
        # --- 1. Definición del Filtro de Media Móvil ---
        # h[n] = 1/L para n=0..L-1
        h = np.ones(L) / L
        
        # --- 2. Respuesta en Frecuencia ---
        w, freq_h = signal.freqz(h, worN=1024, fs=2*np.pi)
        mag = 20 * np.log10(np.abs(freq_h) + 1e-10)
        phase = np.angle(freq_h) # Mostramos fase con saltos para ver la inversión de signo
        
        # --- 3. Generación de Señal y Filtrado ---
        t = self.t_axis
        sig_clean = np.sin(2 * np.pi * f_sig * t)
        noise = np.random.normal(0, noise, len(t))
        sig_original = sig_clean + noise
        
        # Usamos mode='same' para que la salida tenga el mismo tamaño y esté centrada
        sig_filtered = signal.lfilter(h, 1.0, sig_original)

        # --- 4. Actualización de datos ---
        self.sources['taps'].data = {'n': np.arange(len(h)), 'h': h}
        self.sources['freq_resp'].data = {'w': w, 'mag': mag, 'phase': phase}
        self.sources['time_signals'].data = {'t': t, 'original': sig_original, 'filtered': sig_filtered}

app = MovingAverageApp()
app.start()