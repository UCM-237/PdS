% y[n] = 0.8 y[n-1] + 0.2 x[n]
b = 0.2; a = [1 -0.8];
d = [1 zeros(1, 29)];          % δ[n]
h = filter(b, a, d);           % 0.2·0.8^n
polos = roots(a);              % 0.8
fprintf('¿Estable? %d\n', all(abs(polos) < 1))
[H, w] = freqz(b, a);          % [0, π)
