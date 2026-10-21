fs = 8000;
t = 0:1/fs:2-1/fs;
x = chirp(t, 200, 2, 3000);
% STFT: tramos de 256, solape del 75 %
Nw = 256; paso = 64;
w = hanning(Nw).';
ini = 1:paso:length(x)-Nw;
S = zeros(Nw/2+1, length(ini));
for m = 1:length(ini)
    X = fft(w .* x(ini(m):ini(m)+Nw-1));
    S(:, m) = abs(X(1:Nw/2+1));
end
f = (0:Nw/2) * fs / Nw;
tt = (ini - 1 + Nw/2) / fs;
disp(size(S))                   % 129 x 121
imagesc(tt, f, 20*log10(S + 1e-9)); axis xy
xlabel('t (s)'); ylabel('f (Hz)')
