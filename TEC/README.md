# Trabajo de Evaluación Continua (TEC) temas 1, 2, y 3.
En este trabajo, vamos a realizar algunas tareas de procesamiento de señales en la plataforma Raspberry Pi Pico, un sistema basado en un microcontrolador RP2040 que destaca por su flexibilidad y potencia en relación a su bajo coste.	
Entre otras cosas, el microcontrolador RP2040 tiene una arquitectura de doble núcleo (*Dual-core Arm Cortex M0+*), con una frecuencia de reloj variable hasta 133 MHz, 264 kB de memoria SRAM y 2MB de memoria flash.
Sus capacidades de entrada salida ([ver diagrama](pinout)) la hacen una plataforma apta para el desarrollo de aplicaciones relacionadas con el procesamiento de señales, ya que cuenta con 3 canales de entrada ADC con una resolución de 12 bits, y
hasta 16 canales de salida PWM (*Pulse Width Modulation*), 2 canales SPI, 2 I2C, y 2 UART, además de 8 máquinas de estado, *Programmable I/O* (PIO), útiles para dar soporte a periféricos propios.


## Objetivos
1. Ser capaz de implementar algoritmos básicos de generación y análisis de señales en una plataforma digital.

## Tareas a realizar
1. Genera una señal y envíala a la salida PWM
2. Conecta el sensor LDR a uno de los canales de entrada analógicos (ADC) y realiza una adquisición de la señal.
3. Implementa el algoritmo de diezmado temporal en base 2 para calcular la Transformada de Fourier Discreta (DFT).


