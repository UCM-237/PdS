## Introducción

### Señales dispersas en la base wavelet

Una señal suave a trozos tiene pocos coeficientes de detalle grandes, junto a sus saltos y picos, y muchísimos casi nulos: es **dispersa** en la base wavelet. El ruido blanco gaussiano, en cambio, sigue siendo ruido blanco de la misma varianza σ² en cualquier base ortonormal, y reparte su energía por igual entre todos los coeficientes. Esa diferencia permite separarlos.

### Umbral duro y umbral suave

Se calcula la DWT, se aplica a cada detalle una regla de umbral y se reconstruye:

- **Umbral duro**: d̂ = d si |d| > u y 0 si no. Conserva los coeficientes grandes tal como están.
- **Umbral suave**: d̂ = signo(d)(|d| − u) si |d| > u y 0 si no. Además encoge los grandes en u, lo que da resultados más suaves, pero rebaja la altura de los saltos.

La aproximación a_J no se toca: contiene la forma general de la señal.

### Cuánto vale el umbral

Si se conoce σ, el **umbral universal** de Donoho y Johnstone es u = σ√(2 ln N): con probabilidad que tiende a 1, todos los coeficientes de ruido puro quedan por debajo. Como σ no se conoce, se estima con los detalles más finos, d₁, que son casi solo ruido. Para que unos pocos coeficientes grandes de la señal no la estropeen se usa la mediana:

> σ̂ = mediana(|d₁|)/0,6745,

porque la mediana de |Z| con Z ~ N(0, 1) es 0,6745.

### Compresión

Si se guardan solo los K coeficientes más grandes y se anulan los demás, la señal reconstruida es la mejor aproximación con K términos en esa base (la energía del error es la de los coeficientes descartados). Es el principio de JPEG 2000, que usa wavelets sobre imágenes.

## Guía de uso

- **Señal**: tres de las señales de prueba de Donoho y Johnstone (Bloques, Doppler y HeaviSine) y unos escalones, con N = 1024 muestras. Se suma ruido gaussiano de desviación **σ**; **Realización** cambia el ruido.
- **Eliminar ruido**: se umbralizan los detalles con la regla elegida y el umbral u = factor · u_universal. **Comprimir**: se guardan los coeficientes mayores (también los de aproximación) en el porcentaje elegido.
- La gráfica de la izquierda muestra la señal con ruido, la limpia y el resultado, y, si se marca, una media móvil de 9 muestras para comparar. Abajo, los coeficientes con el umbral y la regla de umbral.
- El recuadro da σ̂, el umbral, los coeficientes que quedan y el error cuadrático medio (ECM) y la SNR de la señal con ruido, del resultado y de la media móvil.

## Ejercicios

**1. Estimar el ruido.** Con los valores de partida (Bloques, Haar, J = 5, σ = 0,5), ¿cuánto valen σ̂ y u? Comprueba el cálculo. ¿Qué ECM tiene la señal con ruido y por qué?

<details><summary>Solución</summary>
σ̂ = 0,495, muy cerca de 0,5, y u = 0,495 · √(2 ln 1024) = 0,495 · 3,72 = 1,84. El ECM con ruido es 0,254 ≈ σ² = 0,25: es la varianza del ruido. Es el apartado c del ejercicio 10 de la hoja, con otros números.
</details>

**2. Elegir la wavelet.** Con σ = 0,5, umbral duro y u universal, compara Haar y db4 en Bloques y en HeaviSine. ¿Cuál va mejor en cada una y por qué?

<details><summary>Solución</summary>
En Bloques, Haar: SNR de 14,9 dB frente a 13,7 dB, porque la señal es constante a trozos, como las funciones de Haar. En HeaviSine, db4: 22,2 dB frente a 17,5 dB, porque la señal es suave salvo en dos saltos y Haar la convierte en escalones. La mejor wavelet es la que hace más dispersa la señal.
</details>

**3. Duro, suave y el factor del umbral.** En Bloques con Haar, prueba el umbral duro y el suave con factores de 0,3 a 1,2. ¿Cuál es el mejor de cada uno?

<details><summary>Solución</summary>
Con umbral duro, el mejor está hacia 0,8 (15,0 dB), casi igual que el universal (14,9 dB); con 0,4 quedan 221 coeficientes, muchos de ellos ruido, y baja a 9,8 dB. Con umbral suave el universal es demasiado grande (12,3 dB), porque encoge todos los coeficientes en u y rebaja los saltos; el mejor está hacia 0,5 (15,4 dB). El universal está pensado para quitar *todo* el ruido, no para minimizar el ECM.
</details>

**4. Frente a la media móvil.** Compara el umbral (con la wavelet adecuada) con la media móvil de 9 muestras en Bloques y en Doppler para σ = 0,25 y σ = 1. ¿Cuándo gana cada uno?

<details><summary>Solución</summary>
Con σ = 0,25 gana el umbral con claridad: 22,1 frente a 16,4 dB en Bloques (Haar) y 20,7 frente a 16,9 dB en Doppler (db4). La media móvil redondea los saltos y amortigua las oscilaciones rápidas, y ese error no depende del ruido. Con σ = 1 quedan casi empatados en esas dos señales (10,0 frente a 10,7 y 10,3 frente a 10,4 dB), pero en Escalones (Haar) y HeaviSine (db4) el umbral sigue ganando por 3 a 4 dB. Con mucho ruido, los coeficientes pequeños de la señal quedan por debajo del umbral y se pierden.
</details>

**5. Comprimir.** Sin ruido (σ = 0), en modo Comprimir con J = 7, guarda el 5 % de los coeficientes. Compara la SNR de Haar y db4 en Bloques, Doppler y HeaviSine. ¿Y con el 2 %?

<details><summary>Solución</summary>
Con el 5 % (50 coeficientes): Bloques, 26,6 dB con Haar y 17,8 con db4; Doppler, 14,0 y 22,5 dB; HeaviSine, 23,6 y 44,5 dB. Con el 2 %, HeaviSine con db4 sigue en 25,8 dB, mientras que con Haar baja a 14,3. Cuantos menos coeficientes necesite una base para una señal, mejor la comprime: para señales constantes a trozos, Haar; para señales suaves, wavelets con más momentos nulos.
</details>

## Para profundizar

- [Apuntes del Tema 5](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%20Apuntes.pdf), sección 2, «Aplicaciones».
- [Transparencias T5-02](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%2002%20-%20Wavelets.pdf), eliminación de ruido y compresión.
- [Hoja de ejercicios del Tema 5](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%20Ejercicios.pdf), ejercicio 10, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%20Ejercicios%20resueltos.pdf).
- D. L. Donoho e I. M. Johnstone, «Ideal spatial adaptation by wavelet shrinkage», *Biometrika* 81(3), 1994, 425-455.
- S. Mallat, *A Wavelet Tour of Signal Processing*, 3.ª ed., Academic Press, 2009, capítulos 10 y 11.

## Relación con otros conceptos

- **La DWT.** Herramienta: [DWT y análisis multirresolución](T5-dwt-multirresolucion.html).
- **Filtrado lineal (Tema 4).** La media móvil es un paso bajo y no distingue saltos de ruido. Herramienta: [Filtro de media móvil](T4-media-movil.html).
- **Ruido blanco (Tema 6).** Su invarianza ante cambios de base ortonormal. Herramienta: [Realizaciones, estacionariedad y ergodicidad](T6-realizaciones.html).
- **Cuantificación (Tema 2).** Comprimir es descartar y cuantificar coeficientes. Herramienta: [Cuantificación y SQNR](T2-cuantificacion.html).
