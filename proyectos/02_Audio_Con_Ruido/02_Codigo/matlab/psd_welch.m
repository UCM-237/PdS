function [P, f] = psd_welch(x, fs, N)
% PSD unilateral por el método de Welch: ventana de Hann de N muestras y 50 %
% de solape. Se escribe a mano porque pwelch no recibe el solape igual en
% Matlab (muestras) que en Octave (fracción). Equivale a scipy.signal.welch.
x = x(:);
w = hanning(N, 'periodic');
R = N / 2;
nt = floor((length(x) - N) / R) + 1;
P = zeros(N/2 + 1, 1);
for j = 1:nt
    seg = x((j-1)*R + (1:N));
    seg = (seg - mean(seg)) .* w;
    S = fft(seg);
    P = P + abs(S(1:N/2+1)).^2;
end
P = P / (nt * fs * sum(w.^2));
P(2:end-1) = 2 * P(2:end-1);
f = (0:N/2)' * fs / N;
end
