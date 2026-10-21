function e = bordes(p, u)
% Cruces del umbral con interpolación lineal (posiciones subpíxel, índice desde 1).
s = p(:) - u;
i = find(sign(s(1:end-1)) ~= sign(s(2:end)));
e = i + s(i) ./ (s(i) - s(i+1));
end
