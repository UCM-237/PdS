close all;
Ts=2;
T1=10;
t=0:0.05:15;
y=sin(2*pi/T1*t);
td=0:Ts:15;
yd=sin(2*pi/T1*td);
plot(t,y,'b','LineWidth',2);hold on;
set(gca,'Xtick',0:2:15,'FontSize',16)
grid on;
xlabel('t=nT_s','FontSize',16)
ylabel('x','FontSize',16)


print -depsc AliasBasic1



stem(td,yd,'r','LineWidth',2,'MarkerFaceColor','r');

print -depsc AliasBasic2


T2=10/6;
y2=sin(2*pi/T2*t);
plot(t,y2,'g','LineWidth',2);
stem(td,yd,'r','LineWidth',2,'MarkerFaceColor','r');


print -depsc AliasBasic3
