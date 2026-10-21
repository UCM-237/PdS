import numpy as np
import scipy.signal as signal
from bokeh.models import ColumnDataSource, Slider, Div, Select, Range1d, LinearAxis
from tool import ITApp 

class ZeroPhaseFilterApp(ITApp):
    def __init__(self, title="Filtrado de Fase Cero."):
        super().__init__(title)
        self.set_layout('2ux1b')

    def _setup_sources(self):
        self.fs = 1000 
        self.t_axis = np.arange(400)
        # Fuentes para ver la respuesta en frecuencia y las señales temporales
        self.add_source('freq', ColumnDataSource(data={'f': [], 'mag_single': [], 'mag_double': []}))
        self.add_source('time', ColumnDataSource(data={'t': self.t_axis, 'original': [], 'single': [], 'zero_phase': []}))

    def _setup_controls(self):
        fc = Slider(start=1, end=100, value=90, step=1, title="Frecuencia de Corte (Hz)")
        order = Slider(start=10, end=150, value=40, step=2, title="Orden del Filtro (N)")
        
        self.add_widget('fc', fc)
        self.add_widget('order', order)

    def _setup_plots(self):
        # Plot 1: Respuesta en Magnitud (Simple vs Doble)
        p1 = self.create_plot("RESPUESTA EN MAGNITUD (dB)", "Frecuencia [Hz]", "Magnitud [dB]", x_range=(0, 100), y_range=(-80, 5))
        p1.line('f', 'mag_single', source=self.sources['freq'], color="gray", alpha=0.6, legend_label="Un solo paso")
        p1.line('f', 'mag_double', source=self.sources['freq'], color="navy", line_width=2, legend_label="Doble paso (filtfilt)")

        # Plot 2: Comparación de Fase (Conceptualmente, el doble paso es 0 rad)
        p2 = self.create_plot("RESPUESTA EN FASE (rad)", "Frecuencia [Hz]", "Fase [rad]", x_range=(0, 100))
        p2.line(x=[0, 100], y=[0, 0], color="navy", line_width=3, legend_label="Fase Cero (Simétrica)")
        p2.line('f', 'phase', source=self.sources['freq'], color="gray", line_width=2, legend_label="Doble paso (filtfilt)")
        # p2.div("En un filtrado de fase cero, la fase es estrictamente 0 para todas las frecuencias.")

        # Plot 3: El efecto en el tiempo (Alineación)
        p3 = self.create_plot("COMPARACIÓN TEMPORAL (ALINEACIÓN)", "Muestras", "Amplitud")
        # Add the second y-axis to the plot
        p3.line('t', 'original', source=self.sources['time'], color="olive", legend_label="Original")
        p3.line('t', 'single', source=self.sources['time'], color="firebrick", line_width=1, legend_label="Filtro Causal (Con Retraso)")
        p3.line('t', 'zero_phase', source=self.sources['time'], color="navy", line_width=1, legend_label="Fase Cero (Alineada)")
        
        self.plots.extend([p1, p2, p3])

    def update(self, attr, old, new):
        fc = self.widgets['fc'].value
        N = self.widgets['order'].value
        fsig = 15 

        # 1. Crear señal original (una sinusoide con un transitorio para ver el retraso)
        t = self.t_axis
        sig_original = np.sin(2 * np.pi * fsig * t / self.fs) + np.sin(2 * np.pi * 4 * fsig * t / self.fs)
        # Aplicamos una ventana para que la señal empiece y acabe en cero
        sig_original *= signal.windows.hann(len(t))

        # 2. Diseño del filtro FIR
        taps = signal.firwin(N + 1, fc/(self.fs/2), window='hamming')

        # 3. FILTRADO
        # Paso directo (causal)
        sig_single = signal.lfilter(taps, 1.0, sig_original)
        
        # Estilo 'filtfilt': Invertir -> Filtrar -> Invertir
        # Scipy tiene filtfilt, pero lo haremos "a mano" para ilustrar:
        sig_rev = sig_single[::-1]
        sig_rev_filt = signal.lfilter(taps, 1.0, sig_rev)
        sig_zero_phase = sig_rev_filt[::-1]

        # 4. Respuesta en frecuencia
        w, h = signal.freqz(taps, worN=512, fs=self.fs)
        mag_single = 20 * np.log10(np.abs(h) + 1e-8)
        # El efecto de pasar dos veces es elevar al cuadrado la magnitud (o doblar los dB)
        mag_double = 2 * mag_single 

        self.sources['freq'].data = {
            'f': w,
            'mag_single': mag_single,
            'mag_double': mag_double,
            'phase': np.unwrap(np.angle(h))
        }
        self.sources['time'].data = {
            't': t,
            'original': sig_original,
            'single': sig_single - 2,
            'zero_phase': sig_zero_phase + 2
        }

app = ZeroPhaseFilterApp()
app.start()