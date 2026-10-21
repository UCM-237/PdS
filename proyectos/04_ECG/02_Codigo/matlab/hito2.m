% Hito 2: filtrado. Completa las partes marcadas con TODO.
iniciar();
fs = 360;
[t, x] = cargar('ecg_A.csv');
[~, s] = cargar('ecg_A_limpio.csv');      % solo para medir la distorsión
s0 = s - median(s);
ref = anotaciones();
error_uv = @(y) 1000 * sqrt(mean((y - median(y) - s0).^2));

% segmento ST: de 80 a 120 ms después de cada pico R
st = [];
for r = ref(3:end-2)', st = [st, r + (round(0.08*fs):round(0.12*fs)-1)]; end

% 1. Línea base con un Butterworth paso alto de 0,5 Hz
[b, a] = butter(2, 0.5/(fs/2), 'high');
y_causal = filter(b, a, x);
fprintf('sin filtrar: %.0f µV; Butterworth causal: %.0f µV\n', error_uv(x), error_uv(y_causal));
% TODO: el mismo filtro con fase cero (filtfilt), un FIR de fase lineal (kaiserord + fir1)
%       y un estimador de medianas (medfilt1 de 200 ms y luego de 600 ms).
% TODO: error en el ST de cada opción: media de abs(y(st) - s0(st)).

% 2. TODO: muesca de 50 Hz de segundo orden y paso bajo de unos 40 Hz.

m = t > 30 & t < 32.2;
h = figure;
plot(t(m), s0(m), 'k', t(m), y_causal(m) - median(y_causal)); grid on;
xlabel('t (s)'); ylabel('mV'); legend('limpia', 'Butterworth causal');
guardar_figura(h, 'h2_linea_base.png');
