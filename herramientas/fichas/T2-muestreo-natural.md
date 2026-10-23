## Introducción

### Muestrear con pulsos

Un conversor real no puede tomar valores instantáneos: la señal se observa durante un intervalo corto τ, o se retiene mientras se convierte. Se modela sustituyendo los impulsos del muestreo ideal por pulsos de anchura τ, con un **ciclo de trabajo** d = τ/Ts. Hay dos variantes.

### Muestreo natural

El pulso sigue a la señal mientras dura: x_s(t) = x(t)·p(t), con p(t) un tren de pulsos rectangulares de altura 1. Como p(t) es periódica, su serie de Fourier tiene coeficientes c_k = d·sinc(kd) y

> X_s(f) = Σ_k d·sinc(kd) X(f − k fs).

Cada réplica conserva la forma de X(f); solo cambia su amplitud. La banda base queda multiplicada por d y no se distorsiona, así que un paso bajo sigue recuperando x(t) (escalada). Si d = 1/2, se anulan las réplicas pares, porque sinc(k/2) = 0 para k par no nulo.

### Muestreo de techo plano

El pulso mantiene el valor de la muestra: x_s(t) = Σ_n x(nTs) rect((t − nTs)/τ), que es el muestreo ideal seguido de un filtro con respuesta al impulso rectangular. Por tanto

> X_s(f) = τ sinc(fτ) e^{−jπfτ} · (1/Ts) Σ_k X(f − k fs).

Ahora todo el espectro, incluida la banda base, queda multiplicado por sinc(fτ): la señal recuperada con un paso bajo está distorsionada, con las frecuencias altas más atenuadas. El efecto crece con τ. Se corrige con un **ecualizador** de ganancia 1/sinc(fτ) en la banda útil, o haciendo τ pequeño frente a 1/B.

### El caso límite: τ = Ts

Con techo plano y d = 1, cada muestra se mantiene hasta la siguiente: es el **retenedor de orden cero** de los conversores D/A, que atenúa la banda base según |sinc(f/fs)|, un 36 % (−3,9 dB) en fs/2.

## Guía de uso

- **Natural o Techo plano** elige el tipo de muestreo.
- **fs** es la frecuencia de muestreo y **τ/Ts** el ciclo de trabajo d.
- La señal es x(t) = sinc²(2t), con espectro triangular de banda B = 2 Hz.
- Arriba, x(t) y la señal muestreada con pulsos. Abajo, el módulo del espectro (multiplicado por Ts), con la envolvente que escala las réplicas.
- El recuadro explica cómo se escalan las réplicas y, en techo plano, cuánto se atenúa la señal en f = B.

## Ejercicios

**1. Réplicas que desaparecen.** Con muestreo natural, fs = 6 y d = 0,5, ¿qué réplicas se anulan? ¿Y con d = 0,25?

<details><summary>Solución</summary>
La réplica k se escala por d·sinc(kd). Con d = 0,5 se anulan las de k par (±2, ±4…); con d = 0,25, las de k múltiplo de 4. La banda base solo se escala por d.
</details>

**2. Distorsión de techo plano.** Con techo plano, fs = 6 y d = 0,3, ¿cuánto vale τ? ¿Cuánto se atenúa la componente de f = B = 2 Hz respecto a la de f = 0?

<details><summary>Solución</summary>
τ = 0,3/6 = 0,05 s. La atenuación es sinc(2·0,05) = sinc(0,1) ≈ 0,984: un 1,6 %. Con d = 1 (τ = 1/6 s) sería sinc(1/3) ≈ 0,83, un 17 %.
</details>

**3. El retenedor de orden cero.** Con techo plano y d = 1, ¿cuánto se atenúa una componente en fs/2? ¿Depende de fs?

<details><summary>Solución</summary>
τ = Ts, así que sinc(fτ) en f = fs/2 vale sinc(0,5) = 2/π ≈ 0,64, −3,9 dB, para cualquier fs. Lo que depende de fs es qué parte de la señal cae cerca de fs/2.
</details>

**4. Natural frente a techo plano.** Con fs = 6 y d = 0,6, compara los dos espectros en la banda base. ¿Cuál se puede recuperar con un simple paso bajo?

<details><summary>Solución</summary>
En el natural, la banda base es 0,6·X(f), sin deformar: un paso bajo la recupera (con ganancia 1/d). En el de techo plano, con τ = 0,1 s, es X(f)·sinc(0,1f) (salvo una constante y un retardo), que en f = 2 vale sinc(0,2) ≈ 0,94: hace falta un ecualizador.
</details>

**5. Diseñar el ecualizador.** Con techo plano, fs = 6 y d = 1, ¿qué ganancia debe tener el ecualizador en f = 1 y f = 2 Hz?

<details><summary>Solución</summary>
1/sinc(f/6): en 1 Hz, 1/sinc(1/6) ≈ 1,05; en 2 Hz, 1/sinc(1/3) ≈ 1,21. Es la misma compensación que necesita el ZOH de un D/A (ejercicio 9 c de la hoja, donde a 20 kHz con fs = 44,1 kHz sale 1,44).
</details>

## Para profundizar

- [Apuntes del Tema 2](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%20Apuntes.pdf), sección 3, «Muestreo no ideal», y sección 4, «Retenedor de orden cero».
- [Transparencias T2-01](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%2001%20-%20Muestreo.pdf), «Muestreo no ideal».
- [Hoja de ejercicios del Tema 2](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%20Ejercicios.pdf), ejercicio 9, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%20Ejercicios%20resueltos.pdf).
- A. V. Oppenheim, A. S. Willsky y S. H. Nawab, *Signals and Systems*, 2.ª ed., Prentice Hall, 1997, apartado 7.1 (muestreo con retenedor de orden cero).

## Relación con otros conceptos

- **Muestreo ideal.** El límite τ → 0. Herramienta: [Muestreo ideal](T2-muestreo-ideal.html).
- **Serie de Fourier.** El factor d·sinc(kd) son los coeficientes del tren de pulsos. Herramienta: [Serie de Fourier](T1-serie-fourier.html), con el tren de pulsos.
- **Retenedores.** Techo plano con τ = Ts es el ZOH. Herramienta: [Retenedores](T2-retenedores.html).
- **Reconstrucción.** Herramienta: [Reconstrucción](T2-reconstruccion.html).
