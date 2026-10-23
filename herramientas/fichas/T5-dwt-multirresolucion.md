## Introducción

### Aproximación y detalle

La idea del **análisis multirresolución** es describir una señal como una versión borrosa más las correcciones necesarias para recuperar el detalle. Con la wavelet de Haar es muy concreto: se toman las muestras de dos en dos, y de cada pareja se guardan la media (escalada) y la diferencia,

> a₁[k] = (x[2k] + x[2k+1])/√2,  d₁[k] = (x[2k] − x[2k+1])/√2.

Con a₁ y d₁, que tienen la mitad de muestras cada uno, se recupera x exactamente. Se repite sobre a₁ para obtener a₂ y d₂, y así hasta el nivel J.

### La DWT como banco de filtros

En general, cada nivel filtra con un paso bajo h₀[n] y un paso alto h₁[n] = (−1)^{n} h₀[L−1−n] y se queda con una de cada dos muestras:

> a_{j+1}[k] = Σ_n h₀[n] a_j[2k − n],  d_{j+1}[k] = Σ_n h₁[n] a_j[2k − n].

Como cada diezmado reduce la frecuencia de muestreo a la mitad, d₁ recoge aproximadamente [π/2, π], d₂ [π/4, π/2], d₃ [π/8, π/4]… y a_J el resto, [0, π/2^{J}]: es una partición del eje de frecuencias en **octavas**. El número total de coeficientes es N, el mismo que de muestras, y la transformada es ortonormal: se conserva la energía, Σx² = Σa_J² + Σ_j Σd_j².

### Las componentes

Reconstruyendo con un solo nivel de coeficientes (los demás a cero) se obtienen las **componentes** A_J y D_J, …, D₁, cada una con la longitud de x, que suman la señal: x = A_J + D_J + … + D₁. A_J es la señal vista a la escala 2^{J} y cada D_j lo que se añade al pasar de la escala 2^{j} a la 2^{j−1}.

### Momentos nulos

Las wavelets de Daubechies dbN tienen N **momentos nulos**: Σ_n n^{p} h₁[n] = 0 para p < N. Entonces los detalles de un polinomio de grado menor que N son nulos, y una señal suave a trozos solo tiene detalles grandes cerca de sus discontinuidades. Haar es db1: anula las constantes, pero no las rampas.

## Guía de uso

- **Señal**: escalones con una oscilación de periodo 6 al final, una rampa con un salto, la señal Doppler (una oscilación cada vez más lenta) o un chirp. Todas tienen N = 512 muestras.
- **Wavelet** (Haar, db2 o db4) y **niveles J**. En los extremos se usa la extensión periódica, la opción `'periodization'` de PyWavelets y `'per'` de Matlab.
- Las casillas eligen qué componentes se suman en la reconstrucción (arriba, en rojo).
- En el centro, las componentes apiladas, cada una escalada a su máximo. Abajo, los coeficientes en el orden de `wavedec` y la banda de frecuencias de cada nivel.
- El recuadro da cuántos coeficientes hay, cómo se reparte la energía, la comprobación de Parseval y el error de reconstrucción.

## Ejercicios

**1. Cuántos coeficientes.** Con J = 4, ¿cuántos coeficientes tiene cada nivel? ¿En qué banda de Ω está cada uno? Comprueba en el recuadro que la energía se conserva.

<details><summary>Solución</summary>
d₁: 256, d₂: 128, d₃: 64, d₄: 32 y a₄: 32; en total 512. Las bandas son, aproximadamente, [π/2, π], [π/4, π/2], [π/8, π/4], [π/16, π/8] y [0, π/16]. La diferencia entre Σx² y la suma de los cuadrados de los coeficientes es del orden de 10^{−12}: es cero salvo redondeo, porque la transformada es ortonormal. Es el mismo reparto que el ejercicio 10 de la hoja con N = 1024 y J = 5.
</details>

**2. La oscilación.** En la primera señal, ¿en qué componente aparece la oscilación de periodo 6? ¿Por qué? Compara qué porcentaje de energía recoge ese nivel con Haar y con db4.

