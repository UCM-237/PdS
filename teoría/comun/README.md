# Formato común del material de teoría

Todo el material de teoría (transparencias, apuntes y hojas de ejercicios)
comparte estilo, notación y paleta. Se compila con **XeLaTeX** (`latexmk
-xelatex`, o `make` desde `teoría/`).

## Estructura de un tema

```
teoría/Tx/
  transparencias/Tx-0k-Nombre.tex   beamer 16:9, una presentación por clase
  apuntes/Tx-Apuntes.tex            apuntes que desarrollan las transparencias
  ejercicios/Tx-Ejercicios.tex      hoja de ejercicios (con las soluciones dentro)
  ejercicios/Tx-Ejercicios-Soluciones.tex   la misma hoja con las soluciones
  figuras/generar_figuras.py        genera todas las figuras en PDF
  codigo/python/*.py, codigo/matlab/*.m      ejemplos en paralelo
```

## Ficheros de `comun/`

| Fichero | Contenido |
|---|---|
| `datos.tex` | Asignatura, grado, curso y autores. Cambiar aquí cada curso. |
| `notacion.tex` | Macros de notación (ver abajo). |
| `pds-comun.tex` | Paquetes, paleta de colores, estilos TikZ y de código, `\codigo`. |
| `pds-beamer.tex` | Tema beamer: Fira Sans, logo, `\portada`, bloques `definicion`, `importante`, `ejemplo`, `\nota`, `\gris`, `\herramienta`. |
| `pds-apuntes.tex` | Estilo de apuntes y ejercicios (KOMA `scrartcl`, Libertinus): `\tema`, `\cabecera`, cajas `definicion`, `propiedad`, `ejemplo`, `nota`, `importante`, `encodigo`, entornos `ejercicio`, `solucion` e `incisos`. |
| `pds_estilo.py` | Estilo de las figuras de Matplotlib con la misma paleta y fuente. |
| `probar_codigo.sh` | Ejecuta los ejemplos de un tema en Python y en Octave. |

## Convenios de notación

- Tiempo continuo con paréntesis, `x(t)`; tiempo discreto con corchetes, `x[n]`.
- Frecuencia continua `\omega` (rad/s) o `f` (Hz), con ω = 2πf; discreta `\Omega` (rad/muestra) o `F` (ciclos/muestra). Al muestrear, Ω = ωT_s.
- Transformadas: `\Xc` = X(jω), `\Xd` = X(e^{jΩ}), `X(s)`, `X(z)`, `X[k]`.
- Laplace y Z bilaterales, siempre con su región de convergencia (`\ROC`).
- Ecuación en diferencias en la forma de `filter`/`lfilter`, con `a_0 = 1`.
- `\conv` para la convolución (nunca para el producto), `\sinc` = sin(πt)/(πt), `\Sa` = sin t / t.
- Pares de transformadas: `\parF`, `\parL`, `\parZ`.

## Código

`\codigo{nombre}` muestra `../codigo/python/nombre.py` y
`../codigo/matlab/nombre.m` uno al lado del otro. Las líneas deben tener
como mucho 48 caracteres para que quepan en las transparencias.
`make prueba-codigo` los ejecuta todos.

## Soluciones

Las soluciones están dentro de la hoja, en entornos `solucion`, y solo se
imprimen si se define `\SOLUCIONES` antes de cargar el estilo (lo hace
`Tx-Ejercicios-Soluciones.tex`). `make publicar` copia a `clase/` la hoja
con y sin soluciones.

## Numeración de los temas

Se sigue la guía docente: T1 Introducción, T2 Muestreo, T3 DFT, T4 Filtros,
T5 Aplicaciones, T6 Señales aleatorias.
