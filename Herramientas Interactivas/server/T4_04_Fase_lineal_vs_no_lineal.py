import numpy as np
import scipy.signal as signal
from bokeh.models import ColumnDataSource, Slider, Select, Div, HoverTool
from tool import ITApp 

class PhaseComparisonApp(ITApp):
    def __init__(self, title="Comparativa: Fase Lineal (FIR) vs Fase No Lineal (IIR)"):
        # Layout: h[n] y Fase (u), Señal en Tiempo (b)
        super().__init__(title)
        self.set_layout('2ux1b')

    def _setup_sources(self):
        self.fs = 2000 # Frecuencia de muestreo
        self.t_axis = np.arange(400) # 400 muestras de tiempo
        self.f_axis_hz = np.linspace(0, self.fs/2, 512)
        
        # 1. Respuestas de Fase
        self.add_source('filter', ColumnDataSource(data={'f': [], 'fir_dB': [], 'iir_dB': [], 'fir_rad': [], 'iir_rad': []}))
        
        # 2. Respuestas al Impulso h[n]
        self.add_source('taps', ColumnDataSource(data={'n': [], 'fir_h': [], 'iir_h': []}))
        
        # 3. Señales en el Tiempo
        self.add_source('time_signals', ColumnDataSource(data={'t': self.t_axis, 'orig': [], 'fir_out': [], 'iir_out': []}))

    def _setup_controls(self):
        # Parámetros del Filtro
        f_type = Select(title="Tipo de Filtro:", value="lowpass", options=["lowpass", "highpass"])
        fc = Slider(start=20, end=480, value=150, step=1, title="Frecuencia de Corte (Hz)")
        
        # Parámetros de la Señal Compuesta
        f1 = Slider(start=10, end=100, value=10, step=1, title="Frecuencia Componente 1 (Hz)")
        f2 = Slider(start=10, end=300, value=50, step=1, title="Frecuencia Componente 2 (Hz)")
        f3 = Slider(start=10, end=300, value=100, step=1, title="Frecuencia Componente 3 (Hz)")
        sig_type = Select(title="Forma de la señal:", value="sum", 
                         options=[("sum", "Suma de Sinusoides"), ("pulse", "Pulso Cuadrado")])

        self.add_widget('f_type', f_type)
        self.add_widget('fc', fc)
        self.add_widget('f1', f1)
        self.add_widget('f2', f2)
        self.add_widget('f3', f3)
        self.add_widget('sig_type', sig_type)

    def _setup_plots(self):
        # Plot 2: Respuestas al Impulso h[n] (Simetría)
        p1 = self.create_plot("2. RESPUESTAS AL IMPULSO h[n]", "Frecuencia [Hz]", "Amplitud [dB]", x_range=(0, 300), y_range=(-20, 2))
        p1.line('f', 'fir_dB', source=self.sources['filter'], color="navy", line_width=2, legend_label="FIR (Simétrico)")
        p1.line('f', 'iir_dB', source=self.sources['filter'], color="firebrick", line_width=2, legend_label="IIR (Asimétrico)")

        # Plot 1: Respuestas de Fase (Desenrollada)
        p2 = self.create_plot("1. RESPUESTA DE FASE (∠H(f))", "Frecuencia [Hz]", "Fase [rad]", x_range=(0, 200))
        p2.line('f', 'fir_rad', source=self.sources['filter'], color="navy", line_width=3, legend_label="FIR (Lineal)")
        p2.line('f', 'iir_rad', source=self.sources['filter'], color="firebrick", line_width=3, legend_label="IIR (No Lineal)")
        p2.add_tools(HoverTool(tooltips=[("F", "@f Hz"), ("FIR", "@fir_rad rad"), ("IIR", "@iir_rad rad")]))
        p2.legend.location = "bottom_left"

        
        # Plot 3: Señales en el Tiempo (Distorsión de fase)
        p3 = self.create_plot("3. SEÑAL COMPUESTA (EFECTO DE LA FASE)", "Tiempo [muestras]", "Amplitud", x_range=(0, 400))
        p3.line('t', 'original', source=self.sources['time_signals'], color="gray", line_dash="dashed", line_width=2, legend_label="Original")
        p3.line('t', 'filtered', source=self.sources['time_signals'], color="olive", line_dash="dotted", line_width=4, legend_label="Filtrada")
        p3.line('t', 'fir_out', source=self.sources['time_signals'], color="navy", line_width=2, legend_label="Salida FIR")
        p3.line('t', 'iir_out', source=self.sources['time_signals'], color="firebrick", line_width=2, legend_label="Salida IIR")
        p3.legend.location = "top_right"

        self.plots.extend([p1, p2, p3])

    def update(self, attr, old, new):
        fc = self.widgets['fc'].value
        f_type = self.widgets['f_type'].value
        f1 = self.widgets['f1'].value
        f2 = self.widgets['f2'].value
        f3 = self.widgets['f3'].value
        s_type = self.widgets['sig_type'].value
        nyq = self.fs / 2

        # --- 1. Diseño de Filtros ---
        # A) FIR de Fase Lineal (Orden fijo alto para que sea comparable con IIR)
        N_fir = 51
        taps_fir = signal.firwin(N_fir, fc/nyq, pass_zero="lowpass", window="hamming")

        # B) IIR (Butterworth) de Fase No Lineal (Mismo orden aproximado de rechazo)
        b_iir, a_iir = signal.butter(11, fc/nyq, btype=f_type) # Orden 4

        # --- 2. Cálculo de Fase y h[n] ---
        # Fase (Filtro h[n] completo para IIR)
        w, h_fir = signal.freqz(taps_fir, worN=512, fs=self.fs)
        w, h_iir = signal.freqz(b_iir, a_iir, worN=512, fs=self.fs)
        
        # h[n] (Truncada para IIR para visualización)
        h_fir_n = taps_fir
        h_iir_n = signal.impulse((b_iir, a_iir), N=len(taps_fir)+50)[1]

        # --- 3. Generación y Filtrado de la Señal ---
        t = self.t_axis
        if s_type == "sum":
            # Suma de dos sinusoides
            sig_original = 0.6 * np.sin(2 * np.pi * f1 * t / self.fs) + \
                       0.4 * np.sin(2 * np.pi * f2 * t / self.fs) + \
                       0.3 * np.sin(2 * np.pi * f3 * t / self.fs)
            sig_filtered = 0.6 * np.sin(2 * np.pi * f1 * t / self.fs) + \
                       0.4 * np.sin(2 * np.pi * f2 * t / self.fs)
        else:
            # Un pulso cuadrado (rico en armónicos)
            sig_original = signal.square(2 * np.pi * 5 * t / self.fs) # Pulso de 5Hz
            
        # Filtrado (lfilter introduce el retardo causal)
        sig_fir_out = signal.lfilter(taps_fir, 1.0, sig_original)
        sig_iir_out = signal.lfilter(b_iir, a_iir, sig_original)

        # --- 4. Actualizar ColumnDataSources ---
        self.sources['filter'].data = {
            'f': w,
            'fir_dB': 20*np.log10(np.abs(h_fir)),
            'iir_dB': 20*np.log10(np.abs(h_iir)),
            'fir_rad': np.unwrap(np.angle(h_fir)),
            'iir_rad': np.unwrap(np.angle(h_iir))
        }
        self.sources['taps'].data = {
            'n': np.arange(len(h_iir_n)),
            'fir_h': np.pad(h_fir_n, (0, len(h_iir_n)-len(h_fir_n))), # Relleno con ceros
            'iir_h': h_iir_n
        }
        self.sources['time_signals'].data = {
            't': t,
            'original': sig_original,
            'filtered' : sig_filtered,
            'fir_out': sig_fir_out,
            'iir_out': sig_iir_out
        }

app = PhaseComparisonApp()
app.start()