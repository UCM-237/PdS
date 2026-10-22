N=10000; %10000 muestras
samples=randn(N,1); 
hist(samples,50); %Histograma con 50 bins
xlabel('x');ylabel('hist(x)');
%Normalizar histograma
[h,xbin]=hist(samples,50);
inc=xbin(2)-xbin(1);hnormal=h/N/inc;
bar(xbin,hnormal,1)
%Pintar la probabilidad encima
mu=0;sigma=1;x=-10:0.01:10;
prob=1/sqrt(2*pi*sigma)*exp(-(x-mu).^2/2/sigma^2);
hold on;plot(x,prob,'r');
xlabel('x');ylabel('prob(x)');
