% Hito 1: señal y espectro. Completa las partes marcadas con TODO.
iniciar();
[x, fs] = cargar();
s = cargar('audio_limpio.wav');            % solo para medir la SNR real
n = length(x); t = (0:n-1)' / fs;
n0 = round(1.0 * fs);                      % el primer segundo solo tiene ruido
fprintf('fs = %d Hz, %d muestras, SNR real = %.2f dB\n', fs, n, snr_db(s, x));

% 1. Señal en el tiempo
h = figure;
subplot(2, 1, 1); plot(t, x); grid on; xlabel('t (s)'); ylabel('x(t)'); title('Señal completa');
% TODO: en subplot(2, 1, 2), un detalle de unas decenas de ms donde se vea un clic
guardar_figura(h, 'h1_tiempo.png');

% 2. Espectro del primer segundo y de la señal completa
[f0, X0] = espectro(x(1:n0), fs);
[f, X] = espectro(x, fs);
h = figure;
plot(f, X, f0, X0); grid on; ylim([-110 -10]);
xlabel('f (Hz)'); ylabel('|X| (dB)'); legend('señal completa', 'primer segundo');
guardar_figura(h, 'h1_espectro.png');

% 3. TODO: localiza las rayas del zumbido en X0 (findpeaks) y escribe frecuencia y amplitud.

% 4. TODO: estima sigma del soplido con psd_welch(x(1:n0), fs, 1024).
%    Pista: para ruido blanco, PSD unilateral = 2 sigma^2 / fs.

% 5. Espectrograma: localiza el silbido
[Z, fz, tz] = mi_stft(x, fs, 512);
h = figure;
imagesc(tz, fz, 20*log10(abs(Z) + 1e-9), [-100 -20]); axis xy; colorbar;
xlabel('t (s)'); ylabel('f (Hz)'); title('Espectrograma');
guardar_figura(h, 'h1_espectrograma.png');
% TODO: mide los instantes de inicio y fin del silbido y sus frecuencias.

% Pregunta 1: TODO repite el espectro con N = 256, 1024, 4096 y 16000 muestras.
