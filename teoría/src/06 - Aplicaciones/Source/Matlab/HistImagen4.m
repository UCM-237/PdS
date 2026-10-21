im=imread('moon.tif');
figure;imshow(im); 
figure;imhist(im); 
%Binarizacion segun el histograma
im2=double(im>50);
figure;imshow(im2); 

