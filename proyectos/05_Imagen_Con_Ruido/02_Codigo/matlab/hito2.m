% Hito 2: filtros 1D aplicados por filas y columnas. Completa las partes marcadas con TODO.
iniciar();
y1 = cargar(1); x1 = cargar(1, true);
k = ones(1, 3) / 3;
r = filtrar_sep(y1, k, k);   % filtrar_sep(x, h_vertical, h_horizontal)
fprintf('media 3x3: PSNR = %.2f dB, SSIM = %.3f\n', psnr_db(r, x1), ssim_medio(r, x1));
% TODO: gaussianos de varias σ y un FIR de 15 coeficientes por enventanado (barre fc).
% TODO: respuesta en frecuencia 2D de cada núcleo: |H(fx)|·|H(fy)| con fft(h, 256).

y2 = cargar(2); x2 = cargar(2, true);
% TODO: mediana 3x3 y 5x5 (sin toolbox: apila los k² vecinos desplazados y usa median),
%       y compárala con la media del mismo tamaño.

y3 = cargar(3);
% TODO: muesca IIR de 2.º orden en la frecuencia del pico del H1, aplicada fila a fila con
%       fase cero: filter hacia delante y hacia atrás (o filtfilt si tienes el paquete signal).
