## Introducción

### Observar es enventanar

Analizar L muestras de una señal larga es multiplicarla por una **ventana** w[n] que vale 1 en esas muestras y 0 fuera. Por la propiedad de modulación, el espectro observado es el verdadero convolucionado con el de la ventana:

> X_w(e^{jΩ}) = (1/2π) ∫ X(e^{jθ}) W(e^{j(Ω − θ)}) dθ.

Un tono, que debería ser una línea, se convierte en una copia de W(e^{jΩ}) centrada en su frecuencia. La forma de |W| decide qué se puede ver.

### Lóbulo principal y lóbulos secundarios

- El **lóbulo principal** fija la **resolución**: dos tonos más próximos que su semianchura se funden en un solo pico.
- Los **lóbulos secundarios** fijan la **fuga**: la energía de un tono fuerte se derrama por todo el espectro y puede tapar un tono débil lejano.

La ventana rectangular tiene el lóbulo principal más estrecho posible, 4π/L entre ceros, pero sus lóbulos secundarios solo bajan a −13 dB, porque corta la señal de golpe. Las ventanas que bajan suavemente a cero en los extremos tienen lóbulos secundarios mucho más bajos a cambio de un lóbulo principal más ancho.

### Las ventanas clásicas

Las de la herramienta son de la forma w[n] = a₀ − a₁ cos(2πn/(L − 1)) + a₂ cos(4πn/(L − 1)):

| Ventana | (a₀, a₁, a₂) | Lóbulo principal | Lóbulo secundario |
|---|---|---|---|
| Rectangular | (1, 0, 0) | 4π/L | −13 dB |
| Hann | (0,5; 0,5; 0) | 8π/L | −31 dB |
| Hamming | (0,54; 0,46; 0) | 8π/L | −42 dB |
| Blackman | (0,42; 0,5; 0,08) | 12π/L | −58 dB |

Hamming tiene el primer lóbulo secundario más bajo que Hann, pero sus lóbulos no decrecen con la frecuencia; los de Hann caen 18 dB por octava. Hann es una buena opción general. La rectangular conviene si la señal contiene un número entero de periodos o es un transitorio que cabe entero.

### Escala

La ventana reduce la amplitud del pico: un tono de amplitud A da |X_w| ≈ (A/2) Σ w[n]. Para leer amplitudes se divide por Σ w[n] en vez de por L, que es lo que hace la herramienta.

## Guía de uso

- **Ventana** elige la forma y **L**, la longitud.
- La señal tiene dos tonos: uno de amplitud 1 en F₁ = 0,2 ciclos por muestra y otro de amplitud **A₂** (en dB) separado **F₂ − F₁**.
- Arriba, la ventana y la señal enventanada, y el espectro de la ventana. Abajo, el espectro de la señal enventanada, normalizado para que un tono de amplitud 1 dé 0 dB.
- **dB o Lineal** cambia la escala. El recuadro mide el lóbulo principal y el secundario más alto de la ventana elegida.

## Ejercicios

**1. La tabla de las ventanas.** Con L = 64, anota para cada ventana la anchura del lóbulo principal (en múltiplos de 2π/L) y el nivel del lóbulo secundario más alto. Compáralo con la tabla.

<details><summary>Solución</summary>
Rectangular: 2·2π/L y −13,3 dB. Hann: unas 4·2π/L y −31,5 dB. Hamming: unas 4·2π/L y −42,4 dB. Blackman: unas 6·2π/L y −58,1 dB. Las anchuras salen algo mayores que 4, 4 y 6 porque la herramienta usa la forma simétrica, con L − 1 en el denominador.
</details>

**2. Un tono débil cercano.** Con L = 64, F₂ − F₁ = 0,05 y A₂ = −40 dB, ¿con qué ventanas se ve el segundo tono?

<details><summary>Solución</summary>
Solo con Blackman, con un pico claro en −40 dB. El tono está a 3,2·(1/L) del fuerte: con la rectangular y Hamming cae bajo lóbulos secundarios más altos que él (unos −20 y −36 dB), y con Hann cae en la falda del lóbulo principal. Con F₂ − F₁ = 0,1 ya se ve también con Hann y Hamming.
</details>

**3. Un tono muy débil y lejano.** Con L = 256, F₂ − F₁ = 0,2 y A₂ = −80 dB, compara las cuatro ventanas. ¿Por qué falla Hamming?

<details><summary>Solución</summary>
Con Hann y Blackman se ve el tono a −80 dB. Con la rectangular, los lóbulos secundarios a esa distancia están en torno a −41 dB; con Hamming, en torno a −57 dB. Los lóbulos de Hamming empiezan más bajos que los de Hann pero no decrecen; los de Hann, lejos del tono, son mucho más bajos.
</details>

**4. Resolución.** Pon A₂ = 0 dB y F₂ − F₁ = 0,05. ¿A partir de qué L se ven dos picos en su sitio con la rectangular? ¿Y con Hann?

<details><summary>Solución</summary>
Hace falta |F₂ − F₁| mayor que la semianchura del lóbulo, 1/L con la rectangular y 2/L con Hann. Con la rectangular, unos L = 32 (0,05·32 = 1,6); con Hann, unos L = 48. Con L menores los picos se funden o aparecen desplazados, porque los dos tonos interfieren. Es el ejercicio 12 a de la hoja: Hann necesita el doble de muestras.
</details>

**5. El ejercicio 11 b de la hoja: la ventana cambia la escala.** Con Hann, en escala lineal, ¿qué valor tiene el pico de un tono de amplitud 1? ¿Por qué no es L/2, como con la rectangular?

<details><summary>Solución</summary>
La herramienta normaliza por Σw[n], así que el pico vale 1 con cualquier ventana. Sin normalizar, |X_w| ≈ Σw/2, y para Hann Σw ≈ L/2: el pico sería la mitad que con la rectangular. Por eso la amplitud se lee como 2|X_w[k₀]|/Σw[n]; en la hoja, 2·48/32 = 3.
</details>

## Para profundizar

- [Apuntes del Tema 3](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%20Apuntes.pdf), sección 4 (Análisis espectral con la DFT), «Fuga espectral», «Ventanas» y «Resolución y relleno con ceros».
- [Transparencias T3-03](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%2003%20-%20An%C3%A1lisis%20espectral.pdf), ventanas y resolución.
- [Hoja de ejercicios del Tema 3](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%20Ejercicios.pdf), ejercicios 11 y 12, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T3/codigo/python/espectro_dft.py` y su versión en Matlab.
- F. J. Harris, «On the use of windows for harmonic analysis with the discrete Fourier transform», *Proceedings of the IEEE*, 66(1), 1978.
- A. V. Oppenheim y R. W. Schafer, *Discrete-Time Signal Processing*, 3.ª ed., Pearson, 2010, apartados 7.5 y 10.2.

## Relación con otros conceptos

- **DFT y fuga.** Herramienta: [DFT, fuga y relleno con ceros](T3-dft.html).
- **Diseño FIR por ventanas (Tema 4).** Las mismas ventanas, aplicadas a la respuesta al impulso ideal: el lóbulo principal fija la banda de transición y los secundarios, el rizado. Herramienta: [FIR por el método de ventanas](T4-fir-ventana.html).
- **Propiedades de la transformada de Fourier (Tema 1).** Multiplicar en el tiempo es convolucionar en frecuencia. Herramienta: [Propiedades de la transformada de Fourier](T1-propiedades-fourier.html).
- **Espectrograma y densidad espectral (Tema 6).** Se calculan con ventanas deslizantes.
