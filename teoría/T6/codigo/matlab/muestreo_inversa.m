lam = 2; N = 100000;
u = rand(1, N);                  % U[0,1)
x = -log(1 - u)/lam;             % F^-1(u)
disp([mean(x), 1/lam])           % media
disp([var(x), 1/lam^2])          % varianza
disp([mean(x > 1), exp(-lam)])
