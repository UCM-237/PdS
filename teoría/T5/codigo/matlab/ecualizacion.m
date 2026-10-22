f = imagen_prueba();
g = round(255*(0.35 + 0.3*f)); % 97..158
h = accumarray(g(:) + 1, 1, [256 1]);
F = cumsum(h)/numel(g);       % distribución
T = round(255*F);                % s = T(r)
ge = T(g + 1);
disp([min(g(:)) max(g(:))])      % 97 158
disp([min(ge(:)) max(ge(:))])    % 3 255
disp([std(g(:)) std(ge(:))])     % 16.7 73.3
% Con Image Processing Toolbox: histeq
