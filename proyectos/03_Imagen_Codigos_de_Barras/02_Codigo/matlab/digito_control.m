function c = digito_control(d12)
% Dígito de control EAN-13 (carácter) de una cadena de 12 cifras.
s = sum((d12 - '0') .* repmat([1 3], 1, 6));
c = char('0' + mod(10 - mod(s, 10), 10));
end
