## Introducción

### La DFT como cambio de base

La DFT de N puntos expresa una secuencia como combinación de N exponenciales complejas de frecuencias Ω_k = 2πk/N:

> x[n] = (1/N) Σ_{k=0}^{N−1} X[k] e^{j2πkn/N}.

X[k] dice cuánto hay de la exponencial k en x[n]: su módulo es la amplitud y su argumento, la fase. Esas N exponenciales son ortogonales, así que los coeficientes se obtienen proyectando,

> X[k] = Σ_{n=0}^{N−1} x[n] e^{−j2πkn/N},

y en forma matricial X = W_N x, con la matriz de elementos W_N^{kn}. Cada X[k] es un número complejo, que se puede ver como módulo y fase o como parte real e imaginaria.

### Pares básicos

| x[n] (N puntos) | X[k] |
|---|---|
| δ[n] | 1 para todo k |
| δ[n − m] | W_N^{km}: módulo 1, fase −2πkm/N |
| 1 | N δ[k] |
| e^{j2πk₀n/N} | N δ[k − k₀] |
| cos(2πk₀n/N) | N/2 en k₀ y en N − k₀ |
| sin(2πk₀n/N) | −jN/2 en k₀ y +jN/2 en N − k₀ |
| (−1)ⁿ, N par | N δ[k − N/2] |

Un impulso contiene todas las frecuencias por igual y una constante solo la frecuencia cero: los dos extremos de la dualidad entre tiempo y frecuencia.

### Simetrías y Parseval

- **X[0] = Σ x[n]** es la componente continua (sin dividir por N).
- Si x[n] es **real**, X[N − k] = X*[k]: el módulo es simétrico respecto a k = N/2 y la fase, antisimétrica. Basta conocer la mitad de la DFT.
- Si además es **par circular**, x[n] = x[N − n], la DFT es real; si es **impar circular**, imaginaria pura.
- **Parseval:** Σ|x[n]|² = (1/N) Σ|X[k]|². La energía se conserva, con el factor 1/N de esta definición.

## Guía de uso

- En la gráfica de arriba, haz clic o arrastra para cambiar las 16 muestras de x[n].
- **Secuencia de partida** carga uno de los pares básicos.
- **Módulo y fase o Re e Im** cambia las dos gráficas de abajo.
- El recuadro da X[0] y comprueba Parseval.

## Ejercicios

**1. El ejercicio 2 de la hoja, con N = 16.** Carga cada secuencia de partida y anota su DFT. Compara el impulso con el impulso desplazado: ¿qué cambia y qué no?

<details><summary>Solución</summary>
δ[n] da X[k] = 1. δ[n − 3] da el mismo módulo, 1, y una fase lineal −2π·3k/16, que se ve plegada en (−π, π]. La constante da X[0] = 16; el coseno con k = 2, X[2] = X[14] = 8; el seno, en Re e Im, Im X[2] = −8 e Im X[14] = 8; la alterna, X[8] = 16, la frecuencia Ω = π.
</details>

**2. El pulso.** Carga el pulso de 4. ¿Cuánto vale X[0]? ¿En qué k se anula |X[k]|? Comprueba Parseval.

<details><summary>Solución</summary>
X[0] = 4. |X[k]| = |sin(πk/4)/sin(πk/16)| se anula en k = 4, 8 y 12, donde el pulso contiene un número entero de periodos de la exponencial. La energía es 4 y (1/16)Σ|X[k]|² = 4.
</details>

**3. Hacerla par.** Parte del impulso δ[n] y pon x[1] = x[15] = 0,5. ¿Cómo es la DFT en Re e Im? Ahora pon solo x[1] = 0,5. ¿Qué cambia?

<details><summary>Solución</summary>
Con x[1] = x[15] es par circular y la DFT es real: X[k] = 1 + cos(2πk/16), entre 0 y 2, con la parte imaginaria nula. Con solo x[1] deja de ser par: aparece parte imaginaria, −0,5 sin(2πk/16), aunque el módulo sigue siendo simétrico porque x[n] es real.
</details>

**4. El ejercicio 1 de la hoja, dentro de 16 puntos.** Parte del impulso y pon x[1] = 2 y x[3] = 1, para tener x = (1, 2, 0, 1) seguida de ceros. Compara X[0], X[4], X[8] y X[12] con la DFT de 4 puntos de la hoja, (4, 1 − j, −2, 1 + j). ¿Por qué coinciden?

<details><summary>Solución</summary>
Coinciden. Las dos son muestras de la misma DTFT: la de 4 puntos en Ω = 2πk/4 y la de 16 en Ω = 2πk/16, y k = 4m en 16 puntos es la frecuencia 2πm/4. Las otras 12 muestras de la DFT de 16 puntos interpolan la DTFT entre ellas: es el relleno con ceros.
</details>

**5. Un número no entero de periodos.** Carga el coseno con k = 2 y arrastra las muestras de n = 12 a 15 hasta cero, de modo que queden 1,5 periodos. ¿Qué pasa con la DFT?

<details><summary>Solución</summary>
El coseno ya no completa un número entero de periodos en los 16 puntos: deja de haber solo dos líneas y la energía se reparte entre muchas k. Es la fuga espectral; X[2] baja de 8 a unos 6, y aparecen valores en casi todas las demás muestras.
</details>

## Para profundizar

- [Apuntes del Tema 3](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%20Apuntes.pdf), sección 2 (La transformada discreta de Fourier), «Forma matricial», y sección 3 (Propiedades de la DFT): simetría y Parseval.
- [Transparencias T3-01](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%2001%20-%20DFT.pdf) y [T3-02](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%2002%20-%20Propiedades.pdf).
- [Hoja de ejercicios del Tema 3](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%20Ejercicios.pdf), ejercicios 1, 2, 5 y 9, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T3%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T3/codigo/python/dft_directa.py` y su versión en Matlab.
- A. V. Oppenheim y R. W. Schafer, *Discrete-Time Signal Processing*, 3.ª ed., Pearson, 2010, apartados 8.4 y 8.6.

## Relación con otros conceptos

- **Serie de Fourier (Tema 1).** La DFT es la serie de Fourier de la extensión periódica. Herramienta: [Serie de Fourier](T1-serie-fourier.html).
- **Exponenciales discretas.** Las funciones base de la DFT. Herramienta: [Exponencial discreta](T1-exponencial-discreta.html).
- **Propiedades de la DFT.** Desplazamientos, inversión y modulación, con comprobación. Herramienta: [Propiedades de la DFT](T3-propiedades-dft.html).
- **Fuga y relleno con ceros.** Herramienta: [DFT, fuga y relleno con ceros](T3-dft.html).
- **Par, impar y energía.** Las mismas descomposiciones en versión circular. Herramienta: [Par, impar, energía y potencia](T1-par-impar-energia.html).
