# Material de teoría: transparencias, apuntes y ejercicios (XeLaTeX).
#
#   make T1, make T2    compila todo el tema
#   make figuras        regenera las figuras de todos los temas (Python)
#   make prueba-codigo  ejecuta los ejemplos en Python y en Matlab/Octave
#   make publicar       copia los PDF a clase/
#   make limpiar        borra los ficheros auxiliares de LaTeX
#
# Requisitos: TeX Live con XeLaTeX y latexmk, fuentes Fira y Libertinus,
# Python 3 con numpy, scipy y matplotlib, y Octave con los paquetes
# signal y control (solo para probar el código Matlab).

TEMAS   := T1 T2
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

limpiar:
	@for t in $(TEMAS); do \
	  for d in transparencias apuntes ejercicios; do \
	    [ -d $$t/$$d ] && (cd $$t/$$d && latexmk -c -silent >/dev/null 2>&1); \
	  done; \
	done; true
