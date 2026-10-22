fs = 8000;
t = 0:1/fs:0.1-1/fs;          % 800 muestras
x = sin(2*pi*852*t) ...
    + sin(2*pi*1336*t);          % tecla 8
x = x + 0.5*randn(size(t));
N = 4096;
w = hamming(numel(x))';
X = abs(fft(x.*w, N));
X = X(1:N/2+1);
f = (0:N/2)*fs/N;
baja = find(f > 650 & f < 1000);
alta = find(f > 1150 & f < 1550);
[~, ib] = max(X(baja)); fb = f(baja(ib));
[~, ia] = max(X(alta)); fa = f(alta(ia));
filas = [697 770 852 941];
cols = [1209 1336 1477];
teclas = ['123'; '456'; '789'; '*0#'];
[~, i] = min(abs(filas - fb));
[~, j] = min(abs(cols - fa));
disp([fb fa]); disp(teclas(i, j))  % 8
