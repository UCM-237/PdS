im=imread('estanteria.jpeg');
x=im(:,:,1)
h=fspecial('motion',10,45); %Movimiento
y1=filter2(h,x);
h=fspecial('sobel') %Borde horizontal
y2=filter2(h,x);
figure;imshow(x,[]);
figure;imshow(y1,[]);
figure;imshow(y2,[]);