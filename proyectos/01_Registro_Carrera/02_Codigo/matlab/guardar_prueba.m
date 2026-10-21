function guardar_prueba(ficheros, tipos, cambios)
% Escribe prueba.csv: una fila por sesión con su tipo y sus instantes de cambio (s).
fid = fopen('prueba.csv', 'w');
fprintf(fid, 'sesion,tipo,cambios_s\n');
for i = 1:numel(ficheros)
    fprintf(fid, '%s,%s,%s\n', ficheros{i}, tipos{i}, strtrim(sprintf('%.0f ', cambios{i})));
end
fclose(fid);
end
