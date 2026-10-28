N = 512; L = 9;         % L: longitud
x = repelem(randi([0 1], 1, 64), 8);
h = zeros(1, N); h(1:L) = 1/L;  % movimiento
H = fft(h);
y = real(ifft(fft(x).*H));
y = y + 0.02*randn(1, N);
Y = fft(y);
for K = [0 1e-3 1e-2 1e-1]
  G = conj(H)./(abs(H).^2 + K);
  xe = real(ifft(G.*Y));
  disp([K, sqrt(mean((xe - x).^2))])
end
