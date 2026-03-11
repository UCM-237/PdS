import numpy as np
from bokeh.io import curdoc, save
from bokeh.layouts import column, row
from bokeh.models import CustomJS, Slider
from bokeh.plotting import ColumnDataSource, figure, output_notebook, output_file, show
output_notebook()

n = np.arange(0, 20)
f = 1
C = 1
r = 1
theta = 0
#x = C*np.exp(r*n) * np.exp(1j*2*np.pi*f*n+theta)
x = (r**n) * np.exp(1j*2*np.pi*f*n+theta)

source = ColumnDataSource(data=dict(t=n, x=np.real(x), x_t=np.abs(x), x_b=-np.abs(x)))

p = figure(width=300, height=300, tools=['hover','save'], x_axis_label='Muestra (n)', y_axis_label='x(n)', title='Exponencial Discreta')
p.xaxis.axis_label_text_font_size = '14px'
p.yaxis.axis_label_text_font_size = '14px'
p.circle(x='t', y='x', source=source, line_color='red', line_width=2)
p.line(x='t', y='x_t', source=source, line_color='blue', line_width=1)
p.line(x='t', y='x_b', source=source, line_color='blue', line_width=1)

amp_slider = Slider(start=0.0, end=1.2, value=1, step=.1, title="Amplitud (\u03b1)")
freq_slider = Slider(start=0.0, end=1, value=1, step=.05, title="Frecuencia (f)")
phase_slider = Slider(start=0, end=2*np.pi, value=0, step=.1, title="Fase (phi)")

callback = CustomJS(args=dict(source=source, amp=amp_slider, freq=freq_slider, phase=phase_slider),
                    code="""
    const data = source.data;
    const r = amp.value;
    const f = freq.value;
    const theta = phase.value;
    const t = data['t'];
    const x = data['x'];
    const x_t = data['x_t'];
    const x_b = data['x_b'];
    for (var i = 0; i < t.length; i++) {
        x[i] = Math.pow(r, t[i])*Math.cos(2*Math.PI*f*t[i]+theta);
        x_t[i] = +Math.abs(Math.pow(r, t[i]));
        x_b[i] = -Math.abs(x_t[i]);
    }
    source.change.emit();
""")
amp_slider.js_on_change('value', callback)
freq_slider.js_on_change('value', callback)
phase_slider.js_on_change('value', callback)

layout = row(p, column(amp_slider, freq_slider, phase_slider))
curdoc().title = "PdS - Exponencial discreta"
output_file('../html/T1_Exponencial compleja discreta.html')
save(layout)