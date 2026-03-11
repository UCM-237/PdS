from bokeh.io import curdoc, output_file, save
from bokeh.layouts import column, row
from bokeh.plotting import figure
from bokeh.models import Slider, ColumnDataSource, CustomJS
import numpy as np

# Inicializar valores predeterminados
freq_fundamental = 1
amplitudes = [1] + [0.5] * 6  # Amplitud inicial para fundamental y armónicos
Ts = 1 / freq_fundamental / 50
N = 1024
M = 2*N
num_muestras_inicial = 500  # Número inicial de muestras
x = np.linspace(0, (N - 1) * Ts, N)

# Calcular señal compuesta
def calcular_senal(amplitudes):
    y = amplitudes[0] * np.sin(2 * np.pi * freq_fundamental * x)
    for i, amp in enumerate(amplitudes[1:], start=2):
        y += amp * np.sin(2 * np.pi * freq_fundamental * i * x)
    return y

# Calcular FFT
def calcular_fft(y, num_muestras):
    fft_y = np.fft.fft(y[:num_muestras], n=M) / M
    fft_freq = np.fft.fftfreq(M, d=Ts)
    return fft_freq, np.abs(fft_y)

# Señal inicial
y = calcular_senal(amplitudes)
fft_freq, fft_amplitud = calcular_fft(y, num_muestras_inicial)

# Crear ColumnDataSource
source = ColumnDataSource(data={'x': x, 'y': y})
source_fft = ColumnDataSource(data={'freq': fft_freq, 'amplitud': fft_amplitud})

# Crear figura para la señal
plot = figure(title="Señal Compuesta con Armónicos", width=800, height=200)
plot.line('x', 'y', source=source, line_width=2, color="blue")
plot.xaxis.axis_label = "Tiempo"
plot.yaxis.axis_label = "Amplitud"
plot.x_range.end = 4 / freq_fundamental  # Ajustar rango positivo

# Crear figura para la FFT
plot_fft = figure(title="FFT de la Señal", width=800, height=200)
plot_fft.line('freq', 'amplitud', source=source_fft, line_width=2, color="green")
plot_fft.xaxis.axis_label = "Frecuencia"
plot_fft.yaxis.axis_label = "Amplitud"
plot_fft.x_range.start = 0  # Ajustar rango de frecuencias negativas
plot_fft.x_range.end = freq_fundamental * 7.5  # Ajustar rango positivo

# Sliders para amplitudes de los armónicos
sliders = [
    Slider(start=0, end=2, value=amplitudes[i], step=0.1, title=f"Amplitud Armónico {i}")
    for i in range(7)
]

# Slider para el número de muestras
num_muestras_slider = Slider(start=5, end=5000, value=num_muestras_inicial, step=5, title="Número de Muestras")

# Callback en JavaScript para actualizar datos
callback = CustomJS(
    args=dict(source=source, source_fft=source_fft, sliders=sliders, num_muestras_slider=num_muestras_slider, x=x, Ts=Ts, freq_fundamental=freq_fundamental),
    code="""
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/mathjs/lib/browser/math.js';
    script.onload = function() {
        const N = 1024;
        const M = 2*N;
        const amplitudes = sliders.map(slider => slider.value);
        const num_muestras = num_muestras_slider.value;

        // Calcular la señal compuesta
        let y = new Array(N);
        let y_ = new Array(M).fill(0.0);
        for (let i = 0; i < x.length; i++) {
            y[i] = amplitudes[0] * Math.sin(2 * Math.PI * freq_fundamental * x[i]);
            for (let j = 1; j < amplitudes.length; j++) {
                y[i] += amplitudes[j] * Math.sin(2 * Math.PI * freq_fundamental * (j + 1) * x[i]);
            }
            if (i >= num_muestras) { continue; }
            y_[i] = y[i];
        }

        // Calcular la FFT
        const fft_y = math.fft(y_);
        const fft_spectrum = fft_y.map((complex) => math.abs(complex)/M);
        const fft_freq = new Array(y_.length);
        for (let i = 0; i < fft_freq.length; i++) { fft_freq[i] = i/M/Ts; }

        // Actualizar los datos
        source.data = { x, y };
        source_fft.data = { freq: fft_freq, amplitud: fft_spectrum };
        source.change.emit();
        source_fft.change.emit();
    };
    document.head.appendChild(script);
    """
)

# Asociar sliders con el callback en JavaScript
for slider in sliders:
    slider.js_on_change('value', callback)

num_muestras_slider.js_on_change('value', callback)

# Layout
layout = row(
    column(*sliders, num_muestras_slider),
    column(plot, plot_fft)
)

# Añadir el layout al documento
curdoc().add_root(layout)
curdoc().title = "Transformada de Fourier Discreta (DFT)"

# Especificar el archivo de salida HTML
output_file("../html/T3_DFT.html")

# Guardar el layout en el archivo HTML
save(layout)
