f = @(x) 6*x.*(1 - x);           % objetivo
M = 1.5;                % f <= M*q, q=U[0,1]
N = 100000;
x = rand(1, N);            % candidatos de q
u = rand(1, N);
acept = u*M <= f(x);
xs = x(acept);
disp([mean(acept), 1/M])         % ~ 0.667
disp([mean(xs), var(xs)])        % 0.5, 0.05
