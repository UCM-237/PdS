function m = modulos(codigo)
% Vector de 95 módulos (1 = barra) del código EAN-13 'codigo' (cadena de 13 cifras).
L = {'0001101','0011001','0010011','0111101','0100011','0110001','0101111','0111011','0110111','0001011'};
R = {'1110010','1100110','1101100','1000010','1011100','1001110','1010000','1000100','1001000','1110100'};
paridad = {'LLLLLL','LLGLGG','LLGGLG','LLGGGL','LGLLGG','LGGLLG','LGGGLL','LGLGLG','LGLGGL','LGGLGL'};
par = paridad{codigo(1) - '0' + 1};
s = '101';
for j = 1:6
    d = codigo(j + 1) - '0' + 1;
    if par(j) == 'L', s = [s, L{d}]; else, s = [s, fliplr(R{d})]; end
end
s = [s, '01010'];
for j = 8:13, s = [s, R{codigo(j) - '0' + 1}]; end
s = [s, '101'];
m = s - '0';
end
