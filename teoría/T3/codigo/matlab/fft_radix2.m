x = randn(1024, 1);
N = length(x);
% Reordenación por inversión de bits
X = x(bitrevorder(1:N));
m = 2;                          % tamaño DFT
while m <= N                % log2(N) etapas
    B = reshape(X, m, N/m);     % bloques
    F = B(1:m/2, :);
    G = B(m/2+1:end, :);
    W = exp(-2j*pi*(0:m/2-1).'/m);
    B = [F + W.*G; F - W.*G];   % mariposas
    X = B(:);
    m = 2*m;
end
disp(max(abs(X - fft(x))))      % ≈ 1e-12
