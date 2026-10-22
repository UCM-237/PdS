T = @(x) x.^2;               % sistema a estudiar

x1 = randn(1, 50); x2 = randn(1, 50);
a = 2; b = -3;
izq = T(a*x1 + b*x2);
der = a*T(x1) + b*T(x2);
fprintf('¿Lineal? %d\n', ...
        max(abs(izq - der)) < 1e-10)
