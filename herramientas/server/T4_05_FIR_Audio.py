# import numpy as np
# import scipy.signal as signal
# from bokeh.models import ColumnDataSource, Slider, Select
# from tool import ITApp 

# class FilterSpecApp(ITApp):

#         # 2. Diseño del Filtro FIR (Ventana Hamming)
#         taps = signal.firwin(N + 1, fc_val/(self.fs/2), window='hamming')
#         sig_out = signal.lfilter(taps, 1.0, sig_in)

#         # 3. Respuesta en Frecuencia para el gráfico
#         w, h = signal.freqz(taps, worN=512, fs=self.fs)
        
#         # Simular PSD del ruido para el sombreado del gráfico
#         noise_viz = np.zeros_like(w)
#         noise_viz[(w > fn-bwn/2) & (w < fn+bwn/2)] = 0 # En dB, 0 es el máximo en esta visualización

#         self.sources['freq'].data = {'f': w, 'mag': 20*np.log10(np.abs(h)+1e-8), 'noise_psd': noise_viz}
#         self.sources['time'].data = {'t': t, 'input': sig_in, 'output': sig_out}

# app = FilterSpecApp()
# app.start()

import numpy as np
import scipy.signal as signal
import librosa
from bokeh.models import ColumnDataSource, Slider, Select, FileInput, Div
from io import BytesIO
import base64
from tool import ITApp 

