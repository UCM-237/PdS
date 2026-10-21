function [FX, FY] = frecuencias_2d(forma)
% Rejilla de frecuencias (ciclos/px) en el orden de fftshift.
f = @(n) ((0:n-1) - floor(n / 2)) / n;
[FX, FY] = meshgrid(f(forma(2)), f(forma(1)));
end
