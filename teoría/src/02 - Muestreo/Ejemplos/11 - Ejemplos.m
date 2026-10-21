%% Ejemplos
%% (a) x(t) + x(t-1)
clear all;
close all;

T = 10;
dt = 0.01;
t = [0:dt:T-dt]';
w0 = 2*pi/4;

y1 = cos(w0*t);
y2 = cos(w0*(t-1));

y = y1 + y2;

figure(); grid(); hold on;
plot(t, y1);
plot(t, y);
xlabel('t');
ylabel('y(t)');
title('x(t)=cos(w_0t), y(t)=x(t)+x(t-1)');
legend('x(t)', 'y(t)=x(t)+x(t-1)');
%% (b) dx(t)/dt
clear all;
close all;

T = 10;
dt = 0.01;
t = [0:dt:T-dt]';
w0 = 2*pi/4;

x = cos(w0*t);
y = -sin(w0*t);

figure(); grid(); hold on;
plot(t, x);
plot(t, y);
xlabel('t');
ylabel('y(t)');
title('x(t)=cos(w_0t), y(t)=dx(t)/dt');
legend('cos(w_0t)', 'y(t)=dx(t)/dt');
%% (c) x(t)^2
clear all
close all

w0 = 2*pi/4;
w1 = 2*w0;
T = 2*pi/w0;
dt = 1/1024;
t = [0:dt:T-dt]';

x = cos(w0*t);
y = x.^2;

N = length(y);
X = fft(x);
Y = fft(y);
Xabs = abs(X(1:N/2));
Yabs = abs(Y(1:N/2));
f = 2*pi*[0:N/2-1]'/(N*dt);

figure(); grid(); hold on;
plot(t, x);
plot(t, y);
xlabel('t');
ylabel('y(t)');
title('x(t)=cos(w_0t), y(t)=cos(w_0t)^2');

figure(); grid(); hold on;
stem(f, Xabs);
stem(f, Yabs);
xlim(gca, [0, 2*w0])
xlabel('w');
ylabel('abs(Y(exp(jw))');
title('X(exp(jw)), Y(exp(jw))')
%% (c) x(t)*cos(w0*t)
close all;
clear all;

w0 = 2*pi/4;
T = 10*2*pi/ w0;
dt = T/512;
t = [-T/2:dt:T/2-dt]';

x = sinc((w0/pi)*t);
y = x .* cos(w0*t);

N = length(y);
X = fft(x);
Y = fft(y);
Xabs = abs(X(1:N/2));
Yabs = abs(Y(1:N/2));
f = 2*pi*[0:N/2-1]'/(N*dt);

figure(); grid(); hold on;
plot(t, x);
plot(t, y);
xlabel('t');
ylabel('y(t)');
title('x(t)=cos(w_0t), y(t)=cos(w_0t)');

figure(); grid(); hold on;
stem(f, Xabs);
stem(f, Yabs);
xlim(gca, [0, 4*w0])
xlabel('w');
ylabel('abs(Y(exp(jw))');
title('X(exp(jw)), Y(exp(jw))')
