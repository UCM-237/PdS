%% Tres armónicos
clear all;
close all;

Fs = 48000;
dt = 1 / Fs;
w0 = 2*pi*2000;
Tend = 2;
t = [0:dt:Tend]';

k = [1:4];
y = sum(sin(w0*t*k + 2*pi*rand(1, length(k))), 2);

N = round(2*pi/w0/dt);
yy = y(1:N);
f = [0:N/2-1, -N/2:-1]/(N*dt);

figure();
xlabel('freq (Hz)');
ylabel('Módulo');
title('Espectro en frecuencia');
stem(f, abs(fft(yy)))

figure();
plot(t, y);
xlabel('t');
ylabel('y');
title('Tres armónicos');
xlim(gca, [0, 5*2*pi/w0]);

sound(y, Fs);
%% Diente de sierra
clear all;
close all;

Fs = 48000;
dt = 1 / Fs;
w0 = 2*pi*2000;
Tend = 2;
t = [0:dt:Tend]';

y = sawtooth(w0*t);
plot(t, y)
xlim(gca, [0, 5*2*pi/w0]);
sound(y, Fs)

N = round(2*pi/w0/dt);
yy = y(1:N);
f = [0:N/2-1, -N/2:-1]/(N*dt);

figure();
plot(t, y);
xlim(gca, [0, 5*2*pi/w0]);
xlabel('t');
ylabel('y');
title('Diente de sierra');

figure();
xlabel('freq (Hz)');
ylabel('Módulo');
title('Espectro en frecuencia');
stem(f, abs(fft(yy)))