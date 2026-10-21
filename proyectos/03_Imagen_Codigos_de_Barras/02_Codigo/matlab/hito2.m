% Hito 2: iluminación y filtrado 2D. Completa las partes marcadas con TODO.
iniciar();
img = cargar(4);
% TODO: estima la iluminación (por ejemplo, máximo local con movmax en filas y columnas
%       seguido de gauss) y divide. Compara con restar un paso bajo.
ilum = gauss(img, 25);               % provisional: paso bajo lineal
h = figure;
subplot(1, 3, 1); imagesc(img); axis image off; title('original');
subplot(1, 3, 2); imagesc(ilum); axis image off; title('iluminación estimada');
subplot(1, 3, 3); imagesc(img ./ ilum); axis image off; title('cociente'); colormap gray;
guardar_figura(h, 'h2_iluminacion.png');

img2 = enderezar(cargar(2), 6.0);   % TODO: usa el ángulo que midas tú (H4)
% TODO: recorta la zona del código y compara filtros de media 5x5, 15x1 y 1x5
%       (filtrar_sep(x, ones(1, nf)/nf, ones(1, nc)/nc)); ¿con cuáles se lee una sola fila?
% TODO: respuesta en frecuencia 2D de cada núcleo (fft2 con relleno de ceros y fftshift).
