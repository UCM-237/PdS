%% Reconstrucción (FoH No-causal)
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
  x = x + xd(i)*foh(tt/Ts);
  plot(t, xd(i)*foh(tt/Ts), 'k--');
end
grid();
plot(t, x, 'LineWidth', 2);
stem(n*Ts, xd, 'r:', 'MarkerFaceColor', 'r');
title ('Reconstruccion');
%% Reconstrucción (FoH causal)
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
figure()
plot([0:0.01:2], foh([0:0.01:2]))

x = zeros(size(t));
figure(); hold on;
for i=1:N
  tt = t-(i-1)*Ts;
  x = x + xd(i)*foh(tt/Ts);
  plot(t, xd(i)*foh(tt/Ts), 'k--');
end
grid();
plot(t, x, 'LineWidth', 2);
stem(n*Ts, xd, 'r:', 'MarkerFaceColor', 'r');
title ('Reconstruccion');
%% Funciones 
%function y = foh(t)
%  y = (t >= -1 & t < 0) .* (1 + t) - (t >= 0 & t < 1) .* (t - 1);
%end


function y = foh(t)
  y = (t >= 0 & t < 1) .* (1 + t) - (t >= 1 & t < 2) .* (t - 1);
end

