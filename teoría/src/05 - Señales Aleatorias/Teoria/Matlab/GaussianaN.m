mu = [1 2]; %Media
Sigma = [1 .5; .5 2]; %Covarianza
S = chol(Sigma); %''Raiz cuadrada''
x = repmat(mu,100,1) + randn(100,2)*S;