## Raspberry Pi Pico
La plataforma Raspberry Pi Pico es un sistema basado en un microcontrolador RP2040 de bajo coste (~5€) y alto rendimiento.
Entre sus características, el microcontrolador RP2040 posee una arquitectura de doble núcleo (*Dual-core Arm Cortex M0+*), con una frecuencia de reloj (variable) hasta 133 MHz, 264 kB de memoria SRAM y 2MB de memoria flash.
Sus capacidades de entrada salida ([ver diagrama](#pinout)) la hacen una plataforma apta para el desarrollo de aplicaciones relacionadas con el procesamiento de señales, ya que cuenta con 3 canales de entrada ADC con una resolución de 12 bits, y
hasta 16 canales de salida PWM (*Pulse Width Modulation*), 2 canales SPI, 2 I2C, y 2 UART, además de 8 máquinas de estado, *Programmable I/O* (PIO), útiles para dar soporte a periféricos propios.

![pinout](./img/pico_pinout.png)

Todas estas características la hacen convenientes para aplicaciones de procesamiento de señales. En este trabajo implementaremos en la plataforma Raspberry Pi Pico la generación y adquisición de señales muestreadas y
algoritmos de cálculo de la Transformada Rápida de Fourier (FFT). De esta manera se pretende dar una visión práctica del proceso de adquisición, almacenamiento y procesado de una señal desde un punto de vista práctico.

## Transformada Rápida de Fourier (FFT)
La Transformada Discreta de Fourier es una herramienta de análisis muy importante en muchas aplicaciones de tratamiento digital de la señal. Una razón fundamental es la existencia de algoritmos eficientes para calcular la DFT. En este trabajo centramos la atención en la familia de algoritmos conocidos como Transformada Rápida de Fourier (FFT), basados en el enfoque algorítmico [*divide y vencerás*](https://es.wikipedia.org/wiki/Algoritmo_divide_y_vencer%C3%A1s).

La idea fundamental de estos métodos es la de resolver un problema dividiéndolo recursivamente en un subconjunto de problemas más faciles de resolver. De esta manera, el cálculo de una DFT de longitud $N$ se puede descomponer en el cálculo de diferentes DFT de menor longitud. 
En particular, en el algoritmo de diezmado en base 2, el problema de calcular una DFT de longitud $N$ se divide en el cálculo de dos DFT de longitud $N/2$. Esta división se aplica sucesivamente, hasta llegar a $N=2$, caso que se resuelve directamente. 
Vamos a verlo más detalladamente. Supongamos que tenemos una secuencia cuya longitud es $N=2^L$ (la longitud debe ser una potencia de dos para asegurar que podemos sucesivamente en dos mitades. En caso contrario, si la secuencia tiene una longitud $M < N=2^L$, la rellenaríamos con ceros hasta llegar a $N$, previamente al cálculo de la DFT. Definimos $W_N^{k\cdot n}=\mathrm{e}^{-j \frac{2\pi}{N}kn}$ por conveniencia, entonces $X[k]=\sum_{n=0}^{N-1} x[n]\mathrm{e}^{-j \frac{2\pi}{N}kn}= \sum_{n=0}^{N-1} W_N^{kn}x[n]$.

Ahora dividimos en dos secuencias de longitud $N/2$:

$$ X[k]=\sum_{n=0}^{N/2-1} x[2r]W_N^{k \cdot 2r} + \sum_{n=0}^{N/2-1} x[2r+1] W_N^{k\cdot(2r+1)} $$

Es decir, vemos que se puede descomponer el cálculo separando los elementos pares por un lado ($f[n]=x[2n]$) y los impares por otro $g[n]=x[2n+1]$, y cálculando por tanto dos DFT de longitud $N/2$.

$$ F[k]=\sum_{r=0}^{N/2-1} x[2r] W_N^{k\cdot 2r}   =\sum_{n=0}^{N/2-1} f[n] W_{\frac{N}{2}} ^{k\cdot n} $$

$$ G[k]=\sum_{r=0}^{N/2-1} x[2r+1] W_N^{k\cdot 2r} =\sum_{n=0}^{N/2-1} g[n] W_{\frac{N}{2}} ^{k\cdot n} $$

<span id="fft_calculo_1">(1)</span>

Que ahora podemos combinar mediante la siguiente expresión:

$$X[k]=F[k] + W_N^{k} G[k]$$
<span id="fft_calculo_2">(2)</span>

La ecuación [Eq. 2](fft_calculo_2) nos dice cómo calcular los valores de las muestras de la DFT de $x$ para $0\leq k < N/2$. Lo interesante es que podemos aprovechar las propiedades de periodicidad y simetría de la DFT para calcular las restantes muestras, sabiendo que $X[k+N/2]=F[K+N/2] + W_N^{k+N/2} G[k+N/2]$.

Teniendo en cuenta que $W_N^{k+N/2}=-W_N^{k}$, y que $F[k]$ y $G[k]$ son periódicas de periodo N/2, finalmente nos queda:

$$X[k]=  \begin{matrix}F[k] + W_N^{k} G[k] \& 0 \leq k < N/2 \\\\ F[k] - W_N^{k} G[k] & N/2 \leq k < N \end{matrix}$$

<span id="fft_2">(3)</span>


En resumen, el cálculo la DFT de una secuencia discreta de longitud $N$ se puede descomponer, utilizando [(1)](fft_calculo_1)), en el cálculo de dos DFT de longitud $\frac{N}{2}$. Por otra parte, [(2)](eq:fft_calculo_2) y [(3)](eq:fft_2) nos indican la manera de recombinarlas en una sola DFT de $N$ muestras. Pero, ¿hemos ganado con la descomposición? Vamos a analizarlo *grosso modo*. Resulta que desde un punto de vista computacional, si medimos la complejidad según el número de operaciones complejas (*no pun inteded*), la DFT de una secuencia de longitud $N$ requiere de $N^2$ sumas y $N^2$ productos complejos. Sin embargo, el cálculo mediante [(1)](fft_calculo_1), [(2)](fft_calculo_2) y [(3)](fft_2) conlleva $\frac{N^2}{2}$ y otros tantos productos (En realidad, el cálculo de las operaciones es algo más elaborado, pero esta aproximación debería bastar para ilustrar el beneficio obtenido). Esto *per se* ya puede suponer un ahorro para valores grandes de $N$. Como ejemplo, para $N=5000$ el cálculo directo supone $N^2=25000$ operaciones, frente a $\frac{N^2}{2}=12500$. Además, esta descomposición ese puede aplicar de forma recursiva, con lo que se obtiene una mayor reducción en el número de operaciones. Se puede demostrar que, mientras que para el cálculo directo de la DFT el orden de complejidad del algoritmo es $N^2$, para el diezmado temporal en base 2 se reduce a $N log(N)$. A medida que $N$ aumenta, esta mejora puede suponer la diferencia entre poder abordar o no el cálculo de la DFT, como veremos en la tarea 1.
