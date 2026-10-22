N = 50000;
u1 = rand(1, N); u2 = rand(1, N);
r = sqrt(-2*log(1 - u1));        % radio
th = 2*pi*u2;                    % ángulo
z1 = r.*cos(th); z2 = r.*sin(th);
x = 5 + 2*z1;                    % N(5, 4)
disp([mean(z1), std(z1), std(z2)])
c = corrcoef(z1, z2); disp(c(1, 2))  % ~ 0
disp([mean(x), var(x)])          % ~ 5, 4
disp(mean(abs(z1) < 1))          % ~ 0.683
