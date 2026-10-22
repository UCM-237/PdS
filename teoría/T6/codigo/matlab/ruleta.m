p = [.1 .1 .1 .1 .1 .5];         % dado
F = cumsum(p);                   % 0.1 ... 1
u = rand(1, 60000);
x = zeros(size(u));
for i = 1:numel(u)
  x(i) = find(u(i) < F, 1);  % 1er F > u
end
frec = accumarray(x', 1)'/numel(u);
disp(frec)                       % ~ p
disp([mean(x), sum((1:6).*p)])
