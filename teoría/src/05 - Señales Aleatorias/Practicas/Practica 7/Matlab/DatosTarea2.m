function X = DatosTarea2()
%X = DatosTarea2()
    N = 10000;
    X1 = 12 + 2*randn(N, 1);
    X2 = 3 + 4*rand(N, 1);
    X3 = X1 + 3*X2;
    X = [X1 X2 X3];
end
