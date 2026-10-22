wp=[2*pi*1000,2*pi*7000];
ws=[2*pi*2000,2*pi*6000];
[N,wn]=cheb1ord(wp,ws,0.5,20,'s')
[num,den]=cheby1(N,0.5,wn,'stop','s');
[hw,w]=freqs(num,den);
plot(w/2/pi,abs(hw),'r');hold on;
E=10^(0.5/20);A=10^(20/20);
plot(w/2/pi,1/sqrt(2)*ones(length(w),1));
plot(w/2/pi,1/A*ones(length(w),1));
plot(w/2/pi,1/E*ones(length(w),1));
xlabel('F (Hz)');ylabel('|H(jw)|');