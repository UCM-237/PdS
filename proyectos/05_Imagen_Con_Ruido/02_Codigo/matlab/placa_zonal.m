function z = placa_zonal(n)
% cos(π r² / n): la frecuencia local crece con el radio hasta 0,5 ciclos/px en el borde.
if nargin < 1, n = 512; end
[x, y] = meshgrid((0:n-1) - n / 2);
z = 0.5 + 0.5 * cos(pi * (x.^2 + y.^2) / n);
end
