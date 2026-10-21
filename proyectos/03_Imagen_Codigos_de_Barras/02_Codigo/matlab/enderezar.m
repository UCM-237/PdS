function y = enderezar(img, ang)
% Gira la imagen -ang grados (el código queda horizontal) con interpolación bicúbica,
% ampliando el lienzo y rellenando con la mediana. Sin toolboxes.
[F, C] = size(img);
t = ang * pi / 180;
Fo = ceil(abs(F*cos(t)) + abs(C*sin(t))); Co = ceil(abs(C*cos(t)) + abs(F*sin(t)));
[xo, yo] = meshgrid((1:Co) - (Co+1)/2, (1:Fo) - (Fo+1)/2);
% coordenadas en la imagen original del píxel de salida (giro inverso)
xi = xo*cos(t) - yo*sin(t) + (C+1)/2;
yi = xo*sin(t) + yo*cos(t) + (F+1)/2;
y = interp2(img, xi, yi, 'cubic');
y(isnan(y)) = median(img(:));
end
