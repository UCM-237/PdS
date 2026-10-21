delta=0.01;
[N,wc,beta,type]=kaiserord([0.4 0.55],[0 1],[delta,delta]);
window=kaiser(N+1,beta);
h=fir1(N,wc,type,window);
[hw,w]=freqz(h,1);
K=max(abs(hw));
plot(w/pi,abs(hw)/K);
xlabel('w/\pi'),ylabel('|H(exp(jw))|');
hold on,plot([0,1],10^(-40/20)*[1 1]);