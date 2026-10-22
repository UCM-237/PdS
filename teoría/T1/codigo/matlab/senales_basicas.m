n = -10:10;               % eje temporal
delta = double(n == 0);   % δ[n]
u = double(n >= 0);       % u[n]
r = n .* u;               % r[n] = n u[n]
x = 0.8.^n .* u;          % 0.8^n u[n]

stem(n, x)
xlabel('n'); ylabel('x[n]')
