# 🛠️ Herramientas Interactivas de Procesamiento de Señales

Este repositorio contiene un laboratorio virtual interactivo diseñado para explorar conceptos avanzados de procesamiento digital de señales (DSP), tales como el diseño de filtros FIR/IIR, análisis de fase lineal, retardo de grupo y manipulación de audio.

El objetivo de las herramientas es ayudar 
a visualizar gráfica e interactivamente conceptos importantes del procesamiento de señales. Todo el código proporcionado es experimental y está en constante desarrollo y mejora, y puede contener errores o imprecisiones. 

## 📋 Requisitos Previos
Antes de ejecutar las herramientas, asegúrate de tener instalado Python 3.8+ y las dependencias necesarias. Se recomienda encarecidamente el uso de un entorno virtual.

Instalación de dependencias
Bash
### Actualizar pip
python -m pip install --upgrade pip

### Instalar librerías base
pip install numpy scipy bokeh pandas librosa

### 1. Instalación de librerías base
```bash
pip install numpy scipy bokeh pandas
```
```

## 🚀 Formas de Ejecución
El proyecto está organizado en tres formatos para adaptarse a diferentes necesidades de desarrollo y presentación:

1. Formato Notebook (/notebook)
Ideal para entornos educativos y prototipado rápido.

Archivos: .ipynb

Ejecución: Abrir con Jupyter Lab, Jupyter Notebook o VS Code (con extensión de Jupyter). Las gráficas de Bokeh se renderizarán directamente en las celdas de salida.

2. Formato Standalone (/standalone y /html)
Visualizaciones portátiles que no requieren un servidor de Python activo para ser consultadas.

Archivos: .py (generadores) y .html (resultados).

Ejecución: - Abre los archivos .html directamente en cualquier navegador.

Para generar un nuevo HTML desde el código, ejecuta: python standalone/nombre_app.py.

3. Formato Server (/server) 🌟
Es el modo más robusto. Permite cálculos pesados en tiempo real (filtrado dinámico de audio, animaciones complejas) conectando el front-end con el motor de Python.

Archivos: .py

Ejecución: ```bash
bokeh serve --show server/nombre_app.py

La aplicación se abrirá automáticamente en http://localhost:5006.


# 🛠️ Estructura del Proyecto
tool.py: Clase base ITApp que gestiona el layout, el logging de interacción y la estructura común de las aplicaciones.

/server: Aplicaciones que requieren el motor de Python activo para cálculos dinámicos.

/notebook: Guías interactivas para uso educativo.

/html: Versiones exportadas de las herramientas para consulta rápida sin dependencias.

📝 Guía Paso a Paso (Inicio Rápido)
Clona el repositorio:

```Bash
git clone https://github.com/tu-usuario/nombre-del-repo.git
cd nombre-del-repo
```
Configura el entorno:

``Bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```
Lanza tu primera herramienta (ejemplo de Fase Lineal):


#### 📋 Requisitos Previos

Las herramientas requieren **Python 3.8+**. Se recomienda el uso de un entorno virtual para gestionar las dependencias.


📂 Estructura del Repositorio
tool.py: Núcleo del proyecto. Contiene la clase ITApp que estandariza el layout, la gestión de fuentes de datos (ColumnDataSource) y el registro automático de eventos.

/server: Scripts optimizados para el servidor de Bokeh (ej. Comparativa FIR/IIR, Análisis de Fase).

/notebook: Tutoriales interactivos y experimentos de diseño.

/html: Exportaciones estáticas listas para su visualización.

interaccion_usuario.log: Archivo generado automáticamente que registra cambios en sliders, carga de archivos y telemetría de las gráficas.

📝 Guía de Inicio Rápido
Clonar el repositorio:

Bash
git clone [https://github.com/tu-usuario/dsp-interactive-lab.git](https://github.com/tu-usuario/dsp-interactive-lab.git)
cd dsp-interactive-lab
Ejecutar el explorador de Fase Lineal:

Bash
bokeh serve --show server/FIRPhaseLinearityApp.py
Consultar logs:
Después de interactuar con la herramienta, abre session_log_YYYYMMDD.log para revisar la trazabilidad de los parámetros ajustados.