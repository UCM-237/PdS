function d = cargar_actividad(nombre)
% Estructura con t (s), distancia (m), fc (ppm), vel (m/s), alt (m) y v (km/h), en columna.
% 'nombre' es una fecha ('2026-01-07') o un fichero de sinteticas ('desarrollo_01.csv').
if numel(nombre) > 4 && strcmp(nombre(end-3:end), '.csv')
    ruta = fullfile('..', '..', '01_Datos', 'sinteticas', nombre);
else
    ruta = fullfile('..', '..', '01_Datos', ['actividad_' nombre '.csv']);
end
m = dlmread(ruta, ',', 1, 0);
d.t = m(:, 2); d.distancia = m(:, 3); d.fc = m(:, 4); d.vel = m(:, 5); d.alt = m(:, 6);
d.v = d.vel * 3.6;
end
