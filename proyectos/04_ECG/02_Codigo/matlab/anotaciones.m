function [muestra, tipo] = anotaciones(nombre)
% Lee las anotaciones: muestra del pico R (índice desde 1, ya convertido) y tipo ('N' o 'V').
if nargin < 1, nombre = 'ecg_A_anotaciones.csv'; end
fid = fopen(fullfile('..', '..', '01_Datos', nombre)); fgetl(fid);
c = textscan(fid, '%f %f %s', 'Delimiter', ',');
fclose(fid);
muestra = c{2} + 1; tipo = char(c{3});
end
