## Introducción

### Volver de las muestras a la señal

Reconstruir es obtener una señal continua a partir de x[n]. En frecuencia, la idea es clara: el espectro de la señal muestreada contiene X(f) repetido cada fs, y basta un paso bajo que se quede con la réplica central. En el tiempo, eso equivale a **interpolar**: rellenar los huecos entre muestras con una regla.

### Reconstrucción ideal

El paso bajo ideal de corte fs/2 y ganancia Ts tiene respuesta al impulso h(t) = sinc(t/Ts). Filtrar el tren de impulsos de las muestras da la **fórmula de interpolación**

> x_r(t) = Σ_n x[n] · sinc((t − nTs)/Ts).

Cada muestra aporta un sinc centrado en su instante, que vale 1 allí y 0 en las demás muestras. Si x(t) tenía banda limitada y fs > 2B, x_r(t) = x(t) exactamente. Si no, se reconstruye la señal de banda limitada que tiene esas muestras: cada componente por encima de fs/2 aparece en su alias.

### Por qué no es realizable

sinc(t/Ts) dura infinito hacia el pasado y hacia el futuro: cada valor de x_r(t) depende de todas las muestras, también de las futuras. El filtro no es causal y su respuesta decae despacio (como 1/t). En la práctica se trunca y se retrasa, o se usan interpoladores más sencillos.

### Retenedores

- **Retenedor de orden cero (ZOH).** Mantiene cada muestra hasta la siguiente: la salida es una escalera. Es causal y es lo que hace casi cualquier conversor D/A. Retrasa la señal unos Ts/2 y su error máximo para una señal suave es del orden de max|x'|·Ts: al duplicar fs, el error se reduce a la mitad.
- **Retenedor de orden uno no causal (FOH).** Une las muestras con rectas: interpolación lineal. Necesita conocer la muestra siguiente, así que en tiempo real hay que retrasarlo una muestra. Su error es del orden de max|x''|·Ts²/8: al duplicar fs, se reduce a la cuarta parte.
- **FOH predictivo.** Prolonga la recta que pasa por las dos últimas muestras. Es causal, pero se pasa en los cambios de pendiente y deja saltos en cada muestra.

## Guía de uso

- La señal es x(t) = sin(2πt) + 0,5 sin(2π·3t) + 0,25 sin(2π·6t); su componente más alta es de 6 Hz.
- **Método** elige la reconstrucción ideal (suma de sinc), el ZOH, el FOH no causal o el FOH predictivo.
- **fs** fija la frecuencia de muestreo.
- Arriba, x(t) en gris, las muestras y la señal reconstruida. Abajo, el error x_r(t) − x(t).
- El recuadro da el error eficaz y el máximo y avisa si hay aliasing.

## Ejercicios

**1. Ideal con y sin Nyquist.** Con la reconstrucción ideal, compara fs = 20 y fs = 10. ¿Qué componente se reconstruye mal en el segundo caso y dónde aparece?

<details><summary>Solución</summary>
Con fs = 20 > 12 el error es casi nulo (solo crece en los extremos de la ventana, porque la suma de sinc usa un número finito de muestras). Con fs = 10, la componente de 6 Hz aparece en |6 − 10| = 4 Hz y, al ser un seno, con el signo cambiado: se reconstruye −0,25 sin(2π·4t) en su lugar.
</details>

**2. El error del ZOH.** Con el ZOH, mide el error máximo con fs = 20, 40 y 60. ¿En qué proporción baja?

<details><summary>Solución</summary>
Unos 0,95, 0,59 y 0,41: al duplicar fs baja algo menos de la mitad, y la proporción se acerca a 1/2 al subir fs, porque el error del ZOH es proporcional a Ts. Una cota es max|x'|·Ts, con max|x'| ≤ 2π(1 + 1,5 + 1,5) ≈ 25 1/s: 1,26 con fs = 20; el error real es menor porque los máximos de las derivadas no coinciden.
</details>

**3. El error del FOH.** Repite el ejercicio anterior con el FOH no causal. ¿Cuánto baja ahora? ¿Consigue el ZOH, con la fs más alta de la herramienta, el error del FOH con fs = 20?

<details><summary>Solución</summary>
Unos 0,15, 0,038 y 0,018: al duplicar fs baja a la cuarta parte, porque es proporcional a Ts². Con fs = 60, el ZOH aún tiene un error de 0,41, casi el triple que el FOH con fs = 20; necesitaría unas 170 muestras/s para igualarlo.
</details>

**4. El retardo del ZOH.** Con fs = 10 y el ZOH, compara la escalera con x(t). ¿Hacia dónde está desplazada? ¿Cuánto?

<details><summary>Solución</summary>
Hacia la derecha, unos Ts/2 = 0,05 s: el centro de cada escalón está medio periodo después de la muestra. En frecuencia es el factor e^{−jπf Ts} de la respuesta del ZOH.
</details>

**5. El ejercicio 7 de la hoja, con esta señal.** La hoja reconstruye cos(6πt) + cos(14πt) con fs = 12 y obtiene la componente de 7 Hz en 5 Hz. Con la herramienta, ¿qué fs mínima recupera x(t)? ¿Y qué rango de cortes de filtro serviría con fs = 20?

<details><summary>Solución</summary>
fs > 12 muestras/s, el doble de la componente más alta (6 Hz). Con fs = 20, el corte debe dejar pasar 6 Hz y eliminar la réplica más baja, en 20 − 6 = 14 Hz: entre 6 y 14 Hz. La herramienta usa el corte fs/2 = 10 Hz, que está en ese rango.
</details>

## Para profundizar

- [Apuntes del Tema 2](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%20Apuntes.pdf), sección 4 (Reconstrucción).
- [Transparencias T2-02](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%2002%20-%20Reconstrucci%C3%B3n.pdf), reconstrucción ideal y retenedores.
- [Hoja de ejercicios del Tema 2](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%20Ejercicios.pdf), ejercicios 7 y 10, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T2%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T2/codigo/python/reconstruccion_sinc.py` y `retenedores.py`, y sus versiones en Matlab.
- A. V. Oppenheim y R. W. Schafer, *Discrete-Time Signal Processing*, 3.ª ed., Pearson, 2010, apartado 4.3.

## Relación con otros conceptos

- **Muestreo ideal.** El paso bajo se queda con la réplica central. Herramienta: [Espectro de una señal muestreada](T2-muestreo-ideal.html).
- **Retenedores en frecuencia.** Herramienta: [Retenedores](T2-retenedores.html).
- **Aliasing.** La reconstrucción ideal devuelve el alias fundamental de cada componente. Herramienta: [Aliasing](T2-aliasing.html).
- **Convolución.** Reconstruir es convolucionar el tren de muestras con h(t). Herramienta: [Convolución continua](T1-convolucion-continua.html).
- **Interpolación digital.** Antes de un D/A se suele interpolar en digital para que el retenedor trabaje a más fs. Herramienta: [Diezmado e interpolación](T2-diezmado-interpolacion.html).
