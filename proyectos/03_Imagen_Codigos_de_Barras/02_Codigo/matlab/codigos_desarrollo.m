function c = codigos_desarrollo()
% Celda con los códigos de las imágenes 1, 2 y 3.
fid = fopen(fullfile('..', '..', '01_Datos', 'codigos_desarrollo.csv')); fgetl(fid);
d = textscan(fid, '%s %s', 'Delimiter', ',');
fclose(fid);
c = d{2};
end
