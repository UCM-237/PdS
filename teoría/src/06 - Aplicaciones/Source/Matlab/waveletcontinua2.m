%Signal
Ts=1;Fs=1/Ts;
t=0:Ts:1000;
T1=5;T2=20;
y=sin(2*pi/T1*t)+sin(2*pi/T2*t);
sig.x=t;
sig.y=y;
figure;stairs(t,y);
xlabel('t(seg)');ylabel('y(Amp)');
%Espectograma
figure;spectrogram(y,128,120,[],Fs,'yaxis');
%Daubechies 1 == Haar
type='db1';
[phi,psi,t]=wavefun(type,10);
figure;plot(t,psi);
xlabel('t(seg)');ylabel('\psi(t)');
figure;c=cwt(sig,[1:4,5:5:25],type,'absglb');


