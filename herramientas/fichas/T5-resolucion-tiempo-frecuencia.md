## Introducción

### Una ventana, dos resoluciones

Cada tramo de la STFT es la señal multiplicada por la ventana w[n]. En frecuencia, eso convoluciona el espectro con W(e^{jΩ}): dos tonos se distinguen si están más separados que el lóbulo principal de W, que mide unos 2f_s/L entre los −6 dB en Hann. En el tiempo, un suceso breve aparece en todos los tramos que lo contienen: dos sucesos se distinguen si están más separados que la duración efectiva de la ventana. **Alargar la ventana mejora la primera y empeora la segunda.**

### El principio de incertidumbre

Midiendo la duración y la anchura de banda con las desviaciones típicas de |w(t)|² y de |W(jω)|²,

> σ_t² = ∫ (t − t̄)² |w(t)|² dt / ∫ |w(t)|² dt,  σ_ω² = ∫ ω² |W(jω)|² dω / ∫ |W(jω)|² dω,

se cumple **σ_t σ_ω ≥ 1/2**, con igualdad solo para la ventana gaussiana. Es la misma desigualdad que la de Heisenberg en mecánica cuántica. Ninguna ventana puede ser a la vez muy corta y muy estrecha en frecuencia: el producto tiene un mínimo, y lo único que se elige es cómo repartirlo.

### Anchura rms y lóbulo principal

La anchura rms castiga mucho los lóbulos laterales lejanos. La ventana rectangular tiene el lóbulo principal más estrecho, pero sus lóbulos caen despacio (como 1/ω) y su σ_ω es grande: el producto vale más de 5. Para separar dos tonos de amplitud parecida importa el lóbulo principal; para ver un tono débil junto a uno fuerte, los laterales.

## Guía de uso

- La señal, muestreada a f_s = 4000 Hz, tiene dos tonos de 1000 y 1000 + Δf Hz hasta 0,45 s, y dos clics en 0,7 s y 0,7 s + Δt.
- **Ventana** y **L** fijan la STFT, que avanza R = L/8 muestras. La gaussiana tiene σ = L/6.
- Arriba a la derecha, el espectro medio de los tramos que solo contienen los tonos (promediar quita el efecto del batido entre ellos). Abajo, la energía de cada tramo alrededor de los clics. Los triángulos marcan las posiciones verdaderas.
- El recuadro dice si cada pareja se separa (hay un valle de al menos 3 dB entre los dos máximos) y da σ_t, σ_ω y su producto.

## Ejercicios

**1. Separar los tonos.** Con Hann y L = 128, ¿qué Δf mínimo se separa? ¿Y con L = 256 y L = 512? Compáralo con 2f_s/L.

<details><summary>Solución</summary>
Unos 64, 32 y 16 Hz, que coinciden con 2f_s/L = 62,5, 31 y 16 Hz. La regla de los apuntes funciona: con Hann, dos tonos se separan si distan al menos la mitad del lóbulo principal, que mide 4f_s/L entre ceros.
</details>

**2. Separar los clics.** Con Hann, Δf = 40 Hz, ¿qué Δt mínimo se separa con L = 128, 256 y 512? ¿Cuánto vale el producto Δf_mín · Δt_mín?

<details><summary>Solución</summary>
Unos 16, 34 y 65 ms, la mitad de la duración de la ventana (32, 64 y 128 ms), porque Hann pesa poco en los extremos. El producto Δf_mín · Δt_mín sale aproximadamente 1 en los tres casos (64 · 0,016, 32 · 0,034, 16 · 0,065): duplicar L divide entre dos lo que se separa en frecuencia y multiplica por dos lo que se separa en el tiempo.
</details>

**3. Las dos cosas a la vez.** Con Hann, Δf = 40 Hz y Δt = 20 ms, busca una L que separe tonos y clics. ¿La hay? ¿Y con la rectangular?

<details><summary>Solución</summary>
Con Hann no: los tonos necesitan L ≥ 208 y los clics L ≤ 160. Es el ejercicio 2 de la hoja con otros números. Con la rectangular sí hay un margen estrecho, de unas 136 a 168 muestras, porque su lóbulo principal es la mitad de ancho. El precio son los lóbulos laterales a −13 dB, que en el espectro medio se ven a ambos lados de los tonos.
</details>

**4. El producto de incertidumbre.** Con L = 128, anota σ_t, σ_ω y σ_tσ_ω para las cinco ventanas. ¿Cuál se acerca más a 1/2? ¿Cambia el producto con L?

<details><summary>Solución</summary>
Hann: 4,49 ms, 114 rad/s y 0,513. Hamming: 0,615. Blackman y la gaussiana: 0,502, casi el mínimo. Rectangular: 9,2 ms, 589 rad/s y 5,4, por sus lóbulos lejanos. En Hann y Blackman, al cambiar L, σ_t crece y σ_ω baja en la misma proporción y el producto no cambia. En la rectangular y en Hamming, cuyo salto en los extremos hace caer despacio los lóbulos, σ_ω queda fijada por los lóbulos lejanos, que llegan hasta f_s/2, y el producto crece con L: 2,7, 5,4 y 10,9 en la rectangular con L = 32, 128 y 512.
</details>

**5. Qué ventana elegir.** Con L = 128 y Δt = 15 ms, compara Hann, Blackman y la gaussiana. ¿Cuál separa los clics? ¿Y qué Δf mínimo separa cada una?

<details><summary>Solución</summary>
Blackman y la gaussiana separan los clics a 15 ms (necesitan unos 14 ms) y Hann no (16 ms), porque son más estrechas en el tiempo: tienen σ_t = 3,8 ms frente a 4,5 ms. A cambio necesitan Δf ≥ 71 a 73 Hz, frente a 64 de Hann. Las tres tienen un producto parecido; lo que cambia es el reparto entre tiempo y frecuencia.
</details>

## Para profundizar

- [Apuntes del Tema 5](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%20Apuntes.pdf), sección 1, «Resolución en tiempo y en frecuencia».
- [Transparencias T5-01](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%2001%20-%20STFT.pdf), el compromiso tiempo-frecuencia y el principio de incertidumbre.
- [Hoja de ejercicios del Tema 5](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%20Ejercicios.pdf), ejercicio 2, y sus [soluciones](https://github.com/UCM-237/PdS/blob/main/teor%C3%ADa/clase/T5%20-%20Ejercicios%20resueltos.pdf).
- S. Mallat, *A Wavelet Tour of Signal Processing*, 3.ª ed., Academic Press, 2009, apartados 2.3 y 4.2.

## Relación con otros conceptos

- **La STFT.** Herramienta: [STFT y espectrograma](T5-stft.html).
- **Lóbulo principal y lóbulos laterales (Tema 3).** Herramienta: [Ventanas y fuga espectral](T3-ventanas.html).
- **Escalado en tiempo y frecuencia (Tema 1).** Comprimir una señal en el tiempo la ensancha en frecuencia. Herramienta: [Propiedades de la transformada de Fourier](T1-propiedades-fourier.html).
- **Wavelets.** Reparten el compromiso de otra forma en cada frecuencia. Herramienta: [Escalograma frente a espectrograma](T5-escalograma.html).
