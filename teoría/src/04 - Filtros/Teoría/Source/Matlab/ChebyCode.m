[N,wn]=cheb2ord(0.44,1,2,30,'s')
[num,den]=cheby2(N,30,wn,'low','s');
w0=2*pi*1000*sqrt(28);
wdif=2*pi*8/6*1000
[num,den]=lp2bs(num,den,w0,wdif);
[hw,w]=freqs(num,den);
plot(w/2/pi,abs(hw),'r');hold on;
E=10^(2/20);
A=10^(30/20);
plot(w/2/pi,1/sqrt(2)*ones(length(w),1));
plot(w/2/pi,1/A*ones(length(w),1));
plot(w/2/pi,1/E*ones(length(w),1));
xlabel('F (Hz)');ylabel('|H(jw)|');