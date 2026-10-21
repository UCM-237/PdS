% Hito 4: orientación, desenfoque y lectura de las seis imágenes. Completa las partes TODO.
iniciar();
lecturas = cell(1, 6);
for i = 1:6
    img = cargar(i);
    ang = 0;   % TODO: ángulo del código con la energía de la DFT 2D por direcciones
    rec = enderezar(img, ang);
    % TODO: iluminación, localización, perfil, umbral, deconvolución de Wiener si hace falta
    %       (X = conj(H) Y / (|H|^2 + 1/SNR)) y lectura
    lecturas{i} = '';
end
guardar_lecturas(lecturas);
disp(lecturas);
