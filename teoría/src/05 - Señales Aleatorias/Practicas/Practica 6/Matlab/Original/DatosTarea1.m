function [varargout] = DatosTarea1(dni, caso)
% [a,b,c,...] = DatosTarea1(dni, caso)
%
% dni: dni del alumno (sin letra: por ejemplo '12345678')
% caso: caso del ejercicio (numero entre 1-5)
% a,b,c ...: parametros propios de cada funci�n
%
% Llamar a la funci�n siempre con los dos par�metros de entrada y con tantos 
% parametros de salida como sean necesarios, ordenados alfabeticamente. 
%
% Por ejemplo, para el caso 2: [a,b,c,d,e,f] = DatosTarea1('12345678', 2)
switch(caso)
  case 1
    a = 3;
    b = a + 3 + mod(str2num(dni(5)), 3);
    for i=1:b-a+1
      v(i) = str2num(dni(i));
    end
    varargout{1} = v / sum(v);
  case 2,
    a = 3 + 4*mod(str2num(dni(7)), 3);
    varargout{1} = a;
  case 3,
    lambda = 1 + (7/3)*mod(str2num(dni(6)), 4);
    varargout{1} = lambda;
  case 4,
    a = (1 + str2num(dni(4))) / 12;
    b = 1 - a;
    c = mod(dni(end-1), 4);
    d = a + 3*(1 + mod(str2num(dni(4)), 4));
    e = (1 + str2num(dni(2))/4) ^ 2;
    varargout{1} = a;
    varargout{2} = b;
    varargout{3} = c;
    varargout{4} = d;
    varargout{5} = e;
  case 5,
    b = (1 + str2num(dni(6))) / 12;
    a = 1 - b;
    c = mod(dni(end-1), 4);
    d = a + 3*(1 + mod(str2num(dni(4)), 4));
    e = (1 + str2num(dni(2))/4) ^ 2;
    f = e + (1 + str2num(dni(4))/4) ^ 2;
    varargout{1} = a;
    varargout{2} = b;
    varargout{3} = c;
    varargout{4} = d;
    varargout{5} = e;
    varargout{6} = f;
  case 666,
    display('Los zombies de 28 días no son zombies, son infectados.');
  otherwise,
    error('Opcion no valida');
end