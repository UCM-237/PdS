function [t, x] = cargar(nombre)
% Lee un registro de 01_Datos: t (s) y x (mV) como vectores columna.
d = dlmread(fullfile('..', '..', '01_Datos', nombre), ',', 1, 0);
t = d(:, 1); x = d(:, 2);
end
