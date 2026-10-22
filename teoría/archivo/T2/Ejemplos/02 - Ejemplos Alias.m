%% Señales Sinusoidales I (a)
close all;
clear all;

t = [0:0.1:15]';
n = [0:7]';
Ts = 2;

xc = sin((2*pi/10)*t);
xd = sin((2*pi/10)*Ts*n);

figure(); hold on;
title('y = sin((24\pi/10)t)');
grid();
plot(t, xc, 'g');
stem(n*Ts, xd, 'ro', 'MarkerFaceColor', 'r', 'LineWidth', 2);
%% Señales Sinusoidales I (b)
close all;
clear all;

t = [0:0.1:15]';
n = [0:7]';
Ts = 2;

xc1 = sin((2*pi/(10/6))*t);
xc2 = sin((2*pi/10)*t);
xd = sin((2*pi/(10/6))*Ts*n);

figure(); hold on;
title('y = sin((24\pi/10)t)')
grid();
plot(t, xc1, 'g');
plot(t, xc2, 'b');
stem(n*Ts, xd, 'ro', 'MarkerFaceColor', 'r', 'LineWidth', 2);
%% Señales Sinusoidales II
close all;
clear all;

t = [0:0.01:15]';
n = [0:7]';
Ts = 2;

xc1 = 3*sin((2*pi/5)*t) + sin((2*pi/3)*t);
xc2 = 3*sin((2*pi/5)*t) + sin((-pi/3)*t);
xd = 3*sin((2*pi/5)*Ts*n) + sin((2*pi/3)*Ts*n);

figure(); hold on;
title('y = 3 sin((2\pi/5)t)+sin((2\pi/3)t)')
grid();
plot(t, xc1, 'b');
plot(t, xc2, 'g');
stem(n*Ts, xd, 'ro', 'MarkerFaceColor', 'r');
%% Relación entre Ts y Tc
close all;
clear all;

t = [0:0.1:25]';
n = [0:7]';
Ts = 2;
wc = 2*pi/5;
wd = wc*Ts;
xc = sin(wc*t);
xd = sin(wd*n);

figure(); hold on;
title('x_c(t) = sin(w_c t), x_d(n)=sin(w_d n), w_d=2\pi T_s/T_c')
grid();
plot(t, xc, 'g');
stem(n*Ts, xd, 'ro');
%% Frecuencias Alias
close all;
clear all;

N = 3;
Ts = 0.5;
t = [0:0.01:N*Ts]';
n = [0:N]';
k = [0:3]';
wc = 2*pi/5 + 2*pi*k/Ts;
wd = 2*pi/5 * Ts;
xc = sin(t * wc');
xd = sin(wd*n);

figure(); hold on;
title('x_c(t) = sin(w_c t), x_d(n)=sin(w_d n), w_d=2\pi T_s/T_c')
grid();
plot(t, xc(:, 1), 'r');
plot(t, xc(:, 2), 'b-.');
plot(t, xc(:, 3), 'k-.');
plot(t, xc(:, 4), 'g');
stem(n*Ts, xd, 'ro--');
%% Alias fundamental
close all;
clear all;

t = [0:0.1:15]';
n = [0:7]';
Ts = 2;

xc1 = sin((2*pi/10)*t);
xd1 = sin((2*pi/10)*Ts*n);

xc2 = sin((2*pi/(10/6))*t);
xd2 = sin((2*pi/(10/6))*Ts*n);

figure(); hold on;
plot(t, xc1, 'b');
plot(t, xc2, 'g');
stem(n*Ts, xd1, 'ro');
stem(n*Ts, xd2, 'rx', 'MarkerSize', 10);
grid();
title('y = sin((2\pi/10)t)')
