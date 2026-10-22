b = [0.2 0.3]; a = [1 -1.2 0.72];
x = randn(1, 50000);             % blanco
y = filter(b, a, x);             % sistema
y = y + 0.3*randn(size(x));
w = hanning(256);
[H, f] = tfestimate(x, y, w, [], 256, 1);
Hr = freqz(b, a, 2*pi*f);
k = [1 33 65];               % W=0,pi/4,pi/2
disp([abs(H(k)), abs(Hr(k))])
