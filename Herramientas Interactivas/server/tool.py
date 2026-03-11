import logging
import json
from datetime import datetime

from bokeh.plotting import figure, curdoc
from bokeh.models import Div
from bokeh.layouts import row, column
from bokeh.events import PlotEvent, LODStart, LODEnd, Tap, Pan, PanStart, PanEnd, MouseWheel

class ITApp:

    def __init__(self, title="IT Tool"):
        self.title = title
        self._is_updating = False  # Flag global para evitar recursión
        self.sources = {}
        self.widgets = {}
        self.plots = []
        self.sidebar = []
        
        self._setup_logger()        
        self._setup_sources()
        self._setup_controls()
        self._setup_plots()

    def _setup_logger(self):
        """Configura el logger para grabar en archivo y consola."""
        self.logger = logging.getLogger(self.title)
        self.logger.setLevel(logging.INFO)
        
        # Evitar duplicados si se reinicia la app en el mismo proceso
        if not self.logger.handlers:
            fh = logging.FileHandler(f'logs/session_log_{datetime.now().strftime("%Y%m%d_%H%M")}.log')
            formatter = logging.Formatter('%(asctime)s | %(message)s')
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)
        
        action = {
            'event': 'SESSION_START',
            'source': 'APP',
            'data': self.title
        }
        self.logger.info(json.dumps(action))

    def _setup_sources(self):
        """Define los repositorios de datos"""

    def _setup_controls(self):
        """Configuración de la barra lateral"""

    def _setup_plots(self):
        """Aquí se definen y organizan los gráficos"""

    def add_plot(self, title, x_label, y_label, **kwargs):
        p = self.create_plot(title, x_label, y_label, **kwargs)
        self.plots.append(p)
        return p

    def create_plot(self, title, x_label, y_label, **kwargs):
        """Fábrica de gráficos con estilo consistente"""
        p = figure(title=title, x_axis_label=x_label, y_axis_label=y_label, 
                   tools="pan,wheel_zoom,reset,save", **kwargs)
        p.title.text_font_size = '10pt'
        self._register_plot_events(p)
        return p


    def _register_plot_events(self, plot):
        """Registra automáticamente interacciones táctiles y de ratón en una figura."""
        
        # 1. Registro de Zoom y Pan (Desplazamiento)
        # PanStart/End nos dice cuándo el usuario empieza y termina de mover la gráfica
        plot.on_event(PanEnd, lambda event: self.logger.info(
            json.dumps({
                "event": "PLOT_INTERACTION", 
                "source": plot.title.text, 
                "data": {
                    "TYPE": "Pan/Scroll", 
                    "RANGE": f"x:{plot.x_range.start:.2f}-{plot.x_range.end:.2f}"
                }
            })
        ))

        # 2. Registro de Clics (Tap)
        # Útil para saber si el usuario intenta interactuar con un área vacía
        plot.on_event(Tap, lambda event: self.logger.info(
            json.dumps({
                "event": "PLOT_INTERACTION", 
                "source": plot.title.text, 
                "data": {
                    "TYPE": "Tap", 
                    "COORDS": f"x:{event.x:.2f}, y:{event.y:.2f}"
                }
            })
        ))

        # 3. Registro de cambio de Herramientas
        # Si el usuario activa el Zoom, el Reset o el BoxSelect
        plot.toolbar.on_change('active_drag', lambda attr, old, new: self.logger.info(
            json.dumps({
                "event": "TOOL_CHANGE", 
                "source": plot.title.text, 
                "data": {
                    "TYPE": "Tap", 
                    "ACTIVE_TOOL": new.name if new else 'None'
                }
            })
        ))

    def add_source(self, name, source, trigger_update=False):
        """Registra una fuente de datos y le asigna el callback universal"""
        if trigger_update:
            def on_data_change(attr, old, new):
                self.logger.info(json.dumps({
                    'event': 'DATA_INTERACTION',
                    'source': name,
                    'data': list(new.keys()),
                }))
                self.update(attr, old, new)
            source.on_change('data', on_data_change)

        self.sources[name] = source

    def add_widget(self, name, widget):
        """Registra un widget y le asigna el callback universal"""
        try:
            prop = 'value' if hasattr(widget, 'value') else 'active'
            if prop == 'value':
                def on_value_change(attr, old, new):
                    self.logger.info(json.dumps({
                        'event': 'WIDGET_INTERACTION',
                        'source': name,
                        'data': { 'from': old, 'to': new },
                    }))
                    self.update(attr, old, new)
                widget.on_change('value', on_value_change)
        except Exception as e:
            print(f'Error horrible: {e}')

        self.widgets[name] = widget
        self.sidebar.append(widget)

    def set_layout(self, layout):
        base_width = 700
        base_height = 450
        for i in range(len(self.plots)):
            self.plots[i].width = base_width
            self.plots[i].height = base_height
        
        if layout == '1x1':
            self.plot_layout = self.plots[0]

        if layout == '2x1':
            self.plot_layout = column(self.plots[0], self.plots[1])

        if layout == '1x2':
            self.plot_layout = row(self.plots[0], self.plots[1])

        if layout == '2x2':
            self.plot_layout = column(row(self.plots[0], self.plots[1]), row(self.plots[2], self.plots[3]))

        if layout == '2lx1r':
            self.plots[2].height = 2*base_height
            self.plot_layout = row(column(self.plots[0], self.plots[1]), self.plots[2])
        
        if layout == '1lx2r':
            self.plots[0].height = 2*base_height
            self.plot_layout = row(self.plots[0], column(self.plots[1], self.plots[2]))

        if layout == '1ux2b':
            self.plots[0].width = 2*base_width
            self.plot_layout = column(self.plots[0], row(self.plots[1], self.plots[2]))

        if layout == '2ux1b':
            self.plots[2].width = 2*base_width
            self.plot_layout = column(row(self.plots[0], self.plots[1]), self.plots[2])
            
    def get_layout(self):
        """Retorna el layout final (Sidebar | Gráficos)"""
        return column(
            Div(text=f"<h2>{self.title}</h2>"),
            row(column(self.sidebar, width=300), self.plot_layout)
        )
    
    def log_custom_event(self, event_name, details, source='APP'):
        """Método para que las clases hijas graben eventos específicos (ej. clics en botones)."""
        action = {
            'event': event_name,
            'source': source,
            'data': details
        }
        self.logger.info(json.dumps(action))
    
    def start(self):
        """Inicia la aplicación"""
        curdoc().title = self.title
        curdoc().add_root(self.get_layout())
        self.update(None, None, None)

    def update(self, attr, old, new):
        """Lógica central de cálculo"""

    def _safe_update(self, attr, old, new):
        """Wrapper para proteger todas las subclases"""
        if self._is_updating:
            return
        self._is_updating = True
        try:
            self.update(attr, old, new)
        finally:
            self._is_updating = False
