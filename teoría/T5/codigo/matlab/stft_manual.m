fs = 1000;
t = 0:1/fs:2-1/fs;
x = chirp(t, 50, 2, 400);        % 50->400
L = 128; R = 32; N = 256;    % L, salto, FFT
w = hanning(L)';
ini = 1:R:numel(x)-L+1;
X = zeros(N/2+1, numel(ini));
for m = 1:numel(ini)
  S = fft(x(ini(m):ini(m)+L-1).*w, N);
  X(:, m) = S(1:N/2+1);          % (f, t)
end
f = (0:N/2)*fs/N;
tm = (ini - 1 + L/2)/fs;         % centros
[~, k] = max(abs(X));
disp(size(X))                    % 129 59
disp([tm(1:10:end); f(k(1:10:end))]')
% Igual: spectrogram(x, w, L-R, N, fs)
