% Hito 1: la imagen como señal. Completa las partes marcadas con TODO.
iniciar();
h = figure('visible', 'off');
for n = 1:6
    subplot(2, 3, n); imagesc(cargar(n), [0 1]); colormap(gray); axis image off;
    title(sprintf('imagen\\_%d.png', n));
end
guardar_figura(h, 'h1_imagenes.png');

x = cargar(1, true);
for b = 1:7
    xq = x;          % TODO: cuantifica x con b bits (2^b niveles entre 0 y 1)
    fprintf('%d bits: PSNR = %.2f dB\n', b, psnr_db(xq, x));
end
% TODO: representa la PSNR frente a b junto con el modelo Δ²/12.

z = placa_zonal(512);
% TODO: diezma z y la imagen 2 limpia por 4 (z(1:4:end, 1:4:end)) sin filtrar y con un paso bajo previo.

% TODO: periodograma medio de las filas: resta la media de cada fila, multiplica por una
%       ventana de Hann, fft por filas (fft(x, [], 2)), |X|² promediado sobre las filas.
