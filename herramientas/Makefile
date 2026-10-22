# Herramientas interactivas (Bokeh).
#
#   make            genera html/Tn-*.html y html/index.html (Bokeh desde la CDN)
#   make sin-red    igual, con Bokeh incrustado en cada página
#   make limpiar    borra las páginas generadas
#
# Requisitos: pip install -r requirements.txt

.PHONY: all sin-red limpiar

all:
	python3 generar.py

sin-red:
	PDS_INLINE=1 python3 generar.py

limpiar:
	rm -rf html/T[1-6]-*.html html/index.html html/indice
