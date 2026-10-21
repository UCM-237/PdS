function p = picos_locales(x, dist)
% Máximos locales separados al menos dist muestras; si dos están más cerca, se queda el
% mayor (como scipy.signal.find_peaks con distance). Igual en Matlab y en Octave.
x = x(:);
c = find(x(2:end-1) > x(1:end-2) & x(2:end-1) >= x(3:end)) + 1;
[~, orden] = sort(x(c), 'descend');
quitar = false(size(c));
for i = orden'
    if quitar(i), continue; end
    cerca = abs(c - c(i)) < dist;
    cerca(i) = false;
    quitar = quitar | cerca;
end
p = c(~quitar);
end
