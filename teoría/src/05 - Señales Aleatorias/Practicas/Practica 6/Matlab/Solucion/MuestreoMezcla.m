function [x,aux]=MuestreoMezcla(N)

q_i=[0.4,0.2,0.4];
qsum=cumsum(q_i);
for i=1:N
    %Muestreo ruleta
    index=sum(rand>qsum)+1;
    aux(i)=index;
    switch index
        case 1,
           %gaussiana
           x(i)=3+0.5*randn; 
        case 2,
           %uniforme
           x(i)=4+2*rand;
        case 3,
          %Delta centrada en 7
           x(i)=7; 
    end
end






