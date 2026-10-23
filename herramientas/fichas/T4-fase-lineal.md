## Introducción

### Retardo de fase y retardo de grupo

Un filtro cambia a la vez el módulo y la fase de cada componente. Si una sinusoide de frecuencia Ω pasa por H(e^{jΩ}) = |H| e^{jφ(Ω)}, sale con su amplitud multiplicada por |H| y desplazada −φ(Ω)/Ω muestras, el **retardo de fase**. Para una señal de banda estrecha, un pulso modulado, lo que importa es cuánto se retrasa la envolvente: el **retardo de grupo**

> τ(Ω) = −dφ/dΩ.

### Fase lineal: sin distorsión

Si en la banda de paso la fase es lineal,

> φ(Ω) = −αΩ,

el retardo de grupo es constante, τ = α, y todas las componentes se retrasan lo mismo: la salida es la entrada retrasada α muestras (y filtrada en módulo). La forma de un pulso se conserva. Es lo que hacen los FIR con coeficientes simétricos, con α = (N − 1)/2.

### Fase lineal generalizada

Con φ(Ω) = −αΩ − β el retardo de grupo sigue siendo α, pero cada componente recibe además un desfase constante β. La envolvente de un pulso modulado llega intacta tras α muestras, pero la portadora se desplaza dentro de ella y la forma de onda cambia. Es la fase de los FIR antisimétricos (β = π/2), como los derivadores y los transformadores de Hilbert.

### Fase no lineal

Los IIR, como el Butterworth, tienen fase no lineal: el retardo de grupo varía con la frecuencia y crece cerca del corte. Las componentes de un pulso llegan en instantes distintos y el pulso se deforma: oscilaciones asimétricas y una cola. Importa cuando la forma de onda tiene información (imágenes, ECG, datos digitales); en audio el oído es poco sensible a la fase.

## Guía de uso

- **Filtro** elige un paso bajo ideal con fase −αΩ − β, un FIR de Hamming o un IIR de Butterworth.
- **Entrada** elige tres tonos, un pulso rectangular o un pulso modulado.
- **Ωc/π** es el corte. **α** y **β/π** solo afectan al ideal. **Orden** es N − 1 para el FIR (hasta 60) y N para el IIR (hasta 12).
- Arriba, la entrada, la entrada solo retrasada (verde discontinua) y la salida. Abajo, el módulo, la fase desenrollada y el retardo de grupo en la banda de paso.
- La entrada es periódica (512 muestras), así que no hay transitorio.

## Ejercicios

**1. Retrasar sin deformar.** Con el filtro ideal, β = 0 y los tres tonos, ¿coincide la salida con la entrada retrasada? Cambia α a 30. ¿Qué pasa con el corte Ωc/π = 0,1?

<details><summary>Solución</summary>
Sí, mientras los tres tonos estén en la banda de paso: la salida es la entrada retrasada α muestras. Los tonos están en 2π·8/512 ≈ 0,03π, 0,08π y 0,125π. Con Ωc/π = 0,1 pasan los dos primeros y el tercero queda fuera: la salida es la parte que pasa, retrasada.
</details>

**2. Desfase constante.** Con el ideal y el pulso modulado, pon β/π = 0,5. ¿Se retrasa la envolvente? ¿Y la portadora?

<details><summary>Solución</summary>
La envolvente se retrasa α muestras, exactamente como con β = 0, porque el retardo de grupo sigue siendo α. Pero la portadora se desfasa π/2: donde antes había un coseno ahora hay un seno, y la forma de onda no coincide con la verde.
</details>

**3. FIR de fase lineal.** Con el FIR de Hamming, orden 30, y el pulso rectangular, ¿cuánto vale el retardo de grupo? ¿Cómo son las oscilaciones de la salida?

<details><summary>Solución</summary>
τ = 30/2 = 15 muestras en toda la banda de paso. Las oscilaciones del pulso filtrado (por suprimir las frecuencias altas) son simétricas antes y después de cada flanco, porque h[n] es simétrica. Con orden 60, el retardo pasa a 30.
</details>

**4. IIR: fase no lineal.** Con el Butterworth, Ωc/π = 0,3 y el pulso rectangular, compara los órdenes 2 y 6. ¿Cómo varía el retardo de grupo? ¿Cómo se deforma el pulso?

<details><summary>Solución</summary>
Con orden 2, el retardo va de 1,4 muestras en continua a 1,9 cerca del corte; con orden 6, de 3,8 a 7,9. Las frecuencias cercanas al corte llegan tarde: el pulso sale con oscilaciones solo después de los flancos y con una cola. Más orden significa un corte más abrupto y más distorsión de fase.
</details>

**5. El ejercicio 2 de la hoja.** Calcula el retardo de grupo de h = (1, 2, 1)/4 y de 0,5/(1 − 0,5z^{−1}) en Ω = 0, π/2 y π. ¿Cuál deformaría el pulso? Compáralo con el Butterworth de orden 1 de la herramienta.

<details><summary>Solución</summary>
El FIR tiene fase −Ω: τ = 1 en todas las frecuencias. El IIR tiene τ(0) = 1, τ(π/2) = −0,2 y τ(π) = −1/3: el retardo cambia con la frecuencia y deforma el pulso. El Butterworth de orden 1 con Ωc/π = 0,3 también tiene retardo variable, de 0,98 en continua a 0,62 en el corte.
</details>

## Para profundizar

- [Apuntes del Tema 4](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Apuntes.pdf), sección 1, «Fase y retardo de grupo», y sección 4, «Fase lineal».
- [Transparencias T4-01](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%2001%20-%20Introducci%C3%B3n.pdf) y [T4-04](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%2004%20-%20Filtros%20FIR.pdf), fase y simetría.
- [Hoja de ejercicios del Tema 4](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Ejercicios.pdf), ejercicios 2 y 12, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Ejercicios%20resueltos.pdf).
- A. V. Oppenheim y R. W. Schafer, *Discrete-Time Signal Processing*, 3.ª ed., Pearson, 2010, apartados 5.1 y 5.7.

## Relación con otros conceptos

- **Propiedad del desplazamiento.** Un retraso es una fase lineal. Herramienta: [Propiedades de la transformada de Fourier](T1-propiedades-fourier.html).
- **Tipos de FIR.** Qué simetrías dan fase lineal. Herramienta: [Tipos de FIR de fase lineal](T4-tipos-fir.html).
- **Fase cero.** Quitar el retardo filtrando hacia delante y hacia atrás. Herramienta: [Filtrado de fase cero](T4-fase-cero.html).
- **Fase mínima.** Entre todos los filtros con el mismo módulo, el de menor retardo. Herramienta: [Fase mínima y paso todo](T4-fase-minima-paso-todo.html).
- **Aproximaciones analógicas.** El retardo de grupo de Butterworth, Chebyshev y elíptico. Herramienta: [Aproximaciones de filtros analógicos](T4-filtros-continuos.html).
