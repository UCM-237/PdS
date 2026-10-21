function guardar_restaurada(n, img)
% Escribe restaurada_n.png (8 bits) en la carpeta actual.
imwrite(uint8(round(min(max(img, 0), 1) * 255)), sprintf('restaurada_%d.png', n));
end
