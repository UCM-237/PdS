a = 0.9; N = 200000;
w = randn(1, N);              % blanco, s2=1
x = filter(1, [1 -a], w);
x = x(1001:end);           % sin transitorio
for l = [0 1 5 10]
  est = mean(x(1+l:end).*x(1:end-l));
  teo = a^l/(1 - a^2);
  disp([l, est, teo])
end
