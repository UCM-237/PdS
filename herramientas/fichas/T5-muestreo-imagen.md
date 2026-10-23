## Introducción

### Muestrear en el espacio

Una cámara muestrea la imagen óptica en una rejilla de píxeles. Si la separación entre píxeles es Δ, la frecuencia de muestreo es 1/Δ en cada dirección y, por el teorema de Nyquist, solo se representan sin aliasing las frecuencias espaciales menores que 1/(2Δ). Una frecuencia espacial se mide en **ciclos por píxel** (o por milímetro): unas rayas de periodo P píxeles tienen 1/P ciclos/píxel, y el máximo representable es 0,5, unas rayas de periodo 2.

### Muaré

Si la imagen tiene detalles más finos que el límite, aparecen como **alias** de frecuencia más baja: rayas, ondas o anillos falsos que no estaban en la escena. Es el **muaré** (*moiré*) que se ve al fotografiar una tela fina o una pantalla. Lo mismo pasa al reducir una imagen tomando un píxel de cada M: el límite baja a 1/(2M) ciclos/píxel. La solución es la misma que en el Tema 2: un **paso bajo antes** de submuestrear (las cámaras llevan un filtro óptico delante del sensor), a cambio de perder nitidez.

### Cuantificar los niveles

Cada píxel se guarda con b bits, es decir, con 2^{b} niveles de gris. Con 8 bits (256 niveles) el ojo no distingue los escalones; con muy pocos, los degradados suaves se convierten en bandas: son los **contornos falsos**. El tamaño sin comprimir de una imagen de M×N píxeles es MNb/8 bytes por canal.

## Guía de uso

- **Imagen**: unos anillos cuya frecuencia crece desde el centro (de 0 a 0,5 ciclos/píxel en el borde), rayas oblicuas de 0,42 ciclos/píxel, la imagen de prueba, un texto, un tablero o una foto propia, que se procesa en el navegador.
- **Submuestreo M**: se conserva un píxel de cada M filas y columnas, y se repite en un bloque de M×M para verla al mismo tamaño. **Prefiltro**: ninguno, la media de M×M o un gaussiano de σ = M/2.
- **Bits por píxel** b cuantifica la imagen original (tercera imagen).
- Abajo, la fila central de la original y las muestras que se conservan. El recuadro da la frecuencia máxima sin aliasing, los niveles y el tamaño.

## Ejercicios

**1. Los anillos.** Con los anillos y M = 3 sin prefiltro, ¿a qué distancia del centro empieza el aliasing? ¿Dónde aparecen las copias de los anillos?

<details><summary>Solución</summary>
La frecuencia local de los anillos crece linealmente con la distancia al centro: r píxeles corresponden a r/256 ciclos/píxel. Con M = 3 el límite es 1/6 = 0,167 ciclos/píxel, a unos 43 píxeles del centro. Más allá aparecen anillos falsos, centrados donde la frecuencia local es un múltiplo de 1/M: a 256/3 ≈ 85 píxeles del centro en horizontal y en vertical, y en las diagonales. Con M = 2 el límite sube a 0,25 (64 píxeles) y las copias se van a los bordes.
</details>

**2. El prefiltro.** Con los anillos y M = 3, prueba la media de 3×3 y el gaussiano. ¿Desaparecen las copias? ¿Qué se pierde?

<details><summary>Solución</summary>
El gaussiano de σ = 1,5 las elimina casi por completo: la zona exterior queda gris uniforme, que es lo correcto, porque esos detalles no caben en la imagen reducida. La media de 3×3 las atenúa pero deja restos, porque su respuesta en frecuencia tiene lóbulos laterales (es un sinc). En las dos se pierde el contraste de los anillos cerca del límite. En el perfil se ve que las muestras del prefiltrado siguen la media local de la señal.
</details>

**3. El texto.** Con el texto y M = 4, compara sin prefiltro y con el gaussiano. ¿Qué se lee mejor?

<details><summary>Solución</summary>
Sin prefiltro, los trazos finos de las letras pequeñas desaparecen o se duplican según caigan o no en una muestra, y los bordes quedan dentados. Con el gaussiano, las letras quedan borrosas pero completas y se leen mejor. Es la razón por la que los programas de imagen filtran antes de reducir.
</details>

**4. Contornos falsos.** Con la imagen de prueba, baja b de 8 a 1. ¿A partir de cuántos bits se ven bandas en el fondo? ¿Cuántas?

<details><summary>Solución</summary>
El fondo es una rampa de 0,35 a 0,6. Con b bits el escalón es 1/(2^{b} − 1): con 4 bits (escalón 0,067) la rampa se divide en unas 4 bandas, que ya se ven; con 3 bits (0,143), en 2; con 5 o 6 bits apenas se notan. Con 1 bit la imagen queda en blanco y negro. Es el ruido de cuantificación del Tema 2 visto en una imagen: Δ²/12 de potencia por píxel.
</details>

**5. Tamaño.** ¿Cuánto ocupa la imagen de 256×256 a 8 bits? ¿Y una foto en color de 4000×3000 con 8 bits por canal? ¿Y si se reduce con M = 4?

<details><summary>Solución</summary>
256 · 256 · 1 byte = 64 kB (con kB = 1024 bytes). La foto en color: 4000 · 3000 · 3 = 36 MB, como en el ejercicio 11 de la hoja. Con M = 4 cada dimensión se divide por 4 y el tamaño por 16: 4 kB y 2,25 MB. La compresión (JPEG) reduce otro factor de 10 a 20 aprovechando que la imagen es predecible.
</details>

## Para profundizar

- [Apuntes del Tema 5](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%20Apuntes.pdf), sección 3, «La imagen como señal bidimensional».
- [Transparencias T5-03](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%2003%20-%20Im%C3%A1genes.pdf), muestreo, cuantificación y almacenamiento.
- [Hoja de ejercicios del Tema 5](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%20Ejercicios.pdf), ejercicio 11, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%20Ejercicios%20resueltos.pdf).
- R. C. Gonzalez y R. E. Woods, *Digital Image Processing*, 4.ª ed., Pearson, 2018, apartados 2.4 y 4.5.

## Relación con otros conceptos

- **Aliasing (Tema 2).** El mismo fenómeno en una dimensión. Herramienta: [Aliasing](T2-aliasing.html).
- **Diezmado (Tema 2).** Filtrar y luego quedarse con una muestra de cada M. Herramienta: [Diezmado e interpolación](T2-diezmado-interpolacion.html).
- **Cuantificación (Tema 2).** Herramienta: [Cuantificación y SQNR](T2-cuantificacion.html).
- **El espectro de una imagen.** Herramienta: [DFT 2D y filtrado en frecuencia](T5-dft-2d.html).
