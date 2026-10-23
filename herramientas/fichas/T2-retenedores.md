## Introducción

### Un retenedor es un filtro

Todo método de reconstrucción que forme la salida sumando una misma forma de pulso por cada muestra,

> x_r(t) = Σ_n x[n] h(t − nTs),

es un filtro de respuesta al impulso h(t) aplicado al tren de impulsos de las muestras. Su respuesta en frecuencia H(f) dice dos cosas: cuánto **deforma la banda base** (|f| < fs/2), que debería pasar con ganancia constante, y cuánto **deja pasar de las réplicas** (alrededor de k fs), que debería eliminar.

### Los cuatro retenedores

| Retenedor | h(t) | H(f)/Ts |
|---|---|---|
| Ideal | sinc(t/Ts) | 1 en ∣f∣ < fs/2, 0 fuera |
| Orden cero (ZOH) | pulso de 1 en [0, Ts) | sinc(f/fs) e^{−jπf/fs} |
| Orden uno no causal (FOH) | triángulo de base [−Ts, Ts] | sinc²(f/fs) |
| Orden uno predictivo | 1 + t/Ts en [0, Ts), 1 − t/Ts en [Ts, 2Ts) | (1 + j2πf Ts) sinc²(f/fs) e^{−j2πf/fs} |

### Lo que se ve en sus espectros

- El **ZOH** atenúa la banda base: en fs/2, |sinc(0,5)| = 0,64 (−3,9 dB). Sus lóbulos laterales caen como 1/f, así que deja pasar bastante de las réplicas. Retrasa la señal Ts/2.
- El **FOH** también atenúa la banda base (−7,8 dB en fs/2), pero sus lóbulos caen como 1/f²: atenúa mucho mejor las réplicas. No es causal; retrasado una muestra, es causal con el mismo módulo.
- El **predictivo** es causal, pero el factor |1 + j2πf Ts| realza las altas frecuencias: su salida tiene saltos.
- Los ceros de sinc(f/fs) están en los múltiplos de fs, justo en el centro de las réplicas: por eso los retenedores eliminan bien las réplicas de componentes de baja frecuencia y mal las de componentes cercanas a fs/2.

### En un conversor D/A

Casi todos los D/A usan un ZOH seguido de un **filtro de suavizado** analógico. La caída sinc de la banda base se compensa con un ecualizador digital (ganancia 1/sinc). Para relajar el filtro analógico, se interpola antes en digital: con fs cuatro veces mayor, la banda útil queda en la parte plana del sinc y las réplicas, mucho más lejos.

## Guía de uso

- **Lineal o dB** cambia la escala del módulo.
- A la izquierda, las cuatro respuestas al impulso, con el tiempo en unidades de Ts. A la derecha, el módulo de H(f)/Ts con la frecuencia en unidades de fs: la banda base es f/fs < 0,5.
- Haz clic en la leyenda para ocultar o mostrar cada retenedor.

## Ejercicios

**1. La atenuación del ZOH.** ¿Cuánto atenúa el ZOH una componente en f = fs/4 y en f = fs/2? Léelo en dB.

<details><summary>Solución</summary>
sinc(0,25) ≈ 0,90 (−0,9 dB) y sinc(0,5) ≈ 0,64 (−3,9 dB). Una componente cerca de fs/2 sale bastante atenuada.
</details>

**2. Las réplicas.** Compara el ZOH y el FOH en f = 1,5 fs, el centro del segundo lóbulo lateral. ¿Cuántos dB más atenúa el FOH?

<details><summary>Solución</summary>
|sinc(1,5)| ≈ 0,21, es decir, −13,5 dB para el ZOH, y sinc² ≈ 0,045, −26,9 dB para el FOH: unos 13 dB más. En dB, el FOH es exactamente el doble que el ZOH.
</details>

**3. El predictivo en fs/2.** ¿Cuánto vale |H(f)|/Ts del FOH predictivo en f = fs/2? ¿Atenúa o amplifica?

<details><summary>Solución</summary>
|1 + jπ|·sinc²(0,5) ≈ 3,30·0,405 ≈ 1,34: amplifica un 34 %. El realce de las frecuencias altas es el precio de la causalidad sin retardo.
</details>

**4. El ejercicio 9 de la hoja: D/A de audio.** Con fs = 44,1 kHz, un tono de 20 kHz está en f/fs ≈ 0,454 y su primera imagen en (44,1 − 20)/44,1 ≈ 0,546. Lee en la curva del ZOH en dB cuánto se atenúan uno y otra.

<details><summary>Solución</summary>
−3,17 dB en 0,454 y −4,79 dB en 0,546. La imagen queda solo 1,6 dB por debajo del tono: el ZOH no basta y hace falta un filtro analógico muy abrupto entre 20 y 24,1 kHz.
</details>

**5. Compensar el ZOH.** ¿Qué ganancia debe tener un ecualizador digital en 20 kHz para el caso anterior? ¿Y si antes se interpola por 4 (fs = 176,4 kHz)?

<details><summary>Solución</summary>
1/sinc(0,454) ≈ 1,44 (+3,17 dB). Con fs = 176,4 kHz, 20 kHz está en f/fs ≈ 0,113 y la atenuación es solo 0,18 dB; la primera imagen está en 156,4 kHz, unos 18 dB por debajo, y el filtro analógico puede ser muy sencillo.
</details>

## Para profundizar

- [Apuntes del Tema 2](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%20Apuntes.pdf), sección 4, «Retenedor de orden cero», «Retenedor de orden uno» y «Comparación y conversión D/A».
- [Transparencias T2-02](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%2002%20-%20Reconstrucci%C3%B3n.pdf), «Comparación de los retenedores».
- [Hoja de ejercicios del Tema 2](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%20Ejercicios.pdf), ejercicios 8 y 9, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T2/codigo/python/retenedores.py` y su versión en Matlab.
- A. V. Oppenheim y R. W. Schafer, *Discrete-Time Signal Processing*, 3.ª ed., Pearson, 2010, apartado 4.8.

## Relación con otros conceptos

- **Reconstrucción en el tiempo.** Las mismas cuatro reglas aplicadas a una señal. Herramienta: [Reconstrucción](T2-reconstruccion.html).
- **Muestreo de techo plano.** Es un ZOH con pulsos más cortos. Herramienta: [Muestreo natural y de techo plano](T2-muestreo-natural.html).
- **Transformada de Fourier del pulso y del triángulo.** sinc y sinc². Herramienta: [Propiedades de la transformada de Fourier](T1-propiedades-fourier.html).
- **Interpolación antes del D/A.** Herramienta: [Diezmado e interpolación](T2-diezmado-interpolacion.html).
- **Invarianza al impulso (Tema 4).** Discretizar un filtro analógico también supone elegir cómo se interpreta la señal entre muestras. Herramienta: [Discretización de filtros IIR](T4-discretizacion-iir.html).
