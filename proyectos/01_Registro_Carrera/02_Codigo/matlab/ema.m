function y = ema(t, x, tau)
% Media móvil exponencial de entrenamiento/main.py, válida con muestreo irregular.
y = zeros(size(x)); y(1) = x(1);
for k = 2:numel(x)
    a = 1 - exp(-(t(k) - t(k-1)) / tau);
    y(k) = a * x(k) + (1 - a) * y(k-1);
end
end
