%Close all:
close all
x=0:0.01:20;
m=1;c=0.5
%plot(x,1/sqrt(2*pi*c^2)./x .* exp(-(log(x)-m).^2/2/c^2))
hold on,plot(x,lognpdf(x,m,c))
hold on,plot(x,4.5*normpdf(x,m/2,c*10))

figure
N=10000;
samples=MuestreoRechazo(N,m,c);
[h,l]=hist(samples,50);
bar(l,h/N/(l(2)-l(1)),1)
hold on,plot(x,lognpdf(x,m,c))
