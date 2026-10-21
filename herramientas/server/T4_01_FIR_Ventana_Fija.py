import numpy as np
import scipy.signal as signal
from bokeh.models import ColumnDataSource, Slider, Select

from tool import ITApp 

class FIRDesignApp(ITApp):
    def __init__(self, title="Diseño de Filtros FIR (Método de la Ventana)"):
        super().__init__(title)
        # Layout: 2 arriba (u), 1 abajo (b)
        self.set_layout('2ux1b') 

    def _setup_sources(self):
        # Parámetros base
        self.N = 21 # Orden del filtro (puntos de la ventana)
        self.fs = 500
        self.f_axis = np.linspace(0, self.fs/2, 512)
        self.t_axis = np.arange(self.N) - (self.N - 1) / 2

        # Fuentes de datos
        self.add_source('ideal', ColumnDataSource(data={'f': [], 'mag': []}))
        self.add_source('window', ColumnDataSource(data={'t': [], 'val': []}))
        self.add_source('result_n', ColumnDataSource(data={'f': [], 'mag_db': []}))
        self.add_source('result_f', ColumnDataSource(data={'f': [], 'mag_db': []}))

    def _setup_controls(self):
        # Selectores de tipo
        filter_type = Select(title="Tipo de Filtro:", value="lowpass", 
                            options=[("lowpass", "Paso Bajo"), ("highpass", "Paso Alto"), 
                                     ("bandpass", "Paso Banda"), ("bandstop", "Supresor de Banda")])
        
        window_type = Select(title="Ventana:", value="boxcar", 
                            options=[("boxcar", "Rectangular"), ("hann", "Hanning"), 
                                     ("bartlett", "Bartlett"), ("hamming", "Hamming")])

        # Sliders de frecuencia
        fc1 = Slider(start=10, end=150, value=100, step=1, title="Frecuencia de Corte 1 (Hz)")
        fc2 = Slider(start=150, end=250, value=250, step=1, title="Frecuencia de Corte 2 (Hz)")
        order = Slider(start=11, end=127, value=21, step=2, title="Orden del Filtro (N)")

        self.add_widget('f_type', filter_type)
        self.add_widget('w_type', window_type)
        self.add_widget('fc1', fc1)
        self.add_widget('fc2', fc2)
        self.add_widget('order', order)

    def _setup_plots(self):
        # Plot 1: Ventana (Tiempo)
        p1 = self.create_plot("VENTANA SELECCIONADA (w[n])", "Muestras (n)", "Amplitud")
        p1.segment('t', 0, 't', 'val', source=self.sources['window'], color="navy", dash="dotted")
        p1.scatter(x='t', y='val', marker='circle', size=8, source=self.sources['window'], color="navy")

        # Plot 2: Respuesta al impulso (Magnitud vs Frecuencia)
        p2 = self.create_plot("FILTRO FIR (Respuesta al impulso - h[n])", "Muestras [n]", "Amplitud") #, x_range=(0, 128))
        p2.segment('n', 0, 'n', 'h', source=self.sources['result_n'], color="firebrick", dash="dotted")
        p2.scatter(x='n', y='h', source=self.sources['result_n'], marker='circle', size=8, color="firebrick")
        
        # Plot 3: Respuesta Resultante (Magnitud en dB)
        p3 = self.create_plot("FILTRO IDEAL vs. FIR", "Frecuencia [Hz]", "Magnitud [dB]", y_range=(-80, 5))
        p3.step('f', 'mag_db', source=self.sources['ideal'], color="black", line_width=3, dash="dashed", mode="center")
        p3.line('f', 'mag_db', source=self.sources['result_f'], line_width=3, color="black")

        self.plots.extend([p1, p2, p3])

    def update(self, attr, old, new):
        # 1. Obtener valores de la interfaz
        ft = self.widgets['f_type'].value
        wt = self.widgets['w_type'].value
        f1 = self.widgets['fc1'].value
        f2 = self.widgets['fc2'].value
        N = self.widgets['order'].value
        nyq = self.fs / 2

        # 2. Dibujar Filtro Ideal para visualización
        f_ideal = np.linspace(0, nyq, 1000)
        m_ideal = np.zeros_like(f_ideal)
        if ft == "lowpass":
            m_ideal[f_ideal <= f1] = 1
        elif ft == "highpass":
            m_ideal[f_ideal >= f1] = 1
        elif ft == "bandpass":
            m_ideal[(f_ideal >= f1) & (f_ideal <= f2)] = 1
        else: # bandstop
            m_ideal[(f_ideal <= f1) | (f_ideal >= f2)] = 1
        
        self.sources['ideal'].data = {'f': f_ideal, 'mag': m_ideal, 'mag_db': 20 * np.log10(m_ideal + 1e-10)}

        # 3. Calcular Ventana
        win = signal.get_window(wt, N)
        t_axis = np.arange(N) #- (N - 1) / 2
        self.sources['window'].data = {'t': t_axis, 'val': win}

        # 4. Diseño del filtro FIR (Convolución implícita via firwin)
        # firwin multiplica la sinc (ideal) por la ventana en tiempo
        try:
            if ft == "lowpass":
                taps = signal.firwin(N, f1/nyq, window=wt)
            elif ft == "highpass":
                taps = signal.firwin(N, f1/nyq, window=wt, pass_zero=False)
            elif ft == "bandpass":
                taps = signal.firwin(N, [f1/nyq, f2/nyq], window=wt, pass_zero=False)
            else: # bandstop
                taps = signal.firwin(N, [f1/nyq, f2/nyq], window=wt)

            w, h = signal.freqz(taps, worN=512, fs=self.fs)
            self.sources['result_n'].data = {
                'n': t_axis,
                'h': taps,
            }
            self.sources['result_f'].data = {
                'f': w, 
                'mag_db': 20 * np.log10(np.abs(h) + 1e-10)
            }
        except ValueError:
            pass # Evita errores si f1 >= f2 en banda-paso
        


app = FIRDesignApp()
app.start()