n = 0:999;
x = 0.9.^n;                  % 0.9^n u[n]
E = sum(abs(x).^2);          % 1/(1-0.81)

N = 10000;
m = -N:N;
y = 3*cos(0.1*pi*m);
P = sum(abs(y).^2) / (2*N + 1);   % 9/2
fprintf('E = %.3f, P = %.3f\n', E, P)
