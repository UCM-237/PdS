Fs=100;Ts=1/Fs;N=500;f1=10;f2=30;
k=0:N-1;
td=k*Ts; %Instantes de muestreo
%Señal muestreada
xd=sin(2*pi*f1*td)+sin(2*pi*f2*td);
%FFT
Xd=fft(xd);
%Representaciones
wd=2*pi*k/N; %frecuencia discreta (rad/s)
wc=wd/Ts; %frecuencia continua (rad/s)
fc=wc/2/pi %Frecuencia continua en Hz
figure,plot(k,abs(Xd)); %Respecto a k
ylabel('|X(k)|');xlabel('k');
figure,plot(wd,abs(Xd)); %Aprox DTFT respecto a la w_d
ylabel('|X(e^{jw_d})|');xlabel('w_d (rad/s)');
figure,plot(fc,abs(Xd)); %Aprox CTFT respecto a f_c
ylabel('|X(j f_c)|');xlabel('f_c  (Hz)');
