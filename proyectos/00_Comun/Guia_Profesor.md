# Guía del profesor

## Qué no se distribuye

`05_Solucion/` de cada proyecto contiene la solución completa (código en Matlab y Python, figuras y valores de referencia). Como este repositorio es público, `.gitignore` excluye esa carpeta: la solución se guarda aparte (repositorio privado o copia local) y se coloca en `NN_Proyecto/05_Solucion/` para trabajar con ella.

## Cómo corregir un hito

1. Ejecutar el comando de reproducción que el alumno indica en el anexo. Si falla, aplicar la regla de C3 de la rúbrica.
2. Comparar los valores clave con la tabla «Valores de referencia» de `05_Solucion/README.md`. Las tolerancias indicadas allí son orientativas.
3. Puntuar C1–C5 con la rúbrica común y los criterios específicos del hito.
4. Devolver dos o tres observaciones concretas que el alumno deba incorporar a la memoria final.

## Datos

Los datos de cada proyecto se generan con `05_Solucion/generar_datos.py` y una semilla fija; el generador está en la solución porque con él se podría reconstruir la verdad (anotaciones, posiciones de los clics). Escribe los datos en `01_Datos/` y la verdad en `05_Solucion/`. Para tener datos distintos por alumno (y evitar copias), se puede llamar con `--semilla <DNI sin letra>`; los parámetros de la señal cambian dentro de rangos que mantienen la dificultad.

## Defensa

10 minutos por alumno. Preguntas tipo: cambiar la frecuencia de corte o el orden y predecir el efecto; explicar una figura concreta; justificar por qué no se usó otro método.
