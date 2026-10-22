x = [1 3 4];
h = [0 2];
lin = conv(x, h)            % [0 2 6 8]
for N = [3 4]               % N < 4 y N = 4
    Y = fft(x, N) .* fft(h, N);
    y = real(ifft(Y));
    disp([N, round(y)])     % N=3: 8 2 6
end
