im=imread('moon.tif');
figure;imshow(im); 
figure;imhist(im); 
%Igualizacion de todos los bins
im2=histeq(im);
figure;imshow(im2);
figure;imhist(im2);
%Definicion de histograma
myhist=ones(1,256);
myhist(100:150)=10;
im3=histeq(im,myhist);
figure;imshow(im3);
figure;imhist(im3);
