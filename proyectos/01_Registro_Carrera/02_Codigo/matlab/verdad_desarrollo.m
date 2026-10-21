function [ficheros, tipos, sigmas, cambios] = verdad_desarrollo()
% Tipo, σ de la velocidad (km/h) e instantes de cambio (s) de las sintéticas de desarrollo.
fid = fopen(fullfile('..', '..', '01_Datos', 'sinteticas', 'desarrollo_verdad.csv')); fgetl(fid);
ficheros = {}; tipos = {}; sigmas = []; cambios = {};
while true
    l = fgetl(fid); if ~ischar(l), break; end
    p = strsplit(l, ',');
    ficheros{end+1} = p{1}; tipos{end+1} = p{2}; sigmas(end+1) = str2double(p{3});
    cambios{end+1} = str2num(p{4});
end
fclose(fid);
end
