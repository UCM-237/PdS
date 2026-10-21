T=1;t=0:T:100;
type='db1';

y = 1-abs((t-50)/50);
sig.x=t;sig.y=y; %Crear estructura signal
figure;stairs(t,y);
xlabel('t(seg)');ylabel('y(Amp)');

[phi,psi,t]=wavefun(type,10);
figure;plot(t,psi);
xlabel('t(seg)');ylabel('\psi(t)');

figure;c= cwt(sig,1:32,type,'absglb');
figure;c = cwt(sig,1:32,type,'3Dglb');
