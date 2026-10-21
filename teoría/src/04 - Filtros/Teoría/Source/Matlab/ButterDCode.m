[N,wn]=buttord([0.45,0.65],[0.3,0.75],1,40)
[numz,denz]=butter(N,wn);
[hw,w]=freqz(numz,denz);
plot(w/pi,abs(hw),'r');hold on;
E=10^(1/20);
A=10^(40/20);
plot(w/pi,1/sqrt(2)*ones(length(w),1));
plot(w/pi,1/A*ones(length(w),1));
plot(w/pi,1/E*ones(length(w),1));
xlabel('w/\pi');ylabel('|H(exp(jw))|');