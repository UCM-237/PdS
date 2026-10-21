clear all;
[num,den]=iircomb(20,0.09,'peak');

[hw,w]=freqz(num,den,0:0.001:2*pi);

plot(w/pi/2*300,abs(hw)),
ylabel('|H(exp(jw)|')
xlabel('w_c (Hz)')
