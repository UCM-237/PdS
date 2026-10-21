clear; close all;
p = 0.4;
N = 1000;
for i=1:N
  px(i) = nchoosek(N, i)*(p^i)*(1-p)^(N-i);
end

v = rand(N);
x = sum(v < p);

figure(); hold on;
plot(px)
histogram(x, 'Normalization', 'pdf')

