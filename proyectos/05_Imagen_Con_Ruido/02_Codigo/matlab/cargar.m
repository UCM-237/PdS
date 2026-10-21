function img = cargar(n, limpia)
% imagen_n.png (o imagen_n_limpia.png con limpia = true, solo n = 1, 2, 3) en double entre 0 y 1.
if nargin < 2, limpia = false; end
if limpia
    nombre = sprintf('imagen_%d_limpia.png', n);
else
    nombre = sprintf('imagen_%d.png', n);
end
img = double(imread(fullfile('..', '..', '01_Datos', nombre))) / 255;
end
