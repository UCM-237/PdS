Ts = 0.1;                       % s
n = -50:50;
xn = cos(2*pi*2*n*Ts);          % 2 Hz < fs/2
t = linspace(-1, 1, 1001);
% y(t) = Σ x[n] sinc((t - nTs)/Ts)
S = sinc((t.' - n*Ts) / Ts);
y = S * xn.';
disp(max(abs(y.' - cos(4*pi*t))))
plot(t, y); hold on; stem(n*Ts, xn)
xlim([-1 1])
