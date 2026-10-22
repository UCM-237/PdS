im=imread('estanteria.jpeg');
x=im(:,:,1)
h=1/10^2*ones(10,10); %FIR paso baja
y1=filter2(h,x);
h=-ones(3,3);h(2,2)=8 %FIR Laplaciana
y2=filter2(h,x);
figure;imshow(x,[]);
figure;imshow(y1,[]);
figure;imshow(y2,[]);