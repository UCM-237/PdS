load leleccum;y = leleccum(1:3920);
niveles=3;
ly = length(y);
t=0:ly-1;
subplot(niveles+2,1,1);plot(t,y)
title('Señal');
[coef,sl]=wavedec(y,niveles,'haar');
for i=1:niveles
    yD=wrcoef('D',coef,sl,'haar',i);
    subplot(niveles+2,1,i+1);plot(yD);
    title(sprintf('D%d',i));
end
yA=wrcoef('A',coef,sl,'haar',niveles);
subplot(niveles+2,1,niveles+2);plot(yA);
title(sprintf('A%d',niveles));
