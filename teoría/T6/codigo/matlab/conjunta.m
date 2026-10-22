N = 100000;
x1 = 2 + 2*rand(N, 1);           % U[2,4]
x2 = x1 + randn(N, 1);           % N(x1,1)
X = [x1, x2];                    % N x 2
disp(mean(X))                    % 3, 3
disp(cov(X))            % [1/3 1/3; 1/3 4/3]
c = corrcoef(X); disp(c(1, 2))   % 0.5
