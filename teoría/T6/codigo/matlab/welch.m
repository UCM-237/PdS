a = 0.8; N = 2^14;
x = filter(1, [1 -a], randn(1, N));
w = hanning(256);
[P, f] = pwelch(x, w, [], 256, 1, ...
                'twosided');     % Phi
W = 2*pi*f;                    % f en ciclos
teo = 1./abs(1 - a*exp(-1j*W)).^2;
disp([P(1), teo(1)])             % ~ 25
disp([P(65), teo(65)])        % W=pi/2: 0.61
disp([mean(P), var(x)])          % potencia
