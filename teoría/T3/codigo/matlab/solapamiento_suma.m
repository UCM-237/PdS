x = randn(1, 10000);
h = ones(1, 31) / 31;          % FIR, M = 31
L = 226;                        % bloque
M = length(h);
N = L + M - 1;                  % 256 = 2^8
H = fft(h, N);
y = zeros(1, length(x) + M - 1);
for i = 1:L:length(x)
    xb = x(i:min(i+L-1, end));
    yb = real(ifft(fft(xb, N) .* H));
    n = min(N, length(y) - i + 1);
    y(i:i+n-1) = y(i:i+n-1) + yb(1:n);
end
disp(max(abs(y - conv(x, h))))  % ≈ 1e-15
