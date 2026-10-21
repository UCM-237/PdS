% Hito 4: DFT 2D, desenfoque y cadena completa. Completa las partes marcadas con TODO.
iniciar();
y3 = cargar(3);
[FX, FY] = frecuencias_2d(size(y3));
h = figure('visible', 'off');
subplot(1, 2, 1); imagesc(FX(1, :), FY(:, 1), espectro_2d(y3, false)); axis image; title('sin ventana');
xlabel('f_x (ciclos/px)'); ylabel('f_y (ciclos/px)');
subplot(1, 2, 2); imagesc(FX(1, :), FY(:, 1), espectro_2d(y3, true)); axis image; title('con ventana');
xlabel('f_x (ciclos/px)');
guardar_figura(h, 'h4_espectro_imagen3.png');
% TODO: detecta los picos de la interferencia (por ejemplo, donde log|X| supera mucho a su
%       mediana local) y construye un filtro de muescas 2D. Ojo: espectro_2d está centrado
%       con fftshift y fft2 no.

% TODO: imagen desenfocada: perfil radial de log|Y|², radio del disco y deconvolución de
%       Wiener X = conj(H).*Y ./ (|H|² + K).

for n = 1:6
    restaurada = cargar(n);    % TODO: tu cadena
    guardar_restaurada(n, restaurada);
end
