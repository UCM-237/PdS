N=10000;
y = rand(2,N);
r = sqrt(-2*log(y(1,:)));
theta = 2*pi*y(2,:);
x1 = r.*cos(theta); %x1 normal 
x2 = r.*sin(theta); %x2 normal 
%Sirve para generar una 
%bidimensional (x1,x2) o 
%complejo z=x1+jx2 