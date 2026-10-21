im=imread('moon.tif'); %Carga imagen
whos %Ver el formato
imshow(im); %Dibuja imagen
im2=double(im); %Convierte el uint8 en double
imshow(im2); %Como es double, representa valores 
             %entre 0 y 1, truncando el resto
imshow(im2,[]); %Representa entre el maximo y minimo