% Hito 4: wavelets, clasificación de latidos y alarma. Completa las partes marcadas con TODO.
iniciar();
fs = 360;
[t, x] = cargar('ecg_B.csv');
% TODO: escribe a_trous.m: transformada wavelet diádica no diezmada con h = [1 3 3 1]/8 y
%       g = [2 -2]; en el nivel k intercala 2^(k-1) - 1 ceros entre sus coeficientes.
% TODO: detector sobre la escala con más energía del QRS y comparación con Pan-Tompkins.
% TODO: anchura del QRS y adelanto (RR previo / mediana de los RR vecinos) de cada latido;
%       clasifica N o V.
% TODO: alarma de taquicardia (FC > 100 lpm durante varios latidos seguidos).
r = [];          % tus detecciones en B (índices desde 1)
tipos = '';      % 'N' o 'V' por latido
guardar_latidos('ecg_B_latidos.csv', r, tipos);
