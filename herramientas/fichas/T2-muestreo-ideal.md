## Introducción

### El modelo del tren de impulsos

Para estudiar el muestreo en frecuencia se modela como el producto de la señal por un tren de impulsos de periodo Ts:

> x_s(t) = x(t) · Σ_n δ(t − nTs) = Σ_n x(nTs) δ(t − nTs).

x_s(t) es una señal continua, pero solo contiene la información de las muestras x[n] = x(nTs): sus «pesos» son las muestras. Es un modelo matemático, no un circuito, y permite usar la transformada de Fourier continua para ver qué le pasa al espectro.

### El espectro se repite cada fs

Un producto en el tiempo es una convolución en frecuencia. La transformada de un tren de impulsos de periodo Ts es otro tren de impulsos, de periodo fs = 1/Ts y área fs, así que

> X_s(f) = fs · Σ_k X(f − k fs).

El espectro de la señal muestreada es la suma de copias de X(f), llamadas **réplicas**, desplazadas a cada múltiplo de fs y escaladas por fs. Muestrear no destruye el espectro original: lo repite.

### El teorema del muestreo

Si x(t) tiene banda limitada, X(f) = 0 para |f| > B, cada réplica ocupa [k fs − B, k fs + B]. Las réplicas no se solapan si fs − B > B, es decir, si

> fs > 2B.

Es el **teorema del muestreo** de Nyquist y Shannon, y 2B es la **tasa de Nyquist**. Cuando se cumple, un paso bajo ideal con corte entre B y fs − B y ganancia Ts aísla la réplica central y recupera x(t) exactamente. Cuando no se cumple, las réplicas se solapan y en la zona de solape se suman: es el **aliasing**, y ningún filtro posterior puede separar lo que se ha mezclado.

### Visión discreta

Si en lugar de x_s(t) se mira la secuencia x[n], su DTFT es X_s(f) con el cambio Ω = 2πf/fs. Las réplicas en k fs pasan a estar en Ω = 2πk: es la periodicidad de 2π de cualquier espectro discreto.

## Guía de uso

- La señal es x(t) = sinc²(Bt), cuyo espectro es un triángulo que ocupa |f| ≤ B. **B** fija el ancho de banda.
- **fs** fija la frecuencia de muestreo.
- Arriba, la señal y sus muestras. Abajo, el espectro original X(f) en azul, las réplicas X(f − k fs) en gris y su suma, multiplicada por fs, en rojo.
- El recuadro indica la tasa de Nyquist y, si hay solapamiento, a partir de qué frecuencia; si no lo hay, entre qué valores debe estar el corte del filtro de reconstrucción.

## Ejercicios

**1. La tasa de Nyquist.** Con B = 2 Hz, baja fs desde 12 hasta que las réplicas se toquen. ¿Para qué fs ocurre? ¿Coincide con la tasa de Nyquist?

<details><summary>Solución</summary>
Las réplicas se tocan en fs = 4 muestras/s = 2B. Por debajo, el triángulo central y el desplazado fs se solapan.
</details>

**2. El filtro de reconstrucción.** Con B = 2 Hz y fs = 5 muestras/s, ¿entre qué valores puede estar el corte de un paso bajo ideal que recupere x(t)? ¿Y con fs = 4,2?

<details><summary>Solución</summary>
Entre B = 2 y fs − B = 3 Hz. Con fs = 4,2, entre 2 y 2,2 Hz: cuanto más cerca de la tasa de Nyquist, más estrecha es la banda de transición que se le deja al filtro, y más difícil es construirlo.
</details>

**3. El ejercicio 4 c de la hoja.** x(t) = sinc²(f_c t) tiene banda f_c, no f_c/2. Con B = 3 Hz, ¿cuál es la mínima fs? Compruébalo.

<details><summary>Solución</summary>
Su espectro es un triángulo que ocupa |f| ≤ f_c = 3 Hz: hace falta fs > 6 muestras/s. Un sinc (sin cuadrado) tendría un espectro rectangular de banda f_c/2.
</details>

**4. Qué banda se salva.** Con B = 2 Hz y fs = 3 muestras/s, ¿en qué frecuencias hay aliasing? ¿Qué banda queda intacta?

<details><summary>Solución</summary>
La réplica en fs ocupa [1, 5] Hz y se solapa con la central en 1 ≤ |f| ≤ 2. La banda |f| < fs − B = 1 Hz queda intacta. En la zona de solape, la suma de los dos lados del triángulo da un valor constante: el espectro se aplana.
</details>

**5. El ejercicio 5 de la hoja, a escala.** La hoja muestrea un espectro triangular de banda 100 Hz a 300 y a 150 Hz. Divide todas las frecuencias por 50 (B = 2 Hz, fs = 6 y 3) y comprueba los apartados a y b.

<details><summary>Solución</summary>
Con fs = 6 quedan huecos de fs − 2B = 2 Hz entre réplicas (100 Hz en la hoja). Con fs = 3 hay solape en 1 ≤ |f| ≤ 2 (50 a 100 Hz en la hoja) y allí la suma vale la mitad del pico, constante; |f| < 1 Hz (50 Hz) se conserva intacta.
</details>

## Para profundizar

- [Apuntes del Tema 2](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%20Apuntes.pdf), sección 3, «Modelo con un tren de impulsos», «Espectro de la señal muestreada» y «Visión continua y visión discreta».
- [Transparencias T2-01](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%2001%20-%20Muestreo.pdf), «Espectro de la señal muestreada».
- [Hoja de ejercicios del Tema 2](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%20Ejercicios.pdf), ejercicios 3 a 5, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T2/codigo/python/espectro_muestreado.py` y su versión en Matlab.
- A. V. Oppenheim y R. W. Schafer, *Discrete-Time Signal Processing*, 3.ª ed., Pearson, 2010, apartados 4.1 a 4.3.

## Relación con otros conceptos

- **Transformada de Fourier.** El producto por el tren de impulsos se convierte en una convolución. Herramienta: [Propiedades de la transformada de Fourier](T1-propiedades-fourier.html).
- **Aliasing de sinusoides.** El caso más sencillo de solapamiento. Herramienta: [Aliasing](T2-aliasing.html).
- **Muestreo no ideal.** Con pulsos de anchura finita las réplicas cambian de amplitud. Herramienta: [Muestreo natural y de techo plano](T2-muestreo-natural.html).
- **Reconstrucción.** El paso bajo ideal que se queda con la réplica central. Herramientas: [Reconstrucción](T2-reconstruccion.html) y [Retenedores](T2-retenedores.html).
- **DFT (Tema 3).** La DFT muestrea el espectro: la dualidad hace que la señal se repita en el tiempo. Herramienta: [Extensión periódica](T3-extension-periodica.html).
