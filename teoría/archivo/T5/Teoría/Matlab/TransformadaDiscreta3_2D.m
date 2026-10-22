m=1:100; %Indice de filas
n=1:100; %Indice de columnas
[mm,nn]=meshgrid(m,n); 
for angle=[0,45,90]
F=1/3;ang=angle*pi/180;
Fm=F*cos(ang);Fn=F*sin(ang);
im=sin(2*pi*(Fm*mm+Fn*nn));
figure;imshow(im,[]);
IM=fft2(im);
IM=fftshift(IM);AIM=abs(IM);
figure;imshow(AIM,[])
end