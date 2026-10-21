T = 1;                         % periodo
t = linspace(-T, T, 2000);
K = 19;                        % armónicos
xK = zeros(size(t));
for k = 1:K
    ck = sin(pi*k/2)/(pi*k/2); % c_k, cuadrada par
    xK = xK + 2*ck*cos(2*pi*k*t/T);
end
plot(t, xK); xlabel('t (s)')
