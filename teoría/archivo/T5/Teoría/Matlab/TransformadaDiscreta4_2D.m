im=imread('estanteria.jpeg');
im=im(:,:,2)
figure;imshow(im,[]);
IM=fft2(im);
IM=fftshift(IM);AIM=abs(IM);
figure;imshow(AIM,[])
figure,imshow(log10(1+AIM.^2),[])