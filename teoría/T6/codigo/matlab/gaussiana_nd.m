mu = [1; 2];
S = [2.0 1.2;
     1.2 1.0];                  % covarianza
L = chol(S, 'lower');            % S = L L'
Z = randn(2, 100000);
X = mu + L*Z;                    % 2 x N
disp(mean(X, 2)')                % ~ mu
disp(cov(X'))                    % ~ S
[V, D] = eig(S);                 % ejes
disp(diag(D)')                  % 0.2, 2.8
