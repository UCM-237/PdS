%% Muestreo Sinc
clear all;
close all;

Tc = 2;
Ts = Tc/2;
N = 10;
t = [0:0.1:N*Tc]';
n = [0:N*round(Tc/Ts)]';
xc = Ts*sinc(t/Tc);
xd = Ts*sinc(n*Ts/Tc);

figure(); hold on;
plot(t, xc);
stem(n*Ts, xd, 'rx--');


%% Derivada Sinc
Ts = 2;
N = 20;
t = [0:0.1:N*Ts]';
n = [0:N]';
xc = Ts*sinc(t/Ts);
xd = Ts*sinc(n);
yd = (-1).^n ./ (n*Ts^2);
yd(1) = 0;

figure(); hold on;
plot(t, xc);
stem(n*Ts, xd, 'kx');
stem(n*Ts, yd, 'ro');

