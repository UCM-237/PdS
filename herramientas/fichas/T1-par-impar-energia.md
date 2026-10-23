## Introducción

### Señales pares e impares

Una señal es **par** si x(−t) = x(t): su gráfica es simétrica respecto al eje vertical, como cos(t). Es **impar** si x(−t) = −x(t): es antisimétrica, como sin(t), y necesariamente x(0) = 0. La mayoría de las señales no son ni pares ni impares, pero cualquiera se descompone de forma única en una parte par y otra impar:

> x_p(t) = [x(t) + x(−t)]/2,  x_i(t) = [x(t) − x(−t)]/2,  x(t) = x_p(t) + x_i(t).

En tiempo discreto las definiciones son las mismas con n en lugar de t. Para señales complejas, el papel de la paridad lo hace la simetría **hermítica**, x*(−t) = x(t).

La paridad importa en frecuencia: una señal real y par tiene una transformada de Fourier real y par, y una real e impar, una transformada imaginaria pura e impar.

### Energía y potencia

La **energía** de una señal mide su «tamaño» total:

> E = ∫ |x(t)|² dt (en continuo),  E = Σ |x[n]|² (en discreto),

y la **potencia media** es la energía por unidad de tiempo en una ventana cada vez mayor:

> P = lim_{T→∞} (1/2T) ∫_{−T}^{T} |x(t)|² dt,  P = lim_{N→∞} (1/(2N + 1)) Σ_{n=−N}^{N} |x[n]|².

Si una señal es de duración finita, o decae lo bastante deprisa, tiene E finita y P = 0: es una **señal de energía**. Si tiene E infinita pero P finita y no nula, como una sinusoide, un escalón o cualquier señal periódica, es una **señal de potencia**. Algunas, como la rampa, no son ni lo uno ni lo otro.

### Energía de las partes par e impar

El producto x_p·x_i es impar, así que su integral es nula. Por eso la energía se reparte sin términos cruzados:

> E_x = E_p + E_i.

### Cómo se ve en las gráficas

Las dos gráficas de abajo calculan E(T) y P(T) en la ventana [−T, T] para T de 1 a 1000. Si E(T) se aplana, la señal es de energía; si P(T) tiende a un valor no nulo, es de potencia; si las dos crecen, no es de ninguno de los dos tipos.

## Guía de uso

- **Señal** elige entre un pulso rectangular (1 en [0,5; 2,5)), una exponencial causal, un escalón, una sinusoide, una rampa y una exponencial bilateral impar, sgn(t)·e^{−a|t|}.
- **a** es el decaimiento de las exponenciales y **φ** la fase de la sinusoide, cos(t + φ).
- **t₀** desplaza la señal: x(t − t₀). Desplazar cambia la parte par e impar, pero no la energía ni la potencia.
- **Continuo o Discreto** usa t real o n entero (las sumas sustituyen a las integrales).
- Arriba, x y su reflejada x(−t); en medio, x_p y x_i; abajo, E(T) y P(T) en escala logarítmica de T.

## Ejercicios

**1. Descomponer un escalón.** Con el escalón y t₀ = 0, ¿cuánto valen x_p(t) y x_i(t)? ¿Es de energía o de potencia?

<details><summary>Solución</summary>
x_p(t) = 1/2 para todo t ≠ 0 y x_i(t) = sgn(t)/2. Su energía es infinita y P = 1/2: es una señal de potencia (ejercicio 3 b de la hoja). P(T) se acerca a 0,5 en la gráfica.
</details>

**2. Repartir la energía.** Con el pulso rectangular, calcula a mano E_x, E_p y E_i. Comprueba en el recuadro que E_x = E_p + E_i.

<details><summary>Solución</summary>
E_x = 2 (amplitud 1 durante 2 unidades). Como el pulso y su reflejado no se solapan, x_p y x_i valen ±1/2 en un intervalo total de longitud 4: E_p = E_i = 4·(1/2)² = 1, y 1 + 1 = 2.
</details>

**3. Exponencial causal.** Con a = 0,5, ¿cuánto vale la energía? Compárala con la del caso discreto, Σ e^{−2an} para n ≥ 0.

<details><summary>Solución</summary>
En continuo, E = ∫₀^∞ e^{−2at} dt = 1/(2a) = 1. En discreto, Σ (e^{−1})ⁿ = 1/(1 − e^{−1}) ≈ 1,58. La suma no es una aproximación de la integral con paso 1: cada muestra cuenta como una unidad de tiempo completa y la de n = 0 ya vale 1.
</details>

**4. Fase y paridad.** Con la sinusoide, ¿qué φ hace que la señal sea par? ¿Y impar? ¿Cambia la potencia con φ?

<details><summary>Solución</summary>
φ = 0 (o π) da ±cos t, par, con x_i = 0. φ = ±π/2 da ∓sin t, impar, con x_p = 0. Para otros φ, x_p = cos φ cos t y x_i = −sin φ sin t. La potencia es siempre 1/2.
</details>

**5. Ni energía ni potencia.** Con la rampa t·u(t), mira E(T) y P(T). Compáralo con el ejercicio 3 a de la hoja, x(t) = t.

<details><summary>Solución</summary>
E(T) = T³/3 y P(T) = T²/6 crecen sin límite: la rampa no es de energía ni de potencia. Para x(t) = t la potencia en [−T, T] es T²/3, que también diverge.
</details>

## Para profundizar

- [Apuntes del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Apuntes.pdf), sección 2, apartados «Pares e impares» y «Señales de energía y de potencia».
- [Transparencias T1-01](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%2001%20-%20Se%C3%B1ales.pdf), clasificación de señales.
- [Hoja de ejercicios del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios.pdf), ejercicios 2 y 3, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T1/codigo/python/energia_potencia.py` y su versión en Matlab.
- A. V. Oppenheim, A. S. Willsky y S. H. Nawab, *Signals and Systems*, 2.ª ed., Prentice Hall, 1997, apartados 1.1 y 1.2.

## Relación con otros conceptos

- **Inversión de la variable independiente.** x(−t) es la base de la descomposición. Herramienta: [Operaciones sobre la variable independiente](T1-variable-independiente.html).
- **Teorema de Parseval.** La energía se puede calcular también en frecuencia, con |X(f)|². Herramientas: [Propiedades de la transformada de Fourier](T1-propiedades-fourier.html) y [Serie de Fourier](T1-serie-fourier.html), que lo usa con la potencia.
- **Simetrías de la DFT (Tema 3).** La versión circular de la parte par e impar tiene DFT real e imaginaria. Herramienta: [Propiedades de la DFT](T3-propiedades-dft.html).
- **Potencia de ruido (Temas 2 y 6).** La SQNR es un cociente de potencias. Herramienta: [Cuantificación y SQNR](T2-cuantificacion.html).
