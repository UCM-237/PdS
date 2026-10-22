f = imagen_prueba();
sx = [1 0 -1;
      2 0 -2;
      1 0 -1];                   % d/dn
media = ones(5)/25;
gx = conv2(f, sx, 'same');
gy = conv2(f, sx', 'same');
g = hypot(gx, gy);             % |gradiente|
fs = conv2(f, media, 'same');
bordes = g > 0.5;
disp(mean(bordes(:)))            % 0.18
disp(f(81, 11:20))               % degradado
disp(gx(81, 11:20))             % 8*0.25/256
