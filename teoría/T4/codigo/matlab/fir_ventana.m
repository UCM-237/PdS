% Ωp = 0,3π, Ωs = 0,5π, αs = 40 dB -> Hann
Wc = 0.4*pi;                % (Ωp + Ωs)/2
L = 16;                     % 3,11π/(0,2π)
n = -L:L;
hd = Wc/pi * sinc(Wc/pi * n);
w = hanning(2*L + 1).';     % sin ceros
h = hd .* w;                % 33 coef.
[H, W] = freqz(h, 1, 4096);
As = -20*log10(abs(H(W >= 0.5*pi)));
disp(min(As))               % 44 dB
% Casi igual (ganancia 1 en Ω = 0):
h2 = fir1(2*L, 0.4, hanning(2*L + 1));
