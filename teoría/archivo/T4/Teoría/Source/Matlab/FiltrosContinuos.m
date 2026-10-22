
num=10;den=[1,10];
den=10;num=[1,10];

num=10;den=poly([-1+3j,-1-3j])

den=10;num=poly([-1+3j,-1-3j])


num=9;den=poly([3j,-3j])

den=9;num=poly([3j,-3j])

close all;
[Hw,w]=freqs(num,den,[0:0.1:10])

subplot(2,1,1);
semilogx(w,20*log10(abs(Hw)),'LineWidth',2);grid on
set(gca,'FontSize',14)
xlabel('w (rad/s)','FontSize',14);
ylabel('Magnitude (dB)','FontSize',14);
print -depsc FiltroContinuo6a


subplot(2,1,2);
plot(w,abs(Hw),'LineWidth',2)
set(gca,'FontSize',14)
xlabel('w (rad/s)','FontSize',14);
ylabel('|H(jw)|','FontSize',14);grid on
print -depsc FiltroContinuo6b