load train;x=y;
h=1/4*[1 1 1 1]; %FIR paso baja
[H,w]=freqz(h,1);AH=abs(H); 
plot(w/pi,AH/max(AH));
xlabel('w/\pi');ylabel('|H(w)|');
y=filter(h,1,x);
X=fft(x);X=fftshift(X);
Y=fft(y);Y=fftshift(Y);
N=length(X); w=2*pi*(0:N-1)/N-pi;
AX=abs(X); AY=abs(Y);
plot(w/pi,AX,w/pi,AY);
xlabel('w/\pi');
legend('|X(w)|', '|Y(w)|');