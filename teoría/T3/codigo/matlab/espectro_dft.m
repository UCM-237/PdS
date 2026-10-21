fs = 1000;                      % Hz
N = 200;                        % Δf = 5 Hz
n = 0:N-1;
x = 2*cos(2*pi*100*n/fs) ...
    + 0.5*cos(2*pi*152*n/fs);
w = hanning(N).';               % ventana
X = fft(x .* w);
X = X(1:N/2+1);                 % k = 0..N/2
f = (0:N/2) * fs / N;           % Hz
A = 2 * abs(X) / sum(w);        % amplitud
[Am, i] = max(A);
disp([f(i), Am])                % 100 Hz, 2
plot(f, 20*log10(A + 1e-12))
xlabel('f (Hz)')
