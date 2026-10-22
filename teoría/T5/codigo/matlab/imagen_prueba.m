function f = imagen_prueba(N)
% Imagen sintética de N x N en [0, 1].
if nargin < 1, N = 256; end
[x, y] = meshgrid((0:N-1)/N);
f = 0.35 + 0.25*x;               % degradado
f((x-0.3).^2 + (y-0.32).^2 < 0.18^2) = .85;
f(x > 0.58 & x < 0.9 ...
  & y > 0.12 & y < 0.45) = 0.12;
fr = y > 0.6 & y < 0.9 ...
     & x > 0.08 & x < 0.48;
f(fr) = 0.5 + 0.4*cos(2*pi*16*x(fr));
r = hypot(x - 0.73, y - 0.75);
an = r < 0.16;
f(an) = 0.5 + 0.4*cos(2*pi*120*r(an).^2);
end
