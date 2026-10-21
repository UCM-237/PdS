function img = cargar(i)
% Imagen codigo_i.png de 01_Datos en double, entre 0 y 1.
img = double(imread(fullfile('..', '..', '01_Datos', sprintf('codigo_%d.png', i)))) / 255;
end
