## Introducción

### La imagen como señal de dos variables

Una imagen digital en escala de grises es una señal f[m, n] de dos índices: m es la fila (de arriba abajo) y n la columna. Todo lo visto para señales de una variable se generaliza: la linealidad, la invarianza al desplazamiento, la respuesta al impulso y la convolución.

### Convolución bidimensional

Un sistema lineal e invariante al desplazamiento queda descrito por su respuesta al impulso h[i, j], el **núcleo** (o máscara). La salida es

> g[m, n] = (h ∗ f)[m, n] = Σ_i Σ_j h[i, j] f[m − i, n − j].

Cada píxel de salida es una combinación lineal de sus vecinos con los pesos del núcleo **girado 180°**. Si no se gira, es una correlación: es lo que hacen `filter2` e `imfilter` de Matlab y `scipy.ndimage.correlate`; `conv2` y `scipy.signal.convolve2d` sí giran. Para núcleos simétricos da igual.

### Núcleos habituales

- **Suavizado** (paso bajo): la media de K×K y el gaussiano. Sus coeficientes suman 1, así que conservan el nivel medio. Promediar K² muestras de ruido independiente divide su desviación típica por K.
- **Derivadas** (paso alto): el Sobel S_x = (1, 2, 1)ᵀ(1, 0, −1) deriva en horizontal y suaviza en vertical; S_y es su traspuesto. El módulo del gradiente, √(g_x² + g_y²), marca los bordes en cualquier dirección. El **laplaciano** [0 1 0; 1 −4 1; 0 1 0] aproxima ∂²f/∂x² + ∂²f/∂y²: es nulo en las zonas uniformes y en las rampas y cambia de signo al cruzar un borde. Sus coeficientes suman 0.
- **Realce**: f − k∇²f resta el laplaciano y exagera los bordes (es una forma de *unsharp masking*).

### Separabilidad y bordes

Un núcleo **separable**, h[i, j] = u[i]v[j], es una matriz de rango 1: se filtra primero por columnas y luego por filas, con 2K productos por píxel en vez de K². La media, el gaussiano y el Sobel lo son; el laplaciano no.

Junto al borde de la imagen faltan vecinos, y hay que decidir qué valores se usan: **ceros**, **repetir** el último píxel o **reflejar** la imagen.

## Guía de uso

- **Imagen**: una imagen de prueba (círculo, rectángulo, rejilla y anillos sobre un fondo en rampa), un tablero de ajedrez, un texto o una foto propia, que se recorta al cuadrado central, se pasa a grises y **no sale del navegador**. Se le puede sumar ruido gaussiano de desviación **σ**.
- **Núcleo**, con sus parámetros (K, σ del gaussiano, k del realce), y **borde**. El núcleo personalizado de 3×3 se escribe con la fila 0 arriba; el valor central es el (1, 1).
- Arriba, la imagen, el resultado (con la escala de grises simétrica para los núcleos que suman 0) y el núcleo con sus valores. Abajo, el perfil de la fila 192 en las dos imágenes.
- El recuadro da la suma de los coeficientes, si el núcleo es separable, el coste por píxel y el rango de valores de g.

## Ejercicios

**1. La media.** Con la imagen de prueba y la media de 5×5, mira el perfil de la fila 192. ¿Qué le pasa a la rejilla de periodo 16 píxeles y a los bordes? ¿Cuántos productos por píxel cuesta, directa y separable? ¿Y con K = 15?

<details><summary>Solución</summary>
Los bordes se convierten en rampas de 5 píxeles y la rejilla pierde amplitud: la media de K muestras de un coseno de periodo P lo multiplica por |sen(πK/P)/(K sen(π/P))|, 0,85 con K = 5. Con K = 15 casi desaparece (0,07). Cuesta 25 productos directamente y 10 separando; con K = 15, 225 y 30, como en el ejercicio 14 de la hoja.
</details>

**2. Sobel en el tablero.** Con el tablero (casillas de 0,15 y 0,85) y Sobel x, ¿qué valores toma g y dónde? ¿Qué cambia con Sobel y y con el módulo del gradiente?

