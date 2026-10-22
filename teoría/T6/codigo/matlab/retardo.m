Ts = 0.01;
t = 0:Ts:6-Ts;
x = sinc(t - 2);                 % buscada
y = sinc(t - 3) ...
    + randn(size(t));            % recibida
[c, lags] = xcorr(y, x);        % y[n+l]x[n]
[~, k] = max(c);
disp(lags(k)*Ts)                 % ~ 1 s
