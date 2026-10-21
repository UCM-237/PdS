function [x, fs] = cargar(nombre)
% Lee un fichero de 01_Datos como vector columna en [-1, 1).
if nargin < 1, nombre = 'audio_ruidoso.wav'; end
[x, fs] = audioread(fullfile('..', '..', '01_Datos', nombre));
x = x(:);
end
