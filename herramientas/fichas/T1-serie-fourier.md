## Introducción

### Una señal periódica es una suma de armónicos

Una señal $x(t)$ de periodo $T_0$ se puede escribir como una suma de exponenciales complejas cuyas frecuencias son múltiplos de la **frecuencia fundamental** $f_0 = 1/T_0$:

> $$x(t) = \sum_{k=-\infty}^{\infty} c_k\, e^{j2\pi k f_0 t}, \qquad c_k = \frac{1}{T_0} \int_{T_0} x(t)\, e^{-j2\pi k f_0 t}\, dt.$$

Cada término es un **armónico**: $k = \pm1$ es el fundamental, $k = \pm2$ el segundo armónico, etc. $c_0$ es el valor medio de la señal. Si $x$ es real, $c_{-k} = c_k^*$, y los términos $k$ y $-k$ se juntan en una sinusoide real de amplitud $2|c_k|$ y fase $\angle c_k$.

### Qué dicen los coeficientes

- La **simetría** de la señal se ve en los $c_k$: si $x$ es par, los $c_k$ son reales; si es impar, imaginarios puros. Si $x$ tiene simetría de media onda ($x(t + T_0/2) = -x(t)$), solo hay armónicos impares, como en la onda cuadrada o la triangular.
- La **suavidad** se ve en lo deprisa que decaen: una señal con saltos (cuadrada, diente de sierra) tiene $|c_k|$ del orden de $1/k$; una continua con picos (triangular, seno rectificado), del orden de $1/k^2$. Cuanto más suave, menos armónicos hacen falta.
- El **tren de pulsos** de anchura $D\,T_0$ (ciclo de trabajo $D$) tiene $c_k = D\,\mathrm{sinc}(kD)$: los armónicos siguen una envolvente sinc con ceros en los múltiplos de $1/D$.

### Teorema de Parseval

La potencia media se reparte entre los armónicos:

> $$P = \frac{1}{T_0} \int_{T_0} |x(t)|^2\, dt = \sum_{k=-\infty}^{\infty} |c_k|^2.$$

Si se trunca la serie a $|k| \le K$, la potencia que falta es la de los coeficientes omitidos. Esto da una medida de lo buena que es la aproximación.

### Fenómeno de Gibbs

Cerca de un salto, la suma parcial oscila y se pasa del valor de la señal. Al aumentar $K$, las oscilaciones se estrechan y se acercan al salto, pero su altura máxima no baja: el exceso es de un 9 % del salto. Lejos de los saltos, la suma parcial converge a la señal; en el propio salto, al punto medio.

## Guía de uso

- **Señal periódica** elige entre un tren de pulsos (centrado en $t = 0$), una onda cuadrada (1 en la primera mitad del periodo y $-1$ en la segunda), una triangular (de $-1$ a 1), un diente de sierra (de $-1$ a 1) y un seno rectificado $|\sin(\pi t)|$. El periodo es $T_0 = 1$.
- **Ciclo de trabajo** solo afecta al tren de pulsos (solo aparece con él): es la fracción del periodo en que vale 1.
- **K** es el número de armónicos de la suma parcial, $|k| \le K$.
- Arriba, la señal y la suma parcial durante tres periodos. Abajo, $|c_k|$ para $|k| \le 60$, con los que entran en la suma en azul.
- El recuadro compara la potencia de $x$ con la de la suma parcial (Parseval) y da el máximo de la suma parcial para ver el fenómeno de Gibbs.

## Ejercicios

**1. La onda cuadrada.** Calcula $|c_1|$ y $|c_2|$ de la onda cuadrada. ¿Qué fracción de la potencia lleva solo el fundamental ($K = 1$)? Compruébalo.

<details><summary>Solución</summary>
$|c_k| = \dfrac{2}{\pi k}$ para $k$ impar y 0 para $k$ par: $|c_1| = 2/\pi \approx 0{,}637$ y $c_2 = 0$. La potencia total es 1 y el fundamental lleva $2 \cdot (2/\pi)^2 = 8/\pi^2 \approx 81$ %.
</details>

**2. Gibbs.** Con la onda cuadrada, sube $K$ hasta 60 y anota el máximo de la suma parcial. ¿Baja al aumentar $K$?

