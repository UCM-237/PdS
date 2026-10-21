function y = mi_istft(Z, N, n)
% Inversa de mi_stft por solape y suma ponderada (WOLA).
R = N / 4;
w = hanning(N, 'periodic');
nt = size(Z, 2);
L = (nt - 1) * R + N;
y = zeros(L, 1); norma = zeros(L, 1);
for j = 1:nt
    S = Z(:, j) * sum(w);
    S = [S; conj(flipud(S(2:end-1)))];
    seg = real(ifft(S)) .* w;
    idx = (j-1)*R + (1:N);
    y(idx) = y(idx) + seg;
    norma(idx) = norma(idx) + w.^2;
end
y = y ./ max(norma, 1e-12);
y = y(N/2 + (1:n));
end
