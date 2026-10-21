clear all;
L=5;
num=0.4*[1,-1];
den=[1,0.2];
numL([0:length(num)-1]*L+1)=num;
denL([0:length(den)-1]*L+1)=den;


[hw,w]=freqz(num,den,0:0.01:2*pi);
[hwL,wL]=freqz(numL,denL,0:0.01:2*pi);

