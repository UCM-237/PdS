function y = rellenar(x, rf, rc)
% Amplía la imagen rf filas y rc columnas por cada lado reflejando los bordes
% (como el modo 'reflect' de scipy.ndimage). Sin toolboxes.
[F, C] = size(x);
fi = [rf:-1:1, 1:F, F:-1:F-rf+1];
ci = [rc:-1:1, 1:C, C:-1:C-rc+1];
y = x(fi, ci);
end
