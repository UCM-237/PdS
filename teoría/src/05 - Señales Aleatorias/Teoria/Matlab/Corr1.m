Ts=0.01;t=0:Ts:10;
x=sinc(t-2);y=sinc(t-3); %Cambiar señales
subplot(2,1,1);plot(t,x,'r',t,y,'b');
xlabel('t (s)');ylabel('x(t)');
[yxc,lags]=xcorr(y,x,200,'unbias');
subplot(2,1,2);plot(lags*Ts,xyc);
xlabel('\tau (s)');ylabel('\phi_{yx}(\tau)');