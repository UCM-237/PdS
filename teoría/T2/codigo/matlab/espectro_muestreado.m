fm = 1.0;                       % banda (Hz)
fs = 3.0;                       % fs > 2 fm
Ts = 1 / fs;
n = -300:300;
x = sinc(fm * n * Ts).^2;       % banda fm
[X, W] = freqz(x, 1, 2048, 'whole');
W = W - pi;                     % [-π, π)
X = fftshift(X);
plot(W / Ts, abs(X) * Ts)       % ω = Ω/Ts
xlabel('\omega (rad/s)')
