function [varargout] = DatosTarea1(dnis,caso)
%[a,b,c,...] = DatosTarea1(dni,caso)
%
% dni:  dni del alumno (sin letra, numero: por ejemplo 123456)
% caso: caso del ejercicio (numero entre 1-6)
% a,b,c ...: parametros propios de cada función
%
% Llamar a la función siempre con los dos parámetros de entrada y con tantos 
% parametros de salida como sean necesarios, ordenados alfabeticamente. 
%
% Por ejemplo, para el caso 2: [a,b,c,d,e] = DatosTarea1(12345,2)


ldni = length(dnis);
switch(caso)
    case 1
        varargout{1} = mod(str2num(dnis(end-2)), 4) + 3;
    case 2,
        aux = [0.1 0.3 0.2 0.4];
        index = mod(str2num(dnis(end)), 4) + 1;
        aux = [aux(index:end), aux(1:index-1)];
        varargout = mat2cell(aux, 1, [1 1 1 1]);
    case 3,
        a = mod(str2num(dnis(end-2)), 4);
        b = 2*(1+a);
        varargout{1} = -a;
        varargout{2} = b;
    case 4,  
        a = mod(str2num(dnis(end-2)), 4);
        varargout{1} = (a+2)*3;
        varargout{2} = (5-a)^2;
    case 5,
        a = mod(str2num(dnis(end-2)), 4) + 1;
        varargout{1} = a;
    case 6,
        a = mod(str2num(dnis(end-2)), 4)+1;     
        b = (a - 2)*2;
        c = a^2;
        d = (5 - a);

        p1 = (a)/10;
        p2 = 1-p1;    
        varargout{1} = p1;      
        varargout{2} = p2;
        varargout{3} = b;
        varargout{4} = c;
        varargout{5} = d;
        varargout{6} = d + 3;
    otherwise,
        error('Opcion no valida');
end