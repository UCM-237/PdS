# Material de teoría: transparencias, apuntes y ejercicios (XeLaTeX).
#
#   make T1 ... make T6 compila todo el tema
#   make figuras        regenera las figuras de todos los temas (Python)
#   make prueba-codigo  ejecuta los ejemplos en Python y en Matlab/Octave
#   make publicar       copia los PDF a clase/
#   make limpiar        borra los ficheros auxiliares de LaTeX
#
# Requisitos: TeX Live con XeLaTeX y latexmk, fuentes Fira y Libertinus,
# Python 3 con numpy, scipy y matplotlib, y Octave con los paquetes
# signal y control (solo para probar el código Matlab).

TEMAS   := T1 T2 T3 T4 T5 T6
LATEXMK := latexmk -xelatex -interaction=nonstopmode -halt-on-error -silent

.PHONY: all $(TEMAS) figuras prueba-codigo publicar limpiar

all: $(TEMAS)

# Cada tema compila los .tex de transparencias/, apuntes/ y ejercicios/
$(TEMAS):
	@for d in transparencias apuntes ejercicios; do \
	  for f in $@/$$d/*.tex; do \
	    [ -f "$$f" ] || continue; \
	    echo "  $$f"; \
	    (cd $$(dirname "$$f") && $(LATEXMK) $$(basename "$$f")) || exit 1; \
	  done; \
	done

figuras:
	@for t in $(TEMAS); do (cd $$t/figuras && python3 generar_figuras.py); done

prueba-codigo:
	@for t in $(TEMAS); do comun/probar_codigo.sh $$t || exit 1; done

# Nombres de los PDF publicados en clase/
publicar: $(TEMAS)
	cp "T1/transparencias/T1-01-Senales.pdf"      "clase/T1 - 01 - Señales.pdf"
	cp "T1/transparencias/T1-02-Operaciones.pdf"  "clase/T1 - 02 - Operaciones.pdf"
	cp "T1/transparencias/T1-03-Sistemas.pdf"     "clase/T1 - 03 - Sistemas.pdf"
	cp "T1/transparencias/T1-04-Aplicaciones.pdf" "clase/T1 - 04 - Aplicaciones.pdf"
	cp "T1/apuntes/T1-Apuntes.pdf"                "clase/T1 - Apuntes.pdf"
	cp "T1/ejercicios/T1-Ejercicios.pdf"          "clase/T1 - Ejercicios.pdf"
	cp "T1/ejercicios/T1-Ejercicios-Soluciones.pdf" "clase/T1 - Ejercicios resueltos.pdf"
	cp "T2/transparencias/T2-01-Muestreo.pdf"     "clase/T2 - 01 - Muestreo.pdf"
	cp "T2/transparencias/T2-02-Reconstruccion.pdf" "clase/T2 - 02 - Reconstrucción.pdf"
	cp "T2/transparencias/T2-03-Cuantificacion.pdf" "clase/T2 - 03 - Cuantificación.pdf"
	cp "T2/transparencias/T2-04-MuestreoDiscreto.pdf" "clase/T2 - 04 - Muestreo discreto.pdf"
	cp "T2/apuntes/T2-Apuntes.pdf"                "clase/T2 - Apuntes.pdf"
	cp "T2/ejercicios/T2-Ejercicios.pdf"          "clase/T2 - Ejercicios.pdf"
	cp "T2/ejercicios/T2-Ejercicios-Soluciones.pdf" "clase/T2 - Ejercicios resueltos.pdf"
	cp "T3/transparencias/T3-01-DFT.pdf"          "clase/T3 - 01 - DFT.pdf"
	cp "T3/transparencias/T3-02-Propiedades.pdf"  "clase/T3 - 02 - Propiedades.pdf"
	cp "T3/transparencias/T3-03-AnalisisEspectral.pdf" "clase/T3 - 03 - Análisis espectral.pdf"
	cp "T3/transparencias/T3-04-FFT.pdf"          "clase/T3 - 04 - FFT.pdf"
	cp "T3/apuntes/T3-Apuntes.pdf"                "clase/T3 - Apuntes.pdf"
	cp "T3/ejercicios/T3-Ejercicios.pdf"          "clase/T3 - Ejercicios.pdf"
	cp "T3/ejercicios/T3-Ejercicios-Soluciones.pdf" "clase/T3 - Ejercicios resueltos.pdf"
	cp "T4/transparencias/T4-01-Introduccion.pdf" "clase/T4 - 01 - Introducción.pdf"
	cp "T4/transparencias/T4-02-FiltrosContinuos.pdf" "clase/T4 - 02 - Filtros continuos.pdf"
	cp "T4/transparencias/T4-03-FiltrosIIR.pdf"   "clase/T4 - 03 - Filtros IIR.pdf"
	cp "T4/transparencias/T4-04-FiltrosFIR.pdf"   "clase/T4 - 04 - Filtros FIR.pdf"
	cp "T4/transparencias/T4-05-FiltrosEspeciales.pdf" "clase/T4 - 05 - Filtros especiales.pdf"
	cp "T4/apuntes/T4-Apuntes.pdf"                "clase/T4 - Apuntes.pdf"
	cp "T4/ejercicios/T4-Ejercicios.pdf"          "clase/T4 - Ejercicios.pdf"
	cp "T4/ejercicios/T4-Ejercicios-Soluciones.pdf" "clase/T4 - Ejercicios resueltos.pdf"
	cp "T5/transparencias/T5-01-STFT.pdf"         "clase/T5 - 01 - STFT.pdf"
	cp "T5/transparencias/T5-02-Wavelets.pdf"     "clase/T5 - 02 - Wavelets.pdf"
	cp "T5/transparencias/T5-03-Imagenes.pdf"     "clase/T5 - 03 - Imágenes.pdf"
	cp "T5/apuntes/T5-Apuntes.pdf"                "clase/T5 - Apuntes.pdf"
	cp "T5/ejercicios/T5-Ejercicios.pdf"          "clase/T5 - Ejercicios.pdf"
	cp "T5/ejercicios/T5-Ejercicios-Soluciones.pdf" "clase/T5 - Ejercicios resueltos.pdf"
	cp "T6/transparencias/T6-01-VariablesAleatorias.pdf" "clase/T6 - 01 - Variables aleatorias.pdf"
	cp "T6/transparencias/T6-02-VariasVariables.pdf" "clase/T6 - 02 - Varias variables.pdf"
	cp "T6/transparencias/T6-03-SenalesAleatorias.pdf" "clase/T6 - 03 - Señales aleatorias.pdf"
	cp "T6/transparencias/T6-04-AnalisisEspectral.pdf" "clase/T6 - 04 - Análisis espectral.pdf"
	cp "T6/apuntes/T6-Apuntes.pdf"                "clase/T6 - Apuntes.pdf"
	cp "T6/ejercicios/T6-Ejercicios.pdf"          "clase/T6 - Ejercicios.pdf"
	cp "T6/ejercicios/T6-Ejercicios-Soluciones.pdf" "clase/T6 - Ejercicios resueltos.pdf"

limpiar:
	@for t in $(TEMAS); do \
	  for d in transparencias apuntes ejercicios; do \
	    [ -d $$t/$$d ] && (cd $$t/$$d && latexmk -c -silent >/dev/null 2>&1); \
	  done; \
	done; true
