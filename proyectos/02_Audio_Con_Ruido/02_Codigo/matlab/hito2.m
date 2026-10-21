% Hito 2: filtrado lineal del zumbido y del soplido. Completa las partes TODO.
iniciar();
[x, fs] = cargar();
s = cargar('audio_limpio.wav');

% 1. Zumbido: cascada de muescas de segundo orden en 50, 100, ..., 300 Hz
r = 0.99;   % TODO: elige r a partir del ancho de muesca que necesitas (ancho ~ (1 - r) fs / pi)
B = zeros(6, 3); A = zeros(6, 3);
for k = 1:6
    w0 = 2*pi*50*k/fs;
    B(k, :) = [1, -2*cos(w0), 1];
    A(k, :) = [1, -2*r*cos(w0), r^2];
end
% Se filtra sección a sección: el polinomio completo de orden 12 es numéricamente inestable
y_causal = x; y_cero = x;
for k = 1:6
    y_causal = filter(B(k, :), A(k, :), y_causal);
    y_cero = filtfilt(B(k, :), A(k, :), y_cero);
end
fprintf('SNR: original %.2f dB, muescas causal %.2f dB, fase cero %.2f dB\n', ...
        snr_db(s, x), snr_db(s, y_causal), snr_db(s, y_cero));
% TODO: dibuja |H(f)| de la cascada entre 0 y 400 Hz (freqz de cada sección y multiplica).
% TODO: diseña también el filtro peine (1 - z^-N) / (1 - rho z^-N) y compáralo.

% 2. Paso bajo con la misma especificación, FIR e IIR
FP = []; FST = []; RP = 0.5; AS = 60;    % TODO: bandas de paso y de rechazo en Hz (H1, pregunta 4)
if ~isempty(FP)
    % FIR por ventana de Kaiser
    [L, wn, beta] = kaiserord([FP FST], [1 0], [1 - 10^(-RP/20), 10^(-AS/20)], fs);
    if mod(L, 2) == 1, L = L + 1; end      % orden par = longitud impar
    hf = fir1(L, wn, kaiser(L + 1, beta));
    y_fir = alinear(filter(hf, 1, y_cero), L / 2);
    fprintf('FIR orden %d: SNR = %.2f dB\n', L, snr_db(s, y_fir));
    % TODO: diseña un IIR (buttord/butter, cheb1ord/cheby1 o ellipord/ellip) con la misma
    %       especificación, dibuja |H| y el retardo de grupo (grpdelay) de los dos y mide la SNR
    %       con filtrado causal y de fase cero.
end
