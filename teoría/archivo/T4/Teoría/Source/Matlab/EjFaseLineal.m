a=-0.5;
b=0.3+0.5i;
c=0.5+sqrt(3)/2i;

polos=[a,1/a,b,b',1/b,1/b',c,c']
hn=poly(polos)
figure(1)
zplane(hn,1)
[hw,w]=freqz(hn)
figure(2)
subplot(2,1,1)
plot(w/pi,abs(hw)),
ylabel('|H(exp(jw)|')
subplot(2,1,2)
plot(w/pi,unwrap(angle(hw))),
ylabel('arg(H(exp(jw))')
xlabel('w/pi')

