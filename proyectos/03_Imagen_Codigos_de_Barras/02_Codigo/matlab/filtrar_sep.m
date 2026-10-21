function y = filtrar_sep(x, hf, hc)
% Filtro separable: hf (columna) en vertical y hc (fila) en horizontal, con bordes reflejados.
rf = floor(numel(hf) / 2); rc = floor(numel(hc) / 2);
y = conv2(hf(:), hc(:)', rellenar(x, rf, rc), 'valid');
y = y(1:size(x, 1), 1:size(x, 2));
end
