% Hito 3: detección de QRS y variabilidad del ritmo. Completa las partes marcadas con TODO.
iniciar();
fs = 360;
[t, x] = cargar('ecg_A.csv');
ref = anotaciones();
y = x;   % TODO: aplica aquí tu cadena de preprocesado del Hito 2

% Etapas de Pan-Tompkins
[b, a] = butter(2, [5 15]/(fs/2));
xf = filtfilt(b, a, y);
d = gradient(xf) * fs;
c = d.^2;
N = round(0.150 * fs);
mwi = conv(c, ones(N, 1)/N, 'same');

% Umbral fijo provisional: sustitúyelo por el umbral adaptativo
picos = picos_locales(mwi, round(0.2 * fs));
picos = picos(mwi(picos) > 0.3 * max(mwi));
% TODO: umbral adaptativo con SPK y NPK, búsqueda hacia atrás y localización del pico R
%       en xf (la integración va retrasada media ventana).
e = evaluar(picos, ref, fs);
fprintf('umbral fijo: VP %d, FP %d, FN %d, Se %.3f, VPP %.3f\n', e.VP, e.FP, e.FN, e.Se, e.VPP);

% TODO: tacograma, FC media, SDNN, RMSSD, histograma de los RR y PSD del tacograma
%       remuestreado a 4 Hz (interp1 + psd_welch) con potencias LF y HF.
