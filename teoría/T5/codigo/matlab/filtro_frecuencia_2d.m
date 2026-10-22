f = imagen_prueba();
[M, N] = size(f);
F = fft2(f);
k = [0:M/2-1, -M/2:-1];          % 0..-1
l = [0:N/2-1, -N/2:-1];
[L, K] = meshgrid(l, k);
D2 = K.^2 + L.^2;
D0 = 20;
H = exp(-D2/(2*D0^2));           % gaussiano
g = real(ifft2(H.*F));
E = abs(F).^2;
disp(sum(E(:).*H(:).^2)/sum(E(:)))
disp([mean(f(:)) mean(g(:))])    % H(1,1)=1
