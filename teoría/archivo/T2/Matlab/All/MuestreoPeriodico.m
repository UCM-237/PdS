gs=tf([1],[1,1,3]);
[x,t]=impulse(gs,[0:0.01:10]);
plot(t,x,'b','LineWidth',2);
set(gca,'Xtick',0:1:10,'FontSize',16)
xlabel('t=nT_s','FontSize',16)
ylabel('x','FontSize',16)
h=legend('x_a(t)');
set(h,'FontSize',16);
grid on;

print -depsc Muestreo1

hold on;
tm=t(1+0:100:end);
xm=x(1+0:100:end)
stem(tm,xm,'r','LineWidth',2,'MarkerFaceColor','r')
h=legend('x_a(t)','x(n)');
set(h,'FontSize',16);

print -depsc Muestreo2