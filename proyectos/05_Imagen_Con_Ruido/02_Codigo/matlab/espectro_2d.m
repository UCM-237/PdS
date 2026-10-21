function L = espectro_2d(x, ventana)
% log10|DFT 2D| centrada; con ventana de Hann separable salvo ventana = false.
if nargin < 2, ventana = true; end
x = x - mean(x(:));
if ventana
    x = x .* (hann_(size(x, 1)) * hann_(size(x, 2))');
end
L = fftshift(log10(abs(fft2(x)) + 1e-9));
end

function w = hann_(n)
w = 0.5 - 0.5 * cos(2 * pi * (0:n-1)' / (n - 1));
end