class FilterSpecApp(ITApp):
  def __init__(self, title="Análisis de Audio y Filtros FIR"):
    super().__init__(title)
    self.set_layout('2ux1b')

  def _setup_sources(self):
    self.fs = 48000    # Frecuencia de muestreo por defecto de librosa
    # 1. Señal de audio (con ruido)
    self.add_source('signal', ColumnDataSource(data={'t': [], 'y': []}))

    # 2. Espectro de Frecuencia (Welch o FFT)
    self.add_source('spectrum', ColumnDataSource(data={'f': [], 'original_db': [], 'filtered_db': [], 'filter_db': []}))
    
    # 3. Visualización de la Ventana FIR
    self.add_source('filter', ColumnDataSource(data={'n': [], 'h': []}))
      
  def _setup_controls(self):
    # Cargador de archivos
    file_input = FileInput(accept=".mp3,.wav")
    file_input.on_change('value', self._on_file_upload)

    # Controles del Filtro
    f_type = Select(title="Tipo de Filtro:", value="lowpass", 
                    options=[("lowpass", "Paso Bajo"), ("highpass", "Paso Alto"),
                             ("bandpass", "Paso Banda"), ("bandstop", "Supresor de Banda"),])
    fc1 = Slider(start=20, end=self.fs/2, value=self.fs/2-100, step=100, title="Frecuencia de Corte 1 (Hz)")
    fc2 = Slider(start=20, end=self.fs/2, value=self.fs/2-100, step=100, title="Frecuencia de Corte 2 (Hz)")
    order = Slider(start=12, end=502, value=12, step=2, title="Orden del Filtro (N)")
    
    win_type = Select(title="Ventana:", value="boxcar", 
                      options=[("boxcar", "Rectangular"), ("hamming", "Hamming"), 
                               ("hann", "Hanning"), ("blackman", "Blackman"),
                               ("kaiser", "Kaiser")])
    beta = Slider(start=0, end=14, value=5, step=0.5, title="Beta (Kaiser)")

    # Controles del RUIDO (Interferencia)
    f_noise = Slider(start=500, end=15000, value=10000, step=100, title="Frecuencia Central Ruido (Hz)")
    bw_noise = Slider(start=100, end=2000, value=10, step=100, title="Ancho de Banda Ruido (Hz)")
    amp_noise = Slider(start=0, end=1.5, value=0.1, step=0.05, title="Amplitud Ruido")

    # 3. Widget de estado para mostrar info del audio
    
    self.status_div = Div(text=self._decorate_text(
      'Por favor, selecciona un archivo MP3.',
      text_color="#667eea",
      background_color=("#e8f4f8", "#d4eef8")
    ))
    self.noise_div = Div(text=self._decorate_text(
      'Modifica la frecuencia, el ancho de banda y la amplitud del ruido.',
      text_color="#ff6b35",
      background_color=("#f8e8e8", "#f8d4d4")
    ))
    self.filter_div = Div(text=self._decorate_text(
      'Modifica el tipo, las frecuencias de corte y el orden del filtro.',
      text_color="#ff6b35",
      background_color=("#f8e8e8", "#f8d4d4")
    ))
  
    self.add_widget('status', self.status_div)
    self.add_widget('file', file_input)
    self.add_widget('noise', self.noise_div)
    self.add_widget('f_noise', f_noise)
    self.add_widget('bw_noise', bw_noise)
    self.add_widget('amp_noise', amp_noise)
    self.add_widget('filter', self.filter_div)
    self.add_widget('f_type', f_type)
    self.add_widget('fc1', fc1)
    self.add_widget('fc2', fc2)
    self.add_widget('order', order)
    self.add_widget('win', win_type)
    self.add_widget('beta', beta)

  def _decorate_text(self, text, text_color="#667eea", background_color=("#e8f4f8", "#d4eef8")):
    return f'<div style="background: linear-gradient(to right, {background_color[0]}, {background_color[1]}); padding: 15px; border-left: 4px solid {text_color}; margin: 10px 0; border-radius: 6px;"> <strong style="color: {text_color};">{text}</strong></div>'

  def _setup_plots(self):
    # Plot 1: Coeficientes del filtro
    p1 = self.create_plot("COEFICIENTES DEL FILTRO - h[n]", "Muestras", "Amplitud")
    p1.segment('n', 0, 'n', 'h', source=self.sources['filter'], color="navy", dash="dotted")
    p1.scatter('n', 'h', source=self.sources['filter'], color="navy", marker='circle', size=6)

    # Plot 2: Espectro de frecuencia del filtro
    p2 = self.create_plot("ESPECTRO DE POTENCIA (PSD) DEL FILTRO", "Frecuencia [Hz]", "Magnitud [dB]", 
                          x_axis_type="log", y_range=(-60, 20))
    p2.line('f', 'filter_db', source=self.sources['spectrum'], color="navy", line_width=2, legend_label="Filtrado")

    # Plot 1: Espectro de Frecuencia (Escala Logarítmica)
    p3 = self.create_plot("ESPECTRO DE POTENCIA (PSD) DEL AUDIO ORIGINAL Y FILTRADO", "Frecuencia [Hz]", "Magnitud [dB]", 
                          x_axis_type="linear", y_range=(-60, 20))
    p3.line('f', 'original_db', source=self.sources['spectrum'], color="black", alpha=0.4, legend_label="Original")
    p3.line('f', 'filtered_db', source=self.sources['spectrum'], color="firebrick", line_width=2, legend_label="Filtrado")
    p3.line('f', 'filter_db', source=self.sources['spectrum'], color="navy", line_width=2, dash="dotted", legend_label="Filtro")
    
    self.plots.extend([p1, p2, p3])

  def _on_file_upload(self, attr, old, new):
    """Callback genérico de ITApp para la carga con Librosa."""
    try:
      # Decodificar el archivo desde base64/bytes
      file_contents = base64.b64decode(new)
      file_io = BytesIO(file_contents)

      # Carga con librosa (mono=True por defecto)
      y, self.fs = librosa.load(file_io, sr=None)
      t = np.arange(len(y))
      f = np.linspace(0, self.fs/2, 512)

      duracion = librosa.get_duration(y=y, sr=self.fs)
      self.status_div.text = self._decorate_text(f"<b>Audio:</b> {duracion:.2f}s | <b>SR:</b> {self.fs}Hz")
      
      # Ajustar el máximo del slider de frecuencia de corte dinámicamente
      self.widgets['fc1'].end = self.fs / 2
      self.widgets['fc2'].end = self.fs / 2

      self.sources['signal'].data = {'t': t, 'y': y}

      self.log_custom_event("LIBROSA_LOAD", f"Archivo cargado: {duracion:.2f}s, SR={self.fs}")
      self.update(None, None, None)
        
    except Exception as e:
      self.status_div.text = f"<b>Error al cargar:</b> {str(e)}"

  def update(self, attr, old, new):
    N = self.widgets['order'].value
    fc1 = self.widgets['fc1'].value
    fc2 = self.widgets['fc2'].value
    wt = self.widgets['win'].value
    ft = self.widgets['f_type'].value
    beta = self.widgets['beta'].value
    fn = self.widgets['f_noise'].value
    bwn = self.widgets['bw_noise'].value
    an = self.widgets['amp_noise'].value
    t = self.sources['signal'].data['t']
    y = self.sources['signal'].data['y']
    fm = self.fs / 2

    if y is None or len(y) == 0:
      return

    # 1. Generar Ruido de Banda Estrecha
    # Filtramos ruido blanco con un pasobanda para crear la interferencia
    white_noise = np.random.normal(0, 1, len(t))
    if fn-bwn/2 < 0:
      fcn = (fn + bwn/2) / (self.fs/2)
      ftn = 'lowpass'
    elif fn + bwn/2 > self.fs/2:
      fcn = (fn - bwn/2)  / (self.fs/2)
      ftn = 'highpass'
    else:
      fcn = [(fn - bwn/2)/(self.fs/2), (fn + bwn/2)/(self.fs/2)]
      ftn = 'bandpass'

    b_noise = signal.firwin(101, fcn, window='hamming', pass_zero=ftn)
    narrow_noise = signal.lfilter(b_noise, 1, white_noise) * an # Escalado para visibilidad
    signal_noise = y + narrow_noise

    # 2. Diseño del Filtro FIR
    # self.widgets['beta'].active = True if wt == 'kaiser' else False
    window = ('kaiser', beta) if wt == 'kaiser' else wt
    fc = fc1/fm if (ft == 'lowpass' or ft == 'highpass') else (fc1/fm, fc2/fm)
    taps = signal.firwin(N + 1, fc, window=window, pass_zero=ft)

    # 3. Análisis Espectral (Usando Welch para mejor visualización en Bokeh)
    # Nperseg se ajusta para tener una resolución decente
    f, psd_original = signal.welch(signal_noise, fs=self.fs, nperseg=4096)

    # 4. Respuesta del filtro para superponerla al espectro
    w_filt, h_filt = signal.freqz(taps, worN=len(f), fs=self.fs)
    psd_filter = psd_original * (np.abs(h_filt)**2)
    psd_filtered = (np.abs(h_filt)**2)

    # 5. Actualización de ColumnDataSources
    self.sources['filter'].data = {
      'n': np.arange(len(taps)),
      'h': taps
    }

    # 6. Convertimos a dB usando la lógica de librosa (referencia al máximo)
    self.sources['spectrum'].data = {
      'f': f[1:], # Evitar DC
      'original_db': librosa.power_to_db(psd_original[1:], ref=np.max),
      'filtered_db': librosa.power_to_db(psd_filter[1:], ref=np.max),
      'filter_db': librosa.power_to_db(psd_filtered[1:], ref=np.max)
    }
    

app = FilterSpecApp()
app.start()