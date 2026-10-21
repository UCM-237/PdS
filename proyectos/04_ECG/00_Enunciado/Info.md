En el análisis y procesado digital de señales de Electrocardiograma (ECG), las **ondas P, QRS y T** representan los eventos eléctricos fundamentales del ciclo cardíaco. Identificar y caracterizar estas deflexiones es la base para la detección automática de arritmias, la variabilidad del ritmo cardíaco (HRV) y la estimación de patologías miocárdicas.

---

### 1. Fisiología y Caracterización en Procesado de Señales

* **Onda P:**
  * **Origen fisiológico:** Despolarización (activación eléctrica) de las aurículas.
  * **Características en la señal:** Onda de baja amplitud ($< 0.25\text{ mV}$) y baja frecuencia. 
  * **Reto en procesado:** Debido a su pequeña magnitud, suele ser la más susceptible a degradarse por ruido EMG (actividad muscular) y desplazamiento de la línea base.

* **Complejo QRS (ondas Q, R, S):**
  * **Origen fisiológico:** Despolarización rápida de los ventrículos.
  * **Características en la señal:** Pico prominente de alta frecuencia y gran amplitud. La onda R es la deflexión positiva principal.
  * **Importancia en procesado:** Es el punto de anclaje de casi todos los algoritmos. La detección del pico R permite delimitar el intervalo R-R (para calcular la frecuencia cardíaca) y segmentar el resto de la señal.

* **Onda T:**
  * **Origen fisiológico:** Repolarización ventricular (recuperación eléctrica de los ventrículos).
  * **Características en la señal:** Onda de frecuencia intermedia, típicamente asimétrica y de amplitud moderada.
  * **Importancia en procesado:** El intervalo entre el inicio del QRS y el final de la onda T se utiliza para calcular el **intervalo QT**, crítico en el diagnóstico de riesgo de arritmias malignas.

---

### 2. Tratamiento en Procesado Digital de Señales (DSP)

1. **Preprocesado y Filtrado:**
   * **Filtro pasa-banda (típicamente 0.5 Hz – 45 Hz):** Se elimina el *baseline wander* (desplazamiento de la línea base $<0.5\text{ Hz}$) y la interferencia de la red eléctrica ($50/60\text{ Hz}$).
2. **Detección del complejo QRS:**
   * Se aplican filtros derivados y operadores de energía (como la transformada de Pan-Tompkins o Transformada Wavelet) para resaltar la pendiente pronunciada de la onda R.
3. **Delimitación de P y T:**
   * Tras fijar la posición del pico R, se abren ventanas temporales a la izquierda (para buscar la onda P) y a la derecha (para la onda T) mediante análisis morfológico o transformadas tiempo-frecuencia.

---

### 3. Referencias Clave en la Literatura Científica

Si buscas estudiar o implementar algoritmos de procesado de ECG, las siguientes publicaciones son los estándares globales y marcos de referencia de la industria:

1. **Pan, J., & Tompkins, W. J. (1985).** *A real-time QRS detection algorithm.* IEEE Transactions on Biomedical Engineering, BME-32(3), 230-236.
   * **Por qué consultarlo:** Es el algoritmo clásico definitivo para la detección del complejo QRS mediante filtrado de banda, derivación, al cuadrado e integración por ventana.
2. **Martínez, J. P., Almeida, R., Olmos, S., Rocha, A. P., & Laguna, P. (2004).** *A wavelet-based ECG delineator: evaluation on standard databases.* IEEE Transactions on Biomedical Engineering, 51(4), 570-581.
   * **Por qué consultarlo:** Trabajo de referencia para delimitar no solo el QRS, sino también las fronteras (inicio y fin) de las ondas P y T utilizando la Transformada Wavelet Discreta (DWT).
3. **Goldberger, A. L., et al. (2000).** *PhysioBank, PhysioToolkit, and PhysioNet: components of a new research resource for complex physiologic signals.* Circulation, 101(23), e215-e220.
   * **Por qué consultarlo:** Presenta las bases de datos de ECG abiertas (como el *MIT-BIH Arrhythmia Database*) estándar para validar la precisión de algoritmos de detección de ondas P, QRS y T.