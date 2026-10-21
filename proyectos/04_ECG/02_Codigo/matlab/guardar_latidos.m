function guardar_latidos(nombre, r, tipos)
% Escribe el fichero de entrega: muestra (desde 0, como las anotaciones) y tipo.
fid = fopen(nombre, 'w');
fprintf(fid, 'muestra,tipo\n');
for i = 1:numel(r), fprintf(fid, '%d,%s\n', r(i) - 1, tipos(i)); end
fclose(fid);
end
