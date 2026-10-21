% Paso alto: Ωs = 0,4π, Ωp = 0,55π,
% rizado δ = 0,01 en las dos bandas
d = 0.01;
[N, Wn, beta, tipo] = kaiserord( ...
    [0.4 0.55], [0 1], [d d]);
N = N + mod(N, 2);              % orden par
h = fir1(N, Wn, tipo, kaiser(N+1, beta));
disp([N+1, beta])               % 31, 3.395
% Parks-McClellan: rizado uniforme
hpm = firpm(N, [0 0.4 0.55 1], [0 0 1 1]);
