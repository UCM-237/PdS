function [Z, f, t] = mi_stft(x, fs, N)
% STFT con ventana de Hann de N muestras y solape del 75 %. Columnas = tramas.
% Se rellena con N/2 ceros por cada lado para que la primera trama esté centrada en t = 0.
R = N / 4;
w = hanning(N, 'periodic');
xp = [zeros(N/2, 1); x(:); zeros(N/2 + N, 1)];
nt = floor((length(xp) - N) / R) + 1;
Z = zeros(N/2 + 1, nt);
for j = 1:nt
    seg = xp((j-1)*R + (1:N)) .* w;
    S = fft(seg);
    Z(:, j) = S(1:N/2+1) / sum(w);
end
f = (0:N/2)' * fs / N;
t = (0:nt-1) * R / fs;
end
