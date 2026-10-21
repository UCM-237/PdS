# ECG

## Contexto
Se trabaja con una senal electrocardiografica que puede contener ruido, deriva de la linea de base, interferencia de red y artefactos de movimiento. El objetivo es analizar la senal, extraer eventos relevantes y justificar un procesamiento que permita medir indicadores cardiacos de forma fiable.

## Objetivo
Detectar complejos QRS y obtener indicadores utiles de la actividad cardiaca, comparando el comportamiento de la senal antes y despues del preprocesado.

## Teoria minima necesaria
Un ECG tipico presenta las ondas P, QRS y T. En una tarea de analisis basico basta con localizar el complejo QRS, porque su pico R es el evento mas facil de detectar y permite estimar la frecuencia cardiaca.

Problemas habituales:
1. Deriva de la linea de base: variacion lenta de baja frecuencia.
2. Interferencia de red: tipicamente 50 Hz o 60 Hz.
3. Ruido muscular o de movimiento: componentes rapidas y no estacionarias.

Procesado habitual:
1. Filtrado pasa banda para conservar aproximadamente la zona util del ECG.
2. Eliminacion de artefactos lentos con detrending o filtrado de muy baja frecuencia.
3. Resaltado de QRS mediante derivada, cuadrado y ventana movil.
4. Deteccion de picos y calculo de intervalos RR.

## Tareas
1. Cargar la senal y representar el ECG en el dominio temporal.
2. Identificar visualmente la amplitud, el periodo cardiaco aproximado y los artefactos dominantes.
3. Analizar el espectro para localizar deriva de base, ruido de red y energia del QRS.
4. Disenar y aplicar un preprocesado justificando el rango de paso banda elegido.
5. Detectar los complejos QRS con un metodo reproducible.
6. Calcular los intervalos RR y estimar la frecuencia cardiaca media.
7. Proponer un criterio simple de alarma o clasificacion, por ejemplo taquicardia, bradicardia o ritmo irregular.
8. Comparar la senal original, la filtrada y la senal usada para deteccion.

## Flujo de trabajo sugerido
1. Representar la senal cruda.
2. Calcular una FFT o periodograma para localizar la energia principal.
3. Aplicar un filtro pasa banda, por ejemplo en torno a 0.5-40 Hz o 5-15 Hz segun el objetivo.
4. Rectificar o cuadrar la respuesta filtrada.
5. Aplicar una ventana movil o envolvente para destacar los picos QRS.
6. Usar un detector de picos para localizar las ondas R.
7. Medir los intervalos RR y estimar la frecuencia cardiaca.

## Ejemplos de codigo
### Lectura y representacion
```matlab
datos = load('ecg.txt');
t = datos(:,1);
x = datos(:,2);

figure;
plot(t, x);
xlabel('Tiempo (s)');
ylabel('Amplitud');
title('ECG original');
grid on;
```

### Filtrado pasa banda
```matlab
Fs = 250;
[b, a] = butter(4, [0.5 40] / (Fs/2), 'bandpass');
x_filtrada = filtfilt(b, a, x);

figure;
plot(t, x, 'Color', [0.7 0.7 0.7]);
hold on;
plot(t, x_filtrada, 'b', 'LineWidth', 1.2);
legend('Original', 'Filtrada');
grid on;
```

### Realce del complejo QRS
```matlab
dx = diff(x_filtrada);
dx = [dx; dx(end)];
energia = dx.^2;

N = round(0.12 * Fs);
ventana = ones(N,1) / N;
envolvente = conv(energia, ventana, 'same');

figure;
plot(t, envolvente, 'k');
xlabel('Tiempo (s)');
ylabel('Energia local');
title('Realce del QRS');
grid on;
```

### Deteccion de picos R
```matlab
[picos, instantes] = findpeaks(envolvente, t, ...
	'MinPeakDistance', 0.25, ...
	'MinPeakProminence', 0.2 * max(envolvente));

rr = diff(instantes);
fc_media = 60 ./ mean(rr);
```

## Ejemplo de interpretacion
- Si la frecuencia cardiaca media supera 100 lpm de forma sostenida, se puede proponer un criterio de taquicardia.
- Si baja por debajo de 60 lpm, se puede proponer bradicardia.
- Si los intervalos RR son muy irregulares, se puede marcar posible arritmia simple o deteccion inestable.

## Entregables
- Memoria tecnica con figuras del ECG original, filtrado y etapa de deteccion.
- Codigo reproducible con el preprocesado y la deteccion QRS.
- Tabla o resumen con numero de latidos detectados, frecuencia cardiaca media y criterio de alarma.

## Criterios de evaluacion
- Calidad de la deteccion QRS y estabilidad de los picos detectados.
- Solidez del preprocesado y justificacion del filtro usado.
- Interpretacion correcta de los intervalos RR y de la frecuencia cardiaca.
- Claridad de las figuras, del codigo y de la conclusion final.
