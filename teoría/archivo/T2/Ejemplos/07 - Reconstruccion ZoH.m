%% Reconstrucción (Zero-order Hold)
close all;
clear all;
N = 20;
n = [0:N]';
Ts = 2;
T = N*Ts;
dt = 0.01;
t = [0:dt:N*Ts-dt]';
wc = pi/(10*Ts);
ws = 2*pi/Ts;
xc = cos(wc*t);
xd = cos(wc*Ts*n);

x = zeros(size(t));
figure(); hold on;
for i=1:N
  tt = t-(i-1)*Ts;
  x = x + xd(i)*zoh(tt/Ts);
  plot(t, xd(i)*zoh(tt/Ts), 'k');
end
grid();
plot(t, xc, 'LineWidth', 4);
stem(n*Ts, xd, 'r--', 'MarkerFaceColor', 'r');
title ('Reconstruccion');
%% Funciones 
function y = zoh(t)
  y = (t > 0 & t < 1)
end
