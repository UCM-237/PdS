function [f, XdB] = espectro(x, fs)
% Módulo de la DFT unilateral en dB, con ventana de Hann.
N = length(x);
w = 0.5 - 0.5 * cos(2*pi*(0:N-1)'/(N-1));
X = fft(x(:) .* w) / sum(w) * 2;
K = floor(N/2) + 1;
f = (0:K-1)' * fs / N;
XdB = 20 * log10(abs(X(1:K)) + 1e-12);
end
