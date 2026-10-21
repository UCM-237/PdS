function p = psnr_db(x, ref)
% PSNR en dB con pico 1.
x = min(max(x, 0), 1);
p = 10 * log10(1 / mean((x(:) - ref(:)).^2));
end
