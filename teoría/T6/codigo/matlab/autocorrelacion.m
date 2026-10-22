N = 1001;
x = 5 + randn(1, N);            % N(5,1) iid
u = 2 + 4*rand(1, N);           % U[2,6] iid
[px, l] = xcorr(x, 100, 'unbiased');
pu = xcorr(u, 100, 'unbiased');
disp([px(101), px(151)])        % ~ 26, ~ 25
disp([pu(101), pu(151)])      % ~ 17.3, ~ 16
