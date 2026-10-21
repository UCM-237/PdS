wp=2*pi*[4000,7000];ws=2*pi*[3000,8000];
[N,wn]=ellipord(wp,ws,1,22,'s')
[num,den]=ellip(N,1,22,wn,'s');
[hw,w]=freqs(num,den);
plot(w/2/pi,abs(hw),'r');hold on;
E=10^(1/20);A=10^(22/20);
plot(w/2/pi,1/sqrt(2)*ones(length(w),1));
plot(w/2/pi,1/A*ones(length(w),1));
plot(w/2/pi,1/E*ones(length(w),1));
xlabel('F (Hz)');ylabel('|H(jw)|');