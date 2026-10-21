x = ones(1, 5);                % pulso, L = 5
[X, w] = freqz(x, 1, 1024, ...
               'whole');       % [0, 2π)
plot(w, abs(X))
xlabel('\omega (rad/muestra)')
