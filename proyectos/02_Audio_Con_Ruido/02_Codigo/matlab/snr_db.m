function v = snr_db(ref, x)
% SNR (dB) de x frente a la referencia limpia ref.
v = 10 * log10(sum(ref.^2) / sum((x - ref).^2));
end
