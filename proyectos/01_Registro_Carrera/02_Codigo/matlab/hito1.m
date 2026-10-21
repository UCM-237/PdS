% Hito 1: señal y espectro. Completa las partes marcadas con TODO.
iniciar();
f = actividades();
for i = 1:numel(f)
    d = cargar_actividad(f{i});
    fprintf('%s: %d muestras, %.1f min, dt mediana %.0f s\n', f{i}, numel(d.t), d.t(end) / 60, median(diff(d.t)));
end
d = cargar_actividad(f{1});
h = figure('visible', 'off');
subplot(3, 1, 1); plot(d.t / 60, d.v); ylabel('km/h');
subplot(3, 1, 2); plot(d.t / 60, d.fc); ylabel('ppm');
subplot(3, 1, 3); plot(d.t / 60, d.alt); ylabel('m'); xlabel('tiempo (min)');
guardar_figura(h, 'h1_senales.png');
% TODO: histograma de dt y huecos de más de 15 s.
% TODO: anomalías (velocidad imposible, saltos de distancia, FC congelada).
% TODO: remuestreo a una rejilla uniforme (interp1) y PSD de Welch (segmentos con ventana de
%       Hann, |fft|² promediado; o pwelch si tienes la toolbox o el paquete signal).
