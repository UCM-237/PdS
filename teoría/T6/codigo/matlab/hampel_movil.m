x = randn(1, 1000);
x(1:97:end) = x(1:97:end) + 8; % atípicos
mad = median(abs(x - median(x)));
disp([std(x), 1.4826*mad])    % sigma = 1
K = 10; t = 3;
y = x; at = false(size(x));
for n = K+1:numel(x)-K
  v = x(n-K:n+K);
  m = median(v);
  S = 1.4826*median(abs(v - m));
  if abs(x(n) - m) > t*S
    y(n) = m; at(n) = true;
  end
end
disp([sum(at(1:97:end)), sum(at)])
% Toolbox: [y, at] = hampel(x, K, t);
