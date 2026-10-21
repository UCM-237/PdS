% Hito 3: ruido, atípicos y cambios de ritmo. Completa las partes marcadas con TODO.
iniciar();
[fich, tipos, sigmas, cambios] = verdad_desarrollo();
T = [0 0 0];
for i = 1:numel(fich)
    d = cargar_actividad(fich{i});
    det = [];   % TODO: escribe detectar_cambios.m (derivada + umbral, segmentación binaria)
    [tp, fp, fn] = evaluar_detecciones(det, cambios{i});
    T = T + [tp fp fn];
end
fprintf('TP %d, FP %d, FN %d\n', T);
% TODO: estadística del ruido de la velocidad (histograma, σ, autocorrelación).
% TODO: atípicos con Hampel / MAD, FC congelada y distancia corregida.
% TODO: indicadores de cada sesión real.
