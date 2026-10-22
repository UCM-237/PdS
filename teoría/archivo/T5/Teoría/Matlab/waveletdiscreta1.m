T=1;t=0:T:100;
y = 1-abs((t-50)/50);
sig.x=t;sig.y=y;
subplot(4,1,1), plot(t,y);
title('Señal analizada');
subplot(4,1,2),
dwtplot(y,5,'db1');
subplot(4,1,3),
cwt(sig,2.^[1:5],'db1','absglb');
subplot(4,1,4),
cwt(sig,1:32,'db1','absglb');
