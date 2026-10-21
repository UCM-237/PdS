"""Hito 4: series, clasificación y entrega. Completa las partes marcadas con TODO."""
from utilidades import cargar_actividad, guardar_prueba

# TODO: STFT de la velocidad de una sesión de series (scipy.signal.stft), bloque de series y
#       periodo con la autocorrelación.
# TODO: estados parado / andando / corriendo y reglas para el tipo de sesión.

resultados = {}
for fichero in ("prueba_1.csv", "prueba_2.csv", "prueba_3.csv"):
    d = cargar_actividad(fichero)
    resultados[fichero] = ("Rodaje", [])      # TODO: tu clasificación y tus cambios de ritmo
guardar_prueba(resultados)
