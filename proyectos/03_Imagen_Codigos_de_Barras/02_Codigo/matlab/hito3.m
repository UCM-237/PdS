% Hito 3: ruido, umbral y lectura. Completa las partes marcadas con TODO.
iniciar();
img = cargar(1);
p = img(round(size(img, 1) / 2), :)';  % TODO: promedia N filas de la zona del código
u = 0.5;                                % TODO: umbral de Otsu u otro justificado
e = bordes(p, u);
fprintf('%d cruces del umbral\n', numel(e));
% TODO: quédate con los 60 bordes del código y calcula las 59 anchuras (diff).
% TODO: escribe decodificar.m: separa las guardas, normaliza cada grupo de 4 rachas a 7
%       módulos, busca el patrón más cercano con ean13_tablas, obtén el primer dígito por la
%       paridad y comprueba el dígito de control con digito_control.
% TODO: estadística del ruido en una zona blanca, varianza frente a N y tasa de lectura
%       frente a sigma del ruido añadido.
