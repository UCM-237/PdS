## Introducción

### Cambiar la frecuencia de muestreo sin pasar por analógico

A menudo hay que cambiar la frecuencia de muestreo de una señal ya digital: pasar audio de 48 a 32 kHz, reducir la tasa de una señal después de filtrarla o aumentarla antes de un conversor D/A. Se hace con dos operaciones básicas y un filtro.

### Compresor y diezmado

El **compresor** por M se queda con una de cada M muestras: y[n] = x[Mn]. Equivale a muestrear la señal original con fs/M. En frecuencia,

> Y(e^{jΩ}) = (1/M) Σ_{k=0}^{M−1} X(e^{j(Ω − 2πk)/M}):

el espectro se ensancha M veces y aparecen M − 1 copias desplazadas. Si X ocupa |Ω| ≤ Ω_m, no hay aliasing solo si Ω_m < π/M. Por eso, antes de comprimir se aplica un paso bajo de corte π/M, el filtro **antialiasing digital**. Filtro más compresor es el **diezmado**.

### Expansor e interpolación

El **expansor** por L intercala L − 1 ceros entre muestras: x_e[n] = x[n/L] si n es múltiplo de L y 0 si no. En frecuencia,

> X_e(e^{jΩ}) = X(e^{jΩL}):

el espectro se comprime L veces y, como sigue siendo periódico de periodo 2π, aparecen L − 1 **imágenes** en los múltiplos de 2π/L. Un paso bajo de corte π/L y ganancia L elimina las imágenes y rellena los ceros con valores interpolados: es la **interpolación**. La ganancia L compensa que el expansor reparte la energía en L veces más muestras.

### Cambio por un factor racional

Para cambiar la frecuencia por L/M se expande por L, se filtra y se comprime por M, en ese orden (al revés se perdería información). Los dos filtros paso bajo se combinan en uno solo, de corte min(π/L, π/M) = π/max(L, M) y ganancia L.

## Guía de uso

- **Señal** elige una secuencia con espectro triangular (de altura 1 y banda Ω_b) o dos tonos de frecuencias Ω_b/2 y Ω_b.
- **Ω_b/π** es la frecuencia máxima de la señal; **L** y **M**, los factores de interpolación y diezmado.
- **Con filtro o Sin filtro** quita el paso bajo para ver las imágenes y el aliasing.
- Cada fila es una etapa: entrada, tras el expansor, tras el filtro y tras el compresor. A la izquierda, la secuencia, con el tiempo en periodos de la entrada para que las etapas se alineen. A la derecha, el módulo de su espectro; en la tercera fila, en gris, el filtro ideal.
- El recuadro da la nueva frecuencia de muestreo, el corte del filtro y avisa de imágenes, aliasing o pérdida de banda.

## Ejercicios

**1. Diezmado sin filtro.** Con dos tonos y Ω_b/π = 0,4 (tonos en 0,2π y 0,4π), L = 1 y M = 3, sin filtro, ¿en qué frecuencias quedan los tonos? ¿Hay aliasing?

<details><summary>Solución</summary>
0,2π·3 = 0,6π y 0,4π·3 = 1,2π, que se pliega a −0,8π: el segundo tono aparece en 0,8π. Hay aliasing porque 0,4π > π/3. Con M = 2 no lo habría: 0,4π y 0,8π.
</details>

**2. El ejercicio 14 de la hoja, con el filtro.** En el caso anterior, pon el filtro. ¿Qué tono sobrevive y dónde queda? ¿Qué se gana y qué se pierde?

<details><summary>Solución</summary>
El filtro, de corte π/3, elimina el tono de 0,4π y deja el de 0,2π, que queda en 0,6π. Se pierde una componente, pero la otra no se contamina con un alias que ya no se podría separar.
</details>

**3. Imágenes del expansor.** Con el espectro triangular, Ω_b/π = 0,5, L = 3, M = 1 y sin filtro, ¿dónde están las imágenes? Pon el filtro: ¿qué ganancia tiene y por qué?

<details><summary>Solución</summary>
El triángulo se comprime a banda π/6 y aparecen imágenes centradas en ±2π/3 que ocupan π/2 ≤ |Ω| ≤ 5π/6 (ejercicio 15 b de la hoja). El filtro de corte π/3 y ganancia 3 deja solo la banda central y devuelve la altura 1 al espectro.
</details>

**4. El ejercicio 16 a de la hoja: de 48 a 32 kHz.** ¿Qué L y M hay que usar? ¿Qué corte tiene el filtro? Configúralo y comprueba que con Ω_b/π = 0,6 no hay aliasing pero sí pérdida.

<details><summary>Solución</summary>
32/48 = 2/3: L = 2, M = 3, y el corte es π/3 a la frecuencia intermedia de 96 kHz, es decir, 16 kHz, la frecuencia de Nyquist de la salida. Una señal hasta 0,6π de 48 kHz (14,4 kHz) cabe en πL/M = 0,667π y pasa entera; con Ω_b/π = 0,8 se perdería la parte por encima de 0,667π.
</details>

**5. Interpolar no añade información.** Con el espectro triangular, Ω_b/π = 1, L = 2 y M = 2 con filtro, ¿se recupera la señal original? ¿Y con L = 2, M = 1?

<details><summary>Solución</summary>
Con L = M = 2 el filtro corta en π/2 del espectro expandido, que corresponde a π/2 del original: se pierde la mitad superior de la banda, porque el compresor exige que la señal quepa en π/2. Con M = 1 la señal pasa entera y solo se duplica la frecuencia de muestreo, sin frecuencias nuevas.
</details>

## Para profundizar

- [Apuntes del Tema 2](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%20Apuntes.pdf), sección 6 (Muestreo de señales discretas): «Diezmado», «Expansión e interpolación» y «Cambio de frecuencia por un factor racional».
- [Transparencias T2-04](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%2004%20-%20Muestreo%20discreto.pdf), muestreo de señales discretas.
- [Hoja de ejercicios del Tema 2](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%20Ejercicios.pdf), ejercicios 14 a 16, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T2/codigo/python/cambio_frecuencia.py` y su versión en Matlab.
- A. V. Oppenheim y R. W. Schafer, *Discrete-Time Signal Processing*, 3.ª ed., Pearson, 2010, apartado 4.6.

## Relación con otros conceptos

- **Diezmado y expansión en el tiempo (Tema 1).** Herramienta: [Operaciones sobre la variable independiente](T1-variable-independiente.html).
- **Aliasing.** El compresor es un muestreo y pliega el espectro igual. Herramienta: [Aliasing](T2-aliasing.html).
- **Sobremuestreo.** Los conversores sobremuestrean y después diezman. Herramienta: [Sobremuestreo y conformado de ruido](T2-sobremuestreo.html).
- **Retenedores.** Interpolar antes del D/A aleja las imágenes del retenedor. Herramienta: [Retenedores](T2-retenedores.html).
- **Diseño FIR (Tema 4).** El filtro es un FIR paso bajo por ventanas. Herramienta: [FIR por el método de ventanas](T4-fir-ventana.html).
