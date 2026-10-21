[N,wn]=ellipord(1,1.4,1,22,'s')
[num,den]=ellip(N,1,22,wn,'low','s');
w0=2*pi*1000*sqrt(24);
wdif=2*pi*25/7*1000
[num,den]=lp2bp(num,den,w0,wdif);
[hw,w]=freqs(num,den);
plot(w/2/pi,abs(hw),'r');hold on;
E=10^(1/20);
A=10^(22/20);
plot(w/2/pi,1/sqrt(2)*ones(length(w),1));
plot(w/2/pi,1/A*ones(length(w),1));
plot(w/2/pi,1/E*ones(length(w),1));
xlabel('F (Hz)');ylabel('|H(jw)|');