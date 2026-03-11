import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, RadioGroup, Div, BoxAnnotation
from bokeh.plotting import figure
from scipy.signal import butter, cheby1, cheby2, ellip, freqs

# Configuración
w_eval = np.logspace(1, 5, 1000) 

def get_filter_data(ftype, N, wc, wp, ws, rp, rs):
    try:
        if ftype == 0: # Butterworth
            b, a = butter(N, wc, btype='low', analog=True)
        elif ftype == 1: # Chebyshev I
            b, a = cheby1(N, rp, wp, btype='low', analog=True)
        elif ftype == 2: # Chebyshev II
            b, a = cheby2(N, rs, ws, btype='low', analog=True)
        else: # Elliptic
            b, a = ellip(N, rp, rs, wp, btype='low', analog=True)
            
        w, h = freqs(b, a, worN=w_eval)
        mag = 20 * np.log10(np.abs(h) + 1e-9)
        phase = np.angle(h, deg=True) # Fase en grados
        return w, mag, phase
    except:
        return w_eval, np.ones_like(w_eval)*-100, np.zeros_like(w_eval)

# Fuentes de datos
source = ColumnDataSource(data=dict(x=[], y_mag=[], y_phase=[]))
ticks_source = ColumnDataSource(data=dict(x=[], alpha_p=[], alpha_s=[]))

# Gráfica de Magnitud
p_mag = figure(title="Respuesta en Magnitud (dB)", width=500, height=400, 
               x_axis_type="log", x_range=(10, 1e5), y_range=(-60, 5))
p_mag.line('x', 'y_mag', source=source, line_width=2, color="navy")
p_mag.yaxis.axis_label = "Ganancia (dB)"
p_mag.line(x='wpd', y='w', source=ticks_source, line_width=2, color="red", line_dash="dotted", legend_label="𝛚ₚ")
p_mag.line(x='xp', y='alpha_pd', source=ticks_source, line_width=2, color="red", line_dash="dashed", legend_label="𝛼ₚ")
p_mag.line(x='wsd', y='w', source=ticks_source, line_width=2, color="blue", line_dash="dotted", legend_label="𝛚ₛ")
p_mag.line(x='xs', y='alpha_sd', source=ticks_source, line_width=2, color="blue", line_dash="dashed", legend_label="𝛼ₛ")

zona_paso = BoxAnnotation(left=10, right=1000, top=5, fill_alpha=0.1, fill_color="green")
zona_paso_mala = BoxAnnotation(left=10, right=1000, bottom=-60, fill_alpha=0.1, fill_color="red")
zona_stop = BoxAnnotation(left=8000, right=1e5, bottom=-60, fill_alpha=0.1, fill_color="green")
zona_stop_mala = BoxAnnotation(left=8000, right=1e5, top=5, fill_alpha=0.1, fill_color="red")
zona_transicion = BoxAnnotation(left=1000, right=8000, top=5, bottom=-60, fill_alpha=0.1, fill_color="grey")

p_mag.add_layout(zona_paso)
p_mag.add_layout(zona_paso_mala)
p_mag.add_layout(zona_stop)
p_mag.add_layout(zona_stop_mala)
p_mag.add_layout(zona_transicion)

# Gráfica de Fase
p_phase = figure(title="Respuesta en Fase (Grados)", width=500, height=300, 
                 x_axis_type="log", x_range=p_mag.x_range)
p_phase.line('x', 'y_phase', source=source, line_width=2, color="navy")
p_phase.yaxis.axis_label = "Fase (deg)"
p_phase.xaxis.axis_label = "Frecuencia (rad/s)"

# Controles
filter_selector = RadioGroup(labels=["Butterworth", "Chebyshev I", "Chebyshev II", "Elíptico"], active=0)
n_slider = Slider(title="Orden del Filtro (N)", value=5, start=1, end=20, step=1)
order_display = Div(text="<b>Orden actual: 5</b>") # Muestra el orden

wc_slider = Slider(title="𝛚꜀ [rad/s]", value=1000, start=100, end=5000, step=100)
wpd_slider = Slider(title="𝛚ₚ [rad/s]", value=1000, start=100, end=5000, step=100)
wsd_slider = Slider(title="𝛚ₛ [rad/s]", value=8000, start=2000, end=10000, step=100)
rpd_slider = Slider(title="𝛼ₚ [dB]", value=1.0, start=0.1, end=10.0, step=0.1)
rsd_slider = Slider(title="𝛼ₛ [dB]", value=40.0, start=10.0, end=60.0, step=1.0)

wp_slider = Slider(title="𝛚ₚ [rad/s]", value=1000, start=100, end=5000, step=100)
ws_slider = Slider(title="𝛚ₛ [rad/s]", value=8000, start=2000, end=10000, step=100)
rp_slider = Slider(title="𝛼ₚ [dB]", value=1.0, start=0.1, end=10.0, step=0.1)
rs_slider = Slider(title="𝛼ₛ [dB]", value=40.0, start=10.0, end=60.0, step=1.0)

def update(attr, old, new):
    ftype = filter_selector.active
    wc_slider.visible = (ftype == 0)
    wp_slider.visible = (ftype == 1 or ftype == 3)
    ws_slider.visible = (ftype == 2)
    rp_slider.visible = (ftype == 1 or ftype == 3)
    rs_slider.visible = (ftype == 2 or ftype == 3)

    N = n_slider.value
    wc, wp, ws = wc_slider.value, wp_slider.value, ws_slider.value
    wpd, wsd = wpd_slider.value, wsd_slider.value
    rp, rs = rp_slider.value, rs_slider.value
    rpd, rsd = rpd_slider.value, rsd_slider.value
    
    w, mag, phase = get_filter_data(ftype, N, wc, wp, ws, rp, rs)
    source.data = dict(x=w, y_mag=mag, y_phase=phase)
    ticks_source.data = dict(
        xp=[w_eval[0], wpd],
        xs=[w_eval[-1], wsd],
        x=[w_eval[0], w_eval[-1]], 
        alpha_p=[-rp, -rp], 
        alpha_s=[-rs, -rs],
        alpha_pd=[-rpd, -rpd], 
        alpha_sd=[-rsd, -rsd],
        wp=[wp, wp],
        ws=[ws, ws],
        wpd=[wpd, wpd],
        wsd=[wsd, wsd],
        wc=[wc, wc],
        w=[-60, 5]
    )

    zona_paso.right = wpd
    zona_paso.bottom = -rpd
    zona_paso_mala.right = wpd
    zona_paso_mala.top = -rpd
    zona_stop.left = wsd
    zona_stop.top = -rsd
    zona_stop_mala.left = wsd
    zona_stop_mala.bottom = -rsd
    zona_transicion.left = wpd
    zona_transicion.right = wsd

for control in [n_slider, wpd_slider, wsd_slider, rpd_slider, rsd_slider, wc_slider, wp_slider, ws_slider, rp_slider, rs_slider]:
    control.on_change('value', update)
filter_selector.on_change('active', update)

update(None, None, None)


spec_label = Div(text="""
    <b style="color: navy;">Especificación del diseño:</b> 
""", width=200)
params_label = Div(text="""
    <b style="color: navy;">Parámetros del diseño:</b> 
""", width=200)


layout = row(
    column(spec_label, wpd_slider, wsd_slider, rpd_slider, rsd_slider, 
    params_label, filter_selector, n_slider, wc_slider, wp_slider, ws_slider, rp_slider, rs_slider),
    column(p_mag)
)
curdoc().add_root(layout)
curdoc().title = "Diseño de Filtros"
