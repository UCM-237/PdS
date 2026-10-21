im=imread('football.jpg'); %Carga imagenes
whos %ver el formato
figure;imshow(im); print -depsc Foot
figure;imshow(im(:,:,1)); print -depsc FootR
figure;imshow(im(:,:,2)); print -depsc FootG
figure;imshow(im(:,:,3)); print -depsc FootB