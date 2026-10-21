% Hito 2: filtrado. Completa las partes marcadas con TODO.
iniciar();
d = cargar_actividad('desarrollo_01.csv');
v_ema = ema(d.t, d.v, 10);
[fich, ~, ~, cambios] = verdad_desarrollo();
fprintf('cambios reales de %s (s): %s\n', fich{1}, mat2str(cambios{1}));
% TODO: H(z) de la EMA con Δt = 1 s, respuesta en frecuencia, corte y retardo.
% TODO: Butterworth de fase cero y mediana móvil sobre la señal remuestreada (sin toolbox:
%       coeficientes por la transformación bilineal, filter hacia delante y hacia atrás);
%       retardo de cada filtro en los cambios de las sintéticas.
% TODO: desnivel positivo de cada actividad real sin filtrar, filtrado y con histéresis.
