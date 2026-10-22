#!/usr/bin/env bash
# Ejecuta todos los ejemplos de código de uno o varios temas.
#   comun/probar_codigo.sh T1 [T2 ...]      (desde teoría/)
# Python: necesita numpy, scipy y matplotlib.
# Matlab: se prueba con Octave (paquetes signal y control) si está instalado;
#         con Matlab basta ejecutar cada .m desde su carpeta.
set -u
fallos=0
for tema in "$@"; do
  for f in "$tema"/codigo/python/*.py; do
    [ -e "$f" ] || continue
    if MPLBACKEND=Agg python3 "$f" > /dev/null 2> /tmp/pds_err.txt; then
      echo "ok    $f"
    else
      echo "FALLO $f"; sed 's/^/      /' /tmp/pds_err.txt; fallos=$((fallos+1))
    fi
  done
  if command -v octave > /dev/null; then
    for f in "$tema"/codigo/matlab/*.m; do
      [ -e "$f" ] || continue
      if octave --no-gui --quiet --eval "pkg load signal; pkg load control; set(0,'defaultfigurevisible','off'); run('$f')" > /dev/null 2> /tmp/pds_err.txt \
         && ! grep -q "^error" /tmp/pds_err.txt; then
        echo "ok    $f"
      else
        echo "FALLO $f"; grep -A3 "^error" /tmp/pds_err.txt | sed 's/^/      /'; fallos=$((fallos+1))
      fi
    done
  else
    echo "(Octave no está instalado: no se prueban los .m)"
  fi
done
[ "$fallos" -eq 0 ] && echo "Todos los ejemplos funcionan." || { echo "$fallos ejemplo(s) fallan."; exit 1; }
