## Introducción

### Discretizar la amplitud

Muestrear discretiza el tiempo; **cuantificar** discretiza la amplitud. Un cuantificador uniforme de B bits divide el margen de entrada, aquí [−1, 1), en 2^B intervalos iguales de anchura

> Δ = 2/2^B,

el **paso de cuantificación**, y sustituye cada valor por un nivel: x_q = kΔ, con k entero entre −2^{B−1} y 2^{B−1} − 1. El índice k es lo que se codifica en binario (normalmente en complemento a dos). El margen bipolar es asimétrico: llega a −1 pero no a +1.

### Redondeo, truncamiento y saturación

- Con **redondeo** se elige el nivel más cercano y el error e = x_q − x está entre −Δ/2 y Δ/2.
- Con **truncamiento** se elige el nivel inmediatamente inferior y el error está entre −Δ y 0: tiene media −Δ/2, un sesgo.
- Si la entrada sale del margen, el cuantificador **satura** en el nivel extremo y el error ya no está acotado por Δ. Saturar es mucho peor que el ruido de cuantificación, así que se deja un margen de seguridad.

### El modelo de ruido aditivo

El cuantificador es un sistema no lineal y sin memoria. Si la señal varía lo suficiente de una muestra a otra (y no satura), el error se comporta como un **ruido** uniforme en [−Δ/2, Δ/2), independiente de la señal y blanco, con potencia

> σ_e² = Δ²/12.

Con ese modelo, la relación señal a ruido de cuantificación (SQNR) es P_x/σ_e². Para una sinusoide que ocupa todo el margen, P_x = 1/2 y

> SQNR = 6,02 B + 1,76 dB.

Cada bit más añade unos 6 dB. Si la amplitud es menor, la SQNR baja 20 log₁₀ de la fracción del margen que se usa: una señal a la cuarta parte del fondo de escala pierde 12 dB, dos bits.

### Cuándo falla el modelo

Con pocos bits, con señales muy pequeñas (del orden de Δ) o muy lentas, el error depende claramente de la señal: tiene forma, no parece ruido, y su histograma no es uniforme. Por eso a veces se añade un poco de ruido antes de cuantificar (*dither*).

## Guía de uso

- **Señal** elige una sinusoide, una suma de dos tonos, una rampa lenta o ruido gaussiano.
- **B** es el número de bits y **Amplitud**, la de la señal en relación con el fondo de escala (1).
- **Redondeo o Truncamiento** elige la regla.
- Arriba, la señal y la señal cuantificada, y la característica del cuantificador. Abajo, el error con sus límites teóricos y el histograma del error en unidades de Δ (sin las muestras saturadas).
- El recuadro da Δ, la media y la varianza del error frente a Δ²/12, la SQNR medida, la del modelo y la fórmula 6,02B + 1,76, y avisa si hay saturación.

## Ejercicios

**1. El ejercicio 11 de la hoja.** Con B = 3 bits, ¿cuánto vale Δ y cuáles son los niveles? Pon la sinusoide con amplitud 0,95: ¿satura? ¿Cuál es el error máximo?

<details><summary>Solución</summary>
Δ = 0,25 y los niveles van de −1 a 0,75 en pasos de 0,25. Con amplitud 0,95 los picos positivos superan 0,875 = 1 − Δ/2, así que el redondeo daría 1,0, que no es un nivel: satura en 0,75 y el error llega a −0,2, más que Δ/2 = 0,125.
</details>

**2. Seis decibelios por bit.** Con la sinusoide y amplitud 0,95, anota la SQNR para B = 6, 8, 10 y 12. ¿Cuánto sube por cada bit? ¿Por qué queda algo por debajo de 6,02B + 1,76?

<details><summary>Solución</summary>
Sube unos 6 dB por bit. Queda unos 0,45 dB por debajo porque la amplitud es 0,95 y no 1: 20 log₁₀ 0,95 ≈ −0,45 dB. Con B = 12, unos 73,6 dB.
</details>

**3. Redondeo frente a truncamiento.** Con B = 8 y la suma de tonos, cambia a truncamiento. ¿Qué pasa con la media del error y con la SQNR?

<details><summary>Solución</summary>
La media pasa de casi 0 a −Δ/2 y el histograma se desplaza a [−1, 0]. La potencia del error (media al cuadrado más varianza) pasa de Δ²/12 a Δ²/4 + Δ²/12 = Δ²/3, cuatro veces más: la SQNR baja unos 6 dB, un bit.
</details>

**4. Cuando el modelo falla.** Con B = 4 y la sinusoide, baja la amplitud a 0,02. ¿Qué sale del cuantificador? ¿Cuánto vale la SQNR? Prueba también la rampa lenta con B = 3.

<details><summary>Solución</summary>
Δ = 0,125 y la señal nunca pasa de Δ/2 = 0,0625: todas las muestras se redondean a 0. El error es −x y la SQNR medida es 0 dB, muy lejos de lo que predice el modelo. Con la rampa lenta el error es un diente de sierra perfectamente regular: no se parece a un ruido aleatorio.
</details>

**5. El ejercicio 13 de la hoja.** ¿Cuántos bits hacen falta para 80 dB con una sinusoide a fondo de escala? ¿Y si su amplitud es la cuarta parte? Comprueba la diferencia de 12 dB con B = 12, comparando amplitudes 0,95 y 0,24.

<details><summary>Solución</summary>
6,02B + 1,76 ≥ 80 da B = 13. Con un cuarto de la amplitud se pierden 12,04 dB y hacen falta 15 bits. En la herramienta, con B = 12, se pasa de unos 73,6 dB a unos 61,6 dB.
</details>

## Para profundizar

- [Apuntes del Tema 2](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%20Apuntes.pdf), sección 5 (Cuantificación y codificación).
- [Transparencias T2-03](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%2003%20-%20Cuantificaci%C3%B3n.pdf), cuantificación y ruido de cuantificación.
- [Hoja de ejercicios del Tema 2](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%20Ejercicios.pdf), ejercicios 11 a 13, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T2/codigo/python/cuantificacion.py` y su versión en Matlab.
- A. V. Oppenheim y R. W. Schafer, *Discrete-Time Signal Processing*, 3.ª ed., Pearson, 2010, apartado 4.8.

## Relación con otros conceptos

- **Energía y potencia.** La SQNR es un cociente de potencias. Herramienta: [Par, impar, energía y potencia](T1-par-impar-energia.html).
- **Sistemas no lineales.** El cuantificador no es lineal. Herramienta: [Propiedades de los sistemas](T1-propiedades-sistemas.html).
- **Sobremuestreo.** El mismo ruido Δ²/12 repartido en más banda. Herramienta: [Sobremuestreo y conformado de ruido](T2-sobremuestreo.html).
- **Cuantificación de coeficientes (Tema 4).** Redondear los coeficientes de un filtro mueve sus polos. Herramienta: [Cuantificación de coeficientes](T4-cuantificacion-coeficientes.html).
- **Procesos aleatorios (Tema 6).** El modelo de ruido blanco uniforme se formaliza con la autocorrelación y la densidad espectral de potencia.
