x=1:100; %Indice de filas
y=1:100; %Indice de columnas
[xx,yy]=meshgrid(x,y); %Matrices de enrejado
F=1/8;angulo=0;
Fx=F*cos(angulo); Fy=F*sin(angulo);
im=0.5*sin(2*pi*(Fx*xx+Fy*yy))+0.5; %Imagen
figure;imshow(im);
im2=im+rand(100,100); %Sumamos ruido
imshow(im2,[]);