<details><summary>Solución</summary>
Su frecuencia es Ω = 2π/6 = π/3, dentro de [π/4, π/2]: aparece en D₂. La oscilación tiene una energía de 0,8²/2 · 112 ≈ 36, el 1,7 % del total. Con Haar, d₂ se queda con el 0,97 % y el resto se reparte en d₁ y d₃; con db4, con el 1,6 %. Los filtros más largos separan mejor las bandas, como se ve en la gráfica de abajo a la derecha.
</details>

**3. Momentos nulos.** Con la rampa con un salto y J = 4, compara los coeficientes de detalle con Haar, db2 y db4. ¿Cuáles son distintos de cero y por qué?

<details><summary>Solución</summary>
Con Haar todos los detalles son distintos de cero: en una rampa, cada diferencia vale −1/(128√2) y en d_j la diferencia crece con la escala. Son pequeños pero no nulos, porque Haar solo tiene un momento nulo. Con db2, que anula también las rampas, solo quedan 4 o 5 coeficientes por nivel, junto al salto en n = 300 y en el extremo (la extensión periódica une x[511] con x[0], otro salto). Con db4, que es más largo, quedan algo más (8 a 13 por nivel), pero también concentrados en los saltos. Es el ejercicio 9 de la hoja.
</details>

**4. La aproximación de Haar.** Con Haar, J = 4 y solo A₄ marcada, ¿qué forma tiene la reconstrucción de los escalones? ¿Por qué el salto de n = 128 sale exacto y el de n = 220 no?

<details><summary>Solución</summary>
A₄ es constante en bloques de 2⁴ = 16 muestras e igual a la media de cada bloque: es el ejercicio 7 de la hoja con bloques de 16. El salto de n = 128 cae en el borde de un bloque (128 = 8 · 16) y se conserva; el de 220 está dentro del bloque de 208 a 223, que toma un valor intermedio. Con db2 o db4, A₄ es más suave, pero oscila un poco junto a los saltos.
</details>

**5. La señal Doppler.** Con db4 y J = 6, ¿en qué componentes está el principio de la señal y en cuáles el final? ¿Qué se pierde al quitar D₁ y D₂?

<details><summary>Solución</summary>
Al principio la oscilación es rápida y está en D₁ y D₂; al final es lenta y está en A₆ y D₆. Cada componente recoge su banda de frecuencias solo en los instantes en que la señal la tiene: la DWT localiza en tiempo y en frecuencia a la vez. Al quitar D₁ y D₂ desaparecen las oscilaciones rápidas de las primeras 80 muestras y el resto apenas cambia, porque esos niveles tienen el 1,7 % de la energía.
</details>

## Para profundizar

- [Apuntes del Tema 5](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%20Apuntes.pdf), sección 2, «Transformada wavelet discreta» y «La DWT como banco de filtros».
- [Transparencias T5-02](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%2002%20-%20Wavelets.pdf), análisis multirresolución, Haar y banco de filtros.
- [Hoja de ejercicios del Tema 5](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%20Ejercicios.pdf), ejercicios 6, 7, 9 y 10, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%20Ejercicios%20resueltos.pdf).
- S. Mallat, *A Wavelet Tour of Signal Processing*, 3.ª ed., Academic Press, 2009, capítulo 7.
- G. Strang y T. Nguyen, *Wavelets and Filter Banks*, Wellesley-Cambridge, 1996.

## Relación con otros conceptos

- **Diezmado (Tema 2).** Cada nivel filtra y diezma por 2. Herramienta: [Diezmado e interpolación](T2-diezmado-interpolacion.html).
- **Filtros FIR (Tema 4).** h₀ y h₁ son FIR de fase casi lineal y bandas complementarias. Herramienta: [Diseño FIR por ventanas](T4-fir-ventana.html).
- **Aplicaciones.** Herramienta: [Eliminación de ruido y compresión con wavelets](T5-ruido-wavelet.html).
- **La transformada continua.** Herramienta: [Escalograma frente a espectrograma](T5-escalograma.html).
