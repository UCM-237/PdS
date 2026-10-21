% Hito 4: series, clasificación y entrega. Completa las partes marcadas con TODO.
iniciar();
% TODO: STFT de la velocidad de una sesión de series (ventana de Hann, fft por tramas),
%       bloque de series y periodo con la autocorrelación.
% TODO: estados parado / andando / corriendo y reglas para el tipo de sesión.
fich = {'prueba_1.csv', 'prueba_2.csv', 'prueba_3.csv'};
tipos = cell(1, 3); cambios = cell(1, 3);
for i = 1:3
    d = cargar_actividad(fich{i});
    tipos{i} = 'Rodaje'; cambios{i} = [];     % TODO: tu clasificación y tus cambios de ritmo
end
guardar_prueba(fich, tipos, cambios);
