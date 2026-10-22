fs = 500;
t = 0:1/fs:1-1/fs;
x = exp(-((t - 0.4)/0.05).^2) ...
    + 0.15*randn(size(t));
[b, a] = butter(3, 15/(fs/2));
y1 = filter(b, a, x);           % retrasa
y2 = filtfilt(b, a, x);         % |H|^2
[~, i1] = max(y1); [~, i2] = max(y2);
disp([t(i1), t(i2)])