<details><summary>Solución</summary>
Ronda 1,18 para cualquier $K$ grande: un exceso de 0,18 sobre 1, que es el 9 % del salto de altura 2. Al subir $K$, el pico se acerca al salto y se estrecha, pero no baja.
</details>

**3. Tren de pulsos.** Con ciclo de trabajo 0,25, ¿cuánto vale $c_0$? ¿Qué armónicos se anulan? ¿Qué pasa si el ciclo de trabajo baja a 0,1?

<details><summary>Solución</summary>
$c_0 = D = 0{,}25$, el valor medio. $c_k = 0{,}25\,\mathrm{sinc}(k/4)$ se anula en $k = \pm4, \pm8, \dots$ Con $D = 0{,}1$, los ceros se van a los múltiplos de 10 y el espectro se ensancha: un pulso más estrecho necesita más armónicos.
</details>

**4. Suavidad y decaimiento.** Compara la cuadrada y la triangular: ¿cuántos armónicos hacen falta en cada una para llevar el 99 % de la potencia?

<details><summary>Solución</summary>
En la triangular, el fundamental ya lleva $2 \cdot 16/\pi^4 \approx 0{,}329$ de $1/3$, un 98,6 %, y con $K = 3$ se supera el 99,8 %. En la cuadrada, con $K = 1$ se tiene el 81 %, con $K = 3$ el 90 % y hacen falta decenas de armónicos para el 99 %: $|c_k|$ decae como $1/k$ en lugar de $1/k^2$.
</details>

**5. Ejercicio 7 de la hoja: Parseval.** Comprueba con la herramienta que la potencia de la cuadrada es 1 y la de la triangular $1/3$, y que las sumas de $|c_k|^2$ se acercan a esos valores.

<details><summary>Solución</summary>
Con $K = 60$ la cuadrada llega a algo más de 0,99 de 1 (la suma de $1/k^2$ converge despacio) y la triangular a 0,3333 de $1/3$ en cuanto $K \ge 5$. La herramienta usa la triangular de $-1$ a 1, desplazada respecto a la de la hoja, pero $|c_k|$ no cambia con un desplazamiento.
</details>

## Para profundizar

- [Apuntes del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Apuntes.pdf), sección 6, «Serie de Fourier de señales continuas periódicas».
- [Transparencias T1-02](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%2002%20-%20Operaciones.pdf), serie de Fourier.
- [Hoja de ejercicios del Tema 1](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios.pdf), ejercicio 7, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T1%20-%20Ejercicios%20resueltos.pdf).
- Código: `teoría/T1/codigo/python/serie_fourier.py` y su versión en Matlab.
- A. V. Oppenheim, A. S. Willsky y S. H. Nawab, *Signals and Systems*, 2.ª ed., Prentice Hall, 1997, capítulo 3.
- J. H. McClellan, R. W. Schafer y M. A. Yoder, *DSP First*, 2.ª ed., Pearson, 2016, capítulo 3.

## Relación con otros conceptos

- **Exponenciales complejas.** Cada armónico es una exponencial $e^{j2\pi k f_0 t}$. Herramienta: [Exponencial compleja continua](T1-exponencial-continua.html).
- **Transformada de Fourier.** Cuando el periodo tiende a infinito, los armónicos se juntan y la serie se convierte en la transformada. Herramienta: [Propiedades de la transformada de Fourier](T1-propiedades-fourier.html).
- **Sistemas LTI.** Una señal periódica a la entrada de un LTI sale con cada armónico multiplicado por $H(jk\omega_0)$. Herramienta: [Respuesta de un sistema LTI continuo](T1-respuesta-lti-continua.html).
- **DFT (Tema 3).** La DFT es la serie de Fourier de una secuencia periódica de periodo $N$. Herramientas: [DFT, fuga y relleno con ceros](T3-dft.html) y [Extensión periódica](T3-extension-periodica.html).
- **Ventanas (Tema 3) y FIR por ventanas (Tema 4).** El fenómeno de Gibbs es la causa del rizado de los filtros diseñados truncando la respuesta ideal. Herramienta: [Diseño FIR por ventanas](T4-fir-ventana.html).
