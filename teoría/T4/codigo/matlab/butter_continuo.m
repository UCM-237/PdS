wp = 2*pi*1e3; ws = 2*pi*5e3;      % rad/s
ap = 1; as = 40;                   % dB
[N, wc] = buttord(wp, ws, ap, as, 's');
disp([N, wc])                      % 4, 7439
[b, a] = butter(N, wc, 's');
w = linspace(0, 2*pi*8e3, 1000);
H = freqs(b, a, w);
plot(w/(2*pi), 20*log10(abs(H)))
xlabel('f (Hz)'); ylabel('dB')
