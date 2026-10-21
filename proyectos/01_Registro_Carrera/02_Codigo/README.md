# Código — Registro de carrera

## Instalación

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Para compilar la memoria a PDF también hace falta `pdflatex` (TeX Live). `pypandoc_binary` ya trae `pandoc`.

## Uso

Desde esta carpeta:

```bash
python generar_entrega.py      # ejecuta los 4 hitos y prepara 04_Entrega_Final/
python hito1_analisis.py       # o cada hito por separado
python hito2_preprocesado.py
python hito3_caracteristicas.py
python hito4_deteccion.py
```

Cada script guarda sus figuras en `03_Hitos/Hito_N_*/figuras/` y sus tablas en `03_Hitos/Hito_N_*/resultados.md`. `generar_entrega.py` además copia las figuras de la memoria, escribe `04_Entrega_Final/resumen_indicadores.csv` y compila `Memoria.pdf`.

## Estructura

| Fichero | Contenido |
|---|---|
| `carrera/carga.py` | lectura de los CSV de `01_Datos/` y rutas del proyecto |
| `carrera/preprocesado.py` | huecos, outliers (Hampel + límite físico), meseta de FC, corrección de distancia, remuestreo, filtros (EMA, Butterworth fase cero, mediana), PSD de Welch |
| `carrera/caracteristicas.py` | ritmo, zonas de FC, desnivel con histéresis, pendiente, deriva cardiaca, parciales, resumen por sesión |
| `carrera/deteccion.py` | estados parado/andando/corriendo, cambios de ritmo (derivada+MAD y segmentación binaria), métricas de validación, clasificador de sesión |
| `carrera/sintetico.py` | generador de sesiones sintéticas con verdad conocida (para validar) |
| `carrera/analisis.py` | cadena completa: carga → preprocesado → características → detección |
| `carrera/graficas.py` | estilo común de las figuras |
| `hitoN_*.py` | figuras y tablas de cada hito |
| `generar_entrega.py` | ejecuta todo y prepara la entrega |

## Uso como librería

```python
from carrera import carga, analisis
r = analisis.analizar(carga.cargar_actividad("../01_Datos/actividad_2026-01-11.csv"))
r["resumen"]      # indicadores
r["cortes"]       # índices (1 Hz) de los cambios de ritmo
r["estados"]      # 0 parado, 1 andando, 2 corriendo
```

Los resultados son deterministas: las señales sintéticas usan semillas fijas.
