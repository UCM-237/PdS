% Hito 4: STFT, silbido y sustracción espectral. Completa las partes TODO.
iniciar();
[x, fs] = cargar();
s = cargar('audio_limpio.wav');
n = length(x); n0 = round(1.0 * fs);

y3 = x;        % TODO: sustituye por la salida de tu cadena del Hito 3
NPS = 512;     % TODO: justifica la longitud de ventana (prueba al menos tres)

[Z, f, t] = mi_stft(y3, fs, NPS);
% Comprobación: la STFT con este solape se invierte sin error
fprintf('error de reconstrucción: %.1e\n', max(abs(mi_istft(Z, NPS, n) - y3)));

% 1. TODO: en cada trama, busca el pico en la banda del silbido; quédate con las tramas
%    donde destaca; ajusta una recta f(t) (polyfit) y pon a cero las celdas a +-ancho Hz.

% 2. TODO: sustracción espectral con la potencia media del ruido en el primer segundo:
%    G = sqrt(max(1 - alfa * Pn ./ abs(Z).^2, beta^2))

y4 = mi_istft(Z, NPS, n);
h = figure;
imagesc(t, f, 20*log10(abs(Z) + 1e-9), [-100 -20]); axis xy; colorbar; xlabel('t (s)'); ylabel('f (Hz)');
guardar_figura(h, 'h4_espectrograma.png');
fprintf('SNR final: %.2f dB\n', snr_db(s, y4));
audiowrite('audio_restaurado.wav', max(min(y4, 1), -1), fs);
