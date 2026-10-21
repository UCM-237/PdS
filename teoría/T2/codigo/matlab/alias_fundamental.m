% Frecuencia discreta en [-π, π)
alias = @(w, Ts) mod(w*Ts + pi, 2*pi) - pi;

Ts = 2;                         % s
w1 = 2*pi/10;                   % rad/s
w2 = 2*pi/(10/6);               % rad/s
disp([alias(w1, Ts), alias(w2, Ts)])  % 0.4π
n = 0:19;
x1 = sin(w1 * Ts * n);
x2 = sin(w2 * Ts * n);
disp(max(abs(x1 - x2)) < 1e-9)  % 1
