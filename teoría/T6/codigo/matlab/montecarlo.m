for N = [100 10000 1000000]
  x = randn(1, N);              % X ~ N(0,1)
  g = cos(x);                    % E{cos X}?
  est = mean(g);
  err = std(g)/sqrt(N);
  disp([N, est, err])
end
disp(exp(-0.5))                  % exacto
