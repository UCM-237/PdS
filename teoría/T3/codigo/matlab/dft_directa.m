x = [1; 3; 4; 0];
N = length(x);
n = 0:N-1;
k = n.';
W = exp(-2j*pi*k*n/N);          % matriz DFT
X = W * x;                      % O(N²)
disp(X.')               % 8, -3-3j, 2, -3+3j
disp(max(abs(X - fft(x))))      % ≈ 0
xr = (W' * X) / N;              % IDFT
disp(real(xr).')