<details><summary>Solución</summary>
g es nulo dentro de las casillas y vale ±2,8 en las dos columnas junto a cada borde vertical: (1 + 2 + 1) · 0,7 = 2,8, positivo donde la imagen crece hacia la derecha. Sobel y responde solo a los bordes horizontales. El módulo marca todos los bordes con 2,8, y junto a las esquinas, donde g_x y g_y se cancelan en parte, menos. Es el ejercicio 13 de la hoja con un borde más grande.
</details>

**3. El laplaciano y el ruido.** Con la imagen de prueba, aplica el laplaciano sin ruido y con σ = 0,05. ¿Qué se ve? ¿Por cuánto multiplica el laplaciano la desviación típica de un ruido blanco?

<details><summary>Solución</summary>
Sin ruido, el laplaciano es nulo en las zonas uniformes y en la rampa del fondo (su segunda derivada es nula) y marca cada borde con una pareja positivo-negativo. Con ruido, este domina: el laplaciano suma cinco muestras independientes con pesos 1, 1, 1, 1 y −4, y multiplica σ por √(4 + 16) = 4,5. Por eso se suaviza antes con un gaussiano (el laplaciano de la gaussiana, LoG).
</details>

**4. El realce.** Con el tablero y el realce con k = 1, ¿qué valores toma g junto a un borde? Compara el núcleo con el personalizado por defecto.

<details><summary>Solución</summary>
El núcleo es [0 −1 0; −1 5 −1; 0 −1 0], el mismo que el personalizado. Junto a un borde, el laplaciano vale ±0,7 y g pasa de 0,15 a −0,55 en el lado oscuro y de 0,85 a 1,55 en el claro: el borde se ve más marcado por el contraste exagerado (bandas de Mach). En las esquinas el efecto se suma y g va de −1,25 a 2,25.
</details>

**5. Convolución o correlación.** Escribe un núcleo personalizado con un 1 a la derecha del centro (fila 1, columna 2) y ceros en el resto. ¿Hacia dónde se desplaza la imagen? ¿Y con una correlación?

<details><summary>Solución</summary>
Con la convolución, g[m, n] = h[0, 1] f[m, n − 1]: la imagen se desplaza un píxel a la **derecha**. Con una correlación (`filter2`, `imfilter`), g[m, n] = f[m, n + 1] y se desplazaría a la izquierda. Con núcleos asimétricos, como el Sobel, la diferencia es el signo del resultado.
</details>

**6. Los bordes de la imagen.** Con el tablero y la media de 5×5, compara los tres modos de borde. ¿Por qué con ceros el valor mínimo baja a 0,054?

<details><summary>Solución</summary>
Con ceros, en la esquina superior izquierda solo 9 de los 25 píxeles del núcleo caen dentro de la imagen, y todos valen 0,15: g = 9 · 0,15/25 = 0,054. Aparece un marco oscuro. Repetir o reflejar inventan vecinos parecidos a los del borde y no oscurecen.
</details>

## Para profundizar

- [Apuntes del Tema 5](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%20Apuntes.pdf), sección 3, «Convolución bidimensional».
- [Transparencias T5-03](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%2003%20-%20Im%C3%A1genes.pdf), convolución bidimensional, núcleos habituales y Sobel.
- [Hoja de ejercicios del Tema 5](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%20Ejercicios.pdf), ejercicios 13 y 14, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%20Ejercicios%20resueltos.pdf).
- R. C. Gonzalez y R. E. Woods, *Digital Image Processing*, 4.ª ed., Pearson, 2018, capítulo 3.

## Relación con otros conceptos

- **Convolución discreta (Tema 1).** La misma operación con un índice más. Herramienta: [Convolución discreta](T1-convolucion-discreta.html).
- **El dominio de la frecuencia.** La convolución es un producto de DFT 2D. Herramienta: [DFT 2D y filtrado en frecuencia](T5-dft-2d.html).
- **Media móvil (Tema 4).** La media de K×K es la media móvil en dos dimensiones. Herramienta: [Filtro de media móvil](T4-media-movil.html).
- **Operaciones puntuales.** Cambian cada píxel sin mirar a sus vecinos. Herramienta: [Histograma y operaciones puntuales](T5-histograma.html).
