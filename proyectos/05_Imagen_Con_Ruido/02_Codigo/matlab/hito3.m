% Hito 3: estadística del ruido. Completa las partes marcadas con TODO.
iniciar();
y1 = cargar(1); x1 = cargar(1, true);
r = y1 - x1;
fprintf('imagen 1: media del residuo = %.4f, sigma = %.4f\n', mean(r(:)), std(r(:)));
% TODO: histograma del residuo con su gaussiana; autocorrelación 2D (fft2, |R|², ifft2).
% TODO: escribe estimar_sigma.m (σ sin la imagen limpia, por ejemplo con el núcleo N de la
%       teoría mínima y la mediana de |conv2(y, N, 'valid')|) y mide su sesgo por Monte Carlo.
% TODO: diagnóstico de las seis imágenes: fracción de impulsos, picos del espectro, σ,
%       pendiente de la varianza local frente a la media local en zonas planas.
% TODO: escribe wiener_local.m: media m y varianza v en ventanas k×k (filtrar_sep con
%       ones(1,k)/k) y x̂ = m + max(v − σ², 0)./v .* (y − m).
% TODO: mediana que solo sustituye los impulsos (imagen 2) y Anscombe para el ruido de Poisson.
