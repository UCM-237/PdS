function guardar_lecturas(lecturas)
% lecturas: celda de 6 cadenas (vacía si no se lee). Escribe lecturas.csv.
fid = fopen('lecturas.csv', 'w');
fprintf(fid, 'imagen,codigo\n');
for i = 1:numel(lecturas), fprintf(fid, 'codigo_%d.png,%s\n', i, lecturas{i}); end
fclose(fid);
end
