function data = DatosTarea3()
    N = 10000;
    mu = 1; sigma = sqrt(0.01);
    a = 2; b = 4;
    p = [0.7 0.3];
    clase = sum(rand(N, 1) < cumsum(p), 2);
    data = zeros(N, 1);
    for i=1:N
        if clase(i) == 1 % Normal
            data(i, 1) = mu + sigma*randn();
        else % Uniforme
            data(i, 1) = a + (b-a)*rand();
        end
    end

    data(:, 2) = 5 + randn(N, 1);
    data(:, 3) = 10 + 4*rand(N, 1);
end


