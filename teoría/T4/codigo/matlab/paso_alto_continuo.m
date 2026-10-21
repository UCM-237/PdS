% Paso 4 kHz, 0,1 dB; supresión 1 kHz, 40 dB
wp_ = 2*pi*4e3; ws_ = 2*pi*1e3;
% 1) Prototipo paso bajo con wp = 1
ws = wp_ / ws_;                     % = 4
[N, wc] = buttord(1, ws, 0.1, 40, 's');
[b, a] = butter(N, wc, 's');
% 2) Paso bajo -> paso alto (Matlab):
%    [bh, ah] = lp2hp(b, a, wp_);
% Equivale a hacerlo en un solo paso:
[N2, wn] = buttord(wp_, ws_, 0.1, 40, 's');
[b2, a2] = butter(N2, wn, 'high', 's');
disp([N, N2])                       % 5, 5
