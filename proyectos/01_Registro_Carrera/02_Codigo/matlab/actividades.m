function f = actividades()
% Fechas de las actividades reales.
l = dir(fullfile('..', '..', '01_Datos', 'actividad_*.csv'));
f = sort(cellfun(@(s) s(11:20), {l.name}, 'UniformOutput', false));
end
