fs = 5000; f0 = 50;
L = fs / f0;                    % 100
a = 0.9;                        % polos
% H(z) = (1+a)/2 (1 - z^-L)/(1 - a z^-L)
b = zeros(1, L+1); b([1 L+1]) = [1 -1];
d = zeros(1, L+1); d([1 L+1]) = [1 -a];
b = b * (1 + a) / 2;
f = [7 50 150 175];                  % Hz
H = freqz(b, d, f, fs);
disp(round(abs(H)*1000)/1000)  % 1 0 0 1
