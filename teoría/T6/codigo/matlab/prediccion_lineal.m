N = 8000; p = 4;
x = filter(1, [1 -1.6 0.9], randn(1, N));
i = [2001 5001];
x(i) = x(i) + 6;              % clics
r = xcorr(x, p, 'biased');
r = r(p+1:end);               % phi[0..p]
a = toeplitz(r(1:p)) \ r(2:p+1).';
% e[n] = x[n] - sum_k a_k x[n-k]
e = filter([1; -a], 1, x);
S = 1.4826*median(abs(e));
disp(round(a.', 2))     % 1.6 -0.9 0 0
disp(find(abs(e) > 5*S) - 1)
