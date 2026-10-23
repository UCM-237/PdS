## Introducción

### Operaciones puntuales

Una **operación puntual** cambia cada píxel con una función de su propio nivel, s = T(r), sin mirar a sus vecinos. Con L = 256 niveles (8 bits, de 0 a 255) basta una tabla de 256 valores. Las más habituales son:

- **Negativo**: s = 255 − r.
- **Corrección gamma**: s = 255 (r/255)^{γ}. Con γ < 1 aclara las zonas oscuras y comprime las claras; con γ > 1, al revés. Las pantallas y las cámaras la usan porque la sensibilidad del ojo no es lineal.
- **Estiramiento del contraste**: lleva el intervalo [r₁, r₂] a [0, 255] con una recta y satura lo de fuera.
- **Umbralización**: s = 255 si r > u y 0 si no. Separa un objeto del fondo cuando sus niveles no se mezclan.

### Histograma

El **histograma** h[r] cuenta los píxeles de cada nivel; dividido entre el número de píxeles, p[r] = h[r]/(MN), es una función de probabilidad. Su suma acumulada F(r) = Σ_{i≤r} p[i] es la **función de distribución** de los niveles. Un histograma estrecho corresponde a una imagen con poco contraste; uno amontonado a la izquierda, a una imagen oscura.

### Ecualización

La **ecualización** usa la propia F como transformación:

> s = T(r) = round((L − 1) F(r)).

Si los niveles fueran continuos, s tendría distribución uniforme: es el método de la inversa del Tema 6 al revés (si R tiene distribución F, F(R) es uniforme). Con niveles discretos, todos los píxeles de un nivel van al mismo nivel nuevo, y el histograma ecualizado no queda plano: los niveles se separan (más contraste donde había muchos píxeles) y algunos se juntan. Una operación puntual nunca crea niveles nuevos.

## Guía de uso

- **Imagen**: la imagen de prueba con poco contraste (niveles de 108 a 159), la normal, una versión oscura, un texto o una foto propia, que se procesa en el navegador.
- **Operación** y sus parámetros: γ, r₁ y r₂ del estiramiento y el umbral u.
- Arriba, la imagen original, la transformada y la curva T(r). Abajo, el histograma (barras) y F(r) (en rojo, eje derecho) de las dos imágenes.
- El recuadro da el rango de niveles, cuántos niveles distintos se usan, la media y la desviación típica.

## Ejercicios

**1. Poco contraste.** Con la imagen de partida, ¿entre qué niveles están los píxeles y cuántos niveles distintos hay? Estira el intervalo [108, 159]. ¿Cuántos niveles distintos quedan? ¿Por qué no aumentan?

<details><summary>Solución</summary>
De 108 a 159, con 52 niveles distintos, desviación 13,8. Al estirar [108, 159] a [0, 255], la recta tiene pendiente 255/51 = 5: la desviación pasa a 69 y la imagen ocupa todo el rango, pero sigue con 52 niveles distintos, ahora separados 5 niveles. Una operación puntual no crea niveles; para obtener más habría que interpolar o tomar la imagen con más bits.
</details>

**2. La ecualización.** Ecualiza la imagen de poco contraste. ¿Cómo es F(r) antes y después? ¿Es plano el histograma ecualizado? ¿Cuántos niveles distintos quedan?

<details><summary>Solución</summary>
F(r) sube de 0 a 1 entre 108 y 159; tras ecualizar es casi una recta de 0 a 255, que es la F de una distribución uniforme. El histograma no es plano: tiene barras aisladas con huecos. Quedan 36 niveles distintos, menos que 52, porque varios niveles poco poblados van al mismo nivel nuevo. La desviación, 72,7, se acerca a la de una uniforme en [0, 255], 255/√12 = 73,6. Es el ejercicio 12 de la hoja con 256 niveles.
</details>

**3. El negativo.** Aplica el negativo. ¿Cómo cambian la media y la desviación típica? Razónalo.

<details><summary>Solución</summary>
La media pasa de 132,5 a 255 − 132,5 = 122,5 y la desviación no cambia (13,8): una transformación s = a + br tiene media a + bμ y desviación |b|σ, y aquí b = −1. El histograma se refleja.
</details>

**4. La imagen oscura.** Con la imagen oscura, compara la corrección gamma con γ = 0,45 y la ecualización. ¿Qué rango ocupa cada una?

<details><summary>Solución</summary>
La original va de 1 a 121 con media 38,5. Con γ = 0,45 pasa a 21–182 con media 97 y conserva 109 de los 121 niveles: aclara las sombras sin saturar, y la curva es la misma para cualquier imagen. La ecualización llega de 31 a 255 con media 133, pero se queda con 56 niveles: separa mucho los niveles más poblados y junta los otros. La gamma es la operación inversa de la que oscureció la imagen (r^{2,2}), por eso la recupera mejor.
</details>

**5. Umbralizar.** Con la imagen de prueba normal, umbraliza con u = 128. ¿Qué objetos quedan en blanco? ¿Por qué no sirve un único umbral para separar el círculo del fondo en toda la imagen?

<details><summary>Solución</summary>
Queda en blanco el círculo (0,85, nivel 217), las partes claras de la rejilla y de los anillos, y el fondo de la derecha, porque el fondo es una rampa de 0,35 a 0,6 (niveles 89 a 153) y cruza el umbral hacia la columna 156. El rectángulo oscuro queda en negro. Un umbral global falla con iluminación no uniforme: se usan umbrales locales o se corrige antes el fondo.
</details>

## Para profundizar

- [Apuntes del Tema 5](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%20Apuntes.pdf), sección 3, «Operaciones puntuales» e «Histograma y ecualización».
- [Transparencias T5-03](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%2003%20-%20Im%C3%A1genes.pdf), operaciones puntuales, histograma y ecualización.
- [Hoja de ejercicios del Tema 5](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%20Ejercicios.pdf), ejercicio 12, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%20Ejercicios%20resueltos.pdf).
- R. C. Gonzalez y R. E. Woods, *Digital Image Processing*, 4.ª ed., Pearson, 2018, apartados 3.2 y 3.3.

## Relación con otros conceptos

- **Función de distribución (Tema 6).** El histograma normalizado es una función de probabilidad y F su distribución. Herramienta: [Distribuciones de probabilidad](T6-distribuciones.html).
- **El método de la inversa (Tema 6).** La ecualización aplica F; generar muestras aplica F^{−1}. Herramienta: [Generación de muestras aleatorias](T6-generacion-muestras.html).
- **Cuantificación.** Herramienta: [Muestreo y cuantificación de imágenes](T5-muestreo-imagen.html).
- **Operaciones con vecinos.** Herramienta: [Convolución bidimensional](T5-convolucion-2d.html).
