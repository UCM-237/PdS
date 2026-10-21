close all;
hold on
t=0:0.01:100;
grid on;
set(gca,'Xtick',0:10:100,'XtickLabel',[0,1,2,3,4,5,6,7,8,9,10],'FontSize',16)
axis([0,100,-1,1]);
x1=exp(-0.05*t);
plot(t(1+[0:1000:end]),x1(1+[0:1000:end]),'k*','MarkerSize',12);
hold on;

pause;
print -depsc MuestreoRec1

plot(t,x1,'b','LineWidth',2)


plot(t(1+[0:1000:end]),x1(1+[0:1000:end]),'k*','MarkerSize',12);


print -depsc MuestreoRec2

x2=cos(2*pi/10*t)
plot(t,x2.*x1,'r','LineWidth',2)

plot(t(1+[0:1000:end]),x1(1+[0:1000:end]),'k*','MarkerSize',12);


print -depsc MuestreoRec3

x3=sawtooth(2*pi/10*t);
plot(t,x3,'g','LineWidth',2)

plot(t(1+[0:1000:end]),x1(1+[0:1000:end]),'k*','MarkerSize',12);


print -depsc MuestreoRec4