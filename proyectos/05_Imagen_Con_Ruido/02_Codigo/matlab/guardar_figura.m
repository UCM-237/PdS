function guardar_figura(h, nombre)
% Guarda la figura en figuras/nombre y la cierra.
print(h, fullfile('figuras', nombre), '-dpng', '-r130');
close(h);
fprintf('figura: figuras/%s\n', nombre);
end
