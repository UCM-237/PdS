% Muestreo natural
clear all;
close all;

kmax = 10;
Ts = 2;
ws = 2*pi / Ts;
wm = ws/4;
dt = 0.01;
t = [0:dt:2*pi/ws]';
w = [-2:0.1:2]';
y = Xjw(w, 1);
[ynat, wnat] = Xp(wm, Ts, wm, kmax);
[ysup, wsup] = Xp(4.5*wm, Ts, 4.5*wm, kmax);

figure()
subplot(311);
plot(w, Xjw(w, 1));
grid();
title('X(jw)');
xlabel('w');
ylabel('X(jw)');
subplot(312);
plot(wnat, ynat)
grid();
title('Xp(jw), |w_m| < w_s/2');
xlabel('w');
ylabel('X_p(jw)');
subplot(313);
plot(wsup, ysup)
grid();
title('Xp(jw), |w_m| > w_s/2');
xlabel('w');
ylabel('X_p(jw)');

%%
function [y, w] = Xp(tau, Ts, wm, kmax)
  ws = 2*pi/Ts;
  w = [-kmax*ws:ws/20:kmax*ws]';
  y = zeros(size(w));
  for k = -kmax:kmax
    y = y + (tau/Ts)*sinc(k*tau/Ts)*Xjw(w - k*ws, wm);
  end
end

function y = Xjw(w, wm)
  y = (wm - abs(w)) .* (abs(w) < wm);
end