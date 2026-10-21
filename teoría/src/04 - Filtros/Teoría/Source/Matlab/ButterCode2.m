[N,wn]=buttord(2*pi*4000,2*pi*1000,0.1,40,'s')
[num,den]=butter(N,wn,'high','s');
[hw,w]=freqs(num,den);
plot(w/2/pi,abs(hw),'r');hold on;
E=10^(0.1/20);A=10^(40/20);
plot(w/2/pi,1/sqrt(2)*ones(length(w),1));
plot(w/2/pi,1/A*ones(length(w),1));
plot(w/2/pi,1/E*ones(length(w),1));
xlabel('F (Hz)');ylabel('|H(jw)|');