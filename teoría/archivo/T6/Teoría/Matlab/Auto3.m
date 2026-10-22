Ts=0.01;t=0:Ts:10;
x=sin(2*pi*F*t);%Señal (modificar)
subplot(2,1,1);plot(t,x);
xlabel('t (s)');ylabel('x(t)');
[xc,lags]=xcorr(x,100,'unbias');
subplot(2,1,2);plot(lags*Ts,xc);
xlabel('\tau (s)');ylabel('\phi_{xx}(\tau)');