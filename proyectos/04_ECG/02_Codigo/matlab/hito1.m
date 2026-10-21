% Hito 1: señal y espectro. Completa las partes marcadas con TODO.
iniciar();
fs = 360;
[t, x] = cargar('ecg_A.csv');
[~, xb] = cargar('ecg_B.csv');
[ref, tipos] = anotaciones();
fprintf('%d muestras, %d latidos anotados en A\n', numel(x), numel(ref));

h = figure;
subplot(2, 1, 1); plot(t, x); grid on; xlabel('t (s)'); ylabel('mV'); title('Registro A');
m = t > 20 & t < 24;
subplot(2, 1, 2); plot(t(m), x(m)); grid on; xlabel('t (s)'); ylabel('mV'); title('Detalle de 4 s');
% TODO: señala las ondas P, QRS y T de un latido; dibuja también el registro B
guardar_figura(h, 'h1_tiempo.png');

[P, f] = psd_welch(x, fs, 8192);
h = figure; semilogy(f, P); grid on; xlabel('f (Hz)'); ylabel('PSD (mV^2/Hz)');
guardar_figura(h, 'h1_psd.png');
% TODO: marca la línea base, la red, la banda del QRS y el ruido muscular.
% TODO: FC por las rayas del espectro en 0-6 Hz y por la autocorrelación (xcorr);
%       compáralas con 60 / mean(diff(ref) / fs).
% TODO: amplitud de la raya de 50 Hz a partir de la potencia en 49-51 Hz.
