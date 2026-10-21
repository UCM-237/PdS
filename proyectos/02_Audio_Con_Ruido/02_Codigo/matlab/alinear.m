function y = alinear(x, retardo)
% Compensa un retardo entero (muestras) de un filtro causal.
y = [x(retardo+1:end); zeros(retardo, 1)];
end
