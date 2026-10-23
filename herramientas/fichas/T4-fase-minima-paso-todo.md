## Introducción

### El mismo módulo, distinta fase

El módulo de una respuesta en frecuencia no determina la fase. Un cero en z₀ y otro en su **recíproco conjugado** 1/z₀* dan factores con el mismo módulo sobre la circunferencia unidad, salvo una constante:

> |1 − z₀ e^{−jΩ}| = |z₀| · |1 − (1/z₀*) e^{−jΩ}|.

Así que, a partir de un filtro, se pueden construir otros con el mismo |H| reflejando ceros dentro o fuera de la circunferencia. Con M ceros hay hasta 2^{M} variantes (contando los pares conjugados juntos), que solo se distinguen por la fase.

### Fase mínima, máxima y mixta

- **Fase mínima:** todos los ceros (y polos) dentro de la circunferencia. Es la variante con menor retardo de grupo en todas las frecuencias y la que concentra la energía de h[n] lo antes posible. Su inverso 1/H es causal y estable.
- **Fase máxima:** todos los ceros fuera. Su h[n] es la de fase mínima invertida en el tiempo y su retardo es el mayor.
- **Fase mixta:** unos dentro y otros fuera.

### Filtros paso todo

Un **paso todo** tiene |H_ap(e^{jΩ})| = 1 para todo Ω. El de primer orden,

> H_ap(z) = (z^{−1} − a*)/(1 − a z^{−1}),

tiene un polo en a y un cero en 1/a*. Su fase es siempre decreciente y su **retardo de grupo, positivo**: solo añade retraso. Se usan para corregir la fase de otro filtro (ecualizadores de fase) y como bloque de reverberadores y desfasadores.

### La descomposición

Todo filtro racional se escribe como

> H(z) = H_min(z) · H_ap(z),

reflejando dentro los ceros que están fuera (H_min) y poniendo en un paso todo lo que falta (H_ap). Como el retardo de H_ap es positivo, el de H es siempre mayor que el de H_min: de ahí el nombre. La fase mínima aparece al invertir canales, en la predicción lineal o al recuperar una fase a partir del módulo.

## Guía de uso

- El filtro es un FIR con cinco ceros: dos pares complejos (**radio r** y **ángulo θ**) y un **cero real c**.
- Las **casillas** reflejan cada par o el cero real fuera del círculo. En el plano, los ceros de H son círculos gruesos, azules si están dentro y rojos si están fuera; en gris discontinuo, la posición reflejada.
- Arriba, los ceros y el módulo, que es el mismo en todos los casos. En medio, la fase desenrollada y el retardo de grupo de H, de H_min y de H_ap. Abajo, h[n] y su energía acumulada, frente a las de fase mínima.
- El recuadro dice si es de fase mínima, máxima o mixta y cuándo llega la mitad de la energía.

## Ejercicios

**1. Fase mixta.** Con los valores de partida (el par 1 reflejado), ¿de qué clase es H? ¿Cuántos ceros tiene fuera? ¿Cambia el módulo al reflejar el par 2?

<details><summary>Solución</summary>
Es de fase mixta, con 2 de los 5 ceros fuera (el par de radio 0,8, en 1/0,8 = 1,25). El módulo no cambia al reflejar el par 2 ni ningún otro: solo cambian la fase, el retardo y h[n].
</details>

**2. Fase mínima.** Desmarca todas las casillas. ¿Qué pasa con el retardo de grupo y con la energía acumulada?

<details><summary>Solución</summary>
H = H_min y H_ap = 1. El retardo es el menor posible (en continua, 0 muestras) y casi la mitad de la energía, un 49 %, está ya en h[0]; el 89 %, en las dos primeras muestras. El retardo incluso es negativo cerca del ángulo del par 1, θ₁ = 0,8, porque esos ceros están cerca de la circunferencia.
</details>

**3. Fase máxima.** Marca las tres casillas. ¿Cómo es h[n] respecto a la de fase mínima? ¿Cuánto vale el retardo en continua?

<details><summary>Solución</summary>
Es la de fase mínima invertida en el tiempo (y con el signo cambiado): h_max[n] = −h_min[5 − n]. La energía llega al final: la mitad, en n = 4. El retardo en continua es 5 muestras; en general τ_max(Ω) = 5 − τ_min(Ω), la longitud menos uno menos el de fase mínima.
</details>

**4. El paso todo.** Con fase mixta, mira el retardo de H_ap. ¿Puede ser negativo? ¿Dónde es mayor? Acerca el radio r₁ a 0,95.

<details><summary>Solución</summary>
Nunca es negativo: un paso todo solo añade retraso. Es mayor cerca del ángulo θ₁ = 0,8, donde están el polo y el cero del paso todo. Con r₁ = 0,95, el pico se hace alto y estrecho: el paso todo concentra su retraso en una banda estrecha.
</details>

**5. El ejercicio 17 de la hoja.** H(z) = (1 − 2z^{−1})/(1 + 0,8z^{−1}). ¿Es de fase mínima? Escríbelo como H_min·H_ap. Con la herramienta, pon c = 0,5 y refléjalo: el cero pasa a 2, como en la hoja. ¿Cuánto vale h[0] para el factor real?

<details><summary>Solución</summary>
No: el cero está en z = 2. H = [2(1 − 0,5z^{−1})/(1 + 0,8z^{−1})]·[(0,5 − z^{−1})/(1 − 0,5z^{−1})], donde el segundo factor es un paso todo, y H_min tiene inversa estable. En la herramienta, el factor reflejado es 0,5 − z^{−1}, con el mismo módulo que 1 − 0,5z^{−1}: el primer coeficiente pasa de 1 a 0,5 y la energía se desplaza a la segunda muestra.
</details>

## Para profundizar

- [Apuntes del Tema 4](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Apuntes.pdf), sección 5 (Filtros especiales): «Fase mínima, máxima y mixta» y «Filtros paso todo».
- [Transparencias T4-05](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%2005%20-%20Filtros%20especiales.pdf), fase mínima y paso todo.
- [Hoja de ejercicios del Tema 4](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Ejercicios.pdf), ejercicio 17, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T4%20-%20Ejercicios%20resueltos.pdf).
- A. V. Oppenheim y R. W. Schafer, *Discrete-Time Signal Processing*, 3.ª ed., Pearson, 2010, apartados 5.5 y 5.6.

## Relación con otros conceptos

- **Polos y ceros.** Carga el paso todo de primer orden. Herramienta: [Polos y ceros en el plano z](T4-polos-ceros-z.html).
- **Fase lineal.** Un FIR de fase lineal tiene sus ceros en parejas z₀ y 1/z₀*: ni mínima ni máxima. Herramienta: [Tipos de FIR de fase lineal](T4-tipos-fir.html).
- **Retardo de grupo.** Herramienta: [Fase lineal y retardo de grupo](T4-fase-lineal.html).
- **Inversión temporal (Tema 1).** La fase máxima es la mínima invertida. Herramienta: [Operaciones sobre la variable independiente](T1-variable-independiente.html).
- **Sistemas inversos.** Solo los de fase mínima tienen inverso causal y estable. Herramienta: [Propiedades de los sistemas](T1-propiedades-sistemas.html).
