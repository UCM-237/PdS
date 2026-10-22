fs = 44100;                     % Hz (CD)
t = 0:1/fs:0.1-1/fs;
x = sin(2*pi*1000*t);           % 1 kHz
% Diezmado por 4 con filtro antialiasing
x4 = decimate(x, 4);            % fs/4
% Cambio racional 44,1 kHz -> 48 kHz
y = resample(x, 160, 147);
disp([length(x), length(x4), length(y)])
