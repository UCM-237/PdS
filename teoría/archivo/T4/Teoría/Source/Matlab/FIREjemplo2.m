L=23;wc=0.4*pi
n=-L:L;
h=sin(wc*n)./n/pi;
h(L+1)=wc/pi;
window=chebwin(2*L+1,40);
h=h.*window';
[hw,w]=freqz(h,1);
K=max(abs(hw));
plot(w/pi,abs(hw)/K);
xlabel('w/\pi'),ylabel('|H(exp(jw))|');
hold on,plot([0,1],10^(-40/20)*[1 1]);