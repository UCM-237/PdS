m=1:100; %Indice de filas
n=1:100; %Indice de columnas
[mm,nn]=meshgrid(m,n); 
F=1/3;ang=30*pi/180;
Fm=F*cos(ang); Fn=F*sin(ang);
im=sin(2*pi*(Fm*mm+Fn*nn));
F=1/10;ang=60*pi/180;
Fm=F*cos(ang); Fn=F*sin(ang);
im=im+sin(2*pi*(Fm*mm+Fn*nn));
imshow(im,[]);
IM=fft2(im);AIM=abs(IM);
imshow(AIM,[])
cm=colormap('jet');
imshow(255*AIM/max(AIM(:)),cm)

