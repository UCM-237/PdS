fs = 8000; t = 0:1/fs:3-1/fs;
s = sin(2*pi*440*t).*(t > 1);
x = s + 0.3*randn(size(t));
L = 256; R = L/2;
w = sqrt(hann(L, 'periodic'));
M = floor((numel(x) - L)/R) + 1;
X = zeros(L, M);
for m = 1:M                   % STFT
  X(:, m) = fft(w.*x((m-1)*R+(1:L)).');
end
A = abs(X).^2;
Pv = mean(A(:, 1:60), 2);     % ruido
a = 2; b = 0.02;              % alfa, beta
P = max(A - a*Pv, b*A);
S = sqrt(P).*exp(1j*angle(X));
y = zeros(size(x));
for m = 1:M                   % ISTFT (OLA)
  i = (m-1)*R + (1:L);
  y(i) = y(i) + (w.*real(ifft(S(:, m)))).';
end
snr = @(z) 10*log10(sum(s.^2)/sum((z-s).^2));
disp([snr(x), snr(y)])        % dB
