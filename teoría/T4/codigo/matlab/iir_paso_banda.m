% Bordes normalizados a π (1 = fs/2)
Wp = [0.45 0.65]; Ws = [0.3 0.75];
[N, Wn] = buttord(Wp, Ws, 1, 40);
disp(N)                     % 7: orden 14
[b, a] = butter(N, Wn);     % paso banda
[H, W] = freqz(b, a, 2000);
plot(W/pi, 20*log10(abs(H)))
xlabel('\Omega/\pi'); ylim([-80 3])
% Para filtrar, mejor por secciones:
[z, p, k] = butter(N, Wn);
sos = zp2sos(z, p, k);      % sosfilt(sos, x)
