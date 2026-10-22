# Tema 2: Señales aleatorias

## Concepto: Señales deterministas vs estocásticas (5 minutos)

## Concepto: Variable aleatoria (15 minutos)

- *Definición*: una variable que puede tomar un valor aleatorio, no conocido a priori.
- Es aleatoria, pero... ¿podemos caracterizarlo de alguna manera?
  - ¿Puede tomar cualquier valor? ¿Son valores continuos o discretos?
  - ¿Todos los valores son igual de probables?
  - ¿Qué más se puede inferir?

- Caso discreto
  - Función de probabilidad de masa: p(x) ~ casos favorables / posibles.
  - Indica como de probable es la ocurrencia de cada valor.

- Caso continuo
  - Probabilidad de masa no tiene sentido: $p(x=x_i) = 0$
  - Función de densidad de probabilidad:


## Concepto: Valor esperado (15 minutos)

- Definición: Formalización del concepto de valor medio. Se expresa matemáticamente como $E(x)=\frac{1}{N}\sum_{n=1}^{N}x_i$

- Remarcamos
  - Medida de centralización: los valores se agrupan en torno a mu_x.
  - Valor central, deja la mitad de valores a cada lado.
  - Minimiza el error cuadrático total de predicción.
    e_p(x) = x_i - x,  \sum_{i=1}^{n}{e_p(x_i)^2}

## Concepto: Muestreo ()
  - Una variable aleatoria es un marco teórico que permite análisis y síntesis.
  - Llamamos muestreo al proceso de generación de los valores que tomar la variable aleatoria, realizando diferentes ocurrencias o experimentos.

  - Los experimentos pueden hacerse de distintas formas: 
    - Entrada determinista sobre un sistema real que posee un componente aleatorio, o bien
    - Entrada aleatoria a un proceso determinista, o bien
    - Simulación

 


