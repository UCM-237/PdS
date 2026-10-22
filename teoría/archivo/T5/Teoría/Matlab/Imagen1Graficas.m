im=imread('moon.tif'); %Carga imagen
whos %Ver el formato
figure,imshow(im);print -depsc Moon1 %Dibuja imagen
im2=double(im); %Convierte el uint8 en double
figure,imshow(im2);print -depsc Moon2 %Como es double, representa valores 
             %entre 0 y 1, truncando el resto
figure,imshow(im2,[]);print -depsc Moon3 %Representa entre el maximo y minimo