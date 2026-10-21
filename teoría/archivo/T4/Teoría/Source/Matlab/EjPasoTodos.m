den=[1,0.4,0.18,-0.3];
num=den(end:-1:1);

figure(1)
zplane(num,den),
[hw,w]=freqz(num,den)
figure(2)
subplot(2,1,1)

plot(w/pi,abs(hw)),
ylabel('|H(exp(jw)|')
subplot(2,1,2)
plot(w/pi,unwrap(angle(hw)))
ylabel('arg(H(exp(jw))')
xlabel('w/pi')
