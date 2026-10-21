fs = 200e3;                    % Hz
Wp = 2*pi*25e3/fs;             % 0,25π
Ws = 2*pi*55e3/fs;             % 0,55π
% 1) Predistorsión con T = 2
wp = tan(Wp/2); ws = tan(Ws/2);
% 2) Filtro continuo
[N, wc] = buttord(wp, ws, 0.5, 15, 's');
[b, a] = butter(N, wc, 's');
% 3) Bilineal: fs = 1/T = 0,5
[bz, az] = bilinear(b, a, 0.5);
% Lo mismo en un paso (frecuencias
% normalizadas a fs/2):
[N2, Wn] = buttord(Wp/pi, Ws/pi, 0.5, 15);
[bz2, az2] = butter(N2, Wn);
disp([N, N2])                  % 3, 3
