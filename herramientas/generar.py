"""Genera todas las herramientas interactivas y el índice por temas.

    python3 generar.py            # páginas que cargan Bokeh desde la CDN
    PDS_INLINE=1 python3 generar.py   # páginas autónomas, sin red

Ejecuta cada ``fuentes/Tn/*.py`` (cada una escribe ``html/Tn-*.html``) y
después escribe ``html/index.html`` con la lista de herramientas.
"""

import html
import json
import pathlib
import runpy
import sys

RAIZ = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "comun"))
import pds_bokeh as pb  # noqa: E402


def generar() -> int:
    fallos = 0
    for fuente in sorted((RAIZ / "fuentes").glob("T*/*.py")):
        try:
            runpy.run_path(str(fuente), run_name="__main__")
            print(f"ok    {fuente.relative_to(RAIZ)}")
        except Exception as e:  # noqa: BLE001
            fallos += 1
            print(f"FALLO {fuente.relative_to(RAIZ)}: {e}")
    return fallos


def indice() -> None:
    entradas = [json.loads(f.read_text(encoding="utf-8"))
                for f in sorted((pb.SALIDA / "indice").glob("*.json"))]
    partes = []
    for tema, nombre in pb.TEMAS.items():
        propias = sorted((e for e in entradas if e["tema"] == tema), key=lambda e: e["titulo"])
        partes.append(f"<h2>Tema {tema} · {html.escape(nombre)}</h2>")
        if not propias:
            partes.append('<p class="vacio">Todavía no hay herramientas de este tema.</p>')
            continue
        partes.append("<ul>")
        for e in propias:
            partes.append(f'<li><a href="{html.escape(e["archivo"])}">{html.escape(e["titulo"])}</a>'
                          f'<span>{e["descripcion"]}</span></li>')
        partes.append("</ul>")
    (pb.SALIDA / "index.html").write_text(f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PdS · Herramientas interactivas</title>
<link href="https://fonts.googleapis.com/css2?family=Fira+Sans:wght@400;600&display=swap" rel="stylesheet">
<style>
  body {{ font-family: {pb.FUENTE}; color: #222; background: #fff; max-width: 860px;
         margin: 0 auto; padding: 24px 16px; line-height: 1.45; }}
  h1 {{ color: {pb.AZUL}; font-weight: 600; margin-bottom: 4px; }}
  h2 {{ color: {pb.AZUL}; font-size: 18px; font-weight: 600; margin-top: 28px;
        border-bottom: 1px solid {pb.REJILLA}; padding-bottom: 4px; }}
  ul {{ list-style: none; padding: 0; }}
  li {{ margin: 10px 0; }}
  li a {{ color: {pb.AZUL}; font-weight: 600; text-decoration: none; }}
  li a:hover {{ text-decoration: underline; }}
  li span {{ display: block; color: {pb.GRIS}; font-size: 14px; }}
  .vacio {{ color: {pb.GRIS}; font-style: italic; }}
</style>
</head>
<body>
<h1>Herramientas interactivas</h1>
<p>Procesamiento de Señales · Grado en Ingeniería Electrónica de Comunicaciones, UCM.
Cada herramienta se abre en el navegador; no hace falta instalar nada.</p>
{chr(10).join(partes)}
</body>
</html>
""", encoding="utf-8")


if __name__ == "__main__":
    n = generar()
    indice()
    print("Índice en html/index.html")
    sys.exit(1 if n else 0)
