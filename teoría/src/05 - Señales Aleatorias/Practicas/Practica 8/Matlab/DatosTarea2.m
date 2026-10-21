function [x, patron, fs] = DatosTarea2()
% [X, PATRON, FS] = DatosTarea2()
% Devuelve una señal X que contiene un PATRON enmascarado por ruido.
% FS contiene el periodo de muestreo de la señal.
  c = 3*1e8;
  l = 905*1e-9;
  f = 100 * 1e6;
  T = 2/f;
  th = pi/6;
  dt = 1 / f / 100;
  t = [0:dt:T];
  ping = @(t) sin(2*pi*f*t) .* (0 < t & t < 1/f);
  patron = ping(t);
  n = 2*(rand(size(t)) - 0.5);
  x = ping(t - th/2/pi/f) + n;
  fs = 1/dt;
end
