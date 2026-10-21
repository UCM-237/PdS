function y = gauss(x, sigma)
% Paso bajo gaussiano 2D (separable), truncado en 4 sigma.
r = ceil(4 * sigma); n = -r:r;
h = exp(-n.^2 / (2 * sigma^2)); h = h / sum(h);
y = filtrar_sep(x, h, h);
end
