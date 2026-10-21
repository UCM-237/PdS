% Hito 3: estadística del ruido, detección de clics y filtro de Wiener. Completa las partes TODO.
iniciar();
[x, fs] = cargar();
s = cargar('audio_limpio.wav');
n0 = round(1.0 * fs);

% 1. Modelo del ruido (usa el primer segundo ya sin zumbido: copia aquí tus filtros del Hito 2)
ruido = x(1:n0);         % TODO: quita el zumbido antes
sd = std(ruido);
fprintf('media %.2e, sigma %.4f, curtosis %.2f\n', mean(ruido), sd, mean((ruido - mean(ruido)).^4) / sd^4 - 3);
[Pw, fw] = psd_welch(ruido, fs, 512);
Pp = abs(fft(ruido)).^2 / (fs * n0); Pp = 2 * Pp(1:n0/2+1); fp = (0:n0/2)' * fs / n0;
h = figure;
semilogy(fp, Pp, fw, Pw); grid on; xlabel('f (Hz)'); ylabel('PSD'); legend('periodograma', 'Welch');
guardar_figura(h, 'h3_psd_ruido.png');
% TODO: histograma con la gaussiana superpuesta y autocorrelación normalizada (xcorr).

% 2. Residuo de predicción en un bloque de ejemplo (Yule-Walker)
bloque = x(round(2.0*fs) + (1:1024));
orden = 16; N = length(bloque); r = zeros(orden + 1, 1);
for k = 0:orden
    r(k+1) = sum(bloque(1:N-k) .* bloque(1+k:N)) / N;
end
a = toeplitz(r(1:orden)) \ r(2:end);
e = filter([1; -a], 1, bloque);
fprintf('curtosis del residuo en el bloque: %.1f\n', mean((e - mean(e)).^4) / std(e)^4 - 3);
% TODO: calcula el residuo por bloques en toda la señal, fija un umbral robusto
%       (k * 1.4826 * MAD) y agrupa las muestras que lo superan en eventos.
% TODO: repara los clics por interpolación y decide el orden respecto a los filtros del H2.

% 3. TODO: filtro de Wiener con las PSD de Welch de la señal y del ruido:
%    H(f) = max(Px - Pn, 0) / Px, aplicado como FIR de fase cero.
