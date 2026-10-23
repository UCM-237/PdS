"""Genera el documento completo: apuntes y ejercicios resueltos de todos
los temas en un solo libro (teoría/completo/PdS-Completo.tex).

Cada tema es un capítulo con sus apuntes y, al final, su hoja de
ejercicios con las soluciones. Los cuerpos se copian de
Tn/apuntes/Tn-Apuntes.tex y Tn/ejercicios/Tn-Ejercicios.tex sin la
cabecera ni el índice, y las etiquetas llevan el prefijo del tema,
porque se repiten de un tema a otro (sec:intro, def:...).

Uso, desde teoría/:  python3 comun/completo.py   (o «make completo»)
"""

import re
from pathlib import Path

TEORIA = Path(__file__).resolve().parent.parent
SALIDA = TEORIA / "completo"
TEMAS = range(1, 7)

# Órdenes cuyo argumento es una etiqueta o una lista de etiquetas
REFS = re.compile(r"\\(label|ref|eqref|pageref|cref|Cref|crefrange|Crefrange|nameref)\{([^{}]*)\}")
# Cajas de tcolorbox numeradas: \begin{definicion}{Título}{marcador} crea
# la etiqueta def:marcador (prop: y ej: para propiedad y ejemplo)
CAJAS = re.compile(r"(\\begin\{(?:definicion|propiedad|ejemplo)\}(?:\[[^\]]*\])?"
                   r"\{(?:[^{}]|\{[^{}]*\})*\})\{([^{}]*)\}")
PREFIJOS_CAJAS = ("def", "prop", "ej")


def etiqueta(clave, prefijo):
    """sec:intro -> T1a-sec:intro; def:senal -> def:T1a-senal."""
    clave = clave.strip()
    tipo, dos_puntos, resto = clave.partition(":")
    if dos_puntos and tipo in PREFIJOS_CAJAS:
        return f"{tipo}:{prefijo}-{resto}"
    return f"{prefijo}-{clave}"


def cuerpo(fichero, prefijo):
    texto = fichero.read_text(encoding="utf-8")
    m = re.search(r"\\begin\{document\}(.*)\\end\{document\}", texto, re.S)
    texto = m.group(1)
    # Fuera la cabecera y el índice de cada documento suelto
    texto = re.sub(r"^.*\\cabecera\{.*\n", "", texto, flags=re.M)
    texto = re.sub(r"^\\tableofcontents\s*\n", "", texto, flags=re.M)
    texto = REFS.sub(lambda m: "\\%s{%s}" % (
        m.group(1), ",".join(etiqueta(c, prefijo) for c in m.group(2).split(","))), texto)
    texto = CAJAS.sub(lambda m: m.group(1) + "{%s}" % (
        f"{prefijo}-{m.group(2)}" if m.group(2).strip() else ""), texto)
    return texto


def nombre_tema(fichero):
    m = re.search(r"\\tema\{(\d+)\}\{([^{}]*)\}", fichero.read_text(encoding="utf-8"))
    return m.group(2)


def capitulo(n):
    apuntes = TEORIA / f"T{n}/apuntes/T{n}-Apuntes.tex"
    ejercicios = TEORIA / f"T{n}/ejercicios/T{n}-Ejercicios.tex"
    nombre = nombre_tema(apuntes)
    hoja = cuerpo(ejercicios, f"T{n}e")
    # Las secciones de la hoja pasan a subsecciones de «Ejercicios»
    hoja = re.sub(r"\\section\*\{", r"\\subsection*{", hoja)
    return f"""% Generado por comun/completo.py: no editar
\\tema{{{n}}}{{{nombre}}}
\\graphicspath{{{{../T{n}/figuras/}}}}
\\renewcommand{{\\rutacodigo}}{{../T{n}/codigo/}}
\\setcounter{{chapter}}{{{n - 1}}}
\\chapter{{{nombre}}}\\label{{tema{n}}}
{cuerpo(apuntes, f"T{n}a")}
\\section{{Ejercicios}}\\label{{tema{n}-ejercicios}}
\\setcounter{{ejercicio}}{{0}}
{hoja}
"""


MAESTRO = r"""% Generado por comun/completo.py: no editar
\documentclass[11pt,a4paper,open=any]{scrreprt}
\def\SOLUCIONES{}
\newcommand{\rutacomun}{../comun/}
\input{../comun/pds-apuntes}
\setcounter{tocdepth}{1}
% Cabecera sin tema en las páginas del principio
\ohead{\sffamily\small\color{pdsgris}\if\relax\detokenize\expandafter{\numtema}\relax\else Tema~\numtema. \nombretema\fi}
\hypersetup{pdftitle={\asignatura. Apuntes y ejercicios resueltos},
  pdfauthor={\autores}}

\begin{document}
\begin{titlepage}
  \sffamily
  \includegraphics[width=3cm]{\rutacomun ucm.png}\par
  \vspace*{\stretch{1}}
  {\large\color{pdsgris}\grado\par\curso\par}
  \vspace{12pt}
  {\Huge\bfseries\color{pdsazul}\asignatura\par}
  \vspace{8pt}
  {\LARGE\bfseries Apuntes y ejercicios resueltos\par}
  \vspace{4pt}
  {\color{pdsazul}\rule{\linewidth}{0.8pt}}\par
  \vspace{4pt}
  {\large\autores\par}
  \vspace*{\stretch{2}}
  {\small\color{pdsgris}Cada tema reúne sus apuntes y, al final, la hoja
  de ejercicios con las soluciones. Las transparencias, los documentos
  sueltos de cada tema y el código de los ejemplos están en
  \url{https://github.com/UCM-237/PdS}.\par}
\end{titlepage}

\tableofcontents

%CAPITULOS%
\end{document}
"""


def main():
    SALIDA.mkdir(exist_ok=True)
    entradas = []
    for n in TEMAS:
        (SALIDA / f"T{n}.tex").write_text(capitulo(n), encoding="utf-8")
        entradas.append(f"\\input{{T{n}}}")
    (SALIDA / "PdS-Completo.tex").write_text(
        MAESTRO.replace("%CAPITULOS%", "\n".join(entradas)), encoding="utf-8")
    print(f"Generado {SALIDA / 'PdS-Completo.tex'}")


if __name__ == "__main__":
    main()
