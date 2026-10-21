function data = DatosTarea3(dnis, caso)
%data = DatosTarea3(dni,caso)
%
% dni:  dni del alumno (sin letra, numero: 123456)
% caso: caso del ejercicio (numero entre 1-4)
% data: vector con las muestradas generadas
%
% Llamar a la función siempre con los dos parámetros de entrada y con tantos 
% parametros de salida como sean necesarios, ordenados alfabeticamente. 
%
% Por ejemplo, para el caso 2: data = DatosTarea3('12345', 2)

ldni = length(dnis);
N = 10000;
index = mod(str2num(dnis(end-2)), 4);
switch(caso)
    case 1
        a = -2*(1 + index);
        b = a - (3*a/2);
        data = a + (b-a)*rand(N, 1);
    case 2,
        c = 2^(index + 1);
        data = randi(c, N, 1);
    case 3,
        m = index;
        c = (m+1) / 4;
        data1 = -(2+m) + m*randn(N/4,1);
        data2 = 4 + m + c*2*randn(3*N/4,1);
        data = [data1; data2];
        data = data(:);
        p = randperm(N);
        data = data(p);
     case 4,
        signo= mod(str2num(dnis(end-2)),2);
        m = 2 + index;
        
        if signo
            m = -m;
        end
        c = 3;
        data = m + c*randn(N,1); 
    otherwise,
        error('Opcion no valida');
end



