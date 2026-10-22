x=imread('moon.tif');
h=1/4^2*ones(4,4); %FIR paso baja
[H,u,v]=freqz2(h);AH=abs(H); 
figure;imshow(AH,[]);
[uu,vv]=meshgrid(u,v);
figure;mesh(uu,vv,AH/max(AH(:)));
xlabel('u');ylabel('v');zlabel('|H(w)|');
y=filter2(h,x);
X=fft2(x);X=fftshift(X);AX=log10(1+(abs(X)).^2);
Y=fft2(y);Y=fftshift(Y);AY=log10(1+(abs(Y)).^2);
figure;imshow(x,[]);figure;imshow(y,[]);
figure;imshow(AX,[]);figure;imshow(AY,[]);
