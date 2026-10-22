im=imread('football.jpg'); %Carga imagen
whos %ver el formato
figure;imshow(im);
figure;imshow(im(:,:,1)); 
figure;imshow(im(:,:,2)); 
figure;imshow(im(:,:,3)); 