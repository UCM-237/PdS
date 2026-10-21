function [P, paridad] = ean13_tablas()
% Patrones de rachas (4 anchos en módulos) de cada dígito en los juegos L, G y R.
% P es 3 x 10 x 4 con el orden L, G, R. paridad{d+1} es la paridad del dígito inicial d.
L = {'0001101','0011001','0010011','0111101','0100011','0110001','0101111','0111011','0110111','0001011'};
R = {'1110010','1100110','1101100','1000010','1011100','1001110','1010000','1000100','1001000','1110100'};
P = zeros(3, 10, 4);
for d = 1:10
    P(1, d, :) = rachas(L{d});
    P(2, d, :) = rachas(fliplr(R{d}));
    P(3, d, :) = rachas(R{d});
end
paridad = {'LLLLLL','LLGLGG','LLGGLG','LLGGGL','LGLLGG','LGGLLG','LGGGLL','LGLGLG','LGLGGL','LGGLGL'};
end

function r = rachas(s)
r = diff([0, find(s(1:end-1) ~= s(2:end)), numel(s)]);
end
