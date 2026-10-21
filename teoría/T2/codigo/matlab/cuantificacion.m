b = 8;                      % bits
V = 1.0;                    % margen [-V, V)
D = 2*V / 2^b;              % escalón Δ
n = 0:99999;
x = 0.99*V*sin(2*pi*0.01234*n);
xq = D * round(x / D);      % redondeo
e = xq - x;
disp([var(e), D^2/12])      % ≈ Δ²/12
snr = 10*log10(var(x) / var(e));
disp([snr, 6.02*b + 1.76])  % dB
