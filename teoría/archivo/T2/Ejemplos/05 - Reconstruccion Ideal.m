%% Reconstrucción (Filtro Ideal)
close all;
clear all;
dt = 0.01;
N = 201;
n = [0:N]';
Ts = 2;
t = [0:dt:100]';
wc = pi/(10*Ts);
ws = 2*pi/Ts;
xc = cos(wc*t);
xd = cos(wc*Ts*n);

hf = sinc(t/Ts);
x = zeros(size(t));
figure(); hold on;
for i=1:N
  tt = t-(i-1)*Ts;
  x = x + xd(i)*sinc(tt/Ts);
  plot(t, xd(i)*sinc(tt/Ts), 'k');
end
plot(t, xc, 'LineWidth', 4);
%plot(t, x, 'LineWidth', 4);
stem(n*Ts, xd, 'r--', 'MarkerFaceColor', 'r');
xlim(gca, [0, 30])
title ('Reconstruccion');
%% Muestreo FoH No-causal
clear all; close all;

Ts = 1;
dt = Ts / 100;
t = [0:dt:2*Ts]';
pi1 = rectpuls((t-Ts/2)/Ts, Ts+dt);
pi2 = rectpuls((t-3*Ts/2)/Ts, Ts+dt);
y = pi1.*(1+t/Ts) - pi2.*((t-Ts)/Ts);
figure();
plot(t, y);