% Hito 1: la fila como señal. Completa las partes marcadas con TODO.
iniciar();
h = figure;
for i = 1:6
    subplot(2, 3, i); imagesc(cargar(i), [0 1]); colormap gray; axis image off;
    title(sprintf('codigo\\_%d.png', i));
end
guardar_figura(h, 'h1_imagenes.png');

img = cargar(1);
fila = round(size(img, 1) / 2);     % TODO: elige una fila que cruce el código
p = img(fila, :)';
h = figure; plot(p); grid on; xlabel('columna (px)'); ylabel('nivel'); title(sprintf('Fila %d', fila));
guardar_figura(h, 'h1_fila.png');

cods = codigos_desarrollo();
ideal = modulos(cods{1});            % 1 = barra (oscura), 95 módulos
fprintf('código %s: %d módulos\n', cods{1}, numel(ideal));
% TODO: localiza el primer y el último borde del código en p y calcula m = anchura / 95.
% TODO: dibuja la señal ideal escalada a m píxeles por módulo sobre la fila muestreada.
% TODO: espectro de la fila (con ventana y relleno de ceros) y envolvente sinc^2(f m).
% TODO: repite la medida del módulo en la imagen 6 y compara las anchuras de las rachas.
