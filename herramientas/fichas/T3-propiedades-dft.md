## Introducción

### Todo es circular

La DFT de N puntos trata la secuencia como un periodo de x̃[n], su extensión periódica, y los índices se toman **módulo N**: ((n))_N = n mod N. Por eso, las propiedades de la DFT son las de la DTFT con una diferencia: desplazar, invertir o convolucionar son operaciones **circulares**. Lo que sale por un extremo entra por el otro.

### Las propiedades

| Operación en n | Efecto en k |
|---|---|
| Linealidad, a x₁[n] + b x₂[n] | a X₁[k] + b X₂[k] |
| Desplazamiento circular, x[((n − m))_N] | W_N^{km} X[k] = e^{−j2πkm/N} X[k] |
| Modulación, e^{j2πln/N} x[n] | X[((k − l))_N] |
| Inversión circular, x[((−n))_N] | X[((−k))_N] |
| Conjugación, x*[n] | X*[((−k))_N] |
| Convolución circular, x₁ ⊛ x₂ | X₁[k] X₂[k] |
| Producto, x₁[n] x₂[n] | (1/N) X₁ ⊛ X₂ |

- **Desplazar** multiplica por una fase lineal: el módulo no cambia y la fase pierde 2πkm/N.
- **Modular** es el dual: desplaza el espectro circularmente l posiciones. Con l = N/2, multiplicar por (−1)ⁿ lleva las frecuencias bajas a las altas.
- **Invertir** una secuencia real equivale a conjugar su DFT, porque X[((−k))_N] = X*[k].

### Simetría de las señales reales

Toda secuencia se descompone en parte **par circular**, x_e[n] = (x[n] + x[((−n))_N])/2, y parte **impar circular**, x_o[n] = (x[n] − x[((−n))_N])/2. Si x[n] es real, la DFT de la parte par es Re X[k] y la de la parte impar, j Im X[k]. Como consecuencia, |X[k]| es simétrico y ∠X[k] antisimétrica respecto a k = N/2.

### Parseval

> Σ_n |x[n]|² = (1/N) Σ_k |X[k]|².

Ninguna de las operaciones de la herramienta, salvo tomar la parte par o impar, cambia la energía.

## Guía de uso

- Haz clic en la gráfica de la izquierda para cambiar las 8 muestras de x[n] (en azul). El resultado y[n] sale con cuadrados naranjas (parte real) y triángulos verdes (parte imaginaria, si la hay).
- **Operación** elige la propiedad y **m o l**, el desplazamiento o la modulación.
- A la derecha, el módulo y la fase de X[k] (tallos azules) y de Y[k] (cuadrados naranjas).
- El recuadro da la regla, la diferencia entre Y[k] y lo que predice la regla, y la comprobación de Parseval.

## Ejercicios

**1. Desplazar no cambia el módulo.** Con la secuencia de partida y el desplazamiento m = 2, ¿cómo es y[n]? Compara los módulos y, en k = 1, las fases de X e Y.

<details><summary>Solución</summary>
y = (0, 0, 1; 0,8; 0,5; 0,2; 0, 0): la secuencia se mueve dos muestras a la derecha. Los módulos coinciden. La fase de Y[1] es la de X[1] menos 2π·1·2/8 = π/2; en k = 2, menos π, y así sucesivamente (plegada en (−π, π]).
</details>

**2. Medio periodo.** Con m = 4, ¿qué relación hay entre Y[k] y X[k]? Ahora, con m = 6, mira y[n]: ¿dónde están las muestras que salen por la derecha?

<details><summary>Solución</summary>
W_8^{4k} = (−1)^{k}: Y[k] = (−1)^{k} X[k], las fases de las k impares cambian π. Con m = 6, las muestras que pasarían de n = 7 vuelven por n = 0: y = (0,5; 0,2; 0, 0, 0, 0, 1; 0,8). Es el desplazamiento circular, no el lineal.
</details>

**3. El ejercicio 6 de la hoja: inversión y modulación.** Aplica la inversión circular. ¿Qué secuencia sale y qué pasa con la fase? Después aplica la modulación con l = 4: ¿qué es y[n] y dónde queda el máximo de |Y[k]|?

<details><summary>Solución</summary>
La inversión da (1, 0, 0, 0, 0; 0,2; 0,5; 0,8): x[0] se queda y el resto se lee al revés. El módulo no cambia y la fase cambia de signo, porque Y[k] = X*[k]. La modulación con l = 4 multiplica por e^{jπn} = (−1)ⁿ: y = (1; −0,8; 0,5; −0,2; 0, …). El espectro se desplaza 4 posiciones y el máximo pasa de k = 0 a k = 4, la frecuencia π: el paso bajo se convierte en paso alto.
</details>

**4. Modulación que rompe la simetría.** Con la modulación y l = 1, ¿es real y[n]? ¿Sigue siendo simétrico |Y[k]|?

<details><summary>Solución</summary>
No: y[n] = e^{j2πn/8} x[n] es compleja y aparecen los triángulos verdes. El espectro se desplaza una posición y deja de ser simétrico respecto a k = 4: la simetría X[N − k] = X*[k] solo vale para secuencias reales.
</details>

**5. Partes par e impar, y el ejercicio 5 de la hoja.** Calcula la parte par circular de la secuencia de partida y compruébala. ¿Qué es su DFT? ¿Y la de la parte impar? Comprueba Parseval con la secuencia de partida.

<details><summary>Solución</summary>
x_e = (1; 0,4; 0,25; 0,1; 0; 0,1; 0,25; 0,4), simétrica respecto a n = 0 en sentido circular. Su DFT es Re X[k], real, con fase 0 o π. La de la parte impar es j Im X[k], con fase ±π/2. La energía es 1 + 0,64 + 0,25 + 0,04 = 1,93, y (1/8)Σ|X[k]|² da lo mismo. En la hoja se usa al revés: a partir de la DFT se obtienen la suma, x[0] y la energía sin calcular la IDFT.
</details>

## Para profundizar

- [Apuntes del Tema 3](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%20Apuntes.pdf), sección 3 (Propiedades de la DFT).
- [Transparencias T3-02](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%2002%20-%20Propiedades.pdf), propiedades de la DFT.
- [Hoja de ejercicios del Tema 3](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%20Ejercicios.pdf), ejercicios 5, 6 y 9, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%20Ejercicios%20resueltos.pdf).
- A. V. Oppenheim y R. W. Schafer, *Discrete-Time Signal Processing*, 3.ª ed., Pearson, 2010, apartado 8.6.

## Relación con otros conceptos

- **Propiedades de la transformada de Fourier (Tema 1).** Las mismas reglas en versión continua. Herramienta: [Propiedades de la transformada de Fourier](T1-propiedades-fourier.html).
- **Par, impar y energía.** La descomposición no circular. Herramienta: [Par, impar, energía y potencia](T1-par-impar-energia.html).
- **Convolución circular.** La propiedad más importante de la tabla. Herramienta: [Convolución circular](T3-convolucion-circular.html).
- **Editor de la DFT.** Pares básicos y simetrías con 16 puntos. Herramienta: [Editor de la DFT](T3-editor-dft.html).
- **Fase lineal (Tema 4).** El retardo de un filtro FIR simétrico es la propiedad del desplazamiento. Herramienta: [Fase lineal y retardo de grupo](T4-fase-lineal.html).
