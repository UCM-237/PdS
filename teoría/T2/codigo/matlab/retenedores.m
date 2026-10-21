Ts = 0.1;                       % s
n = 0:10;
xn = sin(2*pi*1*n*Ts);          % 1 Hz
t = linspace(0, 1, 1001);
% Orden cero: se mantiene la última muestra
y0 = interp1(n*Ts, xn, t, 'previous');
% Orden uno (no causal): une las muestras
y1 = interp1(n*Ts, xn, t, 'linear');
x = sin(2*pi*t);
disp([max(abs(y0 - x)), max(abs(y1 - x))])
plot(t, y0, t, y1, t, x)
