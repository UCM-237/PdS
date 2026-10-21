# Normas de los proyectos

## Lenguaje

Cada proyecto trae el mismo código de partida en **Matlab** (`02_Codigo/matlab/`) y en **Python** (`02_Codigo/python/`). El alumno elige uno y lo indica en cada entrega. Las funciones equivalentes más usadas:

| Tarea | Matlab | Python |
|---|---|---|
| FFT y eje de frecuencias | `fft`, `(0:N-1)*fs/N` | `np.fft.rfft`, `np.fft.rfftfreq(N, 1/fs)` |
| PSD de Welch | `pwelch(x, win, nover, nfft, fs)` | `scipy.signal.welch(x, fs, nperseg=...)` |
| Diseño IIR | `butter`, `cheby1`, `ellip` + `buttord` | `scipy.signal.butter`, `cheby1`, `ellip` + `buttord` |
| Diseño FIR | `fir1`, `firpm`, `kaiserord` | `scipy.signal.firwin`, `remez`, `kaiserord` |
| Filtrar | `filter`, `filtfilt` | `scipy.signal.lfilter`, `filtfilt` |
| Respuesta en frecuencia | `freqz(b, a, n, fs)` | `scipy.signal.freqz(b, a, worN=n, fs=fs)` |
| Espectrograma | `spectrogram(x, win, nover, nfft, fs)` | `scipy.signal.spectrogram` o `stft` |
| Picos | `findpeaks` | `scipy.signal.find_peaks` |
| Leer audio / imagen | `audioread`, `imread` | `scipy.io.wavfile.read`, `matplotlib.image.imread` |

## Reproducibilidad

- Todas las figuras y tablas de un hito se generan con **un solo comando** desde la carpeta del código.
- Nada de rutas absolutas ni datos modificados a mano.
- Si se usan números aleatorios, la semilla es fija.

## Uso de herramientas de IA

Se pueden usar para programar y redactar, indicando en el informe para qué. El alumno debe entender y saber explicar todo lo que entrega: en la defensa se le pedirá cambiar un parámetro y predecir el efecto antes de ejecutarlo.

## Trabajo individual

Se puede comentar el enfoque con otros compañeros, pero el código y el informe son individuales. Dos entregas con el mismo código o el mismo texto se califican con 0